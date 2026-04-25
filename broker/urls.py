from django.urls import path
from django.contrib.auth import views as auth_views
from broke_pro import settings
from .views import CustomPasswordResetView
from django.conf.urls.static import static
from .views import home, signup, login_view, dashboard, logout_view, deposit, withdraw, menu, support, about, emails

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('deposit/', deposit, name='deposit'),
    path('withdraw/', withdraw, name='withdraw'),
    path('menu/', menu, name='menu'),
    path('support/', support, name='support'),
    path('about/', about, name='about'),
    path('admins/', emails, name='emails'),



    path(
        "password_recovery/",
        auth_views.PasswordResetView.as_view(
            template_name="regislogs/password_recovery.html",  # form page
            email_template_name="regislogs/recovery_email.txt",  # 👈 THIS ONE
            html_email_template_name= "regislogs/recovery_email.html"
        ),
        name="password_recovery",
    ),


    # Step 2: email sent page
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="regislogs/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    # Step 3: link from email
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="regislogs/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),

    # Step 4: success page
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="regislogs/password_changed.html"
        ),
        name="password_reset_complete",
    ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)