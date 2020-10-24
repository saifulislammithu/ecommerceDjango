from django.urls import path
from.import views
urlpatterns = [
path('',views.index, name="users"),
path('login/',views.login_view, name="login"),
path('register/',views.register, name="register"),
path('logout_view/',views.logout_view, name="logout"),
]