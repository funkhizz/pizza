from django.test import TestCase
from datetime import datetime
from pizza_online.apps.pizzas.models import Pizza


class TestPizza(TestCase):
    # Run this method before every single test
    def setUp(self):
        self.pizza_1 = Pizza.objects.create(
            title="Assorti pizza",
            slug="",
            image="",
            added=datetime.now(),
            status=True,
        )
        self.pizza_2 = Pizza.objects.create(
            title="Chicken pizza",
            slug="",
            image="",
            added=datetime.now(),
            status=True,
        )

    # Run this method after single test
    def tearDown(self):
        pass

    def test_pizza_title(self):
        self.assertEquals(self.pizza_1.title, "Assorti pizza")
        self.assertEquals(self.pizza_2.title, "Chicken pizza")

        self.pizza_1.title = "Four cheese pizza"
        self.pizza_2.title = "Mushrooms pizza"

        self.assertEquals(self.pizza_1.title, "Four cheese pizza")
        self.assertEquals(self.pizza_2.title, "Mushrooms pizza")

    def test_pizza_slug(self):
        self.assertEquals(self.pizza_1.slug, "assorti-pizza")
        self.assertEquals(self.pizza_2.slug, "chicken-pizza")
