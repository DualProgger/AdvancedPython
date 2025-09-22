import psycopg2

"""
Реализация Singleton через метакласс.
"""
class SingletonMeta(type):
    _instance: None

    def __init__(cls, name, bases, namespace):
        # На данном этапе мы модифицируем объект класса
        # во время его объявления
        super().__init__(name, bases, namespace)
        # Этот код необходим в случае наследования от класса,
        # который уже наследуется от SingletonBase и при этом,
        # экземпляр родительского класса уже создавался
        # иначе во время наследования объект нового класса
        # унаследует и значение атрибута _instance с записанным
        # в нем экземпляром класса
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        # Этот код мы вызываем перед type.__call__ и соответственно
        # до того, как начинаем создавать экземпляр класса.
        # Важно отметить, что на этом этапе мы работаем с объектом
        # класса и изменяя его атрибуты мы модифицируем атрибуты
        # именно объекта класса. Значение атрибута _instance
        # в метаклассе SingletonMeta или родительских классах не изменится.

        # Проверяем записан ли в объекте класса экземпляр
        if cls._instance is None:
            # Если не записан, то создаем экземпляр класса и сохраняем
            # в атрибут объекта класса
            cls._instance = super().__call__(*args, **kwargs)

        # возвращаем экземпляр класса
        return cls._instance


class DBSettings(metaclass=SingletonMeta):
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
    
    def get_connection(host, port, user, password, database):
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        return connection