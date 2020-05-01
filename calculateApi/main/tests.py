from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIRequestFactory
from requests.auth import HTTPBasicAuth
from .models import Add, Calculate
from django.contrib.auth.models import User
import json

class AddTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('test', 'test@gmail.com', 'test123')
        self.client.login(username='test', password='test123')
        Add.objects.create(value="3, 4", user=user)
       
    def test_single_post_statuscode(self):
        response = self.client.post('/add/', {'value': '1'})
        self.assertEqual(response.status_code, 201)

    def test_multiple_post_statuscode(self):
        response = self.client.post('/add/', {'value': '12, 13, 15, 17'})
        self.assertEqual(response.status_code, 201)

    def test_fail_status(self):
        response = self.client.post('/add/', {'value': '12, 13, ,'})
        self.assertEqual(response.status_code, 406)

    def test_fail_content(self):
        response = self.client.post('/add/', {'value': 'qwe'})
        self.assertEqual(response.content, b"Invalid data")
        
    def test_correct_content(self):
        response = self.client.post('/add/', {'value': '1'})
        self.assertEqual(response.content, b"")

class CalculateTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('test', 'test@gmail.com', 'test123')
        self.client.login(username='test', password='test123')
        Add.objects.create(value="3, 4, 1", user=user)
        Calculate.objects.create(number=10, user=user)
        Calculate.objects.create(number=9, user=user)

    def queryset_to_json(self, value, arr):
        dict_array = []
        for c in arr:
            num_dict = {}
            num_dict[value] = c.number
            dict_array.append(num_dict)
        dict_array = json.dumps(dict_array)
        return dict_array
    
    def test_response(self):
        response = self.client.get('/calculate/')
        self.assertEqual(response.content, b"8")
    
    def test_statuscode(self):
        response = self.client.get('/calculate/')
        self.assertEqual(response.status_code, 200)

    def test_all_statuscode(self):
        response = self.client.get('/calculate/?all=1')
        self.assertEqual(response.status_code, 200)

    def test_all_response(self):
        response = self.client.get('/calculate/?all=1')
        user = User.objects.get(username="test")
        cal = Calculate.objects.filter(user=user).order_by("-id")

        calculation_array = self.queryset_to_json("number", cal)

        self.assertEqual(response.content.decode('ascii'), calculation_array)