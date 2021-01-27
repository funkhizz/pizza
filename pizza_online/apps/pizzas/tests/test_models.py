from django.test import TestCase
from datetime import datetime
from pizza_online.apps.pizzas.models import Pizza


class TestPizza(TestCase):
    def test_title(self):
        pizza_1 = Pizza(
            "Assorti pizza",
            "",
            4.99,
            "",
            datetime.now(),
            True,
        )
        pizza_2 = Pizza(
            "Chicken pizza",
            "",
            3.99,
            "",
            datetime.now(),
            True,
        )

        self.assertEqual(pizza_1.title, "Assorti pizza")
        self.assertEqual(pizza_2.title, "Chicken pizza")

        pizza_1.title = "Four cheese pizza"
        pizza_2.title = "Mushrooms pizza"

        self.assertEqual(pizza_1.title, "Four cheese pizza")
        self.assertEqual(pizza_2.title, "Mushrooms pizza")
