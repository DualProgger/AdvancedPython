"""
Отработка навыков по созданию декораторов
"""
# TODO Пример №1 без параметров
def my_decorator(func):
    def wrapper():
        print("Что-то до вызова функции")
        func()
        print("Что-то после вызова функции")
    return wrapper

@my_decorator
def say_hello():
    print("Привет!")

# say_hello()


# TODO Пример №2 с параметрами
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("До вызова")
        result = func(*args, **kwargs)
        print("После вызова")
        return result
    return wrapper

@my_decorator
def greet(name):
    print(f"Привет, {name}!")

# greet("Анна")


# TODO Пример №3 логирование
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Вызов функции {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def add(a, b):
    return a + b

# print(add(3, 5))

# TODO Пример №4 измерение времени выполнения
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} выполнилась за {end - start:.4f} секунд")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    print("Готово!")

# slow_function()


# TODO Отработка навыков: Задача №1
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def hello():
    print("Привет!")

# hello()

# TODO Отработка навыков: Задача №2
def uppercase(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        if isinstance(res, str):
            return res.upper()
        return res
    return wrapper

@uppercase
def get_message():
    return "привет, мир!"

# print(get_message())
