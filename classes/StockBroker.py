#!/usr/bin/python


class StockBroker:

    id = 0
    name = ""
    capital = 0
    quotes = []
    transactions = []

    def __init__(self, id, name, capital, quotes, transactions):
        self.id = id
        self.name = name
        self.capital = capital
        self.quotes = quotes
        self.transactions = transactions
