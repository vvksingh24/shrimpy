from rest_framework import serializers

from trader.utils import redis_client


class CryptoParameterSerializer(serializers.Serializer):
    exchange = serializers.CharField(
        required=True, error_messages={
            'required': 'enter exchange platform', 'blank': 'enter exchange platform'
        }
    )
    fromCurrency = serializers.CharField(
        required=True, error_messages={
            'required': 'enter currency to be converted', 'blank': 'enter currency to be converted'
        }
    )
    toCurrency = serializers.CharField(
        required=True, error_messages={
            'required': 'enter in which currency it should be converted',
            'blank': 'enter in which currency it should be converted'
        }
    )

    def validate(self, data):
        if not redis_client.get(data['exchange'].lower()) or data['exchange'].lower() == 'exchange':
            raise serializers.ValidationError(detail='Exchange not available', code=400)
        return data
