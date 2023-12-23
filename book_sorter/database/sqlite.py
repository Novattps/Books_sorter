import sqlite3

# Путь к файлу базы данных
path_to_database = f'database/books_database.sqlite'


class Database:

    def __init__(self, db_name):
        # Инициализация класса, создание соединения с базой данных
        self.conn = sqlite3.connect(db_name)

    """
        Функция update_format_with_args обновляет формат SQL-запроса и аргументов для использования в запросе с 
        использованием параметров.

       :param sql: Исходный SQL запрос с метками XXX, которые нужно заменить.
       :param parameters: Словарь с параметрами для подстановки.
       :return: Обновленный SQL запрос и кортеж с аргументами.
    """
    def update_format_with_args(self, sql, parameters: dict):
        values = ", ".join([
            f"{item} = ?" for item in parameters
        ])
        sql = sql.replace("XXX", values)
        return sql, tuple(parameters.values())
    """
        Функция get_format_args Генерирует SQL-запрос и аргументы на основе переданных параметров.

        :param sql: Исходный SQL-запрос с частичной подстановкой меток XXX.
        :param parameters: Словарь с параметрами для подстановки.
        :return: Сгенерированный SQL-запрос и кортеж с аргументами.
    """
    def get_format_args(self, sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def check_database(self):
        # Проверка наличия таблицы и создание при необходимости
        sql = ("CREATE TABLE IF NOT EXISTS storage_books("
               "book_name TEXT,"
               "author TEXT,"
               "description,"
               "book_genre TEXT)")
        # создаем таблицу через sql запрос
        self.conn.execute(sql)
        print('Game database was created.')
        # сохраняем базу данных
        self.conn.commit()

    # функция добавления книги в базу данных
    def add_book(self, book_name, author, description, book_genre):
        # пишем sql запрос к базе данных
        sql = '''
        INSERT INTO storage_books (book_name, author, description, book_genre)
        VALUES (?, ?, ?, ?);
        '''
        # подключаемся к базе данных и добавляем данные в таблицу
        self.conn.execute(sql, (book_name, author, description, book_genre))
        # сохраняем базу данных
        self.conn.commit()

    # функция получения книги по параметрам из базы данных
    def get_book(self, **kwargs):
        # пишем неполноценный sql запрос
        sql = "SELECT * FROM storage_books WHERE "
        # с помощью функции get_format_args создаем полноценный sql запрос
        sql, parameters = self.get_format_args(sql, kwargs)
        # соединяемся с базой данных
        with self.conn:
            # выполняем запрос к базе данных
            cursor = self.conn.execute(sql, parameters)
            # получаем результат выполнения запроса(первая запись)
            game_info = cursor.fetchone()

        return game_info

    # функция получения всех книг с базы данных
    def get_all_books(self):
        # пишем sql запрос
        sql = "SELECT * FROM storage_books"
        # выполняем запрос и сохраняем изменения
        with self.conn:
            # выполняем запрос к базе данных
            get_response = self.conn.execute(sql)
            # получаем результат выполнения запроса
            get_response = get_response.fetchall()
        # возвращем полученные данные
        return get_response

    # фукнция удаления игры из базы данных
    def delete_book(self, book_name):
        # пишем неполноценный sql запрос
        sql = f"DELETE FROM storage_books WHERE book_name = '{book_name}'"
        with self.conn:
            # выполняем запрос к базе данных
            self.conn.execute(sql)
            # сохраняем базу данных
            self.conn.commit()
