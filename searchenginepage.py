import sys
from PyQt5 import QtWidgets
#from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel, QTextBrowser
#from PyQt5.QtCore import pyqtSlot
from query_processing import *


class application(QtWidgets.QMainWindow):
    def __init__(self):
            super().__init__()
            self.title = 'UIC search Engine'
            self.left = 10
            self.top = 10
            self.width = 1200
            self.height = 700
            self.window()
            self.results_page = 10

    def window(self):
        self.setWindowTitle('UIC Search engine')
        self.setGeometry(300, 300, 500, 500)
        self.label = QtWidgets.QLabel(self)
        self.label.setText('Search UIC')
        self.label.move(200, 10)
        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.move(120, 50)
        self.textbox.resize(200, 20)
        self.textbox.setToolTip("Enter Your Query here")
        self.b = QtWidgets.QPushButton(self)
        self.b.setText('search')
        self.b.move(330, 48)
        self.b.clicked.connect(self.submit)
        self.result_view = QtWidgets.QTextBrowser(self)
        # self.result_view.setReadOnly(True)
        self.result_view.move(50, 80)
        self.result_view.resize(400, 400)
        self.result_view.hide()
        self.show()

    def submit(self):
        self.results_page = 10
        self.user_query = self.textbox.text()
        self.query=[]
        self.query.append(self.user_query)
        self.result = get_result(self.query)
        display_html = ''
        self.url_list = []
        for url in self.result:

            display_html += self.add_href(url)
            self.url_list.append(self.add_href(url))
        urls = ''.join(self.url_list[:self.results_page])
        self.result_view.setText(urls)
        self.result_view.setOpenExternalLinks(True)
        self.result_view.show()

    def add_href(self,url):
        # return '<a href="' + url + '">' + url + '</a>' + '<pre> Score : ' + str(score) + '</pre><br>'
        return '<a href="' + url + '">' + url + '</a><br><br>'

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = application()
    sys.exit(app.exec_())