import sys
import sqlite3
import insurance
from polic import Polic_form
from show_agent import Show_agent
from new_service import New_service
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlRelationalTableModel, QSqlRelation
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QTableWidgetItem, QVBoxLayout, QWidget, \
    QLineEdit, QPushButton, QFileDialog, QComboBox, QCalendarWidget, QDateEdit, QTableView, QTableWidget, QLabel
from random import randint

ACCESS_LEVEL = 2
LOGIN = ''


class Registration(QDialog):
    def __init__(self):
        super().__init__()
        self.item = None
        uic.loadUi(r'reg.ui', self)
        self.registration.clicked.connect(self.new_user)
        self.setWindowTitle('Регистрация')

    def new_user(self):
        try:
            conn = sqlite3.connect(r'insurance.sqlite')
            cursor = conn.cursor()

            cursor.execute('''INSERT INTO Client(login, password, phone, id_agent) VALUES (?, ?, ?, ?)''',
                           (self.login.text(), self.password.text(), self.phone.text(), str(randint(1, 5))))

            conn.commit()
            conn.close()

            self.item = QMessageBox()
            self.item.setText('Вы добавлены')
            self.item.show()
            self.accept()

        except IndexError:
            self.item = QMessageBox()
            self.item.setWindowTitle('Ошибка')
            self.item.setText('НЕВЕРНЫЕ ДАННЫЕ')
            self.item.show()



class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.item = None
        uic.loadUi(r'login.ui', self)
        self.setWindowTitle('Авторизация')
        self.client.clicked.connect(self.as_client)
        self.agent.clicked.connect(self.as_agent)
        self.registration.clicked.connect(self.new_user)

    def new_user(self):
        self.item = Registration()
        self.item.show()

    def as_client(self):
        try:
            if self.password.text() == search('password', 'Client', self.login.text()):
                global ACCESS_LEVEL, LOGIN
                LOGIN = self.login.text()
                ACCESS_LEVEL = 2
                self.accept()
            else:
                self.item = QMessageBox()
                self.item.setWindowTitle('Ошибка')
                self.item.setText('НЕВЕРНЫЙ ЛОГИН ИЛИ ПАРОЛЬ')
                self.item.show()
        except IndexError:
            self.item = QMessageBox()
            self.item.setWindowTitle('Ошибка')
            self.item.setText('НЕВЕРНЫЙ ЛОГИН ИЛИ ПАРОЛЬ')
            self.item.show()

    def as_agent(self):
        try:
            if self.password.text() == search('password', 'InsuranceAgent', self.login.text()):
                global ACCESS_LEVEL, LOGIN
                LOGIN = self.login.text()
                ACCESS_LEVEL = 1
                self.accept()
            else:
                self.item = QMessageBox()
                self.item.setWindowTitle('Ошибка')
                self.item.setText('НЕВЕРНЫЙ ЛОГИН ИЛИ ПАРОЛЬ')
                self.item.show()
        except IndexError:
            self.item = QMessageBox()
            self.item.setWindowTitle('Ошибка')
            self.item.setText('НЕВЕРНЫЙ ЛОГИН ИЛИ ПАРОЛЬ')
            self.item.show()


class MainWindow(QMainWindow):
    def __init__(self):
        global ACCESS_LEVEL
        super().__init__()
        aut = Login()
        aut.show()
        self.item = None
        self.table = None
        if aut.exec():
            if ACCESS_LEVEL == 2:
                uic.loadUi(r'client_main.ui', self)
                self.layout_client()
            elif ACCESS_LEVEL == 1:
                uic.loadUi(r'agent_main.ui', self)
                self.layout_agent()
        self.setWindowTitle('Главное окно')

    def layout_client(self):
        self.polic.clicked.connect(self.polic_form)
        self.agent.clicked.connect(self.show_agent)
        self.service.clicked.connect(self.new_service)
        self.mine_service.clicked.connect(self.show_service)

    def layout_agent(self):
        self.appllied.clicked.connect(self.show_appllied)
        self.new_application.clicked.connect(self.show_new)

    def show_applied(self):
        self.item = Table_application('Одобренные услуги')

    def polic_form(self):
        global LOGIN
        self.item = Polic_form(LOGIN)
        self.item.show()

    def show_agent(self):
        global LOGIN
        self.item = Show_agent(LOGIN)
        self.item.show()

    def new_service(self):
        global LOGIN
        self.item = New_service(LOGIN)
        self.item.show()

    def show_service(self):
        self.item = Table_application('Мои услуги')

    def show_appllied(self):
        self.item = Table_application('Новые услуги')

    def show_new(self):
        self.item = Table_application('Одобренные услуги')


class Table_application(QWidget):
    def __init__(self, window_name: str):
        super().__init__()
        id_user = 0
        line_id = []
        global LOGIN, ACCESS_LEVEL
        line = ['Номер заявки', 'Клиент', 'Статус', 'Проишествие']
        conn = sqlite3.connect(r'insurance.sqlite')
        cursor = conn.cursor()

        if ACCESS_LEVEL == 2:
            id_user = cursor.execute('''SELECT id_client FROM Client WHERE login = ?''', (LOGIN,)).fetchall()[0][0]
        elif ACCESS_LEVEL == 1:
            line_id = cursor.execute('''SELECT id_client FROM Client 
                                        INNER JOIN (SELECT id_agent FROM InsuranceAgent WHERE login = ?) as query_1 
                                        ON Client.id_agent = query_1.id_agent''', (LOGIN,)).fetchall()

        conn.close()
        line_id = [x[0] for x in line_id]
        set_con()
        self.setWindowTitle(f"{window_name}")
        self.resize(900, 900)
        db = QSqlDatabase.database('INS')
        self.model = QSqlRelationalTableModel(self, db)
        self.model.setTable("Application")
        for i in range(len(line)):
            self.model.setHeaderData(i, Qt.Orientation.Horizontal, line[i])
        self.model.setRelation(1, QSqlRelation("Client", "id_client", "full_name"))
        self.model.setRelation(3, QSqlRelation("InsuranceEvent", "id_event", "event_description"))
        self.model.select()
        if ACCESS_LEVEL == 2:
            self.model.setFilter(f'Application.id_client = {id_user}')
        elif ACCESS_LEVEL == 1:
            self.model.setFilter(f"id_client in {line_id}")
            if window_name == 'Одобренные услуги':
                self.model.setFilter("status = 'одобрено'")
            else:
                self.model.setFilter("status = 'в ожидании'")
        self.model.select()
        self.view = QTableView()
        self.view.setWindowTitle(f"{window_name}")
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()
        self.view.show()


def search(column: str, table: str, uslovie: str):
    con = sqlite3.connect(r'insurance.sqlite')
    kur = con.cursor()
    line_1 = kur.execute(f"""SELECT {column} FROM {table} WHERE login = ?""", (uslovie,)).fetchall()[0]
    con.close()
    return str(line_1[0])


def set_con():
    con = QSqlDatabase.addDatabase("QSQLITE", 'INS')
    con.setDatabaseName(r'insurance.sqlite')
    if not con.open():
        QMessageBox.critical(
            None,
            "QTableView Example - Error!",
            "Database Error: %s" % con.lastError().databaseText(),
        )
        return False
    return True


if __name__ == '__main__':
    insurance.create_database()
    insurance.insert()
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
