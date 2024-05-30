from django.urls import path
from . import views
from allauth.account.views import SignupView, LoginView, LogoutView

class MySignupView(SignupView):
    template_name = 'signup.html'

class MyLoginView(LoginView):
    template_name = 'login.html'

# class MyLogoutView(LogoutView):
#     def get_

urlpatterns = [
    path('', views.home, name="home"),
    path('accounts/signup', MySignupView.as_view(), name='account_signup'),
    path('accounts/login', MyLoginView.as_view(), name='account_login'),
    path('upload_data', views.upload_data, name='upload_data'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('upload_csv_simple/', views.upload_csv_simple, name='upload_csv_simple'),
    path('builder/', views.query_builder, name='builder'),
    path('query/', views.QueryBuilderAPIView.as_view(), name='query'),
    path('users/', views.users, name='users'),

]
