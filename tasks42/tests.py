from django.test import TestCase


class MainViewTest(TestCase):
    fixtures = ['initial_data.json']

    def test_root_url_for_contacts(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'home.html')

        persons_in_context = response.context['persons']

        # only one Person object in context
        self.assertEquals(len(persons_in_context), 1)

        # Person object in content
        self.assertIn('Evhen', response.content)
        self.assertIn('dzh21@tut.by', response.content)
        self.assertIn('Chernigov region', response.content)