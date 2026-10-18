from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("capteurs/", include("capteurs.urls")),
    # Confort : la racine renvoie vers la liste des capteurs.
    path("", RedirectView.as_view(pattern_name="capteurs:liste", permanent=False)),
]
