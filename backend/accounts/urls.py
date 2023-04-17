from django.urls import path

from accounts import views

from rest_framework_simplejwt.views import TokenRefreshView
app_name = "accounts"



urlpatterns = [
    path("login/",views.LoginApiView.as_view(), name="login"),
    path("logout/", views.LogoutApiView.as_view(), name="logout"),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('register/', views.RegisterApiView.as_view(), name="register"),
    path("verify/", views.VerifyEmail.as_view(), name="email_verify"),
    path("resend-verify/", views.ResendEmailLinkApiView.as_view(), name='resend'),
    path("user/", views.UserApiView.as_view(), name="get_user"),
    path('profile/', views.ProfileDetailUpdateApiView.as_view(), name='profile'),
    path('password/change/', views.PasswordChangeApiView.as_view(), name="password_change"),
    path('password/reset/link/', views.PasswordResetLinkApiView.as_view(), name="password_reset_link"),
    path('password/reset/', views.PasswordResetApiView.as_view(), name="password_reset"),
]