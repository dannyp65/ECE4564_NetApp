# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\PreferencesDialog.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 181)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 140, 351, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(20, 10, 351, 121))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.formLayoutWidget = QtWidgets.QWidget(self.tab)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 20, 301, 61))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.ipLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.ipLabel.setObjectName("ipLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.ipLabel)
        self.portLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.portLabel.setObjectName("portLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.portLabel)
        self.portComboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.portComboBox.setMaxVisibleItems(30)
        self.portComboBox.setObjectName("portComboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.portComboBox)
        self.ipLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.ipLineEdit.setObjectName("ipLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ipLineEdit)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Preferences"))
        self.ipLabel.setText(_translate("Dialog", "IP: "))
        self.portLabel.setText(_translate("Dialog", "Port"))
        self.ipLineEdit.setInputMask(_translate("Dialog", "000.000.000.000;_"))
        self.ipLineEdit.setText(_translate("Dialog", "..."))
        self.ipLineEdit.setPlaceholderText(_translate("Dialog", "Default to localhost, if left blank"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Server"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Other"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

