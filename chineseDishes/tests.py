from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from chineseDishes.models import Province, Dish, Ingridient, Dish_Ingridient

# Create your tests here.

class DishesViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        prvc = baker.make("Province")
        dsh = baker.make("Dish", province = prvc)        

        r = self.client.get('/api/dishes/')
        data = r.json()
        print(data)

        assert len(data) == 1
        assert dsh.name == data[0]['name']
        assert dsh.id == data[0]['id']
        assert dsh.province.id == data[0]['province']['id']

    def test_create_dish(self):
        prvc = baker.make("Province")

        r = self.client.post('/api/dishes/',{
            "name":"Блюдо",
            "province": prvc.id,
            "category":"десерт",
            "description":"описание",
            "spice_level" : "0"
        })

        new_dish_id = r.json()['id']

        dishes = Dish.objects.all()
        assert len(dishes) == 1

        new_dish = Dish.objects.filter(id=new_dish_id).first()
        assert new_dish.name == "Блюдо"
        assert new_dish.province.id == prvc.id
        
class ProvincesViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        prvc = baker.make("Province")
        
        r = self.client.get('/api/provinces/')
        data = r.json()
        print(data)

        assert len(data) == 1
        assert prvc.name == data[0]['name']
        assert prvc.id == data[0]['id']

class IngridientsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        ingrdnt = baker.make("Ingridient")
        
        r = self.client.get('/api/ingridients/')
        data = r.json()
        print(data)

        assert len(data) == 1
        assert ingrdnt.name == data[0]['name']
        assert ingrdnt.id == data[0]['id']

class Dish_IngridientsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        ingrdnt = baker.make("Ingridient")
        dsh = baker.make("Dish")
        dsh_ingrdnt = baker.make("Dish_ingridient", dish = dsh, ingridient = ingrdnt)
        
        r = self.client.get('/api/dish_ingridients/')
        data = r.json()
        print(data)

        assert len(data) == 1
        assert dsh_ingrdnt.quantity == data[0]['quantity']
        assert dsh_ingrdnt.id == data[0]['id']
        assert dsh_ingrdnt.ingridient == ingrdnt
        assert dsh_ingrdnt.dish == dsh
