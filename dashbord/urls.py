from django.urls import  path
from django.conf.urls import handler404

from . import views

app_name = 'dashbord'

urlpatterns = [
    path("", view=views.authentication, name="connection"),
    path("index/", view=views.index, name="index"),
    path("logout", view=views.logout, name="logout"),
    path("profile", view=views.profile, name="profile"),
    path("register", view=views.register, name="register"),
    path("supplier", view=views.supplier, name="supplier"),
    path("computer-list", view=views.computer_list, name="computer-list"),
    path('add-computer-photo', view=views.add_computer_photo, name='add-computer-photo'),
    path("add-computer", view=views.add_computer, name="add-computer"),
    path("processed-orders", view=views.processed_orders, name="processed-orders"),
    path("unproccessedorders", view=views.unproccessedorders, name="unproccessed-orders"),
]



