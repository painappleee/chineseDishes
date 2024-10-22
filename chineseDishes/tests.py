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
            "category": 'Десерт',
            "description":"описание",
            "spice_level" : 0
        })

        new_dish_id = r.json()['id']

        dishes = Dish.objects.all()
        assert len(dishes) == 1

        new_dish = Dish.objects.filter(id=new_dish_id).first()
        assert new_dish.name == "Блюдо"
        assert new_dish.province.id == prvc.id
        
    def test_delete_dish(self):
        dishes = baker.make("Dish", 10)
        r = self.client.get('/api/dishes/')
        data = r.json()
        assert len(data) == 10

        dish_id_to_delete = dishes[3].id
        self.client.delete(f'/api/dishes/{dish_id_to_delete}/')

        r = self.client.get('/api/dishes/')
        data = r.json()
        assert len(data) == 9

        assert dish_id_to_delete not in [i['id'] for i in data]

    def test_update_dish(self):
        dishes = baker.make("Dish",10)
        dish: Dish =dishes[2]

        r = self.client.get(f'/api/dishes/{dish.id}/')
        data = r.json()
        assert data['name'] == dish.name

        prvc = baker.make("Province")

        r = self.client.put(f'/api/dishes/{dish.id}/',{
            "name": "Блюдо",
            "description": "Описание",
            "category": "Горячее",
            "spice_level": 8,
            "province": prvc.id
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/dishes/{dish.id}/')
        data  = r.json()
        assert data['name'] == "Блюдо"

        dish.refresh_from_db()
        assert data['name'] == dish.name

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

    def test_create_province(self):

        r = self.client.post('/api/provinces/',{
            "name": "Провинция",
            "capital": "Столица",
            "population": 54736746,
            "area": 67327
        })

        new_province_id = r.json()['id']

        provinces = Province.objects.all()
        assert len(provinces) == 1

        new_province = Province.objects.filter(id=new_province_id).first()
        assert new_province.name == "Провинция"

    def test_delete_province(self):
        provinces = baker.make("Province", 10)
        r = self.client.get('/api/provinces/')
        data = r.json()
        assert len(data) == 10

        province_id_to_delete = provinces[3].id
        self.client.delete(f'/api/provinces/{province_id_to_delete}/')

        r = self.client.get('/api/provinces/')
        data = r.json()
        assert len(data) == 9

        assert province_id_to_delete not in [i['id'] for i in data]

    def test_update_province(self):
        provinces = baker.make("Province",10)
        province: Province = provinces[2]

        r = self.client.get(f'/api/provinces/{province.id}/')
        data = r.json()
        assert data['name'] == province.name

        r = self.client.put(f'/api/provinces/{province.id}/',{
            "name": "Провинция",
            "capital": "Столица",
            "population": 45763829,
            "area": 53678
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/provinces/{province.id}/')
        data  = r.json()
        assert data['name'] == "Провинция"

        province.refresh_from_db()
        assert data['name'] == province.name

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

    def test_create_ingridient(self):
        
        r = self.client.post('/api/ingridients/',{
            "name":"Ингридиент",
            "category": 'Крупы'
        })

        new_ingridient_id = r.json()['id']

        ingridients = Ingridient.objects.all()
        assert len(ingridients) == 1

        new_ingridient = Ingridient.objects.filter(id=new_ingridient_id).first()
        assert new_ingridient.name == "Ингридиент"

    def test_delete_ingridient(self):
        ingridients = baker.make("Ingridient", 10)
        r = self.client.get('/api/ingridients/')
        data = r.json()
        assert len(data) == 10

        ingridient_id_to_delete = ingridients[3].id
        self.client.delete(f'/api/ingridients/{ingridient_id_to_delete}/')

        r = self.client.get('/api/ingridients/')
        data = r.json()
        assert len(data) == 9

        assert ingridient_id_to_delete not in [i['id'] for i in data]

    def test_update_ingridient(self):
        ingridients = baker.make("Ingridient",10)
        ingridient: Ingridient = ingridients[2]

        r = self.client.get(f'/api/ingridients/{ingridient.id}/')
        data = r.json()
        assert data['name'] == ingridient.name

        r = self.client.put(f'/api/ingridients/{ingridient.id}/',{
            "name": "Ингридиент",
            "category": "Крупы"
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/ingridients/{ingridient.id}/')
        data  = r.json()
        assert data['name'] == "Ингридиент"

        ingridient.refresh_from_db()
        assert data['name'] == ingridient.name

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

    def test_create_dish_ingridient(self):

        dsh = baker.make("Dish")
        ingrdnt = baker.make("Ingridient")    

        r = self.client.post('/api/dish_ingridients/',{
            "quantity": 300,
            "typeQuantity": 'гр',
            "dish": dsh.id,
            "ingridient": ingrdnt.id
        })

        new_dish_ingridient_id = r.json()['id']

        dish_ingridients = Dish_Ingridient.objects.all()
        assert len(dish_ingridients) == 1

        new_dish_ingridient = Dish_Ingridient.objects.filter(id=new_dish_ingridient_id).first()
        assert new_dish_ingridient.quantity == 300
        assert new_dish_ingridient.ingridient.id == ingrdnt.id
        assert new_dish_ingridient.dish.id == dsh.id

    def test_delete_dish_ingridient(self):
        dish_ingridients = baker.make("Dish_ingridient", 10)
        r = self.client.get('/api/dish_ingridients/')
        data = r.json()
        assert len(data) == 10

        dish_ingridient_id_to_delete = dish_ingridients[3].id
        self.client.delete(f'/api/dish_ingridients/{dish_ingridient_id_to_delete}/')

        r = self.client.get('/api/dish_ingridients/')
        data = r.json()
        assert len(data) == 9

        assert dish_ingridient_id_to_delete not in [i['id'] for i in data]
    
    def test_update_dish_ingridient(self):
        dish_ingridients = baker.make("Dish_ingridient",10)
        dish_ingridient: Dish_Ingridient = dish_ingridients[2]

        r = self.client.get(f'/api/dish_ingridients/{dish_ingridient.id}/')
        data = r.json()
        assert data['quantity'] == dish_ingridient.quantity

        dsh = baker.make("Dish")
        ingrdnt = baker.make("Ingridient")

        r = self.client.put(f'/api/dish_ingridients/{dish_ingridient.id}/',{
            "quantity": 300,
            "typeQuantity": 'гр',
            "dish": dsh.id,
            "ingridient": ingrdnt.id
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/dish_ingridients/{dish_ingridient.id}/')
        data  = r.json()
        assert data['quantity'] == 300

        dish_ingridient.refresh_from_db()
        assert data['quantity'] == dish_ingridient.quantity
    

        
