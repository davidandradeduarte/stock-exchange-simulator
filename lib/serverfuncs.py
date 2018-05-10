#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint
from classes.StockBroker import StockBroker
from classes.Company import Company


def initStockBrokers():
    names = stockBrokerNames()
    stockBrokers = []

    for i in range(len(names)):
        name = names[i]
        capital = randint(0, 1000)

        sb = StockBroker(i, name, capital, [], [])
        stockBrokers.append(sb)

    return stockBrokers


def initCompanies():
    names = companyNames()
    sectors = companySectors()

    companies = []
    for i in range(len(names)):
        name = names[i]
        sector = sectors[i]
        quote = randint(10, 30)
        marketValue = randint(quote-5, quote+5)
        stock = randint(0, 1000)

        c = Company(i, name, sector, marketValue, quote, stock)
        companies.append(c)

    return companies


def randomStockBroker():
    return randint(0, 9)


def listMarket(companies, showGoBack=False):
    data = "List of companies:\n\n"
    separator = '--------------------------------------------------------\n'
    i = 1
    for c in companies:
        data += '(%s) %s (%s)\nQuote value: %s€; Market value: %s€; Stock: %s;\n%s' % (i,
                                                                                       c.name, c.sector, c.quote, c.marketValue, c.stock, separator)
        i += 1
    if(showGoBack):
        data += "(0) Go back\n%s" % separator
    return data


def stockBrokerNames():
    return ['Banco de Portugal', 'Novo Banco', 'Banco BPI', 'Banco Santander Totta', 'Caixa Geral de Depósitos', 'Banco CTT', 'Deutsche Bank', 'Banco Português de Negócios', 'Banco Popular Portugal', 'Banco Invest']


def companyNames():
    return ['Novabase', 'Sonae Capital', 'Ibersol', 'Pharol', 'Altri', 'Mota-Engil', 'Corticeira Amorim', 'Semapa', 'CTT Correios de Portugal', 'Redes Energéticas Nacionais',
            'Sonae', 'The Navigator Company', 'NOS', 'EDP Renováveis', 'Energias de Portugal', 'Jerónimo Martins', 'Galp Energia', 'Banco Comercial Português']


def companySectors():
    return ['Technology', 'Financial Services', 'Travel & Leisure', 'Telecommunications', 'Industrial Goods & Services', 'Construction & Materials', 'Food & Beverage',
            'Basic Resources', 'Industrial Goods & Services', 'Utilities', 'Retail', 'Basic Resources', 'Media', 'Utilities', 'Utilities', 'Retail', 'Oil & Gas', 'Banks']
