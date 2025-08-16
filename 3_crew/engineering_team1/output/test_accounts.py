import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):

    def test_get_share_price(self):
        self.assertEqual(get_share_price('AAPL'), 150.00)
        self.assertEqual(get_share_price('TSLA'), 750.00)
        self.assertEqual(get_share_price('GOOGL'), 2800.00)
        self.assertEqual(get_share_price('INVALID'), 0.0)

    def setUp(self):
        self.account = Account('test_user', 1000)

    def test_initialization(self):
        self.assertEqual(self.account.username, 'test_user')
        self.assertEqual(self.account.initial_deposit, 1000)
        self.assertEqual(self.account.balance, 1000)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(self.account.transactions, [('Deposit', 1000)])

    def test_deposit(self):
        self.assertTrue(self.account.deposit(500))
        self.assertEqual(self.account.balance, 1500)
        self.assertEqual(self.account.transactions[-1], ('Deposit', 500))

        self.assertFalse(self.account.deposit(-200))

    def test_withdraw(self):
        self.assertTrue(self.account.withdraw(300))
        self.assertEqual(self.account.balance, 700)
        self.assertEqual(self.account.transactions[-1], ('Withdraw', 300))

        self.assertFalse(self.account.withdraw(1500))
        self.assertFalse(self.account.withdraw(0))

    def test_buy_shares(self):
        self.assertTrue(self.account.buy_shares('AAPL', 2))
        self.assertEqual(self.account.balance, 700)
        self.assertEqual(self.account.holdings['AAPL'], 2)
        self.assertEqual(self.account.transactions[-1], ('Buy', 'AAPL', 2))

        self.assertFalse(self.account.buy_shares('AAPL', 0))
        self.assertFalse(self.account.buy_shares('AAPL', 10))

    def test_sell_shares(self):
        self.account.buy_shares('AAPL', 2)
        self.assertTrue(self.account.sell_shares('AAPL', 1))
        self.assertEqual(self.account.balance, 850)
        self.assertEqual(self.account.holdings['AAPL'], 1)
        self.assertEqual(self.account.transactions[-1], ('Sell', 'AAPL', 1))

        self.assertFalse(self.account.sell_shares('AAPL', 0))
        self.assertFalse(self.account.sell_shares('AAPL', 3))

    def test_calculate_portfolio_value(self):
        self.account.buy_shares('TSLA', 1)
        self.account.buy_shares('GOOGL', 1)
        self.assertEqual(self.account.calculate_portfolio_value(), 4550)

    def test_calculate_profit_loss(self):
        self.account.buy_shares('TSLA', 1)
        self.account.buy_shares('GOOGL', 1)
        self.assertEqual(self.account.calculate_profit_loss(), 3550)

    def test_get_holdings(self):
        self.account.buy_shares('TSLA', 1)
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {'TSLA': 1})
        self.assertNotEqual(id(holdings), id(self.account.holdings))

    def test_get_transaction_history(self):
        self.account.deposit(300)
        self.account.buy_shares('AAPL', 1)
        transactions = self.account.get_transaction_history()
        expected_transactions = [
            ('Deposit', 1000),
            ('Deposit', 300),
            ('Buy', 'AAPL', 1)
        ]
        self.assertEqual(transactions, expected_transactions)
        self.assertNotEqual(id(transactions), id(self.account.transactions))

if __name__ == '__main__':
    unittest.main()