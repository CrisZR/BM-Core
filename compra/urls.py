from django import urls
from .views import *

app_name = "compra"

urlpatterns = [
    urls.path("add/", add, name="add"),
]
