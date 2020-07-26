import json

from celery import shared_task
from celery.utils.log import get_task_logger

from trader.shrimpy import Shrimpy
from trader.utils import get_exchanges, redis_client

logger = get_task_logger(__name__)


@shared_task(name='sync_currencies_on_exchange')
def sync_currencies_on_exchange(exchange):
    client = Shrimpy.get_shrimpy_instance()
    ticker_request = client.get_ticker(exchange)
    if ticker_request.status_code == 200:
        tickers = json.loads(ticker_request.content.decode('utf-8'))
        tickers_dict = {}
        for ticker in tickers:
            if ticker.get('priceUsd', -1):
                tickers_dict[ticker.get('symbol').lower()] = {'usd_price': float(ticker['priceUsd'])}
            else:
                tickers_dict[ticker.get('symbol').lower()] = {'usd_price': -1}
            tickers_dict[ticker.get('symbol').lower()]['last_updated'] = ticker.get('lastUpdated')
        redis_client.set(exchange, json.dumps(tickers_dict))
    else:
        logger.info(f'failed to sync currency on {exchange}')


@shared_task
def sync_currencies():
    logger.info('getting all exchanges')
    exchanges = get_exchanges()
    for exchange in exchanges:
        logger.info(f'syncing currencies on {exchange.get("exchange")}')
        sync_currencies_on_exchange.delay(exchange.get('exchange').lower())



