from django.urls import path, include, re_path
from .views import index, home, profile, account_type, update_account_type, pre_checkout, CheckoutView, PaypalPaymentView, payment_canceled, payment_done, StripePaymentView, get_membership, CoinbasePaymentView, CreditView, set_membership_alert
from django.contrib.auth.decorators import login_required

app_name = 'frontend'

urlpatterns = [
    # path('', index, name='index'),
    path('', home, name='home'),
    path('profile', profile, name='profile'),
    path('profile/get_membership', get_membership, name='get_membership'),
    path('profile/set_membership_alert', set_membership_alert, name='set_membership_alert'),
    path('profile/account_type', account_type, name='account_type'),
    path('profile/update_account_type', update_account_type, name='update_account_type'),
    path('pre_checkout', pre_checkout, name='pre_checkout'),
    path('checkout', login_required(CheckoutView.as_view()), name='checkout'),
    path('wallet', login_required(CreditView.as_view()), name='credits'),
    path('wallet/paypalpayment', login_required(PaypalPaymentView.as_view()), name='paypalpayment'),
    path('wallet/stripepayment', login_required(StripePaymentView.as_view()), name='stripepayment'),
    path('wallet/coinbasepayment', login_required(CoinbasePaymentView.as_view()), name='coinbasepayment'),
    path('wallet/payment_done', payment_done, name='payment_done'),
    path('wallet/payment_canceled', payment_canceled, name='payment_canceled'),
    re_path(r'^paypal/',include('paypal.standard.ipn.urls')),
]
