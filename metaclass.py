import logging
import tracemalloc
import time
import functools
import types
import io
import atexit

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

tracemalloc.start()

class LoggingMeta(type):
    def __new__(metacls, name, bases, class_dict, **kwargs):
        # Создаем класс как обычно
        cls = super().__new__(metacls, name, bases, class_dict)
        return cls
    
    def __call__(cls, *args, **kwargs):
        # Логирование создания экземпляра класса
        logger.info(f"Создание экземпляра класса: {cls.__name__}")
        
        # Создаем экземпляр
        instance = super().__call__(*args, **kwargs)
        
        # Добавляем атрибут для статистики вызовов
        instance.__call_stats__ = {}
        
        # Оборачиваем все пользовательские методы в декораторы
        for attr_name in dir(instance):
            if (not attr_name.startswith('__') or attr_name in ['__init__']) and not attr_name.endswith('__'):
                attr_value = getattr(instance, attr_name)
                if callable(attr_value) and not isinstance(attr_value, type):
                    # Обновляем метод в экземпляре с декоратором
                    wrapped_method = LoggingMeta._wrap_method(attr_value, instance, attr_name)
                    setattr(instance, attr_name, wrapped_method)
        
        return instance
    
    @staticmethod
    def _wrap_method(method, instance, method_name):
        """Оборачивает метод в декоратор для логирования"""
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            # Проверяем, является ли метод пользовательским (не dunder)
            if method_name.startswith('__') and method_name.endswith('__') and method_name not in ['__init__']:
                return method(*args, **kwargs)
            
            # Логирование вызова метода
            logger.info(f"Вызов метода: {method_name} объекта {instance.__class__.__name__}")
            
            # Измерение памяти до вызова
            tracemalloc.start()
            memory_before = tracemalloc.get_traced_memory()[0]
            
            # Измерение времени выполнения
            start_time = time.perf_counter()
            
            try:
                # Вызов метода
                result = method(*args, **kwargs)
            finally:
                # Измерение времени выполнения
                end_time = time.perf_counter()
                execution_time_ms = (end_time - start_time) * 1000
                logger.info(f"Время выполнения метода {method_name}: {execution_time_ms:.6f} мс")
                
                # Измерение памяти после вызова
                memory_after = tracemalloc.get_traced_memory()[0]
                memory_diff = memory_after - memory_before
                logger.info(f"Использование памяти: до = {memory_before} байт, после = {memory_after} байт, разница = {memory_diff:+d} байт")
                
                # Обновление статистики вызовов
                if method_name not in instance.__call_stats__:
                    instance.__call_stats__[method_name] = 0
                instance.__call_stats__[method_name] += 1
            
            return result
        return wrapper
    
    @staticmethod
    def get_statistics(obj):
        """Вывод статистики вызовов методов для конкретного экземпляра"""
        if hasattr(obj, '__call_stats__') and obj.__call_stats__:
            logger.info("Статистика вызовов методов:")
            for method_name, count in obj.__call_stats__.items():
                logger.info(f" {method_name} - {count} раз(а)")
        else:
            logger.info("Статистика вызовов методов: нет вызовов")

# Регистрируем функцию для вывода статистики при завершении программы
def print_all_statistics():
    # В реальном приложении здесь можно было бы хранить ссылки на все созданные объекты
    pass

atexit.register(print_all_statistics)

class HttpClient(metaclass=LoggingMeta):
    def __init__(self):
        pass
    
    def __str__(self):
        return "HttpClient"
    
    def request_handler(self):
        return "OK, Status code: 200"
    
    def get_data(self):
        time.sleep(0.001)  # Имитация работы
        return {"data": "some data"}
    
    def send_request(self, url):
        time.sleep(0.002)  # Имитация работы
        return f"Request sent to {url}"


"""
# Пример использования
if __name__ == "__main__":
    # Создание экземпляра (автоматически логируется)
    client = HttpClient()
    
    # Вызов методов (автоматически логируются)
    result1 = client.request_handler()
    result2 = client.get_data()
    result3 = client.send_request("https://example.com")
    result4 = client.get_data()  # Второй вызов
    
    # Вывод статистики
    LoggingMeta.get_statistics(client)
"""