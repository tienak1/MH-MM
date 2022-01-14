from django.urls import path

from django.contrib.auth.views import LogoutView

from .views import SignUpView, CustomLoginView, KeyView

app_name = 'user'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', CustomLoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('viewKey/', KeyView.as_view(), name='viewKey')
]