import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
import psutil
import os
from playsound import playsound

import BatteryNotification_HelpWindow
import BatteryNotification_SettingsWindow
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
TRAY_ICON_EXIST = False

# Класс окна всей программы, в нем идет отрисовка и все функции в том числе и сохранения

class Ui_MainWindow(QMainWindow):
    global CURRENT_LANGUAGE
    

        
    def __init__(self, parent=None):
        super().__init__()
        
        self.setupUi()
        self.setObjectName("MainWindow")
        self.load_file()
        self.translate_app_text()
        
        
        self.battery_information()
        
        
        
    
    def setupUi(self):
        # Отрисовка окна
        #self.setWindowFlag(Qt.FramelessWindowHint) 
        #self.setWindowFlag(Qt.Tool)
        #self.setWindowModality(Qt.ApplicationModal)
        self.resize(590, 540)
        self.setMinimumSize(QSize(590, 540))
        self.setMaximumSize(QSize(590, 540))
        self.setWindowIcon(QIcon('icon.png'))
        font = QFont()
        font.setFamily("Times New Roman")
        self.setFont(font)
        self.setWindowOpacity(1.0)
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.setAnimated(True)
        self.setTabShape(QTabWidget.Rounded)
        
################## Отрисовка menuBar######
        #self.menu= QMainWindow.menuBar(self)

       # self.filemenu = self.menu.addMenu("Файл")
        #saveAction = QAction(QIcon('weather/file.png'), '&Сохранить', self)
        #self.filemenu.addAction(saveAction)
       # saveAction.triggered.connect(self.save_file)
       # loadAction = QAction(QIcon('weather/file.png'), '&Загрузить', self)
       # self.filemenu.addAction(loadAction)
        #loadAction.triggered.connect(self.load_file)
        
        #Ортисовка надписи которая будет исполнять роль статус бара и выводить сообщения
        self.lb_Status_Bar = QLabel(self)
        self.lb_Status_Bar.setAlignment(Qt.AlignLeading|Qt.AlignCenter|Qt.AlignVCenter)
        self.lb_Status_Bar.setGeometry(QRect(10, 510, 565, 35))
        self.lb_Status_Bar.setToolTip("")
        self.lb_Status_Bar.setObjectName("lb_Status_Bar")
        
        
        self.General_Information = QFrame(self)
        self.General_Information.setGeometry(QRect(10, 35, 391, 141))
        self.General_Information.setTabletTracking(False)
        self.General_Information.setToolTip("")
        self.General_Information.setStatusTip("")
        self.General_Information.setWhatsThis("")
        self.General_Information.setAccessibleName("")
        self.General_Information.setAccessibleDescription("")
        self.General_Information.setFrameShape(QFrame.Box)
        self.General_Information.setFrameShadow(QFrame.Raised)
        self.General_Information.setObjectName("General_Information")
        
        self.BatteryBar = QProgressBar(self.General_Information)
        self.BatteryBar.setEnabled(True)
        self.BatteryBar.setGeometry(QRect(10, 10, 61, 121))
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.BatteryBar.setFont(font)
        self.BatteryBar.setToolTip("")
        self.BatteryBar.setLayoutDirection(Qt.LeftToRight)
        self.BatteryBar.setStyleSheet("")
        self.BatteryBar.setMaximum(100)
        
        
       
        self.BatteryBar.setAlignment(Qt.AlignJustify|Qt.AlignTop)
        self.BatteryBar.setTextVisible(False)
        self.BatteryBar.setOrientation(Qt.Vertical)
        self.BatteryBar.setInvertedAppearance(False)
        self.BatteryBar.setTextDirection(QProgressBar.BottomToTop)
        self.BatteryBar.setObjectName("BatteryBar")
        
        self.layoutWidget = QWidget(self.General_Information)
        self.layoutWidget.setGeometry(QRect(80, 10, 300, 121))
        self.layoutWidget.setToolTip("")
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QFormLayout(self.layoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setHorizontalSpacing(10)
        self.formLayout.setVerticalSpacing(15)
        self.formLayout.setObjectName("formLayout")
        
        self.lb_Percent = QLabel(self.layoutWidget)
        font = QFont()
        font.setPointSize(18)
        self.lb_Percent.setFont(font)
        self.lb_Percent.setToolTip("")
        self.lb_Percent.setScaledContents(False)
        self.lb_Percent.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_Percent.setObjectName("lb_Percent")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lb_Percent)
        
        self.lb_Percent_value = QLabel(self.layoutWidget)
        font = QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.lb_Percent_value.setFont(font)
        self.lb_Percent_value.setToolTip("")
        self.lb_Percent_value.setScaledContents(False)
        self.lb_Percent_value.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lb_Percent_value.setObjectName("lb_Percent_value")
        #self.lb_Percent_value.setText(f'{BATTERY_PROPERTIES.percent} %')
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lb_Percent_value)
        
        self.lb_Power = QLabel(self.layoutWidget)
        font = QFont()
        font.setPointSize(18)
        self.lb_Power.setFont(font)
        self.lb_Power.setToolTip("")
        self.lb_Power.setStatusTip("")
        self.lb_Power.setWhatsThis("")
        self.lb_Power.setAccessibleName("")
        self.lb_Power.setAccessibleDescription("")
        self.lb_Power.setScaledContents(False)
        self.lb_Power.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_Power.setObjectName("lb_Power")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lb_Power)
        
        self.lb_Power_value = QLabel(self.layoutWidget)
        font = QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.lb_Power_value.setFont(font)
        self.lb_Power_value.setToolTip("")
        self.lb_Power_value.setStatusTip("")
        self.lb_Power_value.setWhatsThis("")
        self.lb_Power_value.setAccessibleName("")
        self.lb_Power_value.setAccessibleDescription("")
        self.lb_Power_value.setScaledContents(False)
        self.lb_Power_value.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lb_Power_value.setObjectName("lb_Power_value")
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lb_Power_value)
        
        self.lb_Left_Sec = QLabel(self.layoutWidget)
        font = QFont()
        font.setPointSize(18)
        self.lb_Left_Sec.setFont(font)
        self.lb_Left_Sec.setToolTip("")
        self.lb_Left_Sec.setStatusTip("")
        self.lb_Left_Sec.setWhatsThis("")
        self.lb_Left_Sec.setAccessibleName("")
        self.lb_Left_Sec.setAccessibleDescription("")
        self.lb_Left_Sec.setScaledContents(False)
        self.lb_Left_Sec.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_Left_Sec.setObjectName("lb_Left_Sec")
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lb_Left_Sec)
        
        self.lb_Left_Sec_value = QLabel(self.layoutWidget)
        font = QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.lb_Left_Sec_value.setFont(font)
        self.lb_Left_Sec_value.setToolTip("")
        self.lb_Left_Sec_value.setStatusTip("")
        self.lb_Left_Sec_value.setWhatsThis("")
        self.lb_Left_Sec_value.setAccessibleName("")
        self.lb_Left_Sec_value.setAccessibleDescription("")
        self.lb_Left_Sec_value.setScaledContents(False)
        
        self.lb_Left_Sec_value.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lb_Left_Sec_value.setObjectName("lb_Left_Sec_value")
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lb_Left_Sec_value)
        
        self.Setting_Frame = QFrame(self)
        self.Setting_Frame.setGeometry(QRect(410, 35, 170, 141))
        self.Setting_Frame.setToolTip("")
        self.Setting_Frame.setFrameShape(QFrame.Box)
        self.Setting_Frame.setFrameShadow(QFrame.Raised)
        self.Setting_Frame.setObjectName("frame_3")
        
        self.bt_Help = QPushButton(self.Setting_Frame)
        self.bt_Help.setGeometry(QRect(5, 100, 160, 31))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.bt_Help.setFont(font)
        self.bt_Help.setToolTip("")
        self.bt_Help.setObjectName("bt_Help")
        self.bt_Help.clicked.connect(self.show_help_window)
        self.bt_Settings = QPushButton(self.Setting_Frame)
        self.bt_Settings.setGeometry(QRect(5, 60, 160, 31))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.bt_Settings.setFont(font)
        self.bt_Settings.setToolTip("")
        self.bt_Settings.setObjectName("bt_Settings")
        self.bt_Settings.clicked.connect(self.show_settings_window)
        
        self.cmb_Languages = QComboBox(self.Setting_Frame)
        self.cmb_Languages.setGeometry(QRect(5, 20, 160, 31))
        font = QFont()
        font.setPointSize(12)
        self.cmb_Languages.setFont(font)
        self.cmb_Languages.setToolTip("")
        self.cmb_Languages.setLayoutDirection(Qt.LeftToRight)
        self.cmb_Languages.addItems(["Українська", "English", "Русский"])
        self.cmb_Languages.setObjectName("cmb_Languages")
        self.cmb_Languages.currentIndexChanged.connect(self.language_text)
        
        

        ##translate_app_text
        self.lb_Language = QLabel(self.Setting_Frame)
        self.lb_Language.setGeometry(QRect(5, 0, 71, 21))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lb_Language.setFont(font)
        self.lb_Language.setToolTip("")
        self.lb_Language.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_Language.setObjectName("lb_Language")
        
        
        # Отрисовка кнопки "Добавить" или "+"
        #tool_tip_translate = self.translate_app_text(5)
        self.bt_Add_Notification = QPushButton(self)
        self.bt_Add_Notification.setGeometry(QRect(10, 178, 30, 30))
        font = QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.bt_Add_Notification.setFont(font)
        self.bt_Add_Notification.setToolTip("")
        self.bt_Add_Notification.setText('+')
        self.bt_Add_Notification.setStyleSheet("color:green")
        self.bt_Add_Notification.setObjectName("bt_Add_Notification")
        self.bt_Add_Notification.clicked.connect(self.resize_scrollAreaWidgetContents)
        #self.bt_Add_Notification.clicked.connect(self.add_notification) # Приязка функции на клик по кнопке
        
        
        
        
        self.lb_Notifications = QLabel(self)
        self.lb_Notifications.setGeometry(QRect(120, 178, 321, 31))
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lb_Notifications.setFont(font)
        self.lb_Notifications.setToolTip("")
        self.lb_Notifications.setAlignment(Qt.AlignCenter)
        self.lb_Notifications.setObjectName("lb_Notifications")
        
        # Отрисовка ScrollArea
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setGeometry(QRect(10, 210, 570, 305))
        self.scrollArea.setMinimumSize(QSize(570, 300))
        self.scrollArea.setToolTip("")
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QWidget()
###############################################        ###################
        #height_scrollAreaWidgetContents = 300
        ####
        #height_scrollAreaWidgetContents = self.resize_scrollAreaWidgetContents()
        ##################
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 551, 300)) # Нужно будет прописать функцию которая меняет геометрию в зависимости от количества объектов, минимальное 300, когда больше 3 объектов тогда + высота объекта (90) + 10
        
        self.scrollAreaWidgetContents.setLayoutDirection(Qt.LeftToRight)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(9, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        # Отрисовка кнопки "Save"
        self.bt_Save_Changes = QPushButton(self)
        self.bt_Save_Changes.setGeometry(QRect(10, 3, 100, 30))
        font = QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.bt_Save_Changes.setFont(font)
        self.bt_Save_Changes.setToolTip("")
        
        self.bt_Save_Changes.setStyleSheet("color:green")
        self.bt_Save_Changes.setObjectName("bt_Save_Changes")
        self.bt_Save_Changes.clicked.connect(self.save) # Приязка функции на клик по кнопке
        
        
        
    def add_notification(self): 
    # Эта функция добавляет в ScrollArea блоки с уведомлениями, здесь идет отрисовка блока и его дочерниз элементов
        
        
        
        global I_COUNT ########### Глобальный счетчик для придания всем блокам и их элементам уникальных имен
        
        # Отрисовка самого блока (фрейма) 
        # Frame внутри которого будут размещатся остальные элементы
        self.Notification = QFrame(self.scrollAreaWidgetContents)
        self.Notification.setMinimumSize(QSize(530, 90))
        self.Notification.setMaximumSize(QSize(535, 90))
        self.Notification.setToolTip("")
        self.Notification.setFrameShape(QFrame.Box)
        self.Notification.setFrameShadow(QFrame.Raised)
        Notif = self.Notification # Переменная нужна для ссылки на этот фрейм перед тем как ему присвоится имя объекта
        self.Notification.setObjectName(f"Notification_{I_COUNT}") # Присваивание уникального имени объекта
        
        #Отрисовка дочерних элементов 
        
        #Текстовое поле (Line Edit) в которое вводится процент заряда при котором будет выводится уведомления
        self.tb_Percent_Notification = QLineEdit(Notif) 
        self.tb_Percent_Notification.setGeometry(QRect(5, 20, 41, 31))
        font = QFont()
        font.setPointSize(14)
        self.tb_Percent_Notification.setFont(font)
        
        self.tb_Percent_Notification.setText('0')
        self.tb_Percent_Notification.setMaxLength(3) # Установка максимального количества вводимых символов
        validator = QIntValidator(self) # Ограничитель, в даном случае для ввода допустимы только числа
        self.tb_Percent_Notification.setValidator(validator) # Установка механизма допустимости в нужное поле
        ### Соединить из сохранениям
        #self.tb_Percent_Notification.editingFinished.connect(self.save_file)
        
        self.tb_Percent_Notification.editingFinished.connect(self.edit_percent_notification)
        self.tb_Percent_Notification.textChanged.connect(self.change_percent_notification) ############### Связь из функцией при каждом изменении текста
        self.tb_Percent_Notification.setObjectName(f"tb_Percent_Notification_{I_COUNT}") # Присваивание уникального имени объекта
        
        #Текстовое поле (Plain Text Edit) в которе текст уведомления котрый будет выводится в окно с уведомлениям
        self.tb_Message_Notification = QPlainTextEdit(Notif)
        self.tb_Message_Notification.setGeometry(QRect(50, 21, 360, 61))
        font = QFont()
        font.setPointSize(12)
        self.tb_Message_Notification.setFont(font)
        
        ### Соединить из сохранениям
        #self.tb_Message_Notification.textChanged.connect(self.edit_message_notification)
        
        #self.tb_Message_Notification.textChanged.connect(FUNCTION) ############### Связь из функцией при каждом изменении текста
        self.tb_Message_Notification.setObjectName(f"tb_Message_Notification_{I_COUNT}") # Присваивание уникального имени объекта
        
        #CheckBox (True значит что будет выводится окно с уведомлениям, False блокирует эту возможность
        self.chb_Text_Notification = QCheckBox(Notif)
        self.chb_Text_Notification.setGeometry(QRect(420, 20, 111, 21))
        font = QFont()
        font.setPointSize(12)
        self.chb_Text_Notification.setFont(font)
        
        self.chb_Text_Notification.setLayoutDirection(Qt.LeftToRight)
        self.chb_Text_Notification.setChecked(True)
        self.chb_Text_Notification.setObjectName(f"chb_Text_Notification_{I_COUNT}") # Присваивание уникального имени объекта
        
        #CheckBox (True значит что будет осуществлятся звуковое уведомления, False блокирует эту возможность 
        self.chb_Sound_Notification = QCheckBox(Notif)
        self.chb_Sound_Notification.setGeometry(QRect(420, 40, 111, 21))
        font = QFont()
        font.setPointSize(12)
        self.chb_Sound_Notification.setFont(font)
        
        self.chb_Sound_Notification.setLayoutDirection(Qt.LeftToRight)
        self.chb_Sound_Notification.setChecked(False)
        self.chb_Sound_Notification.stateChanged.connect(self.sound_check)
        self.chb_Sound_Notification.setObjectName(f"chb_Sound_Notification_{I_COUNT}") # Присваивание уникального имени объекта
        
        #ComboBox со списком доступных звуков уведомлений (при значении chb_Sound_Notification - False список перестает быть активным)
        self.cmb_Sounds_Notification = QComboBox(Notif)
        self.cmb_Sounds_Notification.setGeometry(QRect(420, 60, 111, 22))
        self.cmb_Sounds_Notification.setEnabled(False)
        self.cmb_Sounds_Notification.setSizeAdjustPolicy(self.cmb_Sounds_Notification.AdjustToMinimumContentsLength)
        
        
        
        
        font = QFont()
        font.setPointSize(10)
        #self.cmb_Sounds_Notification.setModel(sounds_model)
        self.cmb_Sounds_Notification.setFont(font)
        self.cmb_Sounds_Notification.setToolTip("")
        ### Соединить из сохранениям
        #self.cmb_Sounds_Notification.currentIndexChanged.connect(self.save_file)
        #self.cmb_Sounds_Notification.currentIndexChanged.connect(FUNCTION) ########## ############### Связь из функцией при каждом изменении выбранного элемента
        self.cmb_Sounds_Notification.setObjectName(f"cmb_Sounds_Notification_{I_COUNT}") # Присваивание уникального имени объекта
        # Добавление элементов в комбобокс 
        sounds = os.listdir(r"Sounds")
        for x in sounds:
            if x[-4:] == '.wav':
                self.cmb_Sounds_Notification.addItem (x)
        #self.cmb_Sounds_Notification.addItem("")
        #self.cmb_Sounds_Notification.addItem("")
        #self.cmb_Sounds_Notification.addItem("")
        
        #Label надпись "Процент"
        self.lb_Percent_Notification = QLabel(Notif)
        self.lb_Percent_Notification.setGeometry(QRect(5, 3, 71, 15))
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lb_Percent_Notification.setFont(font)
        self.lb_Percent_Notification.setToolTip("")
        self.lb_Percent_Notification.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_Percent_Notification.setObjectName(f"lb_Percent_Notification_{I_COUNT}") # Присваивание уникального имени объекта
        
        #Label надпись "Сообщение"
        self.lb_Message_Notification = QLabel(self.Notification)
        self.lb_Message_Notification.setGeometry(QRect(180, 3, 151, 15))
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lb_Message_Notification.setFont(font)
        self.lb_Message_Notification.setToolTip("")
        self.lb_Message_Notification.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_Message_Notification.setObjectName(f"lb_Message_Notification_{I_COUNT}") # Присваивание уникального имени объекта
        
        #Label надпись "Тип уведомления"
        self.lb_Type_Notification = QLabel(Notif)
        self.lb_Type_Notification.setGeometry(QRect(420, 3, 151, 15))
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lb_Type_Notification.setFont(font)
        self.lb_Type_Notification.setToolTip("")
        self.lb_Type_Notification.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_Type_Notification.setObjectName(f"lb_Type_Notification_{I_COUNT}") # Присваивание уникального имени объекта
        
        #PushButton который удаляет блок с уведомлением
        self.bt_Del_Notification = QPushButton(Notif)
        self.bt_Del_Notification.setGeometry(QRect(5, 55, 30, 30))
        font = QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        self.bt_Del_Notification.setFont(font)
        
        self.bt_Del_Notification.setText("–")
        self.bt_Del_Notification.setStyleSheet("color:red\n""")
        self.bt_Del_Notification.clicked.connect(self.resize_scrollAreaWidgetContents)
        #self.bt_Del_Notification.clicked.connect(self.del_notification) # Привязка функции на клик по кнопке
        self.bt_Del_Notification.setObjectName(f"bt_Del_Notification_{I_COUNT}") # Присваивание уникального имени объекта
        
        
        self.verticalLayout.addWidget(Notif) # Добавление в вертикальную сетку ScrollArea блока с уведомлениям 
        
        I_COUNT += 1 ###################  Добавления к счетчику 1, чтобы в будующем всем блокам и дочерним объектам присваивались уникальные имена
        self.translate_app_text()
        
        
    
    def del_notification(self):
    # Активируется при нажатии на bt_Del_Notification и удаляет родительский блок с уведомлениям
         
        button = self.sender() # Определяет источник сигнала
        parrent_object = button.parentWidget() # Опредления родительского объекта
        parrent_object.deleteLater() # Удаляет родительский объект
        
        #self.lb_Status_Bar.setStyleSheet("QLabel {color: green;}")
        
    def save (self):
        self.save_file(1)
        
    def save_file(self, set=1):
        ### Смысл функции сохранения следующий, определяется список всех дочерных объектов в ScrollArea, в них определяются блоки с уведомлениями которые добавил пользователь
        # эти блоки нужно сохранить, чтобы когда пользователь вновь откроет программу в ней были все добавлены им уведомления
        # программа идентифицирует все блоки, которые есть в ScrollArea и добавит подсписок блока список Notification_list, после идентифицируются дочерные элементы (блок затем дочерные элементы)
        # у некоторых дочерних элементов есть параметры которые нужно сохранить, они и будут добавлены в подсписок к материнскому блоку (фрейму)
        # после этого итоговый список Notification_list будет сохранен в файл. Конец функции
        
        if set == 1:
            Notification_list = [] #итоговый список параметров всех блоков
            
        
            settings = QSettings(CONFIG_FILE_NAME, QSettings.IniFormat)
            settings.setValue("Notification_list",Notification_list.copy())
            Notification_list = self.detect_notification()
            
            settings.setValue("Notification_list", Notification_list.copy())
            
            # сохранения комбобокса с языками
            mo = self.cmb_Languages.metaObject() 
            for k in range(mo.propertyCount()):  # пробегает по всех параметрах текущего объекта (combobox со списком доступнх звуков для уведомления)
                name = mo.property(k).name() # переменной присваивается названия параметра, который проходит в цикле
                if name == 'currentText': 
                    settings.setValue("Language",("{}/{}".format(self.cmb_Languages.objectName(), name), self.cmb_Languages.property(name)))
            
            message_translate = self.translate_app_text(2)
            self.status_bar_message(message_translate[0])
        if set == 2:
            settings = QSettings(CONFIG_FILE_NAME, QSettings.IniFormat)
            mo = self.cmb_Languages.metaObject() 
            for k in range(mo.propertyCount()):  # пробегает по всех параметрах текущего объекта (combobox со списком доступнх звуков для уведомления)
                name = mo.property(k).name() # переменной присваивается названия параметра, который проходит в цикле
                if name == 'currentText': 
                    settings.setValue("Language",("{}/{}".format(self.cmb_Languages.objectName(), name), self.cmb_Languages.property(name)))
            
            
             #Для очистки файла, он перезапишется в конце функции
            
        
        
        

        
        #Список всех дочерных объектов в ScrollArea, нужно для того, чтобы определить фреймы (блоки) уведомлений
    
    
    def detect_notification(self):
        global I_COUNT #Счетчик блоков (фреймов) с уведомлениями
        Notification_list = [] #итоговый список параметров всех блоков
        
        name_Notification = '' #имя блока, нужно для идентификации дочерних элементов каждого блока
        child_list = self.scrollArea.findChildren(QObject)
            
            
            # Цикл проходится по всем дочерним элементам
        for x in child_list:
            
                mo = x.metaObject() #Переменная нужна, чтобы записать параметры объекта - (mo.property())
                
                # Проверка имени объекта, идентифицируем блок с уведомлением - (Notification_X: type(QFrame))
                # Сначала будет определен блок с уведомлениями, а затем его дочерние элементы, и так прогонится каждый блок уведомлений
                
                #Идентификация среди списка дочерних объектов ScrollArea блоков (frame) уведомлений
                if len('Notification_ ') == len(x.objectName()) and 'Notification_' in x.objectName() or len('Notification_  ') == len(x.objectName()) and 'Notification_' in x.objectName(): 
                        Notification_list.append([x.objectName()])# добавляем в список параметров подсписок с блоком уведомлений
                        name_Notification = x.objectName() # имя блока уведомлений, нужен для идентификации его дочерних элементов (следующие if)
                        num_in_Notification_list = Notification_list.index(Notification_list[-1]) # возвращает индекс подспика блока уведомлений в общем списке параметров, нужен чтобы добавить в него параметры дочерних элементов
                        #print(f'num_in_Notification_list {num_in_Notification_list}')
                     
                if f'tb_Percent_{name_Notification}' == x.objectName(): #Идентификация среди списка дочерних объектов ScrollArea текстового поля со значениям заряда батареи
                        for k in range(mo.propertyCount()): # пробегает по всех параметрах текущего объекта (текстовое поле заряд батареи)
                            name = mo.property(k).name() # переменной присваивается названия параметра, который проходит в цикле
                            if name == 'text': # Проверка на нужное имя параметра, конкретно этот параметр возвращает текст, который был введен в это поле пользователем
                                Notification_list[num_in_Notification_list].append(("{}/{}".format(x.objectName(), name), x.property(name))) # Добавляет значения текста поля заряда батареи в подсписок текущего блока уведомлений
                
                if f'tb_Message_{name_Notification}' == x.objectName(): #Идентификация среди списка дочерних объектов ScrollArea текстового поля со значениям текста уведомления
                        for k in range(mo.propertyCount()): # пробегает по всех параметрах текущего объекта (текстовое поле текст уведомления)
                            name = mo.property(k).name() # переменной присваивается названия параметра, который проходит в цикле
                            if name == 'plainText': # Проверка на нужное имя параметра, конкретно этот параметр возвращает текст, который был введен в это поле пользователем
                                Notification_list[num_in_Notification_list].append(("{}/{}".format(x.objectName(), name), x.property(name))) # Добавляет значения текста поля уведомления в подсписок текущего блока уведомлений
                
                if f'chb_Text_{name_Notification}' == x.objectName(): #Идентификация среди списка дочерних объектов ScrollArea checkbox который определяет вызов окна уведомления из сообщениям
                        for k in range(mo.propertyCount()):  # пробегает по всех параметрах текущего объекта (checkbox который определяет вызов окна уведомления из сообщениям)
                            name = mo.property(k).name() # переменной присваивается названия параметра, который проходит в цикле
                            if name == 'checked': # Проверка на нужное имя параметра, конкретно этот параметр возвращает значения checkbox выбраного пользователем
                                Notification_list[num_in_Notification_list].append(("{}/{}".format(x.objectName(), name), x.property(name)))   # Добавляет значения чекбокса текстового окна в подсписок текущего блока уведомлений
                
                if f'chb_Sound_{name_Notification}' == x.objectName(): #Идентификация среди списка дочерних объектов ScrollArea checkbox который определяет вызов звукового уведомления
                        for k in range(mo.propertyCount()): # пробегает по всех параметрах текущего объекта (checkbox который определяет вызов звукового уведомления)
                            name = mo.property(k).name() # переменной присваивается названия параметра, который проходит в цикле
                            if name == 'checked': # Проверка на нужное имя параметра, конкретно этот параметр возвращает значения checkbox выбраного пользователем
                                Notification_list[num_in_Notification_list].append(("{}/{}".format(x.objectName(), name), x.property(name)))  # Добавляет значения чекбокса звукового уведомления в подсписок текущего блока уведомлений         
                
                if f'cmb_Sounds_{name_Notification}' == x.objectName(): #Идентификация среди списка дочерних объектов ScrollArea combobox со списком доступнх звуков для уведомления
                        for k in range(mo.propertyCount()):  # пробегает по всех параметрах текущего объекта (combobox со списком доступнх звуков для уведомления)
                            name = mo.property(k).name() # переменной присваивается названия параметра, который проходит в цикле
                            if name == 'currentText': # Проверка на нужное имя параметра, конкретно этот параметр возвращает значения выбранного элемента в combobox
                                Notification_list[num_in_Notification_list].append(("{}/{}".format(x.objectName(), name), x.property(name))) # Добавляет значения combobox со списком доступнх звуков  в подсписок текущего блока уведомлений      
            #print (Notification_list)
            #print(f'LEN ISv{len(child_list)}')
        return Notification_list
            
            #print(settings.value("Notification_list")) # Просмотр формата вывода параметров
                








    def load_file(self): # Функция загрузки, запускается автоматически в конструкторе __init__
        
        global I_COUNT
        
        settings = QSettings(CONFIG_FILE_NAME, QSettings.IniFormat) 
        
        #Дописать сюда загрузку значения комбобокса с языками
        Language_property = settings.value("Language")
        if Language_property is None: # Возвращает 0 если файл пустой
            return 0
        if Language_property:
            self.cmb_Languages.setCurrentText(Language_property[1])
            
        #Достает из файла значения со списком блоков уведомлений и восстанавливает их в окне
        Load_Notification_list = settings.value("Notification_list") # Возвращает список с блоками уведомлений и их параметрами из файла
        if Load_Notification_list is None: # Возвращает 0 если файл пустой
            return 0
        
        if Load_Notification_list:
            for notification in Load_Notification_list: # Проход по всех подсписках с блоками (каждый подсписок соотвествует блоку уведомлений)
                
                I_COUNT = Load_Notification_list.index(notification) # Присвивает глобальному счетчику значения индекса подсписка с блоком уведомлений, счетчик нужен для функции добавления блоков, благодаря ему именуются эти блоки
                self.add_notification() #Запускает функцию добавления элемента
                # Текстовое поле с зарядом батареии
                Percent_Notification = notification[1] # Присваивает индекс кортежа с именем объекта и её параметром
                tb_Percent_Notification_TEXT = Percent_Notification[1] # Присвоение переменной значения параметра
                self.tb_Percent_Notification.setText(tb_Percent_Notification_TEXT) # Присвоение объекту значения параметра переданого из файла с сохранением
                # Текстовое поле с сообщениям для уведомления
                Message_Notification = notification[2] # Присваивает индекс кортежа с именем объекта и её параметром
                tb_Message_Notification_TEXT = Message_Notification[1] # Присвоение переменной значения параметра
                self.tb_Message_Notification.setPlainText(tb_Message_Notification_TEXT) # Присвоение объекту значения параметра переданого из файла с сохранением
                # Checkbox для определения нужды в  выводе окна с сообщениям
                Text_Notification = notification[3] # Присваивает индекс кортежа с именем объекта и её параметром
                chb_Text_Notification_CHECKED = bool(Text_Notification[1]) # Присвоение переменной значения параметра
                self.chb_Text_Notification.setChecked(chb_Text_Notification_CHECKED) # Присвоение объекту значения параметра переданого из файла с сохранением
                # Checkbox для определения нужды в звуковом уведолмении
                Sound_Notification = notification[4] # Присваивает индекс кортежа с именем объекта и её параметром
                chb_Sound_Notification_CHECKED = bool(Sound_Notification[1]) # Присвоение переменной значения параметра
                self.chb_Sound_Notification.setChecked(chb_Sound_Notification_CHECKED) # Присвоение объекту значения параметра переданого из файла с сохранением
                # ComboBox со списком доступных звуков
                Sounds_Notification = notification[5] # Присваивает индекс кортежа с именем объекта и её параметром
                cmb_Sounds_Notification_CURRENT_TEXT = Sounds_Notification[1] # Присвоение переменной значения параметра
                self.cmb_Sounds_Notification.setCurrentText(cmb_Sounds_Notification_CURRENT_TEXT) # Присвоение объекту значения параметра переданого из файла с сохранением
            
        self.resize_scrollAreaWidgetContents()        
                
                
           

    def edit_percent_notification(self):
        percent_sender = self.sender()
        Percent_Notification = percent_sender.text()
        if int(Percent_Notification) >= 101:
            msg_translate = self.translate_app_text(7)
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText(msg_translate[0]) #########TRANSLATE
            msg.setEscapeButton(QMessageBox.Ok)
            msg.setWindowTitle(msg_translate[1])
            retval = msg.exec_()
            percent_sender.setText('0')
            
        else: percent_sender.setText(str(int(Percent_Notification)))
    
    
    def change_percent_notification(self):
        percent_sender = self.sender()
        Percent_Notification = percent_sender.text()
        if not Percent_Notification.isalnum():
            percent_sender.setText('0')
        
        
            
    def resize_scrollAreaWidgetContents(self):
        global I_COUNT
        button_sender = self.sender()
        #Notification_list = self.detect_notification()
        
        if I_COUNT == 0:
            self.height_scrollAreaWidgetContents = 0
            
        if button_sender is None: 
            self.height_scrollAreaWidgetContents = I_COUNT * 100
            self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 551, self.height_scrollAreaWidgetContents))
            return self.height_scrollAreaWidgetContents
            
            
        if 'bt_Add_Notification' in button_sender.objectName():
            Notification_list = self.detect_notification()
            self.height_scrollAreaWidgetContents = self.height_scrollAreaWidgetContents + 100
            self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 551, self.height_scrollAreaWidgetContents))
            self.add_notification()
            #Notification_list = self.detect_notification()
            message_translate = self.translate_app_text(2)
            self.status_bar_message(message_translate[1])###############################################TRANSLATE
            
        if 'bt_Del_Notification' in button_sender.objectName():
            Notification_list = self.detect_notification()
            self.height_scrollAreaWidgetContents = self.height_scrollAreaWidgetContents - 100
            self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 551, self.height_scrollAreaWidgetContents))
            self.del_notification()
            #Notification_list = self.detect_notification()
            message_translate = self.translate_app_text(2)
            self.status_bar_message(message_translate[2]) ###############################################TRANSLATE
            
        
        return self.height_scrollAreaWidgetContents
        
     
    def sound_check(self):
        checkbox = self.sender()
        notification_frame = checkbox.parentWidget ()
        cmb_child = notification_frame.findChildren(QComboBox)
        cmb_sound = cmb_child[0]
        
        if checkbox.isChecked():
            cmb_sound.setEnabled(True)
        if not checkbox.isChecked():
            cmb_sound.setEnabled(False)
            
    
    def status_bar_message (self, message = ''):
        font = QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lb_Status_Bar.setFont(font)
        self.lb_Status_Bar.setText(message) ###############################################TRANSLATE
        self.lb_Status_Bar.setStyleSheet("QLabel {color: green;}")
        self.timer = QTimer() # 
        self.timer.start(5000) #
        self.timer.timeout.connect(self.clear_message) #
        
    def clear_message (self):
        self.lb_Status_Bar.setText('')
        self.timer = QTimer() #
        self.timer.stop() #

    def translate_app_text(self, set=1):
        Notification_list = self.detect_notification()
        
        # Translate UI MainWindow
        if set == 1:
            
            if self.cmb_Languages.currentText() == 'Українська':
                self.setWindowTitle("Notebook / Laptop Battery Notification")
                self.lb_Percent.setText("Заряд:")
                self.lb_Power.setText("Живлення:")
                self.lb_Left_Sec.setText("Залишилось:")
                self.bt_Add_Notification.setText( "+")
                self.bt_Help.setText("Довідка")
                self.bt_Settings.setText("Налаштування")
                self.lb_Language.setText("Мова")
                self.bt_Save_Changes.setText('Зберегти')
                self.lb_Notifications.setText("Центр сповіщень")
                percent_notification_text = "Відсоток"
                message_notification_text = "Повідомлення"
                type_notification_text = "Тип сповіщення"
                chb_text_notification_text = 'Текст'
                chb_sound_notification_text = 'Звук'
                self.bt_Add_Notification.setToolTip('Натисніть на кнопку, щоб додати нове сповіщення')
                
            if self.cmb_Languages.currentText() == 'Русский':    
                self.setWindowTitle("Notebook / Laptop Battery Notification")
                self.lb_Percent.setText("Заряд:")
                self.lb_Power.setText("Питание:")
                self.lb_Left_Sec.setText("Осталось:")
                self.bt_Add_Notification.setText("+")
                self.bt_Help.setText("Справка")
                self.bt_Settings.setText("Настройки")
                self.lb_Language.setText("Язык")
                self.bt_Save_Changes.setText('Сохранить')
                self.lb_Notifications.setText("Центр уведомлений")
                percent_notification_text = "Процент"
                message_notification_text = "Сообщение"
                type_notification_text = "Тип уведомления"
                chb_text_notification_text = 'Текст'
                chb_sound_notification_text = 'Звук'
                self.bt_Add_Notification.setToolTip('Нажмите на данную кнопку, чтобы добавить новое уведомление')
                
            if self.cmb_Languages.currentText() == 'English':    
                self.setWindowTitle("Notebook / Laptop Battery Notification")
                self.lb_Percent.setText("Level:")
                self.lb_Power.setText("Power:")
                self.lb_Left_Sec.setText("Remaining Time:")
                self.bt_Add_Notification.setText("+")
                self.bt_Help.setText("Help")
                self.bt_Settings.setText("Settings")
                self.lb_Language.setText("Language")
                self.bt_Save_Changes.setText('Save')
                self.lb_Notifications.setText("Notification center")
                percent_notification_text = "Percent"
                message_notification_text = "Message"
                type_notification_text = "Type notification"
                chb_text_notification_text = 'Text'
                chb_sound_notification_text = 'Sound'
                self.bt_Add_Notification.setToolTip('Click on this button for add new notification')
                
                
            
            name_Notification = '' #имя блока, нужно для идентификации дочерних элементов каждого блока
            child_list = self.scrollArea.findChildren(QObject)
            tool_tip_translate = self.translate_app_text(5)
            # Цикл проходится по всем дочерним элементам
            for x in child_list:
            
                if len('Notification_ ') == len(x.objectName()) and 'Notification_' in x.objectName() or len('Notification_  ') == len(x.objectName()) and 'Notification_' in x.objectName(): #Идентификация среди списка дочерних объектов ScrollArea блоков (frame) уведомлений
                        name_Notification = x.objectName() # имя блока уведомлений, нужен для идентификации его дочерних элементов (следующие if)
                
                if f'lb_Message_{name_Notification}' == x.objectName(): 
                        x.setText(message_notification_text)
                
                if f'tb_Message_{name_Notification}' == x.objectName(): 
                        x.setToolTip(tool_tip_translate[1])
                
                if f'lb_Percent_{name_Notification}' == x.objectName(): 
                        x.setText(percent_notification_text)
                
                if f'tb_Percent_{name_Notification}' == x.objectName(): 
                        x.setToolTip(tool_tip_translate[2])
                
                if f'lb_Type_{name_Notification}' == x.objectName(): 
                        x.setText(type_notification_text)
                        
                
                if f'chb_Text_{name_Notification}' == x.objectName(): 
                        x.setText(chb_text_notification_text)
                        x.setToolTip(tool_tip_translate[4])
                
                if f'chb_Sound_{name_Notification}' == x.objectName(): 
                        x.setText(chb_sound_notification_text)
                        x.setToolTip(tool_tip_translate[3])
                if f'bt_Del_{name_Notification}' == x.objectName(): 
                        x.setToolTip(tool_tip_translate[0])
             
        
        # Translate status bar
        if set == 2:   
            if self.cmb_Languages.currentText() == 'Українська':
                save_message = ('Зміни успішно збережено')
                add_notification_message = (f'Сповіщення успішно додано, всього: {len(Notification_list)}')
                del_notification_message = (f'Сповіщення видалено, всього залишилось: {len(Notification_list)-1}')
                return save_message, add_notification_message, del_notification_message
            
            if self.cmb_Languages.currentText() == 'Русский': 
                save_message = ('Изменения успешно сохранены')
                add_notification_message = (f'Уведомление успешно добавлено, всего: {len(Notification_list)}')
                del_notification_message = (f'Уведомление успешно удалено, всего: {len(Notification_list)-1}')
                return save_message, add_notification_message, del_notification_message
            
            if self.cmb_Languages.currentText() == 'English': 
                save_message = ('Ghanges has been saved')
                add_notification_message = (f'Notification succesfully added, count: {len(Notification_list)}')
                del_notification_message = (f'Notification succesfully deleted, count: {len(Notification_list)-1}')
                return save_message, add_notification_message, del_notification_message
        
        # translate Battery information
        if set == 3:
            if self.cmb_Languages.currentText() == 'Українська':
                plugged_text = 'Підключено '
                unplugged_text = 'Не підключено '
                unknown_plugged_text = 'Не визначено '
                determing_text = 'Визначається '
                сharging_text = 'Заряджається '
                unknown_сharging_text = 'Не визначено '
                message_notification_Title = 'Сповіщення'
            
            if self.cmb_Languages.currentText() == 'Русский': 
                plugged_text = 'Подключено '
                unplugged_text = 'Не подключено '
                unknown_plugged_text = 'Не определено '
                determing_text = 'Определяется '
                сharging_text = 'Заряжается '
                unknown_сharging_text = 'Не определено '
                message_notification_Title = 'Уведомление'
            
            if self.cmb_Languages.currentText() == 'English':   
                plugged_text = 'Plugged '
                unplugged_text = 'Unplugged '
                unknown_plugged_text = 'Undefined '
                determing_text = 'Determining '
                сharging_text = 'Charging '
                unknown_сharging_text = 'Undefined '
                message_notification_Title = 'Notification'
            return plugged_text, unplugged_text, unknown_plugged_text, determing_text, сharging_text, unknown_сharging_text, message_notification_Title
        
        # Translate exit maessagebox
        if set == 4:
            if self.cmb_Languages.currentText() == 'Українська':
                exit_message_text = 'Всі незбережені дані буде втрачено, Ви впевнені, що хочете закрити програму?'
                button_Yes_text = 'Так'
                button_No_text = 'Ні'
                button_Tray_text = 'Згорнути у трей'
                exit_message_Title = 'Вихід'
            
            if self.cmb_Languages.currentText() == 'Русский':
                exit_message_text = 'Все несохраненные данные будут потеряны, Вы уверены, что хотите закрыть программу?'
                button_Yes_text = 'Да'
                button_No_text = 'Нет'
                button_Tray_text = 'Свернуть в трей'
                exit_message_Title = 'Выход'
            
            if self.cmb_Languages.currentText() == 'English': 
                exit_message_text = 'All unsaved data will be lost. Are you sure you want to close the application?'
                button_Yes_text = 'Yes'
                button_No_text = 'No'
                button_Tray_text = 'Minimize to tray'
                exit_message_Title = 'Exit'
            return exit_message_text, button_Yes_text, button_No_text, button_Tray_text, exit_message_Title
        
        # Translate Tool Tips
        if set == 5:
            if self.cmb_Languages.currentText() == 'Українська':
                #ToolTip_bt_Add_Notification = 'Натисніть на кнопку, щоб додати нове сповіщення'
                ToolTip_bt_Del_Notification = 'Натисніть на кнопку, щоб видалити поточне сповіщення'
                ToolTip_tb_Message_Notification = 'Запишіть сюди текст для сповіщення'
                ToolTip_tb_Percent_Notification = 'Запишіть сюди заряд батареї, при якому сповіщення буде показано'
                ToolTip_chb_Sound_Notification = 'Натисніть на цей прапірець, якщо хочете ввімкнути / вимкнути звукові сповіщення'
                ToolTip_chb_Text_Notification = 'Натисніть на цей прапірець, якщо хочете ввімкнути / вимкнути текстові сповіщення'
                
            if self.cmb_Languages.currentText() == 'Русский':
                #ToolTip_bt_Add_Notification = 'Нажмите на данную кнопку, чтобы добавить новое уведомление'
                ToolTip_bt_Del_Notification = 'Нажмите на данную кнопку, чтобы удалить текущее уведомление'
                ToolTip_tb_Message_Notification = 'Запишите сюда текст для уведомления'
                ToolTip_tb_Percent_Notification = 'Запишите сюда заряд батареи при котором, уведомления будет показано'
                ToolTip_chb_Sound_Notification = 'Нажмите на этот флажок, если хотите включить / выключить звуковые уведомления'
                ToolTip_chb_Text_Notification = 'Нажмите на этот флажок, если хотите включить / выключить текстовые уведомления'
            
            if self.cmb_Languages.currentText() == 'English': 
                #ToolTip_bt_Add_Notification = 'Click on this button for add new notification'
                
                ToolTip_bt_Del_Notification = 'Click on this button for delete this notification'
                ToolTip_tb_Message_Notification = 'Write down your notification message'
                ToolTip_tb_Percent_Notification = 'Write down percent battery when notification will be show'
                ToolTip_chb_Sound_Notification = 'Click on this checkbox if you wanna turn on / turn off sound notification'
                ToolTip_chb_Text_Notification = 'Click on this checkbox if you wanna turn on / turn off text notification'
            
            return ToolTip_bt_Del_Notification, ToolTip_tb_Message_Notification, ToolTip_tb_Percent_Notification, ToolTip_chb_Sound_Notification, ToolTip_chb_Text_Notification
        
        # Tray ContextMenu
        if set == 6:
        
            if self.cmb_Languages.currentText() == 'Українська':
                show_action_text = "Показати"
                settings_action_text = "Налаштування"
                help_action_text = "Довідка"
                quit_action_text = "Вихід"
                hide_action_text = "Приховати"
                showMessage_Title = 'Notebook / Laptop Battery Notification'
                showMessage_text = 'Програма була згорнута до системного трею'
                
            if self.cmb_Languages.currentText() == 'Русский':
                show_action_text = "Показать"
                settings_action_text = "Настройки"
                help_action_text = "Справка"
                quit_action_text = "Выход"
                hide_action_text = "Скрыть"
                showMessage_Title = 'Notebook / Laptop Battery Notification'
                showMessage_text = 'Программа была свернута в системный трей'
                
            if self.cmb_Languages.currentText() == 'English': 
                show_action_text = "Show"
                settings_action_text = "Settings"
                help_action_text = "Help"
                quit_action_text = "Exit"
                hide_action_text = "Hide"
                showMessage_Title = 'Notebook / Laptop Battery Notification'
                showMessage_text = 'Application was minimized to Tray'
            
            return show_action_text, settings_action_text, help_action_text, quit_action_text, hide_action_text, showMessage_Title, showMessage_text
        
        # Greater percent
        if set == 7:
        
            if self.cmb_Languages.currentText() == 'Українська':
                message = 'Введене число більше 100, будь-ласка введіть число в діапазоні від 0 до 100!'
                title = 'Попередження!'
                
            if self.cmb_Languages.currentText() == 'Русский':
                message = 'Введенное число больше 100, пожалуйста введите число в диапазоне от 0 до 100!'
                title = ''
                
            if self.cmb_Languages.currentText() == 'English': 
                message = 'The entered number is greater than 100, please enter a number between 0 and 100'
                title = 'Warning'
                
            return message, title   
                
###########################MESSAGEBOX#########################################
            #msg = QMessageBox(self)
            #msg.setIcon(QMessageBox.Information)
            #msg.setText("This is a message box")
            #msg.setInformativeText("This is addi")
            #msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            #msg.setWindowTitle("MessageBox demo")
            #retval = msg.exec_()
    def language_text(self):
        self.translate_app_text(1)
        self.save_file(2)
        
        
    
    
    def secs2hours(self,secs):
        mm, ss = divmod(secs, 60)
        hh, mm = divmod(mm, 60)
        return "%d:%02d:%02d" % (hh, mm, ss)
    
    def battery_information(self):
            BATTERY_PROPERTIES = psutil.sensors_battery()
            battery_translate = self.translate_app_text(3)
            self.BatteryBar.setProperty("value",BATTERY_PROPERTIES.percent)###########################################################################################################
            self.lb_Percent_value.setText(f'{BATTERY_PROPERTIES.percent} % ')
            sec_left = str(BATTERY_PROPERTIES.secsleft)
            #self.lb_Power_value.
            
            if BATTERY_PROPERTIES.power_plugged:
                self.lb_Power_value.setText(battery_translate[0]) #################### TRANSLATE? оставлять всегда с пробелом, чтобы буквы не обрезало
            elif not BATTERY_PROPERTIES.power_plugged:
                self.lb_Power_value.setText(battery_translate[1]) 
            elif BATTERY_PROPERTIES.power_plugged is None:
                self.lb_Power_value.setText(battery_translate[2])
            if sec_left.isdigit(): 
                sec_left = f'{self.secs2hours(BATTERY_PROPERTIES.secsleft)} '
                hh, mm, ss = sec_left.split(':')
                if len(hh) >2:
                    self.lb_Left_Sec_value.setText(battery_translate[3]) #################### TRANSLATE
                else:
                    self.lb_Left_Sec_value.setText(f'{self.secs2hours(BATTERY_PROPERTIES.secsleft)} ')
            
            elif BATTERY_PROPERTIES.secsleft == psutil.POWER_TIME_UNLIMITED:
                self.lb_Left_Sec_value.setText(battery_translate[4])
            elif BATTERY_PROPERTIES.secsleft == psutil.POWER_TIME_UNKNOWN:
                self.lb_Left_Sec_value.setText(battery_translate[5])
            
            
            global Object_Notification_list
           
            name_Notification = '' #имя блока, нужно для идентификации дочерних элементов каждого блока
            child_list = self.scrollArea.findChildren(QObject)
            
            # Цикл проходится по всем дочерним элементам
            for x in child_list:
                
                mo = x.metaObject() 
                if len('Notification_ ') == len(x.objectName()) and 'Notification_' in x.objectName() or len('Notification_  ') == len(x.objectName()) and 'Notification_' in x.objectName(): #Идентификация среди списка дочерних объектов ScrollArea блоков (frame) уведомлений
                        name_Notification = x.objectName() # имя блока уведомлений, нужен для идентификации его дочерних элементов (следующие if)
                        k, num = name_Notification.split('_')
                        num_in_Object_Notification_list = int(num)
                        if len(Object_Notification_list) == 0:
                            Object_Notification_list.append([x.objectName()]) 
                           # print('asdasdas')
                        elif num_in_Object_Notification_list == len(Object_Notification_list):
                            #print('sssss')
                            Object_Notification_list.append([x.objectName()]) 
                            
                        #print(num_in_Object_Notification_list)   
                        #print(len(Object_Notification_list))                      
                
                 ######################################### ВАЖНО!!!!!!!!!!!
                ######################################### В будущем можна упросить весь алгоритм, определяя только уведомления и записывая состояния уведомления, то же и касается сохранений и загрузок
                ########################################### например определить список уведомлений ,а потом при помощни переменных с именем блока уведомлений идентифицировать их дочерние объекты, например
                
                ######################################    name_text_check = f'chb_Text_{Notification_1}'  # имя объекта который будем искать
                ######################################    text_check = self.findChild(QCheckBox, name_text_check)  # присваиваем переменной объект
                
                ############################################# и вместо цикла по всем свойствам metaObject можна просто будет использовать методы, например self.text(), self.isChecked() или т.п. 
                ########################################
                
                if f'tb_Message_{name_Notification}' == x.objectName(): 
                    
                    if len(Object_Notification_list[num_in_Object_Notification_list]) == 5: #Длина списка в пять элементов это: название (номер) блока уведомления, текст заряда батареи уведомления, состояние уведомления
                                                                                          # (отключено ждет нужного заряда, включено запуск уведомления, ждет срединное состояние когда уведомление сработало но заряд пока остается тот же перейдет в состояния выключено после смены заряда батареи)
                        for k in range(mo.propertyCount()): # пробегает по всех параметрах текущего объекта 
                                name = mo.property(k).name() # переменной присваивается названия параметра, который проходит в цикле
                                if name == 'plainText': # Проверка на нужное имя параметра, конкретно этот параметр возвращает текст, который был введен в это поле пользователем
                                    Object_Notification_list[num_in_Object_Notification_list][4] = x.property(name)
                    else:
                         
                        for k in range(mo.propertyCount()): # пробегает по всех параметрах текущего объекта (текстовое поле заряд батареи)
                                name = mo.property(k).name() # переменной присваивается названия параметра, который проходит в цикле
                                if name == 'plainText': # Проверка на нужное имя параметра, конкретно этот параметр возвращает текст, который был введен в это поле пользователем
                                    Object_Notification_list[num_in_Object_Notification_list].append(x.property(name))
                                    
                if f'tb_Percent_{name_Notification}' == x.objectName(): 
                    
                    if len(Object_Notification_list[num_in_Object_Notification_list]) == 5: #Сравнение с количеством элементов в панели одного уведопления
                            
                            for k in range(mo.propertyCount()): # пробегает по всех параметрах текущего объекта (текстовое поле заряд батареи)
                               name = mo.property(k).name() # переменной присваивается названия параметра, который проходит в цикле
                               if name == 'text': # Проверка на нужное имя параметра, конкретно этот параметр возвращает текст, который был введен в это поле пользователем
                                    Object_Notification_list[num_in_Object_Notification_list][1] =(x.property(name))
                               if x.property(name) == str(BATTERY_PROPERTIES.percent) and Object_Notification_list[num_in_Object_Notification_list][2] == 'off':
                                        Object_Notification_list[num_in_Object_Notification_list][2] = 'on'
                                        Object_Notification_list[num_in_Object_Notification_list][3] = x.property(name)
                                   #     print(f'{Object_Notification_list[num_in_Object_Notification_list][0]} message_on')
                               
                               elif str(BATTERY_PROPERTIES.percent) != Object_Notification_list[num_in_Object_Notification_list][3] and Object_Notification_list[num_in_Object_Notification_list][2] == 'waiting':
                                        Object_Notification_list[num_in_Object_Notification_list][2] = 'off'
                                        Object_Notification_list[num_in_Object_Notification_list][3] = x.property(name)
                                       # print(f'{Object_Notification_list[num_in_Object_Notification_list][0]} message_off')
                               
                               
                    else:   
                        for k in range(mo.propertyCount()): # Эта часть запускается в начале запуска програмы, то есть первый проход после запуска, нужен для того, чтобы определить состояния блоков уведомлений
                                                             #если заряд в уведомлении соответствует заряду батареии добавляеться нужное состояние и идет вывод уведомления
                                                              # если заряд в уведомлении не соответствует заряду батареии добавляется в список нужное состояние 
                               name = mo.property(k).name() 
                               if name == 'text': 
                                    Object_Notification_list[num_in_Object_Notification_list].append(x.property(name))
                                    if x.property(name) != str(BATTERY_PROPERTIES.percent): #and len(Object_Notification_list[num_in_Object_Notification_list]) == 2:
                                        Object_Notification_list[num_in_Object_Notification_list].append('off')
                                        Object_Notification_list[num_in_Object_Notification_list].append(x.property(name))
                                    if x.property(name) == str(BATTERY_PROPERTIES.percent): #and len(Object_Notification_list[num_in_Object_Notification_list]) == 2:
                                        Object_Notification_list[num_in_Object_Notification_list].append('on')
                                        Object_Notification_list[num_in_Object_Notification_list].append(x.property(name))
                                           
                
                    
            
                
              
            for x in Object_Notification_list:
                
                if x[1] == str(BATTERY_PROPERTIES.percent) and x[2] == 'on':
                    x[2] = 'waiting'
                    
                    name_text_check = f'chb_Text_{x[0]}'
                    text_check = self.findChild(QCheckBox, name_text_check)
                    name_sound_check = f'chb_Sound_{x[0]}'
                    sound_check = self.findChild(QCheckBox, name_sound_check)
                    name_sound_combobox = f'cmb_Sounds_{x[0]}'
                    sound_combobox = self.findChild(QComboBox, name_sound_combobox)
                    if sound_check.isChecked():
                        name_sound_file = sound_combobox.currentText()
                        path_to_sound_file = 'Sounds'
                        playsound(f'{path_to_sound_file}\{name_sound_file}')
                    if text_check.isChecked():
                        msg = QMessageBox(self)
                        msg.setIcon(QMessageBox.Information)
                        msg.setText(x[-1])
                        #msg.setInformativeText("This is addi")
                        msg.setStandardButtons(QMessageBox.Ok)# | QMessageBox.Cancel)
                        msg.setWindowTitle(battery_translate[6])
                        retval = msg.exec_()
                    
                        
                
    def closeEvent(self, event):
        #reply = QMessageBox.question(self, 'Message',
            #"Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)
        global TRAY_ICON_EXIST
        exit_message_translate = self.translate_app_text(4)
        reply = QMessageBox()
        reply.setWindowIcon(QIcon('icon.png'))
        font = QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        reply.setWindowTitle(exit_message_translate[4])
        reply.setText(exit_message_translate[0])
        reply.setFont(font)
        reply.setIcon(QMessageBox.Information)
        reply.setStandardButtons(QMessageBox.Yes|QMessageBox.Cancel|QMessageBox.No)
        buttonYes = reply.button(QMessageBox.Yes)
        buttonYes.setText(exit_message_translate[1])
        buttonNo = reply.button(QMessageBox.No)
        buttonNo.setText(exit_message_translate[2])
        buttonTray = reply.button(QMessageBox.Cancel)
        buttonTray.setText(exit_message_translate[3])
        retval = reply.exec_()
        if reply.clickedButton() == buttonYes:
            event.accept()
        elif reply.clickedButton() == buttonNo: 
            event.ignore()
        elif reply.clickedButton() == buttonTray: 
            event.ignore()
            if TRAY_ICON_EXIST:
                print('true')
                self.tray_icon.setParent(None)
                tray_menu_translate = self.translate_app_text(6)
                self.tray_icon = QSystemTrayIcon(QIcon('icon.png'),self)
                #self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
                show_action = QAction(tray_menu_translate[0], self)
                settings_action = QAction(tray_menu_translate[1], self)
                help_action = QAction(tray_menu_translate[2], self)
                quit_action = QAction(tray_menu_translate[3], self)
                hide_action = QAction(tray_menu_translate[4], self)
                show_action.triggered.connect(self.show)
                settings_action.triggered.connect(self.show_settings_window)
                help_action.triggered.connect(self.show_help_window)
                hide_action.triggered.connect(self.hide)
                quit_action.triggered.connect(qApp.quit)
                tray_menu = QMenu()
                tray_menu.addAction(show_action)
                tray_menu.addAction(hide_action)
                tray_menu.addAction(settings_action)
                tray_menu.addAction(help_action)
                tray_menu.addAction(quit_action)
                
                self.tray_icon.setContextMenu(tray_menu)
                self.tray_icon.show()
                self.hide()
                self.tray_icon.showMessage(
                   tray_menu_translate[5],
                   tray_menu_translate[6],
                    QIcon('icon.png'),
                    2000)
            elif TRAY_ICON_EXIST == False:
                tray_menu_translate = self.translate_app_text(6)
                self.tray_icon = QSystemTrayIcon(QIcon('icon.png'),self)
                #self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
                show_action = QAction(tray_menu_translate[0], self)
                settings_action = QAction(tray_menu_translate[1], self)
                help_action = QAction(tray_menu_translate[2], self)
                quit_action = QAction(tray_menu_translate[3], self)
                hide_action = QAction(tray_menu_translate[4], self)
                show_action.triggered.connect(self.show)
                settings_action.triggered.connect(self.show_settings_window)
                help_action.triggered.connect(self.show_help_window)
                hide_action.triggered.connect(self.hide)
                quit_action.triggered.connect(qApp.quit)
                tray_menu = QMenu()
                tray_menu.addAction(show_action)
                tray_menu.addAction(hide_action)
                tray_menu.addAction(settings_action)
                tray_menu.addAction(help_action)
                tray_menu.addAction(quit_action)
                
                self.tray_icon.setContextMenu(tray_menu)
                self.tray_icon.show()
                self.hide()
                self.tray_icon.showMessage(
                   tray_menu_translate[5],
                   tray_menu_translate[6],
                    QIcon('icon.png'),
                    2000)
                TRAY_ICON_EXIST = True
            
    def show_settings_window(self):
        self.settings_ui = BatteryNotification_SettingsWindow.Settings_Window()
        
    def show_help_window(self):
        self.settings_ui = BatteryNotification_HelpWindow.Help_Window()
        
        







        
                        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    timer = QTimer()
    timer.timeout.connect(ui.battery_information)
    timer.start(1000)
    sys.exit(app.exec_())
    
    
    
    
        
        
    
        