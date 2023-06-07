from django.test import TestCase
from django.urls import reverse
from pubs_app.models import PubsBars


class IndexPageViewTest(TestCase):
    def test_view_by_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_view_by_name(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "pubs_app/index.html")
        self.assertContains(response, "Do you want to visit new pubs without the risk of being disappointed?", 1, 200)


class PubsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_pubs = 13
        for pub_id in range(number_of_pubs):
            PubsBars.objects.create(
                name = f"Pub {pub_id}",
                map_url = "https://goo.gl/maps/qY984V1Zaio8p3me9",
                open_time = "1:00",
                close_time = "1:00",
                beer_rating = 5,
                outside_tables = True,
                foosball = True,
                overall_rating = 5,
            )

    def test_view_by_url(self):
        response = self.client.get("/list/")
        self.assertEqual(response.status_code, 200)

    def test_view_by_name(self):
        response = self.client.get(reverse("pubs_list"))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse("pubs_list"))
        self.assertTemplateUsed(response, "pubs_app/pubsbars_list.html")
        self.assertContains(response, "Pubs & Bars", 2, 200)

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('pubs_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['pubs_list']), 10)

    def test_lists_remaining_pubs_after_pagination(self):
        response = self.client.get(reverse('pubs_list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['pubs_list']), 3)
