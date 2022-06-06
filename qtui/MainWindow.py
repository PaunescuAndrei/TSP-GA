# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from pyqtgraph import PlotWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1300, 900)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.leftside = QVBoxLayout(self.verticalLayoutWidget)
        self.leftside.setObjectName(u"leftside")
        self.leftside.setContentsMargins(0, 0, 0, 0)
        self.graphPlot = PlotWidget(self.verticalLayoutWidget)
        self.graphPlot.setObjectName(u"graphPlot")

        self.leftside.addWidget(self.graphPlot)

        self.logList = QListWidget(self.verticalLayoutWidget)
        self.logList.setObjectName(u"logList")

        self.leftside.addWidget(self.logList)

        self.leftside.setStretch(0, 5)
        self.leftside.setStretch(1, 2)
        self.splitter.addWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget_2 = QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.rightside = QVBoxLayout(self.verticalLayoutWidget_2)
        self.rightside.setObjectName(u"rightside")
        self.rightside.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.verticalLayoutWidget_2)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.submenu1 = QWidget(self.widget)
        self.submenu1.setObjectName(u"submenu1")
        self.horizontalLayout_6 = QHBoxLayout(self.submenu1)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.startButton = QPushButton(self.submenu1)
        self.startButton.setObjectName(u"startButton")

        self.horizontalLayout_6.addWidget(self.startButton)

        self.stopButton = QPushButton(self.submenu1)
        self.stopButton.setObjectName(u"stopButton")

        self.horizontalLayout_6.addWidget(self.stopButton)


        self.verticalLayout.addWidget(self.submenu1)

        self.submenu2 = QWidget(self.widget)
        self.submenu2.setObjectName(u"submenu2")
        self.horizontalLayout_4 = QHBoxLayout(self.submenu2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.switchButton = QPushButton(self.submenu2)
        self.switchButton.setObjectName(u"switchButton")

        self.horizontalLayout_4.addWidget(self.switchButton)

        self.exportButton = QPushButton(self.submenu2)
        self.exportButton.setObjectName(u"exportButton")

        self.horizontalLayout_4.addWidget(self.exportButton)


        self.verticalLayout.addWidget(self.submenu2)


        self.rightside.addWidget(self.widget)

        self.infoWidget = QWidget(self.verticalLayoutWidget_2)
        self.infoWidget.setObjectName(u"infoWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoWidget.sizePolicy().hasHeightForWidth())
        self.infoWidget.setSizePolicy(sizePolicy)
        self.verticalLayout_4 = QVBoxLayout(self.infoWidget)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.currentInstanceWidget = QWidget(self.infoWidget)
        self.currentInstanceWidget.setObjectName(u"currentInstanceWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.currentInstanceWidget)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.currentinstancelabel = QLabel(self.currentInstanceWidget)
        self.currentinstancelabel.setObjectName(u"currentinstancelabel")

        self.horizontalLayout_3.addWidget(self.currentinstancelabel)

        self.currentInstanceValue = QLabel(self.currentInstanceWidget)
        self.currentInstanceValue.setObjectName(u"currentInstanceValue")

        self.horizontalLayout_3.addWidget(self.currentInstanceValue)


        self.verticalLayout_4.addWidget(self.currentInstanceWidget)

        self.currentBestWidget = QWidget(self.infoWidget)
        self.currentBestWidget.setObjectName(u"currentBestWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.currentBestWidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.currentbestlabel = QLabel(self.currentBestWidget)
        self.currentbestlabel.setObjectName(u"currentbestlabel")

        self.horizontalLayout_2.addWidget(self.currentbestlabel)

        self.current_best_value = QLabel(self.currentBestWidget)
        self.current_best_value.setObjectName(u"current_best_value")

        self.horizontalLayout_2.addWidget(self.current_best_value)


        self.verticalLayout_4.addWidget(self.currentBestWidget)

        self.optimalBestWidget = QWidget(self.infoWidget)
        self.optimalBestWidget.setObjectName(u"optimalBestWidget")
        self.horizontalLayout = QHBoxLayout(self.optimalBestWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.optimalbestlabel = QLabel(self.optimalBestWidget)
        self.optimalbestlabel.setObjectName(u"optimalbestlabel")

        self.horizontalLayout.addWidget(self.optimalbestlabel)

        self.optimal_best_value = QLabel(self.optimalBestWidget)
        self.optimal_best_value.setObjectName(u"optimal_best_value")

        self.horizontalLayout.addWidget(self.optimal_best_value)


        self.verticalLayout_4.addWidget(self.optimalBestWidget)

        self.timeElapsedWidget = QWidget(self.infoWidget)
        self.timeElapsedWidget.setObjectName(u"timeElapsedWidget")
        self.horizontalLayout_5 = QHBoxLayout(self.timeElapsedWidget)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.timeElapsedLabel = QLabel(self.timeElapsedWidget)
        self.timeElapsedLabel.setObjectName(u"timeElapsedLabel")

        self.horizontalLayout_5.addWidget(self.timeElapsedLabel)

        self.timeElapsedValue = QLabel(self.timeElapsedWidget)
        self.timeElapsedValue.setObjectName(u"timeElapsedValue")

        self.horizontalLayout_5.addWidget(self.timeElapsedValue)


        self.verticalLayout_4.addWidget(self.timeElapsedWidget)


        self.rightside.addWidget(self.infoWidget)

        self.connectionsWidget = QWidget(self.verticalLayoutWidget_2)
        self.connectionsWidget.setObjectName(u"connectionsWidget")
        self.verticalLayout_5 = QVBoxLayout(self.connectionsWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, -1, -1, 0)
        self.connections = QLabel(self.connectionsWidget)
        self.connections.setObjectName(u"connections")
        font = QFont()
        font.setPointSize(10)
        self.connections.setFont(font)
        self.connections.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.connections)

        self.contributorsTree = QTreeWidget(self.connectionsWidget)
        self.contributorsTree.setObjectName(u"contributorsTree")
        self.contributorsTree.setRootIsDecorated(False)
        self.contributorsTree.setSortingEnabled(True)

        self.verticalLayout_5.addWidget(self.contributorsTree)


        self.rightside.addWidget(self.connectionsWidget)

        self.rightside.setStretch(2, 1)
        self.splitter.addWidget(self.verticalLayoutWidget_2)

        self.verticalLayout_3.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1300, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.switchButton.setText(QCoreApplication.translate("MainWindow", u"Switch Instance", None))
        self.exportButton.setText(QCoreApplication.translate("MainWindow", u"Export Solution", None))
        self.currentinstancelabel.setText(QCoreApplication.translate("MainWindow", u"Current Instance:", None))
        self.currentInstanceValue.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.currentbestlabel.setText(QCoreApplication.translate("MainWindow", u"Current Best:", None))
        self.current_best_value.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.optimalbestlabel.setText(QCoreApplication.translate("MainWindow", u"Optimal Best:", None))
        self.optimal_best_value.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.timeElapsedLabel.setText(QCoreApplication.translate("MainWindow", u"Time Elapsed:", None))
        self.timeElapsedValue.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.connections.setText(QCoreApplication.translate("MainWindow", u"Connections", None))
        ___qtreewidgetitem = self.contributorsTree.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"Contribution", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"ip", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"id", None));
    # retranslateUi

