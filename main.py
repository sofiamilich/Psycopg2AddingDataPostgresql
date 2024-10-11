# Импорт модуля psycopg2
import psycopg2

# Импорт модуля extensions из модуля psycopg2
from psycopg2 import extensions

# Импорт переменных из файла config_db
from config_db import host, db_name, db_password, db_user, port

db_conn = None
try:
    # Подключение к базе данных
    db_conn = psycopg2.connect(
        host=host,
        database=db_name,
        user=db_user,
        password=db_password,
        port=port
    )
    print(f"[INFO] Соединение с базой данных '{db_name}' установлено.")



    # Вывод текущего уровня изоляции транзакций
    current_iso_level = db_conn.isolation_level
    print(f"Текущий уровень изоляции: {current_iso_level}")

    # Установка нового уровня изоляции транзакций
    serializable = extensions.ISOLATION_LEVEL_SERIALIZABLE
    db_conn.set_isolation_level(serializable)

    new_iso_level = db_conn.isolation_level
    print(f"Новый уровень изоляции: {new_iso_level}")





    # Автоматическая фиксация изменений
    db_conn.autocommit = True

    # Создание курсора при помощи контекстного менеджера
    with db_conn.cursor() as cur:

        # Удаление таблицы list_users если она существует
        cur.execute("drop table if exists list_users;")

        # Создание таблицы list_users
        cur.execute("""
            create table list_users (
                id int4,
                last_name varchar(35),
                first_name varchar(25),
                middle_name varchar(35),
                email varchar(60)
            );
        """)
        print("[INFO] Таблица 'list_users' создана.")

        # Добавление данных в таблицу list_users
        sql_query = ("insert into list_users(id, last_name, first_name, "
                     "middle_name, email) values (%s, %s, %s, %s, %s);")

        data_table = [
            (1, 'Бондарчук', 'Тимофей', 'Порфирьевич', 'timofey6484@yandex.ru'),
            (2, 'Кая', 'Анфиса', 'Наумовна', 'anfisa26@yandex.ru'),
            (3, 'Леваневская', 'Ника', 'Николаевна', 'nika23081977@gmail.com'),
            (4, 'Иньшов', 'Игнат', 'Ефимович', 'ignat.inshov@mail.ru'),
            (5, 'Капустов', 'Иван', 'Никитович', 'ivan67@outlook.com'),
            (6, 'Балин', 'Марк', 'Андреевич', 'mark1974@hotmail.com')
        ]

        cur.executemany(sql_query, data_table)
        print("[INFO] Данные вставлены в таблицу 'list_users'.")

except Exception as e:
    if db_conn:
        # Отмена внесённых изменений
        db_conn.rollback()
    print("[ERROR] Ошибка при работе с PostgreSQL:", e)

finally:
    if db_conn is not None:
        try:
            db_conn.close()
            print(f"[INFO] Соединение с базой данных '{db_name}' закрыто.")
        except Exception as e:
            print("[ERROR] Ошибка при закрытии соединения с базой данных:", e)