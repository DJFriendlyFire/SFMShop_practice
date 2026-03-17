import socket
import time

import requests


def measure_api_performance(url: str):
    """Измерить производительность API endpoint"""
    result = {}

    total_time = time.time()
    # Измерение времени DNS-запроса
    hostname = url.split("/")[2].split(":")[0]
    start = time.time()
    ip = socket.gethostbyname(hostname)
    dns_time = time.time() - start
    result["dns"] = dns_time

    # Измерение времени подключения
    start = time.time()
    response = requests.get(url)
    request_time = time.time() - start
    result["request"] = request_time

    # Измерение времени ответа сервера
    result["server"] = response.elapsed.total_seconds()

    # Измерение общего времени загрузки
    result["total"] = time.time() - total_time

    return result


if __name__ == "__main__":
    print(measure_api_performance("http://127.0.0.1:8000/products"))
