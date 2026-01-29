from chemicals.views import ChemicalRenderView, index_view
from django.urls import path

app_name = "chemicals"

urlpatterns = [
    path("", index_view, name="index"),
    path("answer/", ChemicalRenderView.as_view(), name="answer"),
]
