import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui,QtCore
from query_processing import get_result



class application(QtWidgets.QMainWindow):
    def __init__(self):
            super().__init__()
            self.number_of_links = 10
            self.window()

    def window(self):
        self.setWindowTitle('UIC Search engine')
        self.setGeometry(300, 100, 700, 800)
        self.imglabel = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap('uic_logo_red.png')
        self.pixmap = self.pixmap.scaledToWidth(40)
        self.pixmap = self.pixmap.scaledToHeight(40)
        self.imglabel.setPixmap(self.pixmap)
        self.imglabel.move(280,15)
        self.label = QtWidgets.QLabel(self)
        self.label.setText("<font color='Black'>Search</font>")
        self.label.setFont(QtGui.QFont('Arial', 20,weight=QtGui.QFont.Bold)) 
        self.label.move(330, 15)
        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.move(220, 60)
        self.textbox.resize(220, 20)
        self.textbox.setToolTip("Enter Your Query here")
        self.b = QtWidgets.QPushButton(self)
        self.b.setText('search')
        self.b.move(450, 57)
        self.b.clicked.connect(self.submit)
        self.results = QtWidgets.QTextBrowser(self)
        # self.results.setReadOnly(True)
        self.results.move(110, 160)
        self.results.resize(500, 500)
        self.results.hide()
        self.also_search_for = QtWidgets.QLabel(self)
        self.also_search_for.setText('Also search for: ')
        self.also_search_for.move(30,90)
        self.also_search_for.hide()
        self.keyphrase_1 = QtWidgets.QLabel(self)
        self.keyphrase_1.move(130,95)
        self.keyphrase_1.resize(200,20)
        self.keyphrase_1.hide()
        self.keyphrase_2 = QtWidgets.QLabel(self)
        self.keyphrase_2.move(280,95)
        self.keyphrase_2.resize(200,20)
        self.keyphrase_2.hide()
        self.keyphrase_3 = QtWidgets.QLabel(self)
        self.keyphrase_3.move(130,112)
        self.keyphrase_3.resize(200,20)
        self.keyphrase_3.hide()
        self.keyphrase_4 = QtWidgets.QLabel(self)
        self.keyphrase_4.move(280,112)
        self.keyphrase_4.resize(200,20)
        self.keyphrase_4.hide()

        self.more = QtWidgets.QPushButton('See more', self)
        self.more.move(350, 700)
        self.more.resize(250, 30)
        #self.more.setStyleSheet()
        self.more.clicked.connect(self.on_click_label)
        # self.more.linkActivated(self.on_click_label)
        self.more.hide()
        self.show()

    def submit(self):
        self.results.setText("")
        self.number_of_links = 10
        self.user_query = self.textbox.text()
        if not self.user_query:
            return
        self.query=[]
        self.query.append(self.user_query)
        self.result_url,self.top_phrases ,self.title= get_result(self.query)
        self.urls = []
        for url,title in self.result_url:
            self.urls.append(self.make_hyperlink(url,title))
        for i, word in enumerate(self.top_phrases[:4]):
            label = getattr(self, 'keyphrase_{}'.format(i+1))
            #label = self.findChild(QtWidgets.QLabel, find_label)
            label.setText(word)
        urls = ''.join(self.urls[:self.number_of_links])
        self.results.setText(urls)
        self.results.setOpenExternalLinks(True)
        self.more.setText('See more')
        self.more.show()
        if self.top_phrases:
            self.also_search_for.show()
        self.keyphrase_1.show()
        self.keyphrase_2.show()
        self.keyphrase_3.show()
        self.keyphrase_4.show()
        self.results.show()

    def make_hyperlink(self,url,title):
        return  '<h5>'+title +'</h5>' +'</br><a href="' + url + '">' + url + '</a></br>'

    
    @QtCore.pyqtSlot()
    def on_click_label(self):
        self.number_of_links= self.number_of_links + 10
        self.results.setText(''.join(self.urls[:self.number_of_links]))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = application()
    sys.exit(app.exec_())