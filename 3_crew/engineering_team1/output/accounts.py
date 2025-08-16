
def get_share_price(symbol):
    share_prices = {
        'AAPL': 150.00,
        'TSLA': 750.00,
        'GOOGL': 2800.00
    }
    return share_prices.get(symbol, 0.0)

class Account:
    def __init__(self, username, initial_deposit):
        self.username = username
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = [('Deposit', initial_deposit)]

    def deposit(self, amount):
        if amount <= 0:
            return False
        self.balance += amount
        self.transactions.append(('Deposit', amount))
        return True

    def withdraw(self, amount):
        if self.can_withdraw(amount):
            self.balance -= amount
            self.transactions.append(('Withdraw', amount))
            return True
        return False

    def buy_shares(self, symbol, quantity):
        if quantity <= 0:
            return False
        price = get_share_price(symbol)
        total_cost = price * quantity
        if self.can_buy_shares(symbol, quantity):
            self.balance -= total_cost
            self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
            self.transactions.append(('Buy', symbol, quantity))
            return True
        return False

    def sell_shares(self, symbol, quantity):
        if quantity <= 0:
            return False
        price = get_share_price(symbol)
        if self.can_sell_shares(symbol, quantity):
            self.balance += price * quantity
            self.holdings[symbol] -= quantity
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            self.transactions.append(('Sell', symbol, quantity))
            return True
        return False

    def calculate_portfolio_value(self):
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def calculate_profit_loss(self):
        current_value = self.calculate_portfolio_value()
        return current_value - self.initial_deposit

    def get_holdings(self):
        return self.holdings.copy()

    def get_transaction_history(self):
        return self.transactions.copy()

    def can_withdraw(self, amount):
        return amount > 0 and self.balance >= amount

    def can_buy_shares(self, symbol, quantity):
        price = get_share_price(symbol)
        total_cost = price * quantity
        return total_cost <= self.balance

    def can_sell_shares(self, symbol, quantity):
        return self.holdings.get(symbol, 0) >= quantity