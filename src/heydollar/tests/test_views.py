from django.test import TestCase
from django.core.urlresolvers import reverse

class HeydollarIndexViewTest(TestCase):

    def setUp(self):
        super(HeydollarIndexViewTest, self).setUp()
        self.view = reverse('index')

    def test_can_access_index_page(self):
        ''' Should be able to access home-index page
        '''
        r = self.client.get(self.view)
        self.assertEqual(r.status_code, 200)

    def test_index_page_includes_balance_sheet_summary_table(self):
        ''' Index page content should include balance sheet summary table
        '''
        r = self.client.get(self.view)
        print vars(r)
        self.assertEqual(1,2)