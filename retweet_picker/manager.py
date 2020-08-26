import datetime
import logging
import random
import sys
import time
import uuid

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

from core.models import Order
from retweet_picker.bot_check import BotCheck
from retweet_picker.models import GiveawayResults, GiveawayStats, TwitterGiveawayID, ContestUserAccounts
from retweet_picker.process import ProcessRetrievedTweets
from retweet_picker.twitter_interact import TwitterInteract
from .utils import display_time, giveaway_ends
from giveaways.models import Giveaway

class TwitterUser(TwitterInteract):

    def __init__(self, username=None):
        super(TwitterInteract, self).__init__()
        self.username = username
        self.user_obj = self.get_user_obj()

    def get_user_obj(self):
        return self.api.get_user(self.username)._json

    def get_follower_count(self):
        return self.user_obj.get('followers_count')


def change_order_status(order_id, status=None):
    if order_id and status:
        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
        except Exception as e:
            logging.error(f"Could not modify order status {e}")

def get_user(user_obj):
    return ContestUserAccounts.objects.get_or_create(user_id=user_obj.user_id)

class GiveawayManager:

    def __init__(self,
                 user_id=None,
                 order_id=None,
                 sponsors=[],
                 giveaway_amount=0,
                 duration=None,
                 new_giveaway=True,
                 scheduled_task=False,
                 existing_tweet_url=None,
                 tweet_text=None):
        """

        :param user_id: user_id
        :param order_id: Order ID
        :param sponsors: Sponsors and also who to follow
        :param giveaway_amount: Amount pulled from item
        :param duration: Duration to run giveaway
        :param new_giveaway: Set to false when using for tweet retriever
        :param existing_tweet_url: Could eventually just check if this is present
        :param tweet_text: Text to include in body
        """
        try:
            if sponsors and duration:
                self.giveaway_text = self.build_tweet(amount=giveaway_amount,
                                                      duration=duration,
                                                      sponsors=sponsors)
        except Exception as e:
            logging.error(f'Could not load Giveaway manager. Reason: {e}')
        self.sponsors = sponsors
        self.giveaway_amount = giveaway_amount
        self.duration = duration
        self.tweet_text = tweet_text
        self.new_giveaway = new_giveaway
        self.winner = None
        self.scheduled_task = scheduled_task # When True it will skip sleep mechanism
        self.tweet_id = None
        self.twitter_interact = TwitterInteract()
        self.launched_tweet = None
        self.participants = None
        self.user_id = user_id
        self.order_id = order_id
        self.start_time = None
        self.end_time = None
        self.tweet_id_key = None  # UUID for TwitterGiveawayId
        self.tweet_url = None
        self.results = None
        self.existing_tweet_url = None
        if existing_tweet_url:
            self.existing_tweet_url = existing_tweet_url
            self.process_retrieved_tweets = ProcessRetrievedTweets(tweet_url=existing_tweet_url, user_id=self.user_id)
            self.build_tweet_url()

    logging.info("Ready to go")

    def generate_giveaway_id(self):
        return str(uuid.uuid4())[0:8]

    def build_sponsors(self, sponsors=[]):
        sponsor_text = ''
        if sponsors:
            if len(sponsors) > 1:
                last_person = sponsors.pop(-1)
                sponsor_text = ', '.join(sponsors) + f' & {last_person}'
            else:
                sponsor_text = ', '.join(sponsors)
        return sponsor_text

    def build_tweet_url(self):
        if self.new_giveaway:
            logging.info("Creating new giveaway")
            tweet_json = self.launched_tweet._json
            author = tweet_json.get('user').get('screen_name')
            self.tweet_id = tweet_json.get('id_str')
        if self.existing_tweet_url:
            author = self.process_retrieved_tweets.author
            self.tweet_id = self.process_retrieved_tweets.tweet_id
        tweet_url = f'https://twitter.com/{author}/status/{self.tweet_id}'
        self.tweet_url = tweet_url
        self.tweet_id_key, created = TwitterGiveawayID.objects.get_or_create(tweet_url=tweet_url)
        return tweet_url

    def build_tweet(self, amount=None, duration=None, sponsors=[]):
        giveaway_id = str(uuid.uuid4())[0:8]
        sponsor_text = self.build_sponsors(sponsors)
        beautiful_time = display_time(duration)
        tweet_text = f"I'll give ${amount} to a random user who retweets this tweet within the next {beautiful_time}.\n\nMust be following {sponsor_text}\n\nSponsor a giveaway like this at gridgaming.io/shop\n\nID:{giveaway_id}"
        return tweet_text

    def create_giveaway_entry(self):
        try:

            giveaway_title = f'${self.giveaway_amount} Giveaway'
            Giveaway.objects.create(title=giveaway_title,
                                    description=f'${self.giveaway_amount} lasting for {display_time(self.duration)}',
                                    url=self.build_tweet_url(),
                                    giveaway_end_date=giveaway_ends(self.duration),
                                    visible=True,
                                    sponsored=True)
        except Exception as e:
            print('Error creating giveaway entry')
            print(e)

    def launch_giveaway(self):
        """ Launch a giveaway with the wording for the tweet """
        self.start_time = datetime.datetime.now()
        logging.info(f"[+] Giveaway launch time: {self.start_time}")
        change_order_status(self.order_id, 'L')

        # Record sponsor initial follower count
        # TODO Add sponsor initial follower count
        self.launched_tweet = self.twitter_interact.api.update_status(self.giveaway_text)

    def retrieve_tweets(self):
        self.tweet_url = self.build_tweet_url()
        contest = ProcessRetrievedTweets(tweet_url=self.tweet_url, user_id=self.user_id)
        contest.run_pipeline()
        self.participants = contest.participants

    def choose_winner(self):
        logging.info(f'[*] Randomly selecting from {len(self.participants)} users')
        winner = random.choice(self.participants)
        # TODO Add bot analysis
        # TODO Integrate
        results, created = GiveawayResults.objects.get_or_create(giveaway_id=self.tweet_id_key)
        self.results = results
        self.results.participants = len(self.participants)
        self.results.winner = winner
        self.results.save()
        self.winner = winner.user_screen_name
        logging.info(f'Giveaway winner is: @{self.winner}')
        change_order_status(self.order_id, 'T')
        return winner

    def perform_winner_analysis(self, winner=None):
        # TODO Add following sponsors relationship
        eligibility = True
        reason = None
        bc = BotCheck(username=winner)
        logging.info(bc.user_analysis)
        bot = bc.bot_prediction()
        if bot:
            eligibility = False
            reason = "User is a bot"
        following, member_not_followed = self.contestant_following_sponsors(winner)
        if not following:
            eligibility = False
            reason = f"Winner was not following {member_not_followed}"
        return reason, eligibility

    def contestant_following_sponsors(self, contestant):
        following_sponsors = True
        member_not_followed = None
        for sponsor in self.sponsors:
            following_sponsors = self.check_relationship(user_a=sponsor, user_b=contestant)
            if not following_sponsors:
                member_not_followed = sponsor
                following_sponsors = False
        return following_sponsors, member_not_followed



    def check_relationship(self, user_a=None, user_b=None):
        """
        user_a: Person you want to check is being followed
        user_b: Person who should be following
        """
        friends = self.twitter_interact.api.show_friendship(source_screen_name=user_a, target_screen_name=user_b)
        following = friends[1].following

        if following:
            logging.info(F'{user_b} is following {user_a}!')
        else:
            logging.info(F'{user_b} is NOT following {user_a} :(')

        return following

    def reply_to_original_tweet(self):
        self.end_time = datetime.datetime.now()
        self.twitter_interact.api.update_status(f"WINNER: @{self.winner} 🏆", in_reply_to_status_id=self.tweet_id)

    def notify_winner(self):
        winner_message = f'Congratulations! You won ${self.giveaway_amount}! What is your cashapp or paypal?'
        logging.info(f'[*] Notifying winner with this text: {winner_message}')
        change_order_status(self.order_id, 'C')
        self.twitter_interact.send_user_message(self.winner, winner_message)

    def remove_tweet(self):
        # Possible feature to remove tweet and keep clean timeline
        pass

    def populate_giveaway_stats(self):
        giveaway_id, created = TwitterGiveawayID.objects.get_or_create(tweet_url=self.tweet_url)
        giveaway_stats, created = GiveawayStats.objects.get_or_create(giveaway_id=giveaway_id)
        giveaway_stats.giveaway_start_time = self.start_time
        giveaway_stats.giveaway_end_time = self.end_time
        # TODO Add retweet count and follower counts
        if self.order_id:
            giveaway_stats.order_id = self.order_id
        giveaway_stats.save()

    def sleep_for_duration(self):
        giveaway_duration = int(self.duration) * 60
        logging.info(f'Giveaway is live! Choosing winner in {self.duration} minutes')
        time.sleep(giveaway_duration)

    def test_method(self, duration):
        print(f'sleeping for {duration}')
        time.sleep(duration)


    def run_pipeline(self):
        if self.new_giveaway:
            self.launch_giveaway()
            self.create_giveaway_entry()
            # if not self.scheduled_task:
            #     self.sleep_for_duration()
        else:
            self.retrieve_tweets()
            eligible_to_win = False
            rerolls = []
            while not eligible_to_win:
                winner_obj = self.choose_winner()
                reason, eligible_to_win = self.perform_winner_analysis(self.winner)
                if not eligible_to_win:
                    logging.info(f'{self.winner} is not eligible... rerolling: Reason: {reason}')
                    reroll_record, created = get_user(winner_obj)
                    rerolls.append(reroll_record)
            # Add people who got rerolled
            self.results.save()
            if rerolls:
                logging.info("Adding {rerolls} rerolls to db".format(rerolls=len(rerolls)))
                self.results.re_rolls.add(*rerolls)
            self.populate_giveaway_stats()
            
        # if self.new_giveaway:
            self.reply_to_original_tweet()
            self.notify_winner()
