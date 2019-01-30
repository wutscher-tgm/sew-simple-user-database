"""
Created on 22.01.2019

@author: Richard Wutscher<rwutscher@student.tgm.ac.at>
@version: 0.1

@description: Client für die simple user database
"""
import ast
import base64
import urllib

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem

from clientView import Ui_MainWindow as ClientView
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import json


class ClientController(object):

    def __init__(self):
        self.dialog = QtWidgets.QMainWindow()
        self.view = ClientView()

        self.view.setupUi(self.dialog)

        self.loadUsers()
        self.view.sendButton.clicked.connect(self.send)

    def loadUsers(self):

        res = requests.get('http://localhost:5000/students')
        res = json.loads(res.text)

        #print(res)

        self.view.tableWidget.setColumnCount(3)
        self.view.tableWidget.setRowCount(len(res)+1)
        self.view.tableWidget.setItem(0, 0, QTableWidgetItem('Picture'))
        self.view.tableWidget.setItem(0, 1, QTableWidgetItem('Email'))
        self.view.tableWidget.setItem(0, 2, QTableWidgetItem('Username'))


        for index, element in enumerate(res):
            if element['picture'] != None and False:
                image = element['picture']
                image = base64.b64encode(base64.b64decode(image))
                bytearr = QtCore.QByteArray.fromBase64(image)
                pixmap = QPixmap()
                pixmap.loadFromData(bytearr)
                #pixmap.scaled(10, 10, QtCore.Qt.KeepAspectRatio)
                item = QTableWidgetItem()
                item.setData(1,pixmap)
                self.view.tableWidget.setItem(index+1, 0, item)

            self.view.tableWidget.setItem(index+1, 1, QTableWidgetItem(element['email']))
            self.view.tableWidget.setItem(index+1, 2, QTableWidgetItem(element['username']))

        pass
    def show(self):
        self.dialog.show()

    def send(self):
        username = self.view.usernameCreate
        email = self.view.emailCreate
        picture = self.view.linkCreate

        res = requests.post('http://localhost/students?username='+username+'&email='+email+'pictureLink='+picture)
        print('hallo')

    def close(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    controller = ClientController()
    controller.show()
    app.exec_()

    controller.close()