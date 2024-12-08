import sqlite3

def create_database():
    conn = sqlite3.connect(r"insurance.sqlite")
    cursor = conn.cursor()

    # Создание таблиц
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS InsuranceAgent (
            id_agent INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name VARCHAR(255),
            phone VARCHAR(15),
            login VARCHAR(50),
            password VARCHAR(255)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Client (
            id_client INTEGER PRIMARY KEY,
            full_name VARCHAR(255),
            date_of_birth DATE,
            gender VARCHAR(10) CHECK (gender IN ('муж', 'жен')),
            phone VARCHAR(15),
            address TEXT,
            login VARCHAR(50),
            password VARCHAR(255),
            id_agent INTEGER,
            id_policy INTEGER,
            FOREIGN KEY (id_agent) REFERENCES InsuranceAgent(id_agent),
            FOREIGN KEY (id_policy) REFERENCES InsurancePolicy(id_policy)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TypeOfInsurance (
            id_type INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255),
            description TEXT
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS InsuranceEvent (
            id_event INTEGER PRIMARY KEY AUTOINCREMENT,
            id_type INTEGER,
            event_description TEXT,
            FOREIGN KEY (id_type) REFERENCES TypeOfInsurance(id_type)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS InsurancePolicy (
            id_policy INTEGER PRIMARY KEY AUTOINCREMENT,
            date_start DATE,
            personal_code CHAR(16)
        );
    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Application (
        id_application INTEGER PRIMARY KEY,
        id_client INTEGER,
        status CHAR(10),
        id_event INTEGER,
        FOREIGN KEY (id_client) REFERENCES Client(id_client),
        FOREIGN KEY (id_event) REFERENCES InsuranceEvent(id_event)
        );
    ''')

    conn.commit()
    conn.close()


def insert():
    con = sqlite3.connect(r"insurance.sqlite")
    cursor = con.cursor()
    # Добавление агентов
    cursor.execute('''
        INSERT OR REPLACE INTO InsuranceAgent (id_agent, full_name, phone, login, password) VALUES 
        (1, 'Киряева Елена Дмитриевна', '79123456701', 'agent1', 'passwd1'),
        (2, 'Егоров Андрей Игоревич', '79124567822', 'agent2', 'passwd2'),
        (3, 'Крючков Михаил Алексеевич', '79125678933', 'agent3', 'passwd3'),
        (4, 'Якушкина Кристина Юрьевна', '79126789044', 'agent4', 'passwd4'),
        (5, 'Ноздрова Елена Викторовна', '79127890155', 'agent5', 'passwd5')
    ''')

    # Добавление клиентов
    cursor.execute('''
        INSERT OR REPLACE INTO Client (id_client, full_name, date_of_birth, gender, phone, address, login, password, id_agent, id_policy) VALUES
        (1, 'Иванов Иван Иванович', '1990-01-12', 'муж', '79213456781', 'Москва, ул. Ленина, д. 1', 'ivanov', 'password1', 1, 1),
        (2, 'Петров Петр Петрович', '1985-02-23', 'муж', '79214567892', 'Москва, ул. Пушкина, д. 2', 'petrov', 'password2', 2, 2),
        (3, 'Сидоров Сидор Сидорович', '1992-03-05', 'муж', '79215678903', 'Москва, ул. Гагарина, д. 3', 'sidorov', 'password3', 1, 3),
        (4, 'Кузнецов Николай Николаевич', '1978-04-17', 'муж', '79216789014', 'Москва, ул. Толстого, д. 4', 'kuznetsov', 'password4', 3, 4),
        (5, 'Смирнова Александра Алексеевна', '2000-05-30', 'жен', '79217890125', 'Москва, ул. Чехова, д. 5', 'smirnova', 'password5', 3, 5)
    ''')

    # Добавление вида страхования
    cursor.execute('''
        INSERT OR REPLACE INTO TypeOfInsurance (id_type, title, description) VALUES
        (1, 'Медицинское страхование', 'Предоставляет полис обязательного медицинского страхования (ОМС), который подтверждает право на бесплатную медицинскую помощь.');
    ''')

    # Добавление страховых случаев
    cursor.execute('''
        INSERT OR REPLACE INTO InsuranceEvent (id_event, id_type, event_description) VALUES
        (1, 1, 'Лечение серьезной травмы.'),
        (2, 1, 'Лечение астмы.'),
        (3, 1, 'Лечение острой аллергической реакции.'),
        (4, 1, 'Лечение кариеса.'),
        (5, 1, 'Проведение прививок.')
    ''')

    # Добавление полисов страхования
    cursor.execute('''
        INSERT OR REPLACE INTO InsurancePolicy (id_policy, date_start, personal_code) VALUES
        (1, '2011-01-20', '8634567890123456'),
        (2, '2006-02-26', '8645678901234567'),
        (3, '2023-03-17', '8656789012345678'),
        (4, '2021-04-28', '8667890123456789'),
        (5, '2021-06-01', '8678901234567890')
    ''')

    cursor.execute('''
        INSERT OR REPLACE INTO Application (id_application, id_client, status, id_event) VALUES
        (1, 1, 'в ожидании', 1),
        (2, 2, 'одобрено', 2),
        (3, 3, 'одобрено', 3),
        (4, 4, 'одобрено', 4),
        (5, 5, 'в ожидании', 5)
    ''')

    # Сохранение изменений и закрытие соединения
    con.commit()
    con.close()
