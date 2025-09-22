class SingletonMeta(type):
    """
    Метакласс для реализации паттерна Singleton.
    Контролирует создание единственного экземпляра класса.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DBSettings(metaclass=SingletonMeta):
    """
    Класс для хранения настроек подключения к базе данных.
    Реализует паттерн Singleton через метакласс SingletonMeta.
    """

    def __init__(self, host, port, user, password, database):
        """
        Инициализирует настройки подключения к базе данных.
        
        :param host: хост базы данных
        :param port: порт базы данных
        :param user: имя пользователя
        :param password: пароль пользователя
        :param database: название базы данных
        """
        if not hasattr(self, '_initialized'):  # Защита от повторной инициализации
            self.host = host
            self.port = port
            self.user = user
            self.password = password
            self.database = database
            self._initialized = True

    def get_connection(self):
        """
        Возвращает строку подключения к базе данных.
        
        :return: строка подключения
        """
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
