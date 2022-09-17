from django.urls import path

from app.views import delete_coin, home

urlpatterns = [
   path("", home, name="home"),
   path("delete/<int:id>", delete_coin, name="delete")
]