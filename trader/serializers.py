from rest_framework import serializers

from trader.utils import redis_client


class CryptoParameterSerializer(serializers.Serializer):
    exchange = serializers.CharField(
        required=True, error_messages={'required': 'provide exchange in query params', 'blank':'provide exchange'}
    )
    fromCurrency = serializers.CharField(
        required=True, error_messages={'required': 'provide currency you want convert','blank':'provide from currency'}
    )
    toCurrency = serializers.CharField(
        required=True, error_messages={'required': 'provide currency you want convert to', 'blank':'provide to currency'}
    )

    def validate(self, data):
        if not redis_client.get(data['exchange'].lower()) or data['exchange'].lower() == 'exchange':
            raise serializers.ValidationError(detail='Exchange not available', code=400)
        return data
