#!/usr/bin/python


class Transaction:

    company = None
    stockBroker = None
    action = ""
    value = 0
    quantity = 0
    date = ""

    def __init__(self, company, stockBroker, action, value, quantity, date):
        self.company = company
        self.stockBroker = stockBroker
        self.action = action
        self.value = value
        self.quantity = quantity
        self.date = date
