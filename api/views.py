import datetime
from django.db.models import Max
from rest_framework import mixins, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api.models import Restaurant, Menu, Employee, Vote
from api.permisions import (
    IsRestaurantStaffOrIfAuthenticatedReadOnly,
    IsEmployee)
from api.serializers import (
    MenuSerializer,
    RestaurantSerializer,
    EmployeeSerializer
)

YESTERDAY = datetime.date.today() - datetime.timedelta(days=1)


class RestaurantViewSet(
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAdminUser,)


class EmployeeViewSet(
    mixins.CreateModelMixin,
    GenericViewSet,
):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (IsAdminUser,)


class MenuViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsRestaurantStaffOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        if self.action == "list":

            return Menu.objects.filter(created_at__gt=YESTERDAY)


class VoteAPIView(APIView):
    permission_classes = (IsAuthenticated, IsEmployee,)

    def get(self, request, menu_id):
        user = self.request.user
        employee = Employee.objects.get(user__username=user.username)
        menu = Menu.objects.get(id=menu_id)

        if Vote.objects.filter(
            employee__user__username=user.username,
            voted_at__gt=YESTERDAY,
            menu__id=menu_id,
        ).exists():
            res = {"msg": "You already voted!", "data": None, "success": False}
            return Response(data=res, status=status.HTTP_200_OK)
        else:
            Vote.objects.create(employee=employee, menu=menu)
            menu.votes += 1
            menu.save()

            qs = Menu.objects.filter(created_at__gt=YESTERDAY)
            serializer = MenuSerializer(qs, many=True)
            res = {
                "msg": "You voted successfully!",
                "data": serializer.data,
                "success": True,
            }
            return Response(data=res, status=status.HTTP_200_OK)


class TodaysResult(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        max_votes = Menu.objects.filter(created_at__gt=YESTERDAY).aggregate(
            Max("votes")
        )["votes__max"]
        winner = Menu.objects.get(votes=max_votes)
        serializer = MenuSerializer(winner)
        return Response(serializer.data)
