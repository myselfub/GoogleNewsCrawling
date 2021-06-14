"""
    Version: 1.1
    Author: Ecoplay 김유빈
    Create Date: 2021.02.26
    Last Update Date: 2021.03.01
    21.02.27: 프로토타입 완성
    21.03.28: 크기, 정보 등 추가
    21.03.02: 아이콘변경
"""

import sys
import urllib
# import tkinter as tk
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, \
    QSpinBox, QDesktopWidget, QComboBox, QAction, QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication
import crawling
import os.path


class NewsCrawlingWidget(QMainWindow):
    grid = QGridLayout()
    keyword_edit = None
    page_number_edit = None
    extension_combobox = None

    def __init__(self):
        super().__init__()
        self.img_download()
        self.init_ui()

    def img_download(self):
        directory = 'imgs'
        if not os.path.exists(directory):
            os.makedirs(directory)
        url = 'https://cdn.imweb.me/thumbnail/20200115/e2d89aba8f7be.png'
        icon_img = directory + '/icon_img.png'
        if not os.path.isfile(icon_img):
            urllib.request.urlretrieve(url, icon_img)

    def init_ui(self):
        self.window_ui()
        self.menu_ui()
        self.keyword_ui()
        self.page_number_ui()
        self.combobox_ui()
        self.button_quit_ui()
        q_widget = QWidget()
        # root = tk.Tk()
        # width_px = root.winfo_screenwidth()
        # height_px = root.winfo_screenheight()
        self.setFixedSize(360, 180)
        q_widget.setLayout(self.grid)
        self.setCentralWidget(q_widget)
        self.show()

    def window_ui(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('Ecoplay-NewsCrawling')
        self.setWindowIcon(QIcon('imgs/icon_img.png'))
        self.setLayout(self.grid)

    def menu_ui(self):
        info_action = QAction('정보', self)
        info_action.setToolTip('Information')
        info_action.setStatusTip('Information')
        info_action.triggered.connect(self.info_clicked)

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        help_menu = menubar.addMenu('&Help')
        help_menu.addAction(info_action)

    def keyword_ui(self):
        label = QLabel('검색어 : ')
        label.setToolTip('Keyword')
        label.setFont(QFont('나눔고딕', 15))
        label.setStyleSheet('Color : #222222')
        self.grid.addWidget(label, 0, 0)
        self.keyword_edit = QLineEdit()
        self.keyword_edit.setToolTip('Please enter a keyword.')
        self.keyword_edit.setStatusTip('Keyword.')
        self.keyword_edit.setMaxLength(25)
        self.keyword_edit.setFixedHeight(25)
        self.keyword_edit.setFont(QFont('나눔고딕', 10))
        self.grid.addWidget(self.keyword_edit, 0, 1)

    def page_number_ui(self):
        label = QLabel('페이지수 : ')
        label.setToolTip('Page Number')
        label.setFont(QFont('나눔고딕', 15))
        label.setStyleSheet('Color : #222222')
        self.grid.addWidget(label, 1, 0)
        self.page_number_edit = QSpinBox()
        self.page_number_edit.setToolTip('Please enter a page number.')
        self.page_number_edit.setStatusTip('Page Number.')
        self.page_number_edit.setMinimum(1)
        self.page_number_edit.setMaximum(50)
        self.page_number_edit.setValue(5)
        self.page_number_edit.setFixedHeight(25)
        self.page_number_edit.setFont(QFont('나눔고딕', 10))
        self.grid.addWidget(self.page_number_edit, 1, 1)
        btn = QPushButton('검색', self)
        btn.setToolTip('Search')
        btn.setStatusTip('Search')
        btn.setFont(QFont('나눔고딕', 14))
        btn.setStyleSheet('Color : #5555FA')
        btn.clicked.connect(self.call_crawling)
        self.grid.addWidget(btn, 3, 1)

    def combobox_ui(self):
        label = QLabel('확장자 : ')
        label.setToolTip('File Extension')
        label.setFont(QFont('나눔고딕', 15))
        label.setStyleSheet('Color : #222222')
        self.grid.addWidget(label, 2, 0)
        self.extension_combobox = QComboBox()
        self.extension_combobox.setToolTip('Please select a File extension.')
        self.extension_combobox.setStatusTip('File Extension.')
        self.extension_combobox.addItem('txt')
        self.extension_combobox.addItem('xlsx')
        self.extension_combobox.setFont(QFont('나눔고딕', 11))
        self.keyword_edit.setFixedHeight(25)
        self.grid.addWidget(self.extension_combobox, 2, 1)

    def button_quit_ui(self):
        btn = QPushButton('종료', self)
        btn.setToolTip('Quit')
        btn.setStatusTip('Quit')
        btn.setFont(QFont('나눔고딕', 14))
        btn.setStyleSheet('Color : #FA5555')
        btn.clicked.connect(QCoreApplication.instance().quit)
        self.grid.addWidget(btn, 3, 0)

    def call_crawling(self):
        crawling.crawling(self.keyword_edit.displayText(), self.page_number_edit.value(),
                          self.extension_combobox.currentText())
        self.keyword_edit.clear()
        self.page_number_edit.setValue(5)

    def info_clicked(self):
        message = 'Version: 1.1\n' \
                  'Create Date: 2021.02.26\n' \
                  'Last Update Date: 2021.03.02\n' \
                  'E-Mail : fd9100@naver.com\n' \
                  'Made by KimYuBin'
        q_messagebox = QMessageBox()
        q_messagebox.information(self, 'Information', message, QMessageBox.Close)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NewsCrawlingWidget()
    sys.exit(app.exec_())
