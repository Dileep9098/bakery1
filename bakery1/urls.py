
from django.contrib import admin
from django.urls import path
from mainApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home),
    path("product/<str:fl>/<str:ct>/<str:sp>/",views.product),
    path('single-product/<int:id>/',views.singleProduct),
    path('login/',views.loginPage),
    path('logout/',views.logoutPage),
    path('singup/',views.signupPage),
    path('profile/',views.profilePage),
    path('update-profile/',views.updateProfile),
    path('cart/',views.cartPage),
    path('add-to-cart/<int:id>/',views.addToCart),
    path('delete-cart/<int:pid>/',views.deleteCart),
    path('update-cart/<int:pid>/<str:op>/',views.updateCart),
    path('add-to-wishlist/<int:pid>/',views.addToWishlist),
    path('delete-wishlist/<int:id>/',views.deleteWishlist),
    path('checkout/',views.checkout),
    path('order/',views.orderPage),
    path('confirmation/',views.confirmation),
    path('contact/',views.contact),
    path("search/",views.searchPage),
    path("forget-username/",views.forgetUsername),
    path("forget-otp/",views.forgetOTP),
    path('reviews/',views.reviews),

    path("forget-password/",views.forgetPassword),
    path('paymentSuccess/<str:rppid>/<str:rpoid>/<str:rpsid>/',views.paymentSuccess),




    

    



]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


# from django.contrib import admin
# from django.urls import path
# from django.conf import settings
# from django.conf.urls.static import static
# from mainApp import views
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('',views.home),
#     path('shop/<str:mc>/<str:sc>/<str:br>/',views.shop),
#     path('single-product/<int:id>/',views.singleProduct),
#     path('login/',views.loginPage),
#     path('logout/',views.logoutPage),
#     path('signup/',views.signupPage),
#     path('profile/',views.profilePage),
#     path('update-profile/',views.updateProfilePage),
#     path('add-to-cart/<int:id>/',views.addToCart),
#     path('cart/',views.cartPage),
#     path('delete-cart/<int:pid>/',views.deleteCart),
#     path('update-cart/<int:pid>/<str:op>/',views.updateCart),
#     path('add-to-wishlist/<int:pid>/',views.addToWishlist),
#     path('delete-wishlist/<int:pid>/',views.deleteWishlist),
#     path('checkout/',views.checkoutPage),
#     path('order/',views.orderPage),
#     path('confirmation/',views.confirmationPage),
#     path('contact/',views.contactPage),
#     path('search/',views.searchPage),
#     path('forget-username/',views.forgetUsername),
#     path('forget-otp/',views.forgetOTP),
#     path('forget-password/',views.forgetPassword),
#     path('paymentSuccess/<str:rppid>/<str:rpoid>/<str:rpsid>/',views.paymentSuccess),
# ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
