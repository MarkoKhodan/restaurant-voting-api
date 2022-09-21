from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.models import Menu, Restaurant, Employee
from api.serializers import MenuSerializer


class UnauthenticatedApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(reverse("api:todays_result"))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class EmployeeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
            is_employee=True,
            is_restaurant_staff=False
        )

        self.client.force_authenticate(self.user)
        self.restoraunt = Restaurant.objects.create(name="test")
        Menu.objects.create(restaurant=self.restoraunt)
        Employee.objects.create(user=self.user)

    def test_employee_can_vote(self):

        res = self.client.get(reverse("api:vote", kwargs={"menu_id": 1}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_employee_can_see_menus(self):
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)

        res = self.client.get(reverse("api:menus-list"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_employee_cant_put_menu(self):
        payload = {"restaurant": self.restoraunt}
        res = self.client.post(reverse("api:menus-list"), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class RestaurantStaffApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
            is_employee=False,
            is_restaurant_staff=True
        )

        self.client.force_authenticate(self.user)
        self.restaurant = Restaurant.objects.create(name="test")
        Employee.objects.create(user=self.user)

    def test_restaurant_staff_cant_vote(self):
        res = self.client.get(reverse("api:vote", kwargs={"menu_id": 1}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_staff_can_see_menus(self):
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)

        res = self.client.get(reverse("api:menus-list"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
