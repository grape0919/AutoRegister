# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

import datetime
import static.staticValues as staticValues

class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.resize(960, 550)
        MainWindow.setMinimumSize(QtCore.QSize(960, 550))
        MainWindow.setMaximumSize(QtCore.QSize(960, 550))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(960, 550))
        self.centralwidget.setMaximumSize(QtCore.QSize(960, 550))
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 11, 942, 510))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.inquiryLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.inquiryLabel.setFont(font)
        self.verticalLayout.addWidget(self.inquiryLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(20, -1, 500, -1)
        self.fromDateEdit = QtWidgets.QDateEdit(self.layoutWidget)
        self.horizontalLayout.addWidget(self.fromDateEdit)
        self.dashLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.dashLabel.setFont(font)
        self.horizontalLayout.addWidget(self.dashLabel)
        self.toDateEdit = QtWidgets.QDateEdit(self.layoutWidget)
        self.horizontalLayout.addWidget(self.toDateEdit)
        self.inquiryButton = QtWidgets.QPushButton(self.layoutWidget)
        self.inquiryButton.setMinimumSize(QtCore.QSize(100, 30))
        self.inquiryButton.setMaximumSize(QtCore.QSize(100, 30))
        self.horizontalLayout.addWidget(self.inquiryButton)
        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(2, 4)
        self.horizontalLayout.setStretch(3, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableView = QtWidgets.QTableWidget(self.layoutWidget)
        self.tableView.setMaximumSize(QtCore.QSize(940, 400))
        
        # self.tableView = QtWidgets.QTableView(self.layoutWidget)
        # self.tableView.setMinimumSize(QtCore.QSize(940, 400))
        # self.tableView.setMaximumSize(QtCore.QSize(940, 400))

        # self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)	# row 전체를 선택하도록

        # self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)	# 

        # self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)		# 셀 내용을 수정 불가하도록
        
        self.verticalLayout.addWidget(self.tableView)
        self.registButton = QtWidgets.QPushButton(self.layoutWidget)
        self.registButton.setEnabled(True)
        self.registButton.setMinimumSize(QtCore.QSize(100, 30))
        self.registButton.setMaximumSize(QtCore.QSize(100, 30))
        self.verticalLayout.addWidget(self.registButton)

        self.progressBar = QtWidgets.QProgressBar()
        
        
        #UI스타일
        self.inquiryButton.setStyleSheet(staticValues.buttonStyleSheet)
        self.inquiryButton.setFont(staticValues.buttonFont)
        self.registButton.setStyleSheet(staticValues.buttonStyleSheet)
        self.registButton.setFont(staticValues.buttonFont)

        #오늘 날짜 세팅
        nowDate = datetime.datetime.now()
        self.fromDateEdit.setDate(nowDate)
        self.toDateEdit.setDate(nowDate)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("이카운트 ERP 자동등록 프로그램")
        self.inquiryLabel.setText("조회 기간")
        self.dashLabel.setText("-")
        self.inquiryButton.setText("조회")
        self.registButton.setText("등록")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
