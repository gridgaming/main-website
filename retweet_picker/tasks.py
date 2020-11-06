from django_rq import job
import time
from retweet_picker.manager import GiveawayManager
from background_task import background
from .models import  Membership, GiveawayWinners, DrawPrice, ContestUserParticipation, ContestUserAccounts, TwitterGiveawayID


def start_giveaway_bg(user_id=None,
                      order_id=None,
                      sponsors=None,
                      giveaway_amount=None,
                      duration=None):
    from django.db import connection
    connection.close_if_unusable_or_obsolete()

    gm = GiveawayManager(
        user_id=user_id,
        order_id=order_id,
        sponsors=sponsors,
        giveaway_amount=giveaway_amount,
        duration=duration)

    gm.run_pipeline()
    return gm.tweet_url

def retrieve_tweets_choose_winner_job(existing_tweet_url=None,
                                     user_id=None, order_id=None, giveaway_amount=0, sponsors=None):
    from django.db import connection
    connection.close()
    gm = GiveawayManager(user_id=user_id, order_id=order_id,
                         existing_tweet_url=existing_tweet_url, 
                         new_giveaway=False, giveaway_amount=giveaway_amount, sponsors=sponsors)
    gm.run_pipeline()
    
def fetch_content_from_url(existing_tweet_url=None):
    # from django.db import connection
    # connection.close()
    res = {'success': True, 'msg': ''}
    try:
        gm = GiveawayManager(new_giveaway=False,
                             existing_tweet_url=existing_tweet_url)
        if gm.tweet_id:
            res['tweet_id'] = gm.tweet_id
            res['tweet_url'] = gm.tweet_url
        else:
            res['success'] = False
            res['msg'] = "Can't process this url. Are you sure this url is correct?"
    except Exception as e:
        print(e)
        res['success'] = False
        res['msg'] = "Can't process this url. Are you sure this url is correct?"
    return res

def draw_winner(existing_tweet_url=None, winner_count=1, actions=None, user_id=None):
    # from django.db import connection
    # connection.close()
    gm = GiveawayManager(new_giveaway=False,
                         existing_tweet_url=existing_tweet_url,
                         winner_count=winner_count,
                         sponsors=actions['sponsors'],
                         user_id=user_id)
    res = gm.drawwinner(actions=actions)
    return res

@background(schedule=60)
def load_entry_task(gwid, user_id, pay_status):
    try:
        gw = GiveawayWinners.objects.get(id=gwid)
        tgid = TwitterGiveawayID.objects.get(id=gw.giveaway_id_id)
        tweet_url = tgid.tweet_url
        gm = GiveawayManager(new_giveaway=False,
                             existing_tweet_url=tweet_url,
                             user_id=user_id)
        ret_count = gm.tweet.retweet_count
        dp = DrawPrice.objects.all().first()
        gw.retweet_count = ret_count
        cups = ContestUserParticipation.objects.filter(contest=tgid, user_id=gw.user_id)
        if cups.exists():
            cups[0].contestants.clear()

        toload_count = gw.paid_count + dp.free_max
        if pay_status == 2:
            toload_count = ret_count
        if toload_count > ret_count:
            toload_count = ret_count
        gw.toload_count = toload_count
        gw.save()
        res = gm.retrieve_tweets(gwid=gwid, max_tweets=gw.toload_count)
        if res['success'] == True:
            GiveawayWinners.objects.filter(id=gwid).update(status='L')
            if pay_status == 2:
                mss = Membership.objects.filter(user_id=gw.user_id)
                if mss.exists() and mss[0].plan != 'F':
                    ms = mss[0]
                    ms.done_count += 1
                    ms.save()
            
    except Exception as e:
        print(e)
        res['success'] = False
        res['msg'] = 'Downloading entries failed. Please try again.'
        
    if res['success'] == False:
        GiveawayWinners.objects.filter(id=gwid).update(status='E', load_error=res['msg'])
        
@job('default')
def sleeper():
    from django.db import connection
    connection.close()
    print('sleeping for 10 sec')
    time.sleep(10)
