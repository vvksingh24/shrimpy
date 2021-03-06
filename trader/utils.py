import json
import redis

from django.conf import settings

from trader.shrimpy import Shrimpy

# redis client
redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


def get_exchanges():
    client = Shrimpy.get_shrimpy_instance()
    # get exchanges in real time
    exchange_request = client.get_supported_exchanges()
    # return previously held exchanges if request fails
    if exchange_request.status_code == 200:
        exchanges = json.loads(exchange_request.content.decode('utf-8'))
        redis_client.set('exchanges', json.dumps(exchanges))
        return exchanges
    return json.loads(redis_client.get('exchanges'))


def convert_currency(from_currency_rate, to_currency_rate):
    return from_currency_rate/to_currency_rate


