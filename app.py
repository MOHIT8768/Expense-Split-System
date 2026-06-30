from flask import Flask, request, jsonify
from database import db
from models import User, Group, Expense
from expense_logic import split_equal, calculate_balances, simplify_debts
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
@app.route("/")
def home():
    return "Expense Split API is running"
@app.route("/create_user", methods=["POST"])
def create_user():
    data = request.json
    user = User(
        name=data["name"],
        email=data["email"]
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"})
@app.route("/create_group", methods=["POST"])
def create_group():
    data = request.json
    group = Group(name=data["name"])
    db.session.add(group)
    db.session.commit()
    return jsonify({"message": "Group created"})
@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = request.json
    expense = Expense(
        description=data["description"],
        amount=data["amount"],
        paid_by=data["paid_by"],
        group_id=data["group_id"]
    )
    db.session.add(expense)
    db.session.commit()
    return jsonify({"message": "Expense added"})
@app.route("/split_expense", methods=["POST"])
def split_expense():
    data = request.json
    amount = data["amount"]
    members = data["members"]
    result = split_equal(amount, members)
    return jsonify(result)
@app.route("/settle_balances", methods=["POST"])
def settle_balances():
    data = request.json
    members = data["members"]
    expenses = data["expenses"]
    balances = calculate_balances(expenses, members)
    settlements = simplify_debts(balances)
    return jsonify(settlements)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)