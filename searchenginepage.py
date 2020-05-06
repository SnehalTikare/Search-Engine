import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
#from PyQt5.QtGui import QPixmap
#from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel, QTextBrowser
#from PyQt5.QtCore import pyqtSlot
from query_processing import get_result


class application(QtWidgets.QMainWindow):
    def __init__(self):
            super().__init__()
            self.window()

    def window(self):
        self.setWindowTitle('UIC Search engine')
        self.setGeometry(300, 300, 500, 500)
        self.imglabel = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap('uic_logo_red.png')
        self.pixmap = self.pixmap.scaledToWidth(45)
        self.pixmap = self.pixmap.scaledToHeight(45)
        self.imglabel.setPixmap(self.pixmap)
        self.imglabel.move(150,5)
        self.label = QtWidgets.QLabel(self)
        self.label.setText("<font color='Black'>Search</font>")
        self.label.setFont(QtGui.QFont('Arial', 20,weight=QtGui.QFont.Bold)) 
        self.label.move(200, 10)
        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.move(120, 50)
        self.textbox.resize(200, 20)
        self.textbox.setToolTip("Enter Your Query here")
        self.b = QtWidgets.QPushButton(self)
        self.b.setText('search')
        self.b.move(330, 48)
        self.b.clicked.connect(self.submit)
        self.results = QtWidgets.QTextBrowser(self)
        # self.results.setReadOnly(True)
        self.results.move(50, 80)
        self.results.resize(400, 400)
        self.results.hide()
        self.show()

    def submit(self):
        self.results.setText("")
        self.number_of_links = 10
        self.user_query = self.textbox.text()
        self.query=[]
        self.query.append(self.user_query)
        self.result_url = get_result(self.query)
        self.urls = []
        for url in self.result_url:
            self.urls.append(self.make_hyperlink(url))
        urls = ''.join(self.urls[:self.number_of_links])
        self.results.setText(urls)
        self.results.setOpenExternalLinks(True)
        self.results.show()

    def make_hyperlink(self,url):
        return '<a href="' + url + '">' + url + '</a><br><br>'

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = application()
    sys.exit(app.exec_())