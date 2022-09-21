from django.urls import path, include
from rest_framework import routers

from api.views import (
    RestaurantViewSet,
    MenuViewSet,
    EmployeeViewSet,
    VoteAPIView,
    TodaysResult,
)

router = routers.DefaultRouter()

router.register("restaurants", RestaurantViewSet)
router.register("menus", MenuViewSet, basename="menus")
router.register("employees", EmployeeViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("menus/vote/<int:menu_id>/", VoteAPIView.as_view(), name="vote"),
    path("todays-result/", TodaysResult.as_view(), name="todays_result"),
]

app_name = "api"
