from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from django.forms.models import model_to_dict

from tasks42.models import RequestObject, Person
from tasks42.forms import PersonForm


class MainViewTest(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.response = self.client.get('/')

    def test_url_for_exist_and_template_usage(self):
        self.assertEquals(self.response.status_code, 200)

        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'home.html')

    def test_context_for_one_person_object(self):
        persons_in_context = self.response.context['persons']

        # only one Person object in context
        self.assertEquals(len(persons_in_context), 1)

    def test_content_for_my_contacts(self):
        # Person object in content
        self.assertIn('Evhen', self.response.content)
        self.assertIn('dzh21@tut.by', self.response.content)
        self.assertIn('Chernigov region', self.response.content)

    def test_for_exist_requests_link(self):
        # test requests link
        self.assertIn('requests', self.response.content)
        response_for_requests = self.client.get('/requests/')
        self.assertEquals(response_for_requests.status_code, 200)

    def test_for_setting_in_context(self):
        settings_in_context = self.response.context['settings']

        self.assertEquals(settings_in_context, settings)

    def test_for_editcontacts_link(self):
        self.assertIn('Login', self.response.content)
        edit_page = self.client.get('/editcontacts/', follow=True)
        self.assertEquals(edit_page.status_code, 200)

    def test_photo_exist(self):
        self.assertIn('<img src=', self.response.content)


class RequestsViewTest(TestCase):

    def setUp(self):
        # generate requests
        for i in range(12):
            self.response = self.client.get('/requests/')

    def test_url_for_exist_and_template_use(self):
        self.assertEquals(self.response.status_code, 200)

        self.assertTemplateUsed(self.response, 'requests.html')

    def test_only_ten_first_requests_showing(self):
        requests_in_db = list(RequestObject.objects.order_by(
            'event_date_time'
        ))[:10]

        self.assertIn('Request #', self.response.content)
        self.assertIn(timezone.localtime(requests_in_db[0].event_date_time)
            .strftime('%Y-%m-%d %H:%M:%S'), self.response.content)
        self.assertIn(timezone.localtime(requests_in_db[9].event_date_time)
            .strftime('%Y-%m-%d %H:%M:%S'), self.response.content)


class EditContactsViewTest(TestCase):

    def setUp(self):
        logindata = {
            'username': 'admin',
            'password': 'admin'
        }
        self.response = self.client.post(
            '/accounts/login/',
            logindata,
            follow=True
        )
        self.assertEquals(self.response.context['user'].is_active, True)
        self.response = self.client.get('/editcontacts/')

    def test_exist_and_using_template(self):
        self.assertEquals(self.response.status_code, 200)

        self.assertTemplateUsed(self.response, 'editcontacts.html')

    def test_form_with_contacts_on_page(self):
        self.assertIn('form', self.response.content)
        self.assertIn('value="Save"', self.response.content)

        self.assertIn('value="Evhen"', self.response.content)
        self.assertIn('value="dzh21@tut.by"', self.response.content)
        self.assertIn('value="dzh@default.rs"', self.response.content)

    def test_form_for_saving_data(self):
        person = Person.objects.get(pk=1)
        person.email = 'newemail@gmail.com'

        form = PersonForm(model_to_dict(person), instance=person)
        self.assertEquals(form.is_valid(), True)

        response = self.client.post(
            '/editcontacts/',
            form.cleaned_data,
            follow=True
        )
        self.assertEquals(response.status_code, 200)

        self.assertIn('newemail@gmail.com', response.content)
