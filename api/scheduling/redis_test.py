import redis

from celery_worker import REDIS_PORT, REDIS_HOST, redis_url

r = redis.Redis.from_url(redis_url)
if __name__ == '__main__':
    try:
        response = r.ping()
        if response:
            print("Подключение к Redis успешно!")
        else:
            print("Не удалось подключиться к Redis.")
    except Exception as e:
        print(f"Произошла неизвестная ошибка: {e}")