from django.test import TestCase
from rest_framework.test import APIClient

from chineseDishes.models import Province, Dish, Ingridient, Dish_Ingridient

# Create your tests here.
class DishesViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        prvc = Province.objects.create(
            name = "Хэйлунцзян (黑龙江)",
            capital = "Харбин",
            population = "38 312 224",
            area = "454 000",
        )

        dsh = Dish.objects.create(
            name = "Тун-суи (糖水)",
            description = "Самый популярный десерт провинции Гуандун — суп! Тун-суи (糖水), или «сахарная вода», — исключительно кантонский десерт, в других местах за таковой не признаваемый. Его готовят в нескольких вариантах. Например — чёрный кунжутный суп, который варят из молотого чёрного кунжута с сахаром, добавляя иногда травы — для вкуса и аромата.",
            category="десерт",
            spice_level = "0",
            province = prvc,
        )

        r = self.client.get('/api/dishes/')
        data = r.json()
        print(data)

        assert len(data) == 1
        assert dsh.name == data[0]['name']
        assert dsh.id == data[0]['id']
        assert dsh.province.id == data[0]['province']['id']
        

