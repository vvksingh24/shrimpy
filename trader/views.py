import json

from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils import timezone

from trader.serializers import CryptoParameterSerializer
from trader.utils import convert_currency, redis_client


class ExchangeCryptoView(APIView):
    """
    View for getting exchange rate for currencies
    """

    @staticmethod
    def get(request):
        query_params = request.query_params.dict()
        serializer = CryptoParameterSerializer(data=query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        exchange_data = json.loads(redis_client.get(serializer.data.get('exchange').lower()))
        from_currency_data = exchange_data[serializer.data.get('fromCurrency').lower()]
        to_currency_data = exchange_data[serializer.data.get('toCurrency').lower()]
        if from_currency_data and to_currency_data:
            if from_currency_data.get('usd_price') in (-1, 0, None) or to_currency_data.get('usd_price') in (-1, 0, None):
                return Response({'error': 'realtime data is not available right now please try again after sometime'},
                                status=status.HTTP_202_ACCEPTED)
            acceptable_time = timezone.now() - timezone.timedelta(seconds=60)
            from_currency_updated_at = datetime.strptime(from_currency_data['last_updated'],
                                                         "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
            to_currency_updated_at = datetime.strptime(to_currency_data['last_updated'],
                                                       "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
            if from_currency_updated_at < acceptable_time or to_currency_updated_at < acceptable_time:
                return Response({'error': 'realtime data is not available right now please try again after sometime'},
                                status=status.HTTP_202_ACCEPTED)

            rate = convert_currency(from_currency_data.get('usd_price'), to_currency_data.get('usd_price'))
            return Response({'rate': rate}, status=status.HTTP_200_OK)
        return Response({'error': f'currency not available in {serializer.data.get("exchange")}'},
                        status=status.HTTP_400_BAD_REQUEST)

