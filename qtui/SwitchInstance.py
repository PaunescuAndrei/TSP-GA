# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SwitchInstance.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(603, 196)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.pathwidget = QWidget(self.widget)
        self.pathwidget.setObjectName(u"pathwidget")
        self.horizontalLayout = QHBoxLayout(self.pathwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.filepath = QLineEdit(self.pathwidget)
        self.filepath.setObjectName(u"filepath")

        self.horizontalLayout.addWidget(self.filepath)

        self.browseButton = QPushButton(self.pathwidget)
        self.browseButton.setObjectName(u"browseButton")

        self.horizontalLayout.addWidget(self.browseButton)


        self.verticalLayout_2.addWidget(self.pathwidget)

        self.optimalvaluewidget = QWidget(self.widget)
        self.optimalvaluewidget.setObjectName(u"optimalvaluewidget")
        self.horizontalLayout_2 = QHBoxLayout(self.optimalvaluewidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.optimalvaluewidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label)

        self.optimalValue = QSpinBox(self.optimalvaluewidget)
        self.optimalValue.setObjectName(u"optimalValue")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.optimalValue.sizePolicy().hasHeightForWidth())
        self.optimalValue.setSizePolicy(sizePolicy1)
        self.optimalValue.setMaximum(999999999)

        self.horizontalLayout_2.addWidget(self.optimalValue)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addWidget(self.optimalvaluewidget)


        self.verticalLayout.addWidget(self.widget)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Switch Instance", None))
        self.filepath.setText("")
        self.browseButton.setText(QCoreApplication.translate("Dialog", u"Browse", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Optimal Solution Value:", None))
    # retranslateUi

