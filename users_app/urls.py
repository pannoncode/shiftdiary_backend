from django.urls import path
from users_app.views import NewUserView, UserProfileView


urlpatterns = [
    path("newuser/", NewUserView.as_view(), name="new-user"),
    path("users/", NewUserView.as_view(), name="all-user"),
    path("users/<int:pk>", NewUserView.as_view(), name="delete-patch-user"),
    path("user/", UserProfileView.as_view(), name="user")
]
