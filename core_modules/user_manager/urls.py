from django.urls import path

from core_modules.user_manager import views

urlpatterns = [
    # AUTH
    path("login/", views.LoginUserView.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("refresh/", views.RefreshAPIView.as_view(), name="refresh"),
    # USER API
    path("user/", views.GetUserAPIView.as_view(), name="users list"),
    path("<int:pk>/user-detail/", views.UserDetail.as_view(), name="user details"),
    path("add-user/", views.UserView.as_view(), name="user create"),
]
