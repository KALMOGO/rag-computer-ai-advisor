from django.urls import  path
from django.conf.urls import handler404

from . import views

app_name = 'dashbord'

urlpatterns = [
    path("", view=views.authentication, name="connection"),
    path("index/", view=views.index, name="index"),
    path("logout", view=views.logoutUser, name="logout"),
    path("profile", view=views.profile, name="profile"),
    path("register", view=views.register, name="register"),
    path("supplier", view=views.supplier, name="supplier"),
    path("computer-list", view=views.computer_list, name="computer-list"),
    path('add-computer-photo', view=views.add_computer_photo, name='add-computer-photo'),
    path("add-computer", view=views.add_computer, name="add-computer"),
    path("perform-add-computer", view=views.perform_add_computer, name="perform_add_computer"),
    path("savePreInstalledSoftwares", view=views.savePreInstalledSoftwares, name="savePreInstalledSoftwares"),
    path("perform-add-images", view=views.perform_add_computer_images, name="perform_add_computer_images"),
    path("processed-orders", view=views.processed_orders, name="processed-orders"),
    path("unproccessedorders", view=views.unproccessedorders, name="unproccessed-orders"),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='updateOrderStatus'),
    path('delete-order/<int:order_id>/', views.detete_order, name='deleteOrder'), 
]



