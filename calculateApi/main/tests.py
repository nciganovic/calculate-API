from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIRequestFactory
from requests.auth import HTTPBasicAuth
from .models import Add, Calculate, History
from django.contrib.auth.models import User
import json

class AddTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('test', 'test@gmail.com', 'test123')
        self.client.login(username='test', password='test123')
        self.client.post('/add/', {'value': '-3, 4'})

    def test_single_post_statuscode(self):
        response = self.client.post('/add/', {'value': '1'})
        self.assertEqual(response.status_code, 201)

    def test_multiple_post_statuscode(self):
        response = self.client.post('/add/', {'value': '12, -13, 15, -17'})
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
        self.client.post('/add/', {'value': '3, 4, 1'})
        self.client.get('/calculate/')
        self.client.post('/add/', {'value': '10'})
        self.client.get('/calculate/')
        self.client.post('/add/', {'value': '-9'})

    def queryset_to_json(self, value, arr):
        dict_array = []
        for c in arr:
            num_dict = {}
            num_dict[value] = c.number
            dict_array.append(num_dict)
        dict_array = json.dumps(dict_array)
        return dict_array
    
    def test_content(self):
        response = self.client.get('/calculate/')
        self.assertEqual(response.content, b"9")
    
    def test_statuscode(self):
        response = self.client.get('/calculate/')
        self.assertEqual(response.status_code, 200)

    def test_all_statuscode(self):
        response = self.client.get('/calculate/?all=1')
        self.assertEqual(response.status_code, 200)

    def test_all_content(self):
        response = self.client.get('/calculate/?all=1')
        user = User.objects.get(username="test")
        cal = Calculate.objects.filter(user=user).order_by("-id")

        calculation_array = self.queryset_to_json("number", cal)

        self.assertEqual(response.content.decode('ascii'), calculation_array)

    def test_fail_statuscode(self):
        user = User.objects.get(username="test")
        Add.objects.get(user=user).delete()
        Calculate.objects.filter(user=user).delete()
        response = self.client.get('/calculate/')
        self.assertEqual(response.status_code, 406)
        
    def test_fail_content(self):
        user = User.objects.get(username="test")
        Add.objects.get(user=user).delete()
        Calculate.objects.filter(user=user).delete()
        response = self.client.get('/calculate/')
        self.assertEqual(response.content.decode('ascii'), "Numbers not provided.")

    def test_fail_content_all(self):
        user = User.objects.get(username="test")
        Add.objects.get(user=user).delete()
        Calculate.objects.filter(user=user).delete()
        response = self.client.get('/calculate/?all=1')
        self.assertEqual(response.content.decode('ascii'), "Numbers not provided.")

    def test_fail_statuscode_all(self):
        user = User.objects.get(username="test")
        Add.objects.get(user=user).delete()
        Calculate.objects.filter(user=user).delete()
        response = self.client.get('/calculate/?all=1')
        self.assertEqual(response.status_code, 406)
        

class ResetTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('test', 'test@gmail.com', 'test123')
        self.client.login(username='test', password='test123')
        self.client.post('/add/', {'value': '3, 4, 1'})
        self.client.get('/calculate/')
        self.client.post('/add/', {'value': '10'})
        self.client.get('/calculate/')
        self.client.post('/add/', {'value': '-9'})

    def test_statuscode(self):
        response = self.client.post('/reset/')
        self.assertEqual(response.status_code, 201)

    def test_fail_statuscode(self):
        user = User.objects.get(username="test")
        Add.objects.get(user=user).delete()
        Calculate.objects.filter(user=user).delete()
        response = self.client.post('/reset/')
        self.assertEqual(response.status_code, 406)

    def test_content(self):
        response = self.client.post('/reset/')
        self.assertEqual(response.content.decode('ascii'), "")

    def test_fail_content_no_calc(self):
        user = User.objects.get(username="test")
        Calculate.objects.filter(user=user).delete()
        response = self.client.post('/reset/')
        self.assertEqual(response.content.decode('ascii'), "You dont have any calculations yet.")

    def test_fail_content(self):
        user = User.objects.get(username="test")
        Add.objects.get(user=user).delete()
        Calculate.objects.filter(user=user).delete()
        response = self.client.post('/reset/')
        self.assertEqual(response.content.decode('ascii'), "You dont have any calculations yet.")


class HistoryTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('test', 'test@gmail.com', 'test123')
        self.client.login(username='test', password='test123')
        
        #First calculation
        self.client.post('/add/', {'value': '3, 5'})
        self.client.get('/calculate/')
        self.client.post('/add/', {'value': '8'})
        self.client.get('/calculate/')
        self.client.post('/add/', {'value': '2'})
        self.client.get('/calculate/')
        
        self.client.post('/reset/')

        #Second calculation
        self.client.post('/add/', {'value': '2'})
        self.client.get('/calculate/')
        self.client.post('/add/', {'value': '4, -6'})
        self.client.get('/calculate/')
        self.client.post('/add/', {'value': '8'})
        self.client.get('/calculate/')

        self.client.post('/reset/')
        
    def test_content(self):
        response = self.client.get('/history/')
        json_response = '[{"id": 2, "array": [2, 4, -6, 8], "calculations": [2, 0, 8]}, {"id": 1, "array": [3, 5, 8, 2], "calculations": [8, 16, 18]}]'
        self.assertEqual(response.content.decode('ascii'), json_response)

    def test_statuscode(self):
        response = self.client.get('/history/')
        self.assertEqual(response.status_code, 200)

    def test_content_id(self):
        response = self.client.get('/history/?id=2')
        json_response = '[{"id": 2, "array": [2, 4, -6, 8], "calculations": [2, 0, 8]}]'
        self.assertEqual(response.content.decode('ascii'), json_response)

    def test_statuscode_id(self):
        response = self.client.get('/history/?id=2')
        json_response = '[{"id": 2, "array": [2, 4, -6, 8], "calculations": [2, 0, 8]}]'
        self.assertEqual(response.status_code, 200)

    def test_fail_content(self):
        user = User.objects.get(username="test")
        History.objects.filter(user=user).delete()
        response = self.client.get('/history/')
        self.assertEqual(response.content.decode('ascii'), "History is empty")

    def test_fail_statuscode(self):
        user = User.objects.get(username="test")
        History.objects.filter(user=user).delete()
        response = self.client.get('/history/')
        self.assertEqual(response.status_code, 404)

    def test_fail_content_id(self):
        response = self.client.get('/history/?id=3')
        self.assertEqual(response.content.decode('ascii'), "This element does not exist")

    def test_fail_statuscode_id(self):
        response = self.client.get('/history/?id=3')
        self.assertEqual(response.status_code, 404)

