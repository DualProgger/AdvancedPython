import re
"""
Создать 2 валидатора: имени пользователя и пароля через дескрипторы.
"""

class UsernameValidator:
    """
    Метод вызывается при получении значения атрибута
    Параметры:
        - instance: экземпляр класса, в котором используется дескриптор (User)
        - owner: класс, в котором определен дескриптор (User)
    Возвращает: значение атрибута _username из экземпляра
    """
    def __get__(self, instance, owner):
        return instance._username
    
    """
    Метод вызывается при установке значения атрибута
    Параметры:
        - instance: экземпляр класса, в котором используется дескриптор (User)
        - value: новое значение, которое присваивается атрибуту
    Выполняет валидацию значения перед его установкой
    """
    def __set__(self, instance, value):

        # Проверка на входное значение - должна быть строка
        if not isinstance(value, str):
            raise ValueError("Username must be a string")
        
        # Проверка длины строки от 3 до 20 символов
        if not(3 <= len(value) <= 20):
            raise ValueError("Username must be between 3 and 20 characters")
        
        # Проверка первого символа, что он начинается с буквы
        if not value[0].isalpha():
            raise ValueError("Username must start with a letter")
        
        # Проверка, что имя содержит только допустимые символы (буквы, цифры, подчеркивание)
        # re.fullmatch проверяет, что вся строка соответствует шаблону
        if not re.fullmatch(r'[a-zA-Z0-9_]+', value):
            raise ValueError("Username can contain only letters, digits, and underscores")
        
        # Если все проверки пройдены, то сохраняем значение
        instance._username = value


"""
Дескриптор для валидации пароля
Реализует протокол дескриптора с методами __get__ и __set__
"""
class PasswordValidator:
    """
    Метод вызывается при получении значения атрибута
    Параметры:
        - instance: экземпляр класса, в котором используется дескриптор (User)
        - owner: класс, в котором определен дескриптор (User)
    Возвращает: значение атрибута _password из экземпляра
    """
    def __get__(self, instance, owner):
        return instance._password
    
    def __set__(self, instance, value):

        # Проверка входного значение на строковый тип
        if not isinstance(value, str):
            raise ValueError("Password must be a string")
        
        # Проверка длины пароля не менее 8 символов
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        # Проверка присутствует ли хотя бы одна заглавная буква
        if not any(val.isupper() for val in value):
            raise ValueError("Password must contain at least one uppercase letter")
        
        # Проверка присутствует ли хотя бы одна строчная буква
        if not any(val.islower() for val in value):
            raise ValueError("Password must contain at least one lowercase letter")
        
        # Проверка присутствия хотя бы одной цифры
        if not any(val.isdigit() for val in value):
            raise ValueError("Password must contain at least one digit")
        
        # Если все проверки прошли, то присваиваем значение
        instance._password = value


"""
Класс User
"""
class User:
    username = UsernameValidator()
    password = PasswordValidator()

    def __init__(self, user, passwrd):
        self.username = user
        self.password = passwrd

