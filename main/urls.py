from django.urls import  path
from django.conf.urls import handler404

from . import views

app_name = 'main'
# Page d'erreur
handler404 = views.error_404

urlpatterns = [
    path("", view=views.home, name="description"),
    path("order/ia", view=views.recommendationForm, name="index"),
    path("contact", view=views.contact, name="contact"),
    path("recommendations", view=views.withai_recommendation, name="withai_submit"),
    path("detail/<str:id>/<str:time>", view=views.detail, name="detail"),
    path("success/order", view=views.successPage, name="success-order"),
    path("error/page", view=views.errorPage, name="error-page"),
    path("commander", view=views.processOrderPage, name="process-order"),

    path("order/simple", view=views.recommendationFormWithoutAI, name="order-without-ai"), 
    path("perform/simple/order", view=views.performSimpleOrder, name="perform-simple-order"),
    path("simple/order/<str:id>/recommendation", view=views.displaySimpleOrderRecommendation, name="list-recommendation-withoutai"),
    path("download/order", view=views.downloadOrderPdf, name="download-order"),
    # path("description", view=views.home, name=""),

    # Market place
    path("market", view=views.market, name="market"),
    path("not-find-error", view=views.notUrlfind, name="error_404")

     # path("about", view=views.about, name="about"),
    # path("privacies", view=views.privacy, name="privacies"), 
    # path("order/zoodoAI", view=views.recommendationForm, name="recommendationForm"),

]



