# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DMMREC.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 756)
        MainWindow.setMinimumSize(QSize(1200, 756))
        icon = QIcon()
        icon.addFile(u"Iconos/DMMREC.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_Botones = QHBoxLayout()
        self.horizontalLayout_Botones.setObjectName(u"horizontalLayout_Botones")
        self.label_Com = QLabel(self.centralwidget)
        self.label_Com.setObjectName(u"label_Com")

        self.horizontalLayout_Botones.addWidget(self.label_Com)

        self.comboBoxPort = QComboBox(self.centralwidget)
        self.comboBoxPort.setObjectName(u"comboBoxPort")
        self.comboBoxPort.setMinimumSize(QSize(150, 0))
        self.comboBoxPort.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_Botones.addWidget(self.comboBoxPort)

        self.Buttonrefresh = QPushButton(self.centralwidget)
        self.Buttonrefresh.setObjectName(u"Buttonrefresh")
        icon1 = QIcon()
        icon1.addFile(u"Iconos/Ico_refresh.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Buttonrefresh.setIcon(icon1)

        self.horizontalLayout_Botones.addWidget(self.Buttonrefresh)

        self.Button_connect = QPushButton(self.centralwidget)
        self.Button_connect.setObjectName(u"Button_connect")

        self.horizontalLayout_Botones.addWidget(self.Button_connect)

        self.horizontalSpacer = QSpacerItem(60, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_Botones.addItem(self.horizontalSpacer)

        self.label_Art = QLabel(self.centralwidget)
        self.label_Art.setObjectName(u"label_Art")

        self.horizontalLayout_Botones.addWidget(self.label_Art)

        self.comboBoxArt = QComboBox(self.centralwidget)
        self.comboBoxArt.setObjectName(u"comboBoxArt")
        self.comboBoxArt.setMinimumSize(QSize(220, 0))

        self.horizontalLayout_Botones.addWidget(self.comboBoxArt)

        self.label_Orden = QLabel(self.centralwidget)
        self.label_Orden.setObjectName(u"label_Orden")

        self.horizontalLayout_Botones.addWidget(self.label_Orden)

        self.spinBoxorden = QSpinBox(self.centralwidget)
        self.spinBoxorden.setObjectName(u"spinBoxorden")
        self.spinBoxorden.setMinimumSize(QSize(70, 0))
        self.spinBoxorden.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.spinBoxorden.setMinimum(0)
        self.spinBoxorden.setMaximum(9999)
        self.spinBoxorden.setValue(1)

        self.horizontalLayout_Botones.addWidget(self.spinBoxorden)


        self.gridLayout_2.addLayout(self.horizontalLayout_Botones, 0, 0, 1, 2)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(660, 660))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_im = QLabel(self.widget)
        self.label_im.setObjectName(u"label_im")
        self.label_im.setMinimumSize(QSize(640, 640))
        self.label_im.setMaximumSize(QSize(640, 640))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Light, brush1)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush1)
        brush2 = QBrush(QColor(127, 127, 127, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush2)
        brush3 = QBrush(QColor(170, 170, 170, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush1)
        brush4 = QBrush(QColor(255, 255, 220, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
        brush5 = QBrush(QColor(0, 0, 0, 128))
        brush5.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush5)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
        brush6 = QBrush(QColor(0, 0, 0, 128))
        brush6.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush6)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)
        brush7 = QBrush(QColor(0, 0, 0, 128))
        brush7.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush7)
#endif
        self.label_im.setPalette(palette)
        self.label_im.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_im, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.widget, 1, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.label_bat = QLabel(self.centralwidget)
        self.label_bat.setObjectName(u"label_bat")
        self.label_bat.setMinimumSize(QSize(50, 40))
        self.label_bat.setMaximumSize(QSize(50, 40))
        self.label_bat.setPixmap(QPixmap(u"Iconos/ico-blank.png"))
        self.label_bat.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label_bat)

        self.label_DMM = QLabel(self.centralwidget)
        self.label_DMM.setObjectName(u"label_DMM")
        self.label_DMM.setMinimumSize(QSize(360, 110))
        self.label_DMM.setMaximumSize(QSize(398, 110))
        font = QFont()
        font.setPointSize(48)
        self.label_DMM.setFont(font)
        self.label_DMM.setLocale(QLocale(QLocale.Spanish, QLocale.Spain))
        self.label_DMM.setFrameShape(QFrame.Box)
        self.label_DMM.setFrameShadow(QFrame.Sunken)
        self.label_DMM.setAlignment(Qt.AlignCenter)
        self.label_DMM.setMargin(0)

        self.horizontalLayout.addWidget(self.label_DMM)

        self.label_acdc = QLabel(self.centralwidget)
        self.label_acdc.setObjectName(u"label_acdc")
        self.label_acdc.setMinimumSize(QSize(50, 40))
        self.label_acdc.setMaximumSize(QSize(50, 40))
        self.label_acdc.setPixmap(QPixmap(u"Iconos/ico-blank.png"))
        self.label_acdc.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label_acdc)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(480, 50))
        font1 = QFont()
        font1.setFamily(u"DejaVu Sans")
        font1.setPointSize(26)
        font1.setBold(True)
        font1.setWeight(75)
        self.label.setFont(font1)
        self.label.setFrameShape(QFrame.Panel)
        self.label.setFrameShadow(QFrame.Raised)
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 8):
            self.tableWidget.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMinimumSize(QSize(500, 390))
        self.tableWidget.setFocusPolicy(Qt.NoFocus)

        self.verticalLayout.addWidget(self.tableWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(268, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButton_start = QPushButton(self.centralwidget)
        self.pushButton_start.setObjectName(u"pushButton_start")
        self.pushButton_start.setEnabled(False)
        self.pushButton_start.setMinimumSize(QSize(100, 30))
        self.pushButton_start.setAutoDefault(True)

        self.horizontalLayout_2.addWidget(self.pushButton_start)

        self.pushButton_next = QPushButton(self.centralwidget)
        self.pushButton_next.setObjectName(u"pushButton_next")
        self.pushButton_next.setEnabled(False)
        self.pushButton_next.setMinimumSize(QSize(100, 30))

        self.horizontalLayout_2.addWidget(self.pushButton_next)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout_2.addLayout(self.verticalLayout, 1, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.comboBoxPort, self.Button_connect)
        QWidget.setTabOrder(self.Button_connect, self.comboBoxArt)
        QWidget.setTabOrder(self.comboBoxArt, self.spinBoxorden)
        QWidget.setTabOrder(self.spinBoxorden, self.pushButton_start)
        QWidget.setTabOrder(self.pushButton_start, self.pushButton_next)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"DMMREC", None))
        self.label_Com.setText(QCoreApplication.translate("MainWindow", u"Com Port", None))
        self.Buttonrefresh.setText("")
        self.Button_connect.setText(QCoreApplication.translate("MainWindow", u"C&onnect", None))
        self.label_Art.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.label_Orden.setText(QCoreApplication.translate("MainWindow", u"Batch nr.", None))
        self.label_im.setText("")
        self.label_bat.setText("")
        self.label_DMM.setText(QCoreApplication.translate("MainWindow", u"----.--- --", None))
        self.label_acdc.setText("")
        self.label.setText("")
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Vmax", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Value", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Vmin", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Rel", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"%", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Derivation", None));
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Pass", None));
        self.pushButton_start.setText(QCoreApplication.translate("MainWindow", u"S&tart", None))
        self.pushButton_next.setText(QCoreApplication.translate("MainWindow", u"N&ext", None))
    # retranslateUi

