"""
Created on 22.01.2019

@author: Richard Wutscher<rwutscher@student.tgm.ac.at>
@version: 0.1

@description: Client für die simple user database
"""
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidgetItem

from clientView import Ui_MainWindow as ClientView
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import *
import requests
import json


class ClientController(object):

    def __init__(self):
        self.dialog = QtWidgets.QMainWindow()
        self.view = ClientView()

        self.view.setupUi(self.dialog)

        with open('material.qcss', 'r') as myfile:
            data = myfile.read().replace('\n', '')
            #self.dialog.setStyleSheet(data)

        self.loadUsers()
        self.view.sendButton.clicked.connect(self.send)

    def loadUsers(self):

        res = requests.get('http://localhost:5000/students')
        res = json.loads(res.text)

        print(res)

        self.view.tableWidget.setColumnCount(3)
        self.view.tableWidget.setRowCount(len(res)+1)
        self.view.tableWidget.setItem(0, 0, QTableWidgetItem('Picture'))
        self.view.tableWidget.setItem(0, 1, QTableWidgetItem('Email'))
        self.view.tableWidget.setItem(0, 2, QTableWidgetItem('Username'))

        for index, element in enumerate(res):
            self.view.tableWidget.setItem(index+1, 0, QTableWidgetItem(element['picture']))
            self.view.tableWidget.setItem(index+1, 1, QTableWidgetItem(element['email']))
            self.view.tableWidget.setItem(index+1, 2, QTableWidgetItem(element['username']))

        pass
    def show(self):
        self.dialog.show()

    def send(self):
        print('hallo')
    def received(self, data):
        print("seas")
        #self.view.messages.addItem(data)
        """
        items = []
        for index in range(self.listWidget.count()):
            items.append(self.listWidget.item(index))
        """

    def close(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    controller = ClientController()
    controller.show()
    app.exec_()

    controller.close()