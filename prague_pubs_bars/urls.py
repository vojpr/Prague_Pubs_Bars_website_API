from django.contrib import admin
from django.urls import path
from .views import IndexPageView
from pubs_app.views import PubsListView, PubsGenericAPIView, AuthPubsGenericAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", IndexPageView.as_view(), name="index"),
    path("show/", PubsListView.as_view(), name="pubs_list"),
    path("bars-api/", PubsGenericAPIView.as_view()),
    path("bars-api/<int:id>/", PubsGenericAPIView.as_view()),
    path("auth-bars-api/", AuthPubsGenericAPIView.as_view()),
    path("auth-bars-api/<int:id>/", AuthPubsGenericAPIView.as_view()),
]
