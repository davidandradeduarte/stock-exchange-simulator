#!/usr/bin/python
# -*- coding: utf-8 -*-
from classes.ServerCodes import ServerCodes
from classes.StockBroker import StockBroker
from classes.StockBrokerQuotes import StockBrokerQuotes
from classes.Transaction import Transaction
from classes.Company import Company
from config import *


def sayHello(name, capital):
    print '\n--STOCK EXCHANGE SIMULATOR--'
    print '\nWelcome, %s.\n\nYou have a capital of %s€ to spend on stocks.' % (
        name, capital)


def mainMenu():
    separator = '--------------------------------------------------------'
    return input('\n' + separator + '\n1 - List Market\n2 - Buy\n3 - Sell\n4 - My Quotes\n5 - My Transactions\n6 - My Details\n0 - Exit\n' + separator + '\nSelect an option: ')


def determineStockBroker(sock):
    try:
        sock.sendall(ServerCodes.DetermineStockBroker)
        data = sock.recv(SOCKET_DATA_SIZE)
        fields = data.split(';')

        return StockBroker(fields[0], fields[1], fields[2], [], [])
    except:
        print 'An error occurred on the server.'
        exit(1)


def updateStockBroker(sock, stockBroker):
    # try:
    request = '%s;%s' % (ServerCodes.UpdateStockBroker, stockBroker.id)
    sock.sendall(request)
    data = sock.recv(SOCKET_DATA_SIZE)
    fields = data.split(';')

    stockBroker.id = fields[0]
    stockBroker.name = fields[1]
    stockBroker.capital = fields[2]

    request = '%s;%s' % (ServerCodes.GetStockBrokerQuotes, stockBroker.id)
    sock.sendall(request)
    data = sock.recv(SOCKET_DATA_SIZE)
    fields = data.split(';')
    stockBroker.quotes = []
    for sb in fields:
        sbQuote = sb.split(',')
        companyId = sbQuote[0]
        quantity = int(sbQuote[1])

        request = '%s;%s' % (ServerCodes.GetCompany, companyId)
        sock.sendall(request)
        data = sock.recv(SOCKET_DATA_SIZE)
        companyFields = data.split(';')
        stockBroker.quotes.append(
            StockBrokerQuotes(Company(int(companyFields[0]), companyFields[1], companyFields[2], int(
                companyFields[3]), int(companyFields[4]), int(companyFields[5])), quantity))

    request = '%s;%s' % (
        ServerCodes.GetStockBrokerTransactions, stockBroker.id)
    sock.sendall(request)
    data = sock.recv(SOCKET_DATA_SIZE)
    fields = data.split(';')
    stockBroker.transactions = []
    for t in fields:
        transactionFields = t.split(',')
        companyId = transactionFields[0]
        action = transactionFields[1]
        value = int(transactionFields[2])
        quantity = int(transactionFields[3])
        date = transactionFields[4]
        request = '%s;%s' % (ServerCodes.GetCompany, companyId)
        sock.sendall(request)
        data = sock.recv(SOCKET_DATA_SIZE)
        companyFields = data.split(';')
        stockBroker.transactions.append(Transaction(Company(int(companyFields[0]), companyFields[1], companyFields[2], int(
            companyFields[3]), int(companyFields[4]), int(companyFields[5])), stockBroker, action, value, quantity, date))

    return stockBroker
    # except:
    #    print 'An error occurred on the server.'
    #    exit(1)


def buy(sock, companyId, quantity, stockBrokerId):
    try:
        request = '%s;%s;%s;%s' % (
            ServerCodes.Buy, companyId, quantity, stockBrokerId)
        sock.sendall(request)
        data = sock.recv(SOCKET_DATA_SIZE)
        print "\n%s\n" % data
    except:
        print 'An error occurred on the server.'
        exit(1)


def sell(sock, companyId, quantity, stockBrokerId):
    try:
        request = '%s;%s;%s;%s' % (
            ServerCodes.Sell, companyId, quantity, stockBrokerId)
        sock.sendall(request)
        data = sock.recv(SOCKET_DATA_SIZE)
        print "\n%s\n" % data
    except:
        print 'An error occurred on the server.'
        exit(1)


def listMarket(sock, showGoBack=False):
    try:
        if(showGoBack):
            sock.sendall(ServerCodes.ListMarketWithGoBack)
        else:
            sock.sendall(ServerCodes.ListMarket)
        data = sock.recv(SOCKET_DATA_SIZE)
        print data
        return
    except:
        print 'An error occurred on the server.'
        exit(1)


def listQuotes(stockBroker):
    print "Your Quotes:\n"
    for q in stockBroker.quotes:
        print "Company: %s; Quantity: %s" % (q.company.name, q.quantity)


def listTransactions(stockBroker):
    print "Your Transactions:\n"
    for t in stockBroker.transactions:
        print "Company: %s; Quantity: %s; Date: %s" % (
            t.company.name, t.quantity, t.date)


def printStockBrokerInfo(stockBroker):
    separator = '--------------------------------------------------------'
    print '%s, Capital: %s€\n%s\n' % (
        stockBroker.name, stockBroker.capital, separator)


def printStockBrokerDetails(stockBroker):
    print "Your Details:\n"
    print 'Name: %s\nCapital: %s€' % (
        stockBroker.name, stockBroker.capital)


def numberOfCompanies(sock):
    try:
        sock.sendall(ServerCodes.NumberOfCompanies)
        data = sock.recv(SOCKET_DATA_SIZE)
        return int(data)
    except:
        print 'An error occurred on the server.'
        exit(1)
