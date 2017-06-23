from django.contrib.auth.models import User
from django.test import Client, TestCase


class RedirectsTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        trying to get an url with no language indentifier will redirect to default language 'en'
        """
        c = Client()
        response = c.get('/polls/tests/', follow=True)
        self.assertEqual(response.redirect_chain[0],('/en/polls/tests/', 302),
                         "If no language code in url should redirect to 'en'")

    def testCanLogin(self):
        """
        trying to get an url with no language indentifier will redirect to default language 'en'
        """
        c = Client()
        User.objects.create_user('user123', 'email@test.org', 'passwd')
        c.login(username='user123', password='passwd')
        response = c.get('/admin/', follow=True)
        self.assertContains(response, "You are authenticated as user123")

    def testTesRenderCorrectTemplate(self):
        """
        trying to get an url with no language indentifier will redirect to default language 'en'
        """
        c = Client()
        response = c.get('/polls/tests/', follow=True)
        self.assertEqual('polls/tests.html', response.templates[0].name)


    def testTestContextLooksOk(self):
        """
        trying to get an url with no language indentifier will redirect to default language 'en'
        """
        c = Client()
        response = c.get('/polls/tests/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('tests', response.context['title'])
        self.assertEqual('second', response.context['second'])