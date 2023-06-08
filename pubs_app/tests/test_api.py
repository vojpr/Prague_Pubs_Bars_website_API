from django.urls import reverse
import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from pubs_app.models import PubsBars
from pubs_app.serializers import PubsBarsSerializer
from django.contrib.auth.models import User


class BaseTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username="testuser", password="12345")
        cls.test_token = Token.objects.create(user=cls.test_user)
        number_of_pubs = 3
        for pub_num in range(number_of_pubs):
            PubsBars.objects.create(
                name = f"Pub {pub_num}",
                map_url = "https://goo.gl/maps/qY984V1Zaio8p3me9",
                open_time = "1:00",
                close_time = "1:00",
                beer_rating = 5,
                outside_tables = True,
                foosball = True,
                overall_rating = 5,
            )
        cls.valid_data = {
            "name": "New Pub",
            "map_url": "https://goo.gl/maps/enawNkvv7jXbJhXP6",
            "open_time": "1:00",
            "close_time": "1:00",
            "beer_rating": 4,
            "outside_tables": True,
            "foosball": None,
            "overall_rating": 5,
        }
        cls.valid_updated_data = {
            "name": "Updated Pub Name",
            "map_url": "https://goo.gl/maps/enawNkvv7jXbJhXP6",
            "open_time": "1:00",
            "close_time": "1:00",
            "beer_rating": 4,
            "outside_tables": True,
            "foosball": None,
            "overall_rating": 5,
        }
        cls.invalid_data = {
            "name": "",
            "map_url": "https://goo.gl/maps/enawNkvv7jXbJhXP6",
            "open_time": "1:00",
            "close_time": "1:00",
            "beer_rating": 4,
            "outside_tables": True,
            "foosball": None,
            "overall_rating": 5,
        }


class GetMethodTest(BaseTest):
    def test_get_all_pubs(self):
        response = self.client.get(reverse("get_all_bars"))
        pubs = PubsBars.objects.all()
        serializer = PubsBarsSerializer(pubs, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_pub_valid(self):
        response = self.client.get(reverse("get_bar", kwargs={"id": PubsBars.objects.first().pk}))
        pub = PubsBars.objects.first()
        serializer = PubsBarsSerializer(pub)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_pub_invalid_id(self):
        response = self.client.get(reverse("get_bar", kwargs={"id": PubsBars.objects.last().pk + 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostMethodTest(BaseTest):
    def test_post_pub_valid(self):
        self.assertEqual(PubsBars.objects.count(), 3)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_token.key)
        response = self.client.post(
            reverse("post_bar"), 
            data=json.dumps(self.valid_data), 
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PubsBars.objects.count(), 4)

    def test_post_pub_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_token.key)
        response = self.client.post(
            reverse("post_bar"), 
            data=json.dumps(self.invalid_data), 
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_pub_invalid_authentication(self):
        response = self.client.post(
            reverse("post_bar"), 
            data=json.dumps(self.valid_data), 
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PutMethodTest(BaseTest):
    def test_put_pub_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_token.key)
        self.assertEqual(PubsBars.objects.first().name, "Pub 0")
        response = self.client.put(
            reverse("put_delete_bar", kwargs={"id": PubsBars.objects.first().pk}), 
            data=json.dumps(self.valid_updated_data), 
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PubsBars.objects.first().name, "Updated Pub Name")

    def test_put_pub_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_token.key)
        response = self.client.put(
            reverse("put_delete_bar", kwargs={"id": PubsBars.objects.first().pk}),
            data=json.dumps(self.invalid_data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_pub_invalid_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_token.key)
        response = self.client.put(
            reverse("put_delete_bar", kwargs={"id": PubsBars.objects.last().pk + 1}),
            data=json.dumps(self.invalid_data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_pub_invalid_authentication(self):
        response = self.client.put(
            reverse("put_delete_bar", kwargs={"id": PubsBars.objects.first().pk}),
            data=json.dumps(self.valid_updated_data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteMethodTest(BaseTest):
    def test_delete_pub_valid(self):
        self.assertEqual(PubsBars.objects.count(), 3)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_token.key)
        response = self.client.delete(reverse("put_delete_bar", kwargs={"id": PubsBars.objects.first().pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PubsBars.objects.count(), 2)

    def test_delete_pub_invalid_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_token.key)
        response = self.client.delete(reverse("put_delete_bar", kwargs={"id": PubsBars.objects.last().pk + 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_pub_invalid_authentication(self):
        response = self.client.delete(reverse("put_delete_bar", kwargs={"id": PubsBars.objects.first().pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
