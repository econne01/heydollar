from heydollar.tests.utils import HeydollarBaseTestCase

class AccountModelTest(HeydollarBaseTestCase):

    def test_can_caluclate_balance_based_on_cumulative_transactions(self):
        ''' Should be able to calculate an account's Current Balance by summing past transactions
        '''
        account = self.create_account()
        # Create some transactions for a single account
        self.create_transaction(account=account, post_date='2013-01-01', amount=100)
        self.create_transaction(account=account, post_date='2013-02-02', amount=-25.0)
        self.create_transaction(account=account, post_date='2013-03-03', amount=0.33)
        # Confirm the current balance is the sum of the transactions
        self.assertEqual(account.get_balance(), sum([100, -25.0, 0.33]))
        # Confirm the balance as of a given date is equal to partial sum of transactions
        self.assertEqual(account.get_balance(as_of='2013-02-28'), sum([100, -25.0]))

