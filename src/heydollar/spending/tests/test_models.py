from heydollar.tests.utils import HeydollarBaseTestCase

class CategoryModelTest(HeydollarBaseTestCase):

    def test_can_assign_parent_to_a_category(self):
        ''' Should allow Categories to be grouped under parent Category
        '''
        # Create 2 Categories
        parent_ctgy = self.create_category()
        child_ctgy = self.create_category()
        # Assign one Category as a parent to the other
        child_ctgy.parent = parent_ctgy
        child_ctgy.save()
        # Confirm the hierarchy was saved
        self.assertEqual(child_ctgy.parent, parent_ctgy)


class TransactionModelTest(HeydollarBaseTestCase):

    def test_simple(self):
        ''' Should be able 
        '''
        self.assertTrue(True)
