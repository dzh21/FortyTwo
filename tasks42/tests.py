from django.test import TestCase


class MainViewTest(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.response = self.client.get('/')

    def test_root_url_for_template_usage(self):
        self.assertEquals(self.response.status_code, 200)

        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'home.html')

    def test_root_url_context_for_one_person_object(self):
        persons_in_context = self.response.context['persons']

        # only one Person object in context
        self.assertEquals(len(persons_in_context), 1)

    def test_root_url_content_for_my_contacts(self):
        # Person object in content
        self.assertIn('Evhen', self.response.content)
        self.assertIn('dzh21@tut.by', self.response.content)
        self.assertIn('Chernigov region', self.response.content)