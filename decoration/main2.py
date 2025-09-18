import io
import sys
import psutil
import os
from functools import wraps



"""
Задачи для отработки навыков в создании декораторов
"""
# TODO Задача №1: создать декоратор, который подавляет print внутри функции
def suppress_print(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Сохраняем оригинальный stdout
        original_stdout = sys.stdout
        # Перенаправляем stdout в "никуда"
        sys.stdout = io.StringIO()
        
        try:
            result = func(*args, **kwargs)
        finally:
            # Восстанавливаем оригинальный stdout
            sys.stdout = original_stdout
            
        return result
    return wrapper

# Использование:
@suppress_print
def noisy_function():
    print("Это сообщение не должно появиться")
    return "Результат"

# result = noisy_function()
# print(result)  # Выведет только "Результат"


# TODO Задача №2: создать декоратор, который ограничивает количество вызовов функции
def max_calls(max_count):
    def decorator(func):
        func.call_count = 0
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            if func.call_count >= max_count:
                raise RuntimeError(f"Превышено максимальное количество вызовов ({max_count})")
            
            func.call_count += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Использование:
@max_calls(3)
def limited_function():
    print("Вызов функции")

#limited_function()  # OK
#limited_function()  # OK  
#limited_function()  # OK
#limited_function()  # Ошибка: Превышено максимальное количество вызовов

# TODO Задача №3: создать декоратор, который замеряет память
def memory_usage(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Получаем использование памяти до вызова
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        
        result = func(*args, **kwargs)
        
        # Получаем использование памяти после вызова
        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        mem_used = mem_after - mem_before
        
        print(f"Функция использовала {mem_used:.2f} MB памяти")
        return result
    return wrapper

# Альтернативный вариант без psutil (простой):
def simple_memory_usage(func):
    import tracemalloc
    from functools import wraps
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"Текущая память: {current / 1024 / 1024:.2f} MB")
        print(f"Пиковая память: {peak / 1024 / 1024:.2f} MB")
        return result
    return wrapper

# Использование:
#@simple_memory_usage
@memory_usage
def memory_heavy_function():
    data = [i for i in range(100000)]
    return len(data)

# result = memory_heavy_function()