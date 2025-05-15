from rest_framework import serializers
from supermarket_app.models import Market, Seller, Product


def validate_no_x(value):
    errors = []
    if 'X' in value:
        errors.append('no X in location')
    if 'Y' in value:
        errors.append('no Y in location')

    if errors:
        raise serializers.ValidationError(errors)
    return value


class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=55)
    location = serializers.CharField(max_length=255, validators=[validate_no_x])
    description = serializers.CharField()
    net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)

    def create(self, validated_data):
        return Market.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.description = validated_data.get('description', instance.description)
        instance.net_worth = validated_data.get('net_worth', instance.net_worth)
        instance.save()
        return instance


class SellerDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    # markets = MarketSerializer(read_only=True, many=True)
    markets = serializers.StringRelatedField(many=True)
    

class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    
    def validate_markets(self, value):
        markets = Market.objects.filter(id__in=value)
        if len(markets) != len(value):
            raise serializers.ValidationError({"message": "One or more Market IDs not found"})
        return value
    
    def create(self, validated_data):
        market_ids = validated_data.pop('markets')
        seller = Seller.objects.create(**validated_data)
        markets = Market.objects.filter(id__in=market_ids)
        seller.markets.set(markets)
        return seller
    

class ProductDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    # für strukturierte Daten
    # markets = MarketSerializer(many=True, read_only=True)
    # seller = SellerDetailSerializer(many=True, read_only=True)
    # Liefert nur Strings
    markets = serializers.StringRelatedField(many=True)
    seller = serializers.StringRelatedField(many=True)


class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)    
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    seller = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def validate_markets(self, value):
        markets = Market.objects.filter(id__in=value)
        if len(markets) != len(value):
            raise serializers.ValidationError("One or more Market IDs not found.")
        return value

    def validate_seller(self, value):
        sellers = Seller.objects.filter(id__in=value)
        if len(sellers) != len(value):
            raise serializers.ValidationError("One or more Seller IDs not found.")
        return value

    def create(self, validated_data):
        market_ids = validated_data.pop('markets')
        seller_ids = validated_data.pop('seller')
        product = Product.objects.create(**validated_data)
        product.markets.set(Market.objects.filter(id__in=market_ids))
        product.seller.set(Seller.objects.filter(id__in=seller_ids))
        return product
