# -*- encoding:utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtWebEngineWidgets
import re
import sys, os
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import *
import pandas as pd
import re
from pykml.factory import KML_ElementMaker as KML
from datetime import datetime
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
import folium
import folium.plugins
from folium.plugins import MarkerCluster
import numpy as np
from collections import defaultdict
from mapper_model import *
from PyQt5.uic import loadUiType
import tempfile



FORM_CLASS, _= loadUiType(resource_path("test.ui"))# use ui reference to load the widgets


class Main(QDialog, FORM_CLASS):


    '''The goal of this tool is to create a GUI that
        allows the user to quickly create, select and
        view the kml files'''    # create class instance

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(resource_path(os.path.join('icon', 'Spart mapper ICON.ico'))))
        #self._my_path = os.path.dirname(os.path.realpath(__file__))
        self.launcher = Mapper_Model()

        self.userinput= defaultdict(lambda: None)

        self.file_instruction= True
        self.toolButton_2.setEnabled(False)
        self.toolButton_3.setEnabled(False)
        #self.plainTextEdit.setPlaceholderText('If you have no spart file and just want to plot some (decimal) coordinates you can directly paste them here as tab-delimited text, in the following format: latitude TAB longitude TAB specimen-voucher (optional)')

        self.listWidget.setAlternatingRowColors(True)
        flag = QAbstractItemView.InternalMove
        self.listWidget.setDragDropMode(flag)
        #self.listWidget.setPlaceholderText("list of Output file generated \n None")
        self.temporary= tempfile.TemporaryDirectory()
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        self.Handel_Buttons()


    def closeEvent(self, event):
         close = QMessageBox.question(self, "QUIT", "Are you sure you want to close the program?",QMessageBox.Yes | QMessageBox.No)
         if close == QMessageBox.Yes:
             self.listWidget.clear()
             self.temporary.cleanup()
             #os.removedirs(temp_directory)
             event.accept()
         else:
             event.ignore()


    #======= SETUP UI =================================



    def Handel_Buttons(self):
        self.toolButton.clicked.connect(self.open_file)
        self.toolButton_2.clicked.connect(self.run_toggle)
        self.toolButton_3.clicked.connect(self.save_file)
        self.toolButton_4.clicked.connect(self.clear)
        self.listWidget.itemClicked.connect(self.Clicked)
        self.plainTextEdit.textChanged.connect(self.toggle)



    def toggle(self):
        self.toolButton_2.setEnabled(True)
        self.toolButton_3.setEnabled(True)
        self.userinput['value']= True


    def run_toggle(self):
        print(self.userinput['value'])
        if self.userinput['value'] and self.plainTextEdit.toPlainText() != '':
            self.run_file_user()
        else:
            self.run_file_tab()


    def open_file(self):
        msg = '1) Select the tab file with latitude and longitude values\n'
        msg += '2) Select a spart file for species mapping (Optional)'
        QMessageBox.information(self, 'Add input files', msg)
        sel = 'Select tab file'
        tab = self.file_dialog(sel, ".")
        if tab:
            path = os.path.split(tab)[0]
            msg = 'Select spart file (optional)'
            spart = self.file_dialog(msg, path)
            self.launcher.filepath(tab, spart)
            self.toolButton_2.setEnabled(True)



    def file_dialog(self, msg, path):
        return QFileDialog.getOpenFileName(self, msg, path)[0]



    def run_file_tab(self):
        try:

            self.listWidget.clear()
            self.plainTextEdit.clear()
            self.launcher.tab_file_data()
            self.launcher.tab_kml()
            self.launcher.tab_html()
            f= self.temporary
            self.launcher.result_files['html_file'].save(os.path.join(f.name, self.launcher.result_files['file_name'] + ".html"))
            outfile = open(os.path.join(f.name, self.launcher.result_files['file_name'] + ".kml"),'w+')
            outfile.write(etree.tostring(self.launcher.result_files['kml_file']).decode('utf-8'))
            outfile.close()
            self.listWidget.addItem(self.launcher.result_files['file_name'] + ".kml")
            self.listWidget.addItem(self.launcher.result_files['file_name'] + ".html")

        except Exception as e:
            print(e)
            QMessageBox.warning(self, "Warning", f"The output  is not obtained because {e}")




    def run_file_user(self):
        try:

            self.listWidget.clear()
            self.launcher.user_input_data(self.plainTextEdit.toPlainText())
            self.launcher.user_input_html()
            self.launcher.user_input_kml()
            self.plainTextEdit.clear()
            f= self.temporary
            self.launcher.result_files['html_file'].save(os.path.join(f.name, self.launcher.result_files['file_name'] + ".html"))
            outfile = open(os.path.join(f.name, self.launcher.result_files['file_name'] + ".kml"),'w+')
            outfile.write(etree.tostring(self.launcher.result_files['kml_file']).decode('utf-8'))
            outfile.close()
            self.listWidget.addItem(self.launcher.result_files['file_name'] + ".kml")
            self.listWidget.addItem(self.launcher.result_files['file_name'] + ".html")

        except Exception as e:
            print(e)
            QMessageBox.warning(self, "Warning", f"The output  is not obtained because {e}")





    def save_file(self):
        try:

            dlg = QFileDialog()
            dlg.setFileMode(QFileDialog.Directory)
            if dlg.exec_():
                filenames = dlg.selectedFiles()
                path_text= QDir.toNativeSeparators(str(filenames[0]))
                self.launcher.savepath(path_text)
                outfile = open(os.path.join(path_text, self.launcher.result_files['file_name'] + ".kml"),'w+')
                outfile.write(etree.tostring(self.launcher.result_files['kml_file']).decode('utf-8'))
                outfile.close()
                self.launcher.result_files['html_file'].save(os.path.join(path_text, self.launcher.result_files['file_name'] +".html"))

        except Exception as e:
            print(e)
            QMessageBox.warning(self, "Warning", f"The output  is not saved because {e}")


    def reset_placement(self):

        g = QDesktopWidget().availableGeometry()
        #self.resize(651, 400)
        self.resize(0.4 * g.width(), 0.4 * g.height())
        self.move(g.center().x() - self.width() / 2, g.center().y() - self.height() / 2)


    def state_changed1(self):
        self.m_output = QtWebEngineWidgets.QWebEngineView()

        self.horizontalLayout_4.addWidget(self.m_output)


    def state_changed2(self):

        self.graph1= QGraphicsView()
        self.horizontalLayout_4.addWidget(self.graph1)


    def clear(self):
        try:

            self.toolButton_2.setEnabled(False)
            self.toolButton_3.setEnabled(False)
            self.listWidget.clear()
            self.plainTextEdit.clear()
            self.launcher.result_files['file_name']= None

            if self.horizontalLayout_4.count() > 1:
                item = self.horizontalLayout_4.takeAt(1)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                    self.reset_placement()

        except Exception as e:
            print(e)
            QMessageBox.warning(self, "Warning", f"The output  is not obtained because {e}")





    def Clicked(self, item2):

        try:
            n= self.horizontalLayout_4.count()
            print(n)
            if self.horizontalLayout_4.count() > 1:
                item = self.horizontalLayout_4.takeAt(1)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                    self.reset_placement()
            name= item2.text()
            name= name.split(".")[-1]

            if name == 'html':
                import webbrowser
                new = 2
                xx= os.path.join(self.temporary.name, self.launcher.result_files['file_name']+ ".html")
                
                url = f"file://{xx}"
                webbrowser.open(url,new=new)


            if name == 'kml':
                self.state_changed2()
                f= open(os.path.join(self.temporary.name, self.launcher.result_files['file_name']+ ".kml"), 'r+')
                mytext2= f.read().split('><')

                print_text= ''
                for line in mytext2:
                    print_text += line + '\n'

                self.scene = QGraphicsScene()
                mytext1 = QGraphicsSimpleTextItem(print_text)
                self.scene.addItem(mytext1)
                self.graph1.setScene(self.scene)
                f.close()

        except Exception as e:
            print(e)
            QMessageBox.warning(self, "Warning", f"The output  is not obtained because {e}")




def main1():

    app=QApplication(sys.argv)
    window=Main()
    window.show()
    QApplication.processEvents()
    app.exec_()



if __name__=='__main__':
    main1()
