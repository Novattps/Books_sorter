from database.sqlite import Database, path_to_database
from handlers.main_handlers import start_app


if __name__ == '__main__':
    # Создание экземпляра класса Database для работы с базой данных
    db = Database(path_to_database)
    # с помощью функции check_database проверяем наличие базы данных
    db.check_database()
    # запускаем приложение
    start_app()

