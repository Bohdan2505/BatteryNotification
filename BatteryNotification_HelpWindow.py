import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
import psutil
import os
from playsound import playsound


######################################## Короткий гайд по названиям объектов
#    Cуфиксы показывают тип элемента
    #    tb - Text box  поле для ввода текста (LineEdit, PlainTextEdit  ,TextEdit)
    #    lb - Label
    #    cmb - ComboBox
    #    bt - Button (PushButton)
    #    chb - CheckBox
# Нижние подчеркивания разделяют слова, если в названии объекта присутствует '_Notification' это говорит о то, что объект пренадлежит к блоку уведомлений,
# в конце каждого блока и его дочерних элементов стоит номер который определяет их уникалmное названия
# Названия всей переменной (а не её части) полностью в верхнем регистре, говорит что это глобальная переменная

# Глобальные переменные
CONFIG_FILE_NAME = 'configasdasda3.ini' # Имя файла в который будут сохранятся параметры
I_COUNT = 0 # Будет испольозватся как номер для блока уведомления (подробнее функция Ui_MainWindow().add_notification

Object_Notification_list = []
CURRENT_LANGUAGE = ''

# Класс окна всей программы, в нем идет отрисовка и все функции в том числе и сохранения


class Help_Window(QMainWindow):
    
    

        
    def __init__(self, parent=None):
        super().__init__()
        
        self.helpUi()
        self.setObjectName("MainWindow")
                
        
    def helpUi(self):
        # Отрисовка окна
        #self.setWindowFlag(Qt.FramelessWindowHint) 
        #self.setWindowFlag(Qt.Tool)
        #self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("Help")
        self.resize(590, 540)
        self.setMinimumSize(QSize(590, 540))
        self.setMaximumSize(QSize(590, 540))
        font = QFont()
        font.setFamily("Times New Roman")
        self.setFont(font)
        self.setWindowOpacity(1.0)
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.setAnimated(True)
        self.setTabShape(QTabWidget.Rounded)
        self.show()            

    def closeEvent(self, event):
        event.ignore()
        self.hide()





        
                        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = Help_Window()
    ui.show()
    sys.exit(app.exec_())
    
    
    
    
        
        
    
        