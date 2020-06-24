from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'slotapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('createusers', views.create_users, name='create_users'),
    path('first-page', views.first_page, name='first_page'),
    path('tocart', views.tocart, name='tocart'),
    path('getcart', views.getcart, name='getcart'),
    path('setpause', views.setpause, name='setpause'),
    path('cartminus', views.cartminus, name='cartminus'),
    path('checkout', views.checkout, name='checkout'),
    path('get_available', views.get_available, name='get_available'),
    path('payment', views.slot_payment, name='slot_payment'),
    path('payment_execute', views.slot_payment_execute, name='slot_payment_execute'),
    path('logout', views.user_logout, name='user_logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)