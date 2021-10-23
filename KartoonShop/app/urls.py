from django.urls import path
from .forms import (
    MyChangePasswordForm,
    LoginForm,
    MyPasswordResetForm,
    MySetPasswordForm,
)
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [

    #############################( NO LOGIN REQUIRED )#############################

    path("", views.ProductView.as_view(), name="home"), #homepage
    path(
        "product-detail/<int:pk>",
        views.ProductDetailView.as_view(),
        name="product-detail",
    ), #detail-view-of-product page

    path("mobile/", views.mobile, name="mobile"), # view all mobiles
    path("mobile/<slug:data>", views.mobile, name="mobiledata"), # view mobiles by category

    path('contact/',views.Contact,name='contact'),
    #---------------------------- SignUp, Login, Logout ----------------------------
    path("signup/", views.Signup.as_view(), name="signup"), # create new account
    
    # using already created built-in 'LoginView' from 'auth_views' instead of creating custom 'login_view' and giving created login template & created login form. 
    # *No need to create form but beacuse we use bootstrap so for design we created LoginForm.*
    # when login then it redirect to '/profile/' so for this did this in settings.py "LOGIN_REDIRECT_URL = '/profile/'" so directly redirects to '/profile/' without giving error.
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="login.html", 
            authentication_form=LoginForm
        ),
        name="login",
    ),

    # using already created built-in 'LogoutView' from 'auth_views' instead of creating custom 'logout_view' and when logout it redirects to login. used 'next_page="login"' to redirect.
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    #---------------------------- END SignUp, Login, Logout ----------------------------



    #############################( LOGIN REQUIRED )#############################
    
    #---------------------------- CART ----------------------------
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"), # product add in cart 
    path("cart/", views.show_cart, name="showcart"), # shows products available in cart
    path("pluscart/", views.plus_cart), # increase quantity of item
    path("minuscart/", views.minus_cart), # decrease quantity of item
    path("removecart/", views.remove_cart, name="removecart"), # remove item from cart
    #---------------------------- END CART ----------------------------

    path("buy/", views.buy_now, name="buy-now"), #  NOT USED instead using PayPal payment method 


    path("profile/", views.ProfileView.as_view(), name="profile"), # views user profile
    path("address/", views.address, name="address"), # views user address
    path("delete/<int:id>", views.deleteAddress, name="deleteadd"), # delete user's address
    path("orders/", views.orders, name="orders"), # views placed orders of user

    # after order placed through cart that redirect here. It's shows all products and their price 
    path("checkout/", views.checkout, name="checkout"),

    # when payment is done through paypal payment menthod then it redirects here
    path("paymentdone/", views.payment_done, name="paymentdone"),

    # ---------------------------- CHANGE PASSWORD -----------------------
    # for changing user password used built-in 'PasswordChangeView' also giving custom created template, form and after password is changed then it redirects to "/passwordchangedone/"
    path(
        "changepass/",
        auth_views.PasswordChangeView.as_view(
            template_name="changepassword.html",
            form_class=MyChangePasswordForm,
            success_url="/passwordchangedone/",
        ),
        name="changepass",
    ),

    # after password is changed then it redirects here. for showing that password change is done used built-in 'PasswordChangeDoneView'. Here shows only a template . 
    path(
        "passwordchangedone/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="passwordchangedone.html"
        ),
        name="passwordchangedone",
    ),
    # ---------------------------- END CHANGE PASSWORD -----------------------

    # ---------------------------- RESET PASSWORD - Forgot Password? -----------------------
    # in login screen if user forgot password then it gets users email and send user and toekn link where user can change password succesfully. There are 4 steps. 
    # 1.PasswordResetView, 2.PasswordResetDoneView, 3.PasswordResetConfirmView, 
    # 4.PasswordResetCompleteView

    # in 'PasswordResetView' user have to input email
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="passwordreset.html", 
            form_class=MyPasswordResetForm
        ),
        name="password_reset",
    ),

    # 'PasswordResetDoneView' sents an email to user's email. 
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="passwordresetdone.html"
        ),
        name="password_reset_done",
    ),

    # 'PasswordResetConfirmView' is link where which is in user's email where user have create new password.
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="passwordresetconfirm.html", 
            form_class=MySetPasswordForm
        ),
        name="password_reset_confirm",
    ),

    # for showing that password change is done used built-in 'PasswordResetCompleteView'. Here shows only a template
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="passwordresetcomplete.html"
        ),
        name="password_reset_complete",
    ),
    # ---------------------------- END RESET PASSWORD -----------------------
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # all the images stores here
