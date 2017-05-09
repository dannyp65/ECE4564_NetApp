#!/usr/bin/env python3

"""
ECE4564: Network Application - Spring 2017
Instructor:     William O. Plymale
Assignment:     Assignment 1 - Twitter Inquirer
Date:           02/13/2017
File name:      client.py
Developer:      Team 16 - Anup Jasani, John Stradling, Kenta Yoshimura, Nhan Pham
Description:    This client application runs on Raspberry Pi 3 (Rpi)
                the client application will capture "question" tweet using Twitter API and build question payload.
                Then it sends the question payload to server Rpi via socket interface. The client app receives a answer
                payload from the server, parses it then tweet the answer on twitter
Last modify:    02/13/2017
"""

import socket
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time
import json
import os
import random
import pickle
import hashlib
from mainwindow import Ui_MainWindow
from preferences import Ui_Dialog as Dialog

states = (
         'Alabama','Alaska','Arizona','Arkansas','California','Colorado',
         'Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho',
         'Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana',
         'Maine','Maryland','Massachusetts','Michigan','Minnesota',
         'Mississippi', 'Missouri','Montana','Nebraska','Nevada',
         'New Hampshire','New Jersey','New Mexico','New York',
         'North Carolina','North Dakota','Ohio',
         'Oklahoma','Oregon','Pennsylvania','Rhode Island',
         'South  Carolina','South Dakota','Tennessee','Texas','Utah',
         'Vermont','Virginia','Washington','West Virginia',
         'Wisconsin','Wyoming'
)
activities = ('Hiking', 'Camping', 'Bike Trails')
miles = ('5', '10', '15', '20', '25', '30')
ports = [x for x in range(1024, 65535)]
rand_ports = sorted(random.sample(ports, 50))
activity, state, city, radius, host, port = '', '', '', '', '172.29.16.168', 5554
weather_stats = []
places = []


# this function generates a MD5 checksum value from string
def MD5_Encode(str):
    endata = str.encode('utf-8')
    m = hashlib.md5()
    m.update(endata)
    return m.hexdigest()


# this function receives a string and a checksum value
# it generates a new checksum value for the input string
# then checking it with the checksum to see if the transferred string is correct
def Check_Payload(str, checksum):
    compute_checksum = MD5_Encode(str)
    if checksum == compute_checksum:
        return True
    else:
        return False


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.stateComboBox.addItem('---')
        self.stateComboBox.addItems(states)
        self.activityComboBox.addItem('---')
        self.activityComboBox.addItems(activities)
        self.radiusComboBox.addItem('---')
        self.radiusComboBox.addItems(miles)

        self.actionExit.setStatusTip("Exit Application")
        self.actionClear.setStatusTip("Clear All Forms")
        self.actionInstructions.setStatusTip("Get Instructions on How to Use the Application")
        self.actionPreferences.setStatusTip("Change Server Settings")

        self.searchButton.clicked.connect(self.search_clicked)
        self.stateComboBox.currentTextChanged.connect(self.state_changed)
        self.activityComboBox.currentTextChanged.connect(self.activity_changed)
        self.cityLineEdit.editingFinished.connect(self.city_changed)
        self.radiusComboBox.currentTextChanged.connect(self.radius_changed)
        self.actionPreferences.triggered.connect(self.open_preferences)
        self.actionExit.triggered.connect(self.quit_app)

    def state_changed(self, s):
        global state
        state = s
        print("State:", state)

    def activity_changed(self, a):
        global activity
        activity = a
        print("Activity:", activity)

    def city_changed(self):
        global city
        city = self.cityLineEdit.text()
        print("City:", city)

    def radius_changed(self, r):
        global radius
        radius = r
        print("Radius:", radius)

    def set_browser(self):
        print_to_browser = []
        self.printLabel.clear()
        for x in places:
            grab = x.split(', ')
            if len(grab) == 7:
                name = grab[0][2:-1]
                st_addr = grab[1][1:]
                city_addr = grab[2][:-1]
                statezip_addr = grab[3]
                country = grab[4][:-1]
                rating = grab[5]
                pic_ref = grab[6][1:-2]
                addr = st_addr + ", " + city_addr + ", " + statezip_addr + ", " + country
                print_to_browser.append([name, addr, rating])
            elif len(grab) == 6:
                name = grab[0][2:-1]
                city_addr = grab[1][:-1]
                statezip_addr = grab[2]
                country = grab[3][:-1]
                rating = grab[4]
                pic_ref = grab[5][1:-2]
                addr = city_addr + ", " + statezip_addr + ", " + country
                print_to_browser.append([name, addr, rating])
            else:
                print("Found no results")
        c = 1
        for x in print_to_browser:
            self.printLabel.setText(self.printLabel.text() + "{0}. ".format(c))
            for y in x:
                self.printLabel.setText(self.printLabel.text() + y + " ")
            self.printLabel.setText(self.printLabel.text() + '''<br>''' + '''<a href='https://www.google.com/maps/dir/Current+Location/{0}'>Directions</a>'''.format(x[1]) + '''<br>''')
            c += 1

    def set_images(self):
        if "rain" in weather_stats[5] or "thunderstorm" in weather_stats[5]:
            self.rainLabel.setPixmap(QPixmap(os.getcwd() + '/weather_pics/rain.png'))
        else:
            self.rainLabel.setPixmap(QPixmap())

        self.tempStatLabel.setText("Min: {0}{3}F, Current: {1}{3}F, Max: {2}{3}F".format(weather_stats[1], weather_stats[0], weather_stats[2], chr(176)))
        if float(weather_stats[0]) > 70:
            self.tempLabel.setPixmap(QPixmap(os.getcwd() + '/weather_pics/hot.png'))
            #print("Hot temp")
        elif 70 >= float(weather_stats[0]) > 50:
            self.tempLabel.setPixmap(QPixmap(os.getcwd() + '/weather_pics/therm.png'))
            #print("Normal temp")
        else:
            self.tempLabel.setPixmap(QPixmap(os.getcwd() + '/weather_pics/cold.png'))
            #print("Cold temp")
        self.windStatLabel.setText("Wind Speed: {0} miles/hour".format(weather_stats[3]))
        if float(weather_stats[3]) > 7:
            self.windLabel.setPixmap(QPixmap(os.getcwd() + '/weather_pics/highwind.png'))
            #print("High wind")
        else:
            self.windLabel.setPixmap(QPixmap(os.getcwd() + '/weather_pics/lowwind.png'))
            #print("Low wind")
        self.cloudsStatLabel.setText("Cloudiness: {0}%".format(weather_stats[4]))
        if float(weather_stats[4]) > 66:
            self.cloudsLabel.setPixmap(QPixmap(os.getcwd() + '/weather_pics/cloudy.png'))
            #print("Cloudy")
        elif 66 >= float(weather_stats[4]) > 33:
            self.cloudsLabel.setPixmap(QPixmap(os.getcwd() + '/weather_pics/partlycloudy.png'))
            #print("Partly Cloudly")
        else:
            self.cloudsLabel.setPixmap(QPixmap(os.getcwd() + '/weather_pics/sunny.png'))
            #print("Sunny")

    def search_clicked(self):
        if activity == '' or state == '' or city == '' or radius == '' or host == '' or port == '':
            print("Something is not set in the menu or the server settings")
        else:
            print("Searching...")
            main()

    def open_preferences(self):
        self.dialog = QtWidgets.QDialog()
        self.dialog.ui = Dialog()
        self.dialog.ui.setupUi(self.dialog)
        self.dialog.ui.portComboBox.addItem('1024')
        self.dialog.ui.portComboBox.addItems(str(x) for x in rand_ports)

        self.dialog.ui.buttonBox.accepted.connect(self.settings_ok)
        self.dialog.ui.ipLineEdit.editingFinished.connect(self.host_changed)
        self.dialog.ui.portComboBox.currentTextChanged.connect(self.port_changed)

        self.dialog.exec_()
        self.dialog.show()

    def port_changed(self, p):
        global port
        port = int(p)
        print("Port:", port)

    def host_changed(self):
        global host
        host = self.dialog.ui.ipLineEdit.text()
        print("Host:", host)

    def settings_ok(self):
        self.statusbar.showMessage("Server Settings Changed")
        print("Ok")

    def quit_app(self):
        QtCore.QCoreApplication.instance().quit()

def main():
    size = 16384
    s = None
    try:
        print('Connecting to Server')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object that use IPv4 and TCP
        s.connect((host, port))
    except socket.error as message:
        if s:
            s.close()
        print("Unable to open socket: " + str(message))
        sys.exit(1)
    print('Connected to Server')

    data_str = ','.join((activity, city, state, radius))
    checksum = MD5_Encode(data_str)  # generate a MD5 cheksum value for the question
    tuple_data = (data_str, checksum)  # pack the question and checksum value into a tuple
    pickle_data = pickle.dumps(tuple_data)  # pickling the tuple
    print('Sending Parameters to Server')
    s.send(pickle_data)  # send pickled data to the server

    print('Sent and Waiting to Receive')
    recv_pickle = s.recv(size)  # receive data from the server
    recv_data = pickle.loads(recv_pickle)  # unpickling the data
    print('Payload Received\nChecking MD5 Checksum')

    # checking if the receive answer is authentic
    if Check_Payload(recv_data[0], recv_data[1]):
        global weather_stats, places
        print('Checksum Verified\n')
        places = recv_data[0].split('[?]')[0].split('[!]')
        weather_stats = recv_data[0].split('[?]')[1].split('[!]')
        #print("-----\nTemp(Min, Current, Max): {0}{5}F, {1}{5}F, {2}{5}F \nWind Speed: {3}mi/hr \nClouds: {4}%\nRain: {6}\n-----\n".format(weather_stats[1], weather_stats[0], weather_stats[2], weather_stats[3], weather_stats[4], chr(176), weather_stats[5]))
        mainwindow.set_images()
        mainwindow.set_browser()
    else:
        print('MD5 Verification Fail!')
    s.close()
    return True


if __name__ == '__main__':  # runs the application
    app = QApplication(sys.argv)  # need application object to start PyQt5, takes cmd line args
    mainwindow = MyMainWindow()
    mainwindow.show()
    sys.exit(app.exec_())  # mainloop of app - event handling starts
