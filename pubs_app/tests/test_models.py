from django.test import TestCase
from pubs_app.models import PubsBars
import datetime


class PubsBarsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        PubsBars.objects.create(
                name = "Pub 1",
                map_url = "https://goo.gl/maps/qY984V1Zaio8p3me9",
                open_time = "1:00",
                close_time = "23:00",
                beer_rating = 5,
                outside_tables = True,
                foosball = None,
                overall_rating = 5,
            )

    def test_object_creation(self):
        pub = PubsBars.objects.first()
        self.assertEqual(pub.name, "Pub 1")
        self.assertEqual(pub.map_url, "https://goo.gl/maps/qY984V1Zaio8p3me9")
        self.assertEqual(pub.open_time, datetime.time(1, 0))
        self.assertEqual(pub.close_time, datetime.time(23, 0))
        self.assertEqual(pub.beer_rating, 5)
        self.assertEqual(pub.outside_tables, True)
        self.assertEqual(pub.foosball, None)
        self.assertEqual(pub.overall_rating, 5)
