# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QTextBrowser, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(882, 669)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(18)
        self.label.setFont(font)

        self.horizontalLayout_3.addWidget(self.label)

        self.uname = QLineEdit(self.centralwidget)
        self.uname.setObjectName(u"uname")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.uname.sizePolicy().hasHeightForWidth())
        self.uname.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.uname)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setFont(font)
        self.label_2.setText(u"\u5bc6\u7801\uff1a")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.password = QLineEdit(self.centralwidget)
        self.password.setObjectName(u"password")
        sizePolicy1.setHeightForWidth(self.password.sizePolicy().hasHeightForWidth())
        self.password.setSizePolicy(sizePolicy1)
        self.password.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_2.addWidget(self.password)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy2)
        self.label_8.setFont(font)

        self.horizontalLayout_11.addWidget(self.label_8)

        self.uid_edit = QLineEdit(self.centralwidget)
        self.uid_edit.setObjectName(u"uid_edit")
        sizePolicy1.setHeightForWidth(self.uid_edit.sizePolicy().hasHeightForWidth())
        self.uid_edit.setSizePolicy(sizePolicy1)
        self.uid_edit.setInputMethodHints(Qt.ImhNone)

        self.horizontalLayout_11.addWidget(self.uid_edit)


        self.verticalLayout_6.addLayout(self.horizontalLayout_11)


        self.verticalLayout.addLayout(self.verticalLayout_6)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(15)
        self.label_5.setFont(font1)

        self.horizontalLayout_6.addWidget(self.label_5)

        self.oj_url = QLineEdit(self.centralwidget)
        self.oj_url.setObjectName(u"oj_url")
        sizePolicy1.setHeightForWidth(self.oj_url.sizePolicy().hasHeightForWidth())
        self.oj_url.setSizePolicy(sizePolicy1)
        self.oj_url.setInputMethodHints(Qt.ImhUrlCharactersOnly)

        self.horizontalLayout_6.addWidget(self.oj_url)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setFont(font)

        self.horizontalLayout_4.addWidget(self.label_3)

        self.browse_path = QPushButton(self.centralwidget)
        self.browse_path.setObjectName(u"browse_path")
        sizePolicy1.setHeightForWidth(self.browse_path.sizePolicy().hasHeightForWidth())
        self.browse_path.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setPointSize(13)
        self.browse_path.setFont(font2)

        self.horizontalLayout_4.addWidget(self.browse_path)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.save_path = QLineEdit(self.centralwidget)
        self.save_path.setObjectName(u"save_path")
        sizePolicy1.setHeightForWidth(self.save_path.sizePolicy().hasHeightForWidth())
        self.save_path.setSizePolicy(sizePolicy1)

        self.verticalLayout_3.addWidget(self.save_path)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.push_to_remote = QCheckBox(self.centralwidget)
        self.push_to_remote.setObjectName(u"push_to_remote")
        sizePolicy1.setHeightForWidth(self.push_to_remote.sizePolicy().hasHeightForWidth())
        self.push_to_remote.setSizePolicy(sizePolicy1)
        self.push_to_remote.setFont(font1)
        self.push_to_remote.setCursor(QCursor(Qt.PointingHandCursor))

        self.verticalLayout_4.addWidget(self.push_to_remote)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)
        self.label_4.setFont(font1)

        self.horizontalLayout_5.addWidget(self.label_4)

        self.remote_url = QLineEdit(self.centralwidget)
        self.remote_url.setObjectName(u"remote_url")
        self.remote_url.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.remote_url.sizePolicy().hasHeightForWidth())
        self.remote_url.setSizePolicy(sizePolicy1)
        self.remote_url.setInputMethodHints(Qt.ImhUrlCharactersOnly)

        self.horizontalLayout_5.addWidget(self.remote_url)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy2)
        self.label_6.setFont(font1)

        self.horizontalLayout_7.addWidget(self.label_6)

        self.git_uname = QLineEdit(self.centralwidget)
        self.git_uname.setObjectName(u"git_uname")
        self.git_uname.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.git_uname.sizePolicy().hasHeightForWidth())
        self.git_uname.setSizePolicy(sizePolicy1)

        self.horizontalLayout_7.addWidget(self.git_uname)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy2)
        self.label_7.setFont(font1)

        self.horizontalLayout_8.addWidget(self.label_7)

        self.token = QLineEdit(self.centralwidget)
        self.token.setObjectName(u"token")
        self.token.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.token.sizePolicy().hasHeightForWidth())
        self.token.setSizePolicy(sizePolicy1)

        self.horizontalLayout_8.addWidget(self.token)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)


        self.verticalLayout.addLayout(self.verticalLayout_4)

        self.skip_problems = QCheckBox(self.centralwidget)
        self.skip_problems.setObjectName(u"skip_problems")
        sizePolicy1.setHeightForWidth(self.skip_problems.sizePolicy().hasHeightForWidth())
        self.skip_problems.setSizePolicy(sizePolicy1)
        self.skip_problems.setFont(font1)
        self.skip_problems.setCursor(QCursor(Qt.PointingHandCursor))

        self.verticalLayout.addWidget(self.skip_problems)

        self.do_not_save_snapshots = QCheckBox(self.centralwidget)
        self.do_not_save_snapshots.setObjectName(u"do_not_save_snapshots")
        sizePolicy1.setHeightForWidth(self.do_not_save_snapshots.sizePolicy().hasHeightForWidth())
        self.do_not_save_snapshots.setSizePolicy(sizePolicy1)
        self.do_not_save_snapshots.setFont(font1)

        self.verticalLayout.addWidget(self.do_not_save_snapshots)

        self.start_button = QPushButton(self.centralwidget)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(sizePolicy1)
        self.start_button.setFont(font1)

        self.verticalLayout.addWidget(self.start_button)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.log = QTextBrowser(self.centralwidget)
        self.log.setObjectName(u"log")
        font3 = QFont()
        font3.setPointSize(15)
        font3.setStyleStrategy(QFont.PreferAntialias)
        self.log.setFont(font3)
        self.log.viewport().setProperty("cursor", QCursor(Qt.IBeamCursor))

        self.horizontalLayout.addWidget(self.log)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.horizontalLayout_9.addWidget(self.progressBar)


        self.verticalLayout_2.addLayout(self.horizontalLayout_9)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"HydroTool", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u540d\uff1a", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"UID\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"OJ\u7f51\u5740\uff1a", None))
        self.oj_url.setText(QCoreApplication.translate("MainWindow", u"http://oiclass.com", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u4f4d\u7f6e\uff1a", None))
        self.browse_path.setText(QCoreApplication.translate("MainWindow", u"\u6d4f\u89c8", None))
        self.push_to_remote.setText(QCoreApplication.translate("MainWindow", u"\u63a8\u9001\u5230\u8fdc\u7a0bgit\u4ed3\u5e93", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u4ed3\u5e93\u5730\u5740\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u540d\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u5bc6\u7801(token)\uff1a", None))
        self.skip_problems.setText(QCoreApplication.translate("MainWindow", u"\u8df3\u8fc7\u5df2\u6709\u9898\u76ee", None))
        self.do_not_save_snapshots.setText(QCoreApplication.translate("MainWindow", u"\u4e0d\u4fdd\u5b58\u9898\u76ee\u56fe\u7247\u4ee5\u52a0\u901f", None))
        self.start_button.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb", None))
    # retranslateUi

