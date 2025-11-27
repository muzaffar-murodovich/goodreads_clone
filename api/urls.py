from api.views import BookReviewsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('reviews', BookReviewsViewSet, basename='review')

urlpatterns = router.urls