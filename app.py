from flask import Flask, request, jsonify

app = Flask(__name__)

balance = 0  # Global balance (not persistent, for simplicity)

@app.route('/deposit', methods=['POST'])
def deposit():
    global balance
    data = request.get_json()
    amount = data.get('amount')

    if amount is None or not isinstance(amount, (int, float)):
        return jsonify({"error": "Invalid amount provided."}), 400

    if amount > 1000:
        balance += amount
        return jsonify({"message": f"Deposited {amount}. New balance is {balance}."})
    else:
        return jsonify({"error": "Amount must be greater than 1000."}), 400

@app.route('/withdraw', methods=['POST'])
def withdraw():
    global balance
    data = request.get_json()
    amount = data.get('amount')

    if amount is None or not isinstance(amount, (int, float)):
        return jsonify({"error": "Invalid amount provided."}), 400

    if amount > 500:
        if balance >= amount:
            balance -= amount
            return jsonify({"message": f"Withdrew {amount}. New balance is {balance}."})
        else:
            return jsonify({"error": "Insufficient balance."}), 400
    else:
        return jsonify({"error": "Amount must be greater than 500."}), 400

@app.route('/balance', methods=['GET'])
def check_balance():
    global balance
    return jsonify({"balance": balance})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')