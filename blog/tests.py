from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()
    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn = navbar.find('a', text='스마트 부산')
        self.assertEqual(logo_btn.attrs['href'], '/')

        logo_btn = navbar.find('a', text='Home')
        self.assertEqual(logo_btn.attrs['href'], '/')

        logo_btn = navbar.find('a', text='Blog')
        self.assertEqual(logo_btn.attrs['href'], '/blog/')

        logo_btn = navbar.find('a', text='About Me')
        self.assertEqual(logo_btn.attrs['href'], '/about_me/')
    def test_post_list(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual(soup.title.text, 'Blog')

        self.navbar_test(soup)

    def test_post_detail(self):
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world',
        )

        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
