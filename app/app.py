import os
import socket
from flask import Flask
from redis import Redis

# Pobieramy adres Redisa ze zmiennej środowiskowej (to ustawi K8s!)
redis_host = os.environ.get('REDIS_HOST', 'localhost')
app = Flask(__name__)
redis = Redis(host=redis_host, port=6379)

@app.route('/')
def hello():
    try:
        redis.incr('hits')
        count = redis.get('hits').decode('utf-8')
        # Wyświetlamy też nazwę Poda (hostname), żeby widzieć Load Balancing w K8s!
        return f"Witaj! Odwiedzono nas {count} razy.\nObsługuje mnie Pod: {socket.gethostname()}\n"
    except Exception as e:
        return f"Błąd połączenia z Redisem: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)