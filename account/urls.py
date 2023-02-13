from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="login_user"),
    path('register/',views.register, name="register_user"),
    path('logout/',views.logout_user, name="logout_user"),
    path('',views.dashboard, name="dashboard"),
    path('apply/<int:meroshare_id>',views.apply, name="apply"),
    path('history/',views.history, name="history"),
    path('delete/<int:meroshare_id>',views.delete, name="history"),

]