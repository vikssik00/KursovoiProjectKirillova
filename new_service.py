import sqlite3
from PyQt6.QtWidgets import QWidget, QLineEdit, QDateEdit, QComboBox, QPushButton, QMessageBox


class New_service(QWidget):
    def __init__(self, login):
        super().__init__()
        self.item = None
        self.login = login
        self.setGeometry(0, 0, 700, 200)
        # self.name = QLineEdit(self)
        self.calendar = QDateEdit(self)
        self.pol = QComboBox(self)
        self.form_button = QPushButton(self)
        self.setUI()
        self.setWindowTitle('Новая услуга')

    def setUI(self):
        # self.name.setPlaceholderText('Введите ФИО')
        self.calendar.setCalendarPopup(True)
        conn = sqlite3.connect(r'insurance.sqlite')
        cursor = conn.cursor()

        for i in cursor.execute('''SELECT event_description FROM InsuranceEvent''').fetchall():
            self.pol.addItem(i[0])
        self.form_button.setText('Сформировать')
        self.form_button.clicked.connect(self.word)
        # self.name.setGeometry(10, 10, 180, 30)
        self.calendar.setGeometry(10, 55, 680, 30)
        self.pol.setGeometry(10, 100, 680, 30)
        self.form_button.setGeometry(10, 140, 680, 40)

    def word(self):
        # name = self.name.text()
        date = '-'.join(list(reversed(self.calendar.text().split('.'))))
        pol = self.pol.currentText()
        con = sqlite3.connect(r'C:\Users\lulun\PycharmProjects\PythonProject1\insurance.sqlite')
        cursor = con.cursor()

        line = cursor.execute(f'''SELECT InsuranceAgent.id_agent, query_1.id_client FROM InsuranceAgent
                                INNER JOIN (SELECT * FROM Client WHERE login = ?) as query_1
                                ON InsuranceAgent.id_agent = query_1.id_agent''', (self.login,)).fetchall()[0]

        client = str(line[1])

        line = cursor.execute('''SELECT id_event FROM InsuranceEvent WHERE event_description = ?''', (pol, )).fetchall()[0]

        event = str(line[0])
        cursor.execute('''INSERT INTO Application (id_client, status, id_event) VALUES (?, 'в ожидании', ?)''', (client, event))

        con.commit()
        con.close()
        self.item = QMessageBox()
        self.item.setText('Услуга сформирована. Ожидайте результат проверки')
        self.item.show()

