import sqlite3
from PyQt6.QtWidgets import QWidget, QLabel

class Show_agent(QWidget):
    def __init__(self, login):
        super().__init__()
        self.setGeometry(0, 0, 300, 100)
        self.name = QLabel(self)
        self.phone = QLabel(self)
        self.name.setGeometry(30, 20, 230, 20)
        self.phone.setGeometry(30, 60, 230, 20)

        conn = sqlite3.connect(r'../Users/lulun/PycharmProjects/PythonProject1/insurance.sqlite')
        cursor = conn.cursor()

        line = cursor.execute(f'''SELECT InsuranceAgent.full_name, InsuranceAgent.phone FROM InsuranceAgent
                        INNER JOIN (SELECT * FROM Client WHERE login = ?) as query_1
                        ON InsuranceAgent.id_agent = query_1.id_agent''', (login, )).fetchall()[0]

        conn.close()

        self.name.setText(line[0])
        self.phone.setText(line[1])