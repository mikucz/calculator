from django.urls import include, path
from rest_framework import routers

from calculator import views

router = routers.DefaultRouter()
router.register(r"operators", views.OperatorViewSet)

urlpatterns = [
    path("calculator/", include(router.urls)),
]
