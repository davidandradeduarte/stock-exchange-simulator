#!/usr/bin/python
import socket
import os
from lib.clientfuncs import *
from config import *
from classes.ClientCodes import ClientCodes

os.system('clear')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.connect(server_address)

# determine stock broker
stockBroker = determineStockBroker(sock)
sayHello(stockBroker.name, stockBroker.capital)
nOfCompanies = numberOfCompanies(sock)

while True:
    while True:
        try:
            action = mainMenu()
            break
        except:
            print "Invalid option."
    action = str(action)
    if action == ClientCodes.ListMarket:
        os.system('clear')
        listMarket(sock)
    elif action == ClientCodes.Buy:
        os.system('clear')
        printStockBrokerInfo(stockBroker)
        listMarket(sock, True)
        goBack = False
        while True:
            try:
                companyId = input('Company ID: ') - 1
                if(companyId >= -1 and companyId < nOfCompanies):
                    if companyId == -1:
                        goBack = True
                    break
                else:
                    print "Invalid option."
            except:
                print "Invalid option."
        if goBack:
            os.system('clear')
        else:
            while True:
                try:
                    quantity = input('Quantity: ')
                    if(quantity > 0):
                        break
                    else:
                        print "Invalid option."
                except:
                    print "Invalid option."
            os.system('clear')
            printStockBrokerInfo(stockBroker)
            buy(sock, companyId, quantity, stockBroker.id)
            stockBroker = updateStockBroker(sock, stockBroker)
    elif action == ClientCodes.Sell:
        os.system('clear')
        printStockBrokerInfo(stockBroker)
        listMarket(sock, True)
        goBack = False
        while True:
            try:
                companyId = input('Company ID: ') - 1
                if(companyId >= -1 and companyId < nOfCompanies):
                    if companyId == -1:
                        goBack = True
                    break
                else:
                    print "Invalid option."
            except:
                print "Invalid option."
        if goBack:
            os.system('clear')
        else:
            while True:
                try:
                    quantity = input('Quantity: ')
                    if(quantity > 0):
                        break
                    else:
                        print "Invalid option."
                except:
                    print "Invalid option."
            os.system('clear')
            printStockBrokerInfo(stockBroker)
            sell(sock, companyId, quantity, stockBroker.id)
            stockBroker = updateStockBroker(sock, stockBroker)
    elif action == ClientCodes.ListQuotes:
        os.system('clear')
        printStockBrokerInfo(stockBroker)
        listQuotes(stockBroker)
    elif action == ClientCodes.ListTransactions:
        os.system('clear')
        printStockBrokerInfo(stockBroker)
        listTransactions(stockBroker)
    elif action == ClientCodes.StockBrokerInfo:
        os.system('clear')
        printStockBrokerDetails(stockBroker)
    elif action == ClientCodes.Exit:
        print '\nThank you for using our service. See you next time.'
        sock.close()
        exit(0)
    else:
        print "Invalid option."
    # break
sock.close()
