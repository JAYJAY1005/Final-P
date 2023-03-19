from django.urls import path
from rest_framework import routers
from .views import PostViewSet

router = routers.SimpleRouter()
router.register('posts', PostViewSet) #라우터로 'posts' 라고 설정 해놓음

urlpatterns = router.urls