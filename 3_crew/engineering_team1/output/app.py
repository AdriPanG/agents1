import gradio as gr
from accounts import Account

current_account = None

def create_account(username, initial_deposit):
    global current_account
    current_account = Account(username, initial_deposit)
    return f"Account created for {username} with initial deposit of {initial_deposit}"

def deposit_funds(account, amount):
    if current_account is None:
        return "Please create an account first."
    if current_account.deposit(amount):
        return f"{amount} deposited successfully. Current balance: {current_account.balance}"
    else:
        return "Invalid deposit amount."

def withdraw_funds(account, amount):
    if current_account is None:
        return "Please create an account first."
    if current_account.withdraw(amount):
        return f"{amount} withdrawn successfully. Current balance: {current_account.balance}"
    else:
        return "Insufficient funds or invalid amount."

def buy_shares(account, symbol, quantity):
    if current_account is None:
        return "Please create an account first."
    if current_account.buy_shares(symbol, quantity):
        return f"Bought {quantity} shares of {symbol}. Current balance: {current_account.balance}"
    else:
        return "Insufficient funds or invalid quantity."

def sell_shares(account, symbol, quantity):
    if current_account is None:
        return "Please create an account first."
    if current_account.sell_shares(symbol, quantity):
        return f"Sold {quantity} shares of {symbol}. Current balance: {current_account.balance}"
    else:
        return "Invalid quantity or insufficient shares."

def view_holdings(account):
    if current_account is None:
        return "Please create an account first."
    return current_account.get_holdings()

def view_transactions(account):
    if current_account is None:
        return "Please create an account first."
    return current_account.get_transaction_history()

def view_portfolio_value(account):
    if current_account is None:
        return "Please create an account first."
    return current_account.calculate_portfolio_value()

def view_profit_loss(account):
    if current_account is None:
        return "Please create an account first."
    return current_account.calculate_profit_loss()

account_management_interface = gr.Interface(
    create_account,
    [
        gr.Textbox(label="Username"),
        gr.Number(label="Initial Deposit")
    ],
    gr.Textbox(label="Account Status"),
    title="Creating Account"
)

deposit_interface = gr.Interface(
    deposit_funds,
    [
        gr.Textbox(label="Account"),
        gr.Number(label="Deposit Amount")
    ],
    gr.Textbox(label="Deposit Status"),
    title="Deposit Funds"
)

withdraw_interface = gr.Interface(
    withdraw_funds,
    [
        gr.Textbox(label="Account"),
        gr.Number(label="Withdraw Amount")
    ],
    gr.Textbox(label="Withdraw Status"),
    title="Withdraw Funds"
)

buy_shares_interface = gr.Interface(
    buy_shares,
    [
        gr.Textbox(label="Account"),
        gr.Textbox(label="Symbol"),
        gr.Number(label="Quantity")
    ],
    gr.Textbox(label="Buy Shares Status"),
    title="Buy Shares"
)

sell_shares_interface = gr.Interface(
    sell_shares,
    [
        gr.Textbox(label="Account"),
        gr.Textbox(label="Symbol"),
        gr.Number(label="Quantity")
    ],
    gr.Textbox(label="Sell Shares Status"),
    title="Sell Shares"
)

portfolio_value_interface = gr.Interface(
    view_portfolio_value,
    gr.Textbox(label="Account"),
    gr.Number(label="Portfolio Value"),
    title="Portfolio Value"
)

profit_loss_interface = gr.Interface(
    view_profit_loss,
    gr.Textbox(label="Account"),
    gr.Number(label="Profit/Loss"),
    title="Profit/Loss Calculation"
)

holdings_interface = gr.Interface(
    view_holdings,
    gr.Textbox(label="Account"),
    gr.Textbox(label="Holdings"),
    title="View Holdings"
)

transactions_interface = gr.Interface(
    view_transactions,
    gr.Textbox(label="Account"),
    gr.Textbox(label="Transaction History"),
    title="View Transaction History"
)

demo = gr.TabbedInterface(
    [
        account_management_interface,
        deposit_interface,
        withdraw_interface,
        buy_shares_interface,
        sell_shares_interface,
        portfolio_value_interface,
        profit_loss_interface,
        holdings_interface,
        transactions_interface
    ]
)

if __name__ == "__main__":
    demo.launch()