from rest_framework.routers import DefaultRouter

from .api_views import CapteurViewSet

router = DefaultRouter()
router.register("capteurs", CapteurViewSet, basename="capteur")

urlpatterns = router.urls
