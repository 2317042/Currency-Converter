from flask import Flask, jsonify, request, render_template

app = Flask(__name__, template_folder=".")

# Sample exchange rates (base USD)
exchange_rates = {
    "USD": 1.0,
    "EUR": 0.92,
    "INR": 83.0,
    "JPY": 150.0,
    "GBP": 0.80
}

@app.route("/")
def home():
    return render_template("ex6.html", currencies=list(exchange_rates.keys()))

@app.route("/api/convert", methods=["POST"])
def convert_currency():
    data = request.get_json() or {}
    amount = data.get("amount")
    from_currency = data.get("from")
    to_currency = data.get("to")
    if amount is None or from_currency is None or to_currency is None:
        return jsonify({"error": "Invalid input"}), 400

    try:
        amount = float(amount)
    except:
        return jsonify({"error": "Amount must be numeric"}), 400

    if from_currency not in exchange_rates or to_currency not in exchange_rates:
        return jsonify({"error": "Currency not supported"}), 400

    usd_amount = amount / exchange_rates[from_currency]
    converted = usd_amount * exchange_rates[to_currency]

    return jsonify({"result": round(converted, 2)})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
