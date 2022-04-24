"""GuptaIndustries URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import settings
from MyApp import views as my


from django.contrib.staticfiles.urls import static,staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', my.home),
    path('about/', my.about),
    path('product/<str:cn>/', my.product),
    path('ordersummaryview/', my.ordersummaryview.as_view(), name='ordersummaryview'),
    path('wishlistview/', my.wishlistview.as_view(), name='wishlistview'),

    path('contact/',my.contact),
    path('faq/', my.faq),
    path('login/', my.login),
    path('signup/', my.signup),
    path('checkout2/',my.ch),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/',my.logout),
    path('cart/<int:num>/',my.cart),
    path('removesingle/<int:num>/',my.removesingle),
    path('addsingle/<int:num>/',my.addsingle),
    path('remove/<int:num>/', my.remove),
    path('wremove/<int:num>/', my.wremove),





    path('wishlist/',my.wishlist),
    path('wish/<int:num>/',my.wish),
    path('checkout/',my.check),

    path('payment/', include(('payment.urls','payment'),namespace='payment')),
    path('paypal/',include('paypal.standard.ipn.urls')),

]
urlpatterns=urlpatterns+staticfiles_urlpatterns()
urlpatterns=urlpatterns+static(settings.MEDIA_URL,
                               document_root=settings.MEDIA_ROOT)