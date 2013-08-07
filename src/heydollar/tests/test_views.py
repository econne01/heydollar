from django.test import TestCase
from django.core.urlresolvers import reverse

class HeydollarBaseViewTest(TestCase):

    def setUp(self):
        super(HeydollarBaseViewTest, self).setUp()
        self.view = reverse('index')

    def test_can_access_index_page(self):
        ''' Should be able to access home-index page
        '''
        r = self.client.get(self.view)
        self.assertEqual(r.status_code, 200)
