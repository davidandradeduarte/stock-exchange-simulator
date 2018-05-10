#!/usr/bin/python


class Company:

    id = 0
    name = ""
    sector = ""
    quote = 0
    marketValue = 0
    stock = 0

    def __init__(self, id, name, sector, marketValue, quote, stock):
        self.id = id
        self.name = name
        self.sector = sector
        self.quote = quote
        self.marketValue = marketValue
        self.stock = stock
