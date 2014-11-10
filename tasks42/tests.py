from django.test import TestCase
from tasks42.models import RequestObject
from django.utils import timezone


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

        # test requests link
        self.assertIn('requests', response.content)
        response = self.client.get('/requests/')
        self.assertEquals(response.status_code, 200)

    def test_root_url_for_setting_in_context(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

        settings_in_context = response.context['settings']

        self.assertEquals(settings_in_context.USE_TZ, True)
        self.assertEquals(settings_in_context.TIME_ZONE, 'Europe/Minsk')


class RequestsViewTest(TestCase):

    def test_requests_link(self):
        response = self.client.get('/requests/')
        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, 'requests.html')

        for i in xrange(20):
            response = self.client.get('/requests/')

        # context
        requests_in_context = response.context['requests']
        requests_list = list(requests_in_context)
        self.assertEquals(len(requests_list), 10)

        first_ten_requests_list = list(RequestObject.objects.order_by(
            'event_date_time'
        ))[:10]

        self.assertEquals(requests_list, first_ten_requests_list)

        # content
        self.assertIn('Request #', response.content)
        self.assertIn(timezone.localtime(
            first_ten_requests_list[0].event_date_time
        ).strftime('%Y-%m-%d %H:%M:%S'), response.content)
        self.assertIn(timezone.localtime(
            first_ten_requests_list[9].event_date_time
        ).strftime('%Y-%m-%d %H:%M:%S'), response.content)
