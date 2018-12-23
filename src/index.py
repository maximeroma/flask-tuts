from flask import Flask, jsonify, request

from src.model.expense import Expense, ExpenseSchema
from src.model.income import Income, IncomeSchema
from src.model.transaction_type import TransactionType

app = Flask(__name__)

transactions = [
    Income('Salary', 5000),
    Income('Dividends', 250),
    Expense('Pizza', 50),
    Expense('Rock Concert', 100)
]

incomes = [{'description': 'salary', 'amount': 5000}]


@app.route('/incomes')
def get_incomes():
    schema = IncomeSchema(many=True)
    incomes = schema.dump(
        [
            transaction
            for transaction in transactions
            if transaction.type == TransactionType.INCOME
        ]
    )
    return jsonify(incomes.data)


@app.route('/incomes', methods=['POST'])
def add_income():
    income = IncomeSchema().load(request.get_json())
    transactions.append(income.data)
    return '', 204


@app.route('/expenses')
def get_expenses():
    schema = ExpenseSchema(many=True)
    expenses = schema.dump(
        [
            transaction
            for transaction in transactions
            if transaction.type == TransactionType.EXPENSE
        ]
    )
    return jsonify(expenses.data)


@app.route('/expenses', methods=['POST'])
def add_expense():
    expense = ExpenseSchema().load(request.get_json())
    transactions.append(expense.data)
    return "", 204


if __name__ == "__main__":
    app.run()
