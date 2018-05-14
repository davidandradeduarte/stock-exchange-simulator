#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import os
from threading import Thread, active_count
from time import gmtime, strftime
from lib.serverfuncs import *
from classes.ServerCodes import ServerCodes
from classes.StockBrokerQuotes import StockBrokerQuotes
from classes.Transaction import Transaction
from config import *

os.system('clear')
stockBrokers = initStockBrokers()
companies = initCompanies()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.bind(server_address)
print 'server '


class Server(Thread):

    connection = None

    def __init__(self, connection):
        self.connection = connection
        Thread.__init__(self)

    def run(self):
        while True:
            data = self.connection.recv(SOCKET_DATA_SIZE)

            serverCode = data
            if len(data.split(';')) > 1:
                serverCode = data.split(';')[0]

            if serverCode == ServerCodes.DetermineStockBroker:
                id = randomStockBroker()
                stockBroker = stockBrokers[id]
                data = "%s;%s;%s" % (
                    stockBroker.id, stockBroker.name, stockBroker.capital)
                self.connection.sendall(data)
            elif serverCode == ServerCodes.ListMarket:
                data = listMarket(companies)
                self.connection.sendall(data)
            elif serverCode == ServerCodes.ListMarketWithGoBack:
                data = listMarket(companies, True)
                self.connection.sendall(data)
            elif serverCode == ServerCodes.Buy:
                fields = data.split(';')

                companyId = int(fields[1])
                quantity = int(fields[2])
                stockBrokerId = int(fields[3])
                company = companies[companyId]
                stockBroker = stockBrokers[stockBrokerId]

                if company.stock - quantity >= 0:
                    transaction = quantity * company.quote
                    if stockBroker.capital > transaction:
                        company.stock - quantity
                        stockBroker.capital -= transaction

                        companyExists = False
                        for sbq in stockBroker.quotes:
                            if(sbq.company.id == company.id):
                                companyExists = True
                                sbq.quantity += quantity

                        if not companyExists:
                            stockBroker.quotes.append(
                                StockBrokerQuotes(company, quantity))

                        stockBroker.transactions.append(
                            Transaction(company, stockBroker, "Buy", company.quote, quantity, strftime("%Y-%m-%d %H:%M:%S", gmtime())))
                        data = "Successful transaction. %s stock exchange(s) purchased from %s." % (
                            quantity, company.name)
                    else:
                        data = "Transaction canceled. There's not enough capital for the purchase."
                else:
                    data = "Transaction canceled. There are not enough stock to complete the purchase."
                self.connection.sendall(data)
            elif serverCode == ServerCodes.Sell:
                fields = data.split(';')

                companyId = int(fields[1])
                quantity = int(fields[2])
                stockBrokerId = int(fields[3])
                company = companies[companyId]
                stockBroker = stockBrokers[stockBrokerId]

                companyExists = False
                sbQuote = None
                sbqId = 0
                i = 0
                for sbq in stockBroker.quotes:
                    if(sbq.company.id == company.id):
                        companyExists = True
                        sbQuote = sbq
                        sbqId = i
                    i += 1

                if not companyExists:
                    # terminate
                    data = "Transaction canceled. You don't own any quotes from %s." % company.name
                else:
                    if sbQuote.quantity - quantity < 0:
                        data = "Transaction canceled. You can't sell %s quotes from %s.\nYou only own %s quote(s) from this company." % (
                            str(quantity), company.name, str(sbQuote.quantity))
                    else:
                        variation = (
                            (float(company.quote) - float(company.marketValue)) / float(company.marketValue)) * 100
                        if variation > 10 or variation < -10:
                            if variation > 10:
                                data = "Transaction canceled. Value of variation greater than 10%."
                            elif variation < -10:
                                data = "Transaction canceled. Value of variation less than 10%."
                        else:
                            finalQtt = stockBroker.quotes[sbqId].quantity - quantity
                            if finalQtt == 0:
                                stockBroker.quotes.pop(sbqId)
                            else:
                                stockBroker.quotes[sbqId].quantity = finalQtt
                            stockBroker.capital += company.quote * quantity
                            company.stock += quantity
                            stockBroker.transactions.append(
                                Transaction(company, stockBroker, "Sell", company.quote, quantity, strftime("%Y-%m-%d %H:%M:%S", gmtime())))
                            data = "Successful transaction. %s stock exchange(s) sold to %s." % (
                                quantity, company.name)
                self.connection.sendall(data)
            elif serverCode == ServerCodes.UpdateStockBroker:
                fields = data.split(';')
                stockBrokerId = int(fields[1])
                stockBroker = stockBrokers[stockBrokerId]
                data = "%s;%s;%s" % (
                    stockBroker.id, stockBroker.name, stockBroker.capital)
                self.connection.sendall(data)
            elif serverCode == ServerCodes.NumberOfCompanies:
                data = str(len(companies))
                self.connection.sendall(data)
            elif serverCode == ServerCodes.GetStockBrokerQuotes:
                fields = data.split(';')
                stockBrokerId = int(fields[1])
                stockBroker = stockBrokers[stockBrokerId]
                data = " "
                i = 0
                end = len(stockBroker.quotes)
                for sbQuote in stockBroker.quotes:
                    i += 1
                    if i == end:
                        data += "%s,%s" % (sbQuote.company.id,
                                           sbQuote.quantity)
                    else:
                        data += "%s,%s;" % (sbQuote.company.id,
                                            sbQuote.quantity)
                self.connection.sendall(data)
            elif serverCode == ServerCodes.GetStockBrokerTransactions:
                fields = data.split(';')
                stockBrokerId = int(fields[1])
                stockBroker = stockBrokers[stockBrokerId]
                data = " "
                i = 0
                end = len(stockBroker.transactions)
                for t in stockBroker.transactions:
                    i += 1
                    if i == end:
                        data += "%s,%s,%s,%s,%s" % (t.company.id,
                                                    t.action, t.value, t.quantity, t.date)
                    else:
                        data += "%s,%s,%s,%s,%s;" % (t.company.id,
                                                     t.action, t.value, t.quantity, t.date)
                self.connection.sendall(data)
            elif serverCode == ServerCodes.GetCompany:
                fields = data.split(';')
                companyId = int(fields[1])
                company = companies[companyId]
                data = "%s;%s;%s;%s;%s;%s" % (
                    company.id, company.name, company.sector, company.quote, company.marketValue, company.stock)
                self.connection.sendall(data)
            else:
                # no more data
                connection.close()
                break


while True:
    sock.listen(1)
    connection, client_address = sock.accept()
    if active_count() <= 10:
        thread = Server(connection)
        thread.start()
    else:
        data = "Error. Maximum number of stock brokers connected (10)"
        connection.sendall(data)
