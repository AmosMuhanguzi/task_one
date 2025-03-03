from flask import Flask, request, jsonify

app = Flask(__name__)

class BankAccount:
    def __init__(self, account_number, account_holder, initial_balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposited ${amount}. New balance is ${self.balance}."
        else:
            return "Deposit amount must be positive."

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return f"Withdrew ${amount}. New balance is ${self.balance}."
        else:
            return "Insufficient funds or invalid amount."

    def get_balance(self):
        return self.balance

    def account_info(self):
        return {
            "account_number": self.account_number,
            "account_holder": self.account_holder,
            "balance": self.balance
        }

accounts = {}  # Store accounts in memory (not persistent)

@app.route('/create', methods=['POST'])
def create_account():
    data = request.get_json()
    account_number = data.get('account_number')
    account_holder = data.get('account_holder')
    initial_balance = data.get('initial_balance', 0)
    accounts[account_number] = BankAccount(account_number, account_holder, initial_balance)
    return jsonify({"message": "Account created successfully."})

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.get_json()
    account_number = data.get('account_number')
    amount = data.get('amount')
    if account_number in accounts:
        result = accounts[account_number].deposit(amount)
        return jsonify({"message": result})
    else:
        return jsonify({"message": "Account not found."})

@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()
    account_number = data.get('account_number')
    amount = data.get('amount')
    if account_number in accounts:
        result = accounts[account_number].withdraw(amount)
        return jsonify({"message": result})
    else:
        return jsonify({"message": "Account not found."})

@app.route('/balance/<account_number>', methods=['GET'])
def get_balance(account_number):
    if account_number in accounts:
        balance = accounts[account_number].get_balance()
        return jsonify({"balance": balance})
    else:
        return jsonify({"message": "Account not found."})

@app.route('/info/<account_number>', methods=['GET'])
def account_info(account_number):
    if account_number in accounts:
        info = accounts[account_number].account_info()
        return jsonify(info)
    else:
        return jsonify({"message": "Account not found."})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')