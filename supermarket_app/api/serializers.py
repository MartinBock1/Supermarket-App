from rest_framework import serializers
from supermarket_app.models import Market, Seller, Product


# Eine benutzerdefinierte Validierungsfunktion, die prüft, ob 'X' oder 'Y' im String vorkommt.
def validate_no_x(value):
    """
    Validiert das location-Feld.
    Verhindert das Vorkommen von 'X' oder 'Y' im Text.
    """
    errors = []
    if 'X' in value:
        errors.append('no X in location')
    if 'Y' in value:
        errors.append('no Y in location')

    if errors:
        raise serializers.ValidationError(errors)
    return value


# class MarketSerializer(serializers.Serializer):
#     """
#     Serializer für Markt-Daten. Wird für Erstellen und Anzeigen verwendet.
#     """
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=55)
#     location = serializers.CharField(max_length=255, validators=[validate_no_x])
#     description = serializers.CharField()
#     net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)

#     def create(self, validated_data):
#         """
#         Erstellt ein neues Market-Objekt aus validierten Daten.
#         """
#         return Market.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Aktualisiert ein bestehendes Market-Objekt mit neuen Daten.
#         """
#         instance.name = validated_data.get('name', instance.name)
#         instance.location = validated_data.get('location', instance.location)
#         instance.description = validated_data.get('description', instance.description)
#         instance.net_worth = validated_data.get('net_worth', instance.net_worth)
#         instance.save()
#         return instance


class MarketSerializer(serializers.ModelSerializer):
    """
    Serializer für das Market-Modell.

    Dieser Serializer verwendet Django REST Frameworks ModelSerializer, 
    um automatisch alle Felder des Market-Modells zu serialisieren.

    Vorteile:
    - Alle Felder aus dem Market-Modell werden automatisch eingebunden (id, name, location, description, net_worth).
    - Die Methoden create() und update() werden intern generiert.
    - Felder werden automatisch validiert basierend auf den Model-Felddefinitionen.

    Verwendet:
    - für die Darstellung von Market-Daten (GET)
    - für das Erstellen oder Aktualisieren von Märkten (POST/PUT)
    """
    
    sellers = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Market
        fields = '__all__'
        # exclude = ['id']
    
    def get_sellers():
        pass


class SellerSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(read_only=True, many=True)
    market_ids = serializers.PrimaryKeyRelatedField(
        queryset=Market.objects.all(),
        many=True,
        write_only=True,
        source='markets'
    )

    market_count = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ["id", "name", "market_ids", "market_count", "markets", "contact_info"]

    def get_market_count(self, obj):
        return obj.markets.count()


# WICHTIG:
"""
Der 'SellerSerializer' ersetzt 'SellerDetailSerializer' & 'SellerCreateSerializer' 
"""
# class SellerDetailSerializer(serializers.Serializer):
#     """
#     Detail-Serializer für Verkäufer (Lesen von Daten).
#     Gibt Verkäuferdaten zusammen mit den zugehörigen Märkten zurück.
#     """
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=255)
#     contact_info = serializers.CharField()
#     # Märkte werden als String angezeigt (entspricht __str__)
#     markets = serializers.StringRelatedField(many=True)
#     # Alternativ: strukturierte Ausgabe
#     # markets = MarketSerializer(read_only=True, many=True)


# class SellerCreateSerializer(serializers.Serializer):
#     """
#     Serializer für das Erstellen eines Sellers mit zugehörigen Market-IDs.
#     """
#     name = serializers.CharField(max_length=255)
#     contact_info = serializers.CharField()
#     markets = serializers.ListField(child=serializers.IntegerField(), write_only=True)

#     def validate_markets(self, value):
#         """
#         Validiert, ob alle angegebenen Market-IDs existieren.
#         """
#         markets = Market.objects.filter(id__in=value)
#         if len(markets) != len(value):
#             raise serializers.ValidationError({"message": "One or more Market IDs not found"})
#         return value

#     def create(self, validated_data):
#         """
#         Erstellt einen neuen Seller und verknüpft ihn mit Märkten.
#         """
#         market_ids = validated_data.pop('markets')
#         seller = Seller.objects.create(**validated_data)
#         markets = Market.objects.filter(id__in=market_ids)
#         seller.markets.set(markets)
#         return seller


class ProductDetailSerializer(serializers.Serializer):
    """
    Detail-Serializer für Produkte (Lesen).
    Gibt strukturierte Infos über Produkte, Märkte und Verkäufer zurück.
    """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    # Einfache String-Repräsentation der Märkte und Verkäufer
    markets = serializers.StringRelatedField(many=True)
    seller = serializers.StringRelatedField(many=True)
    # Alternativ strukturierte Darstellung:
    # markets = MarketSerializer(many=True, read_only=True)
    # seller = SellerDetailSerializer(many=True, read_only=True)


class ProductCreateSerializer(serializers.Serializer):
    """
    Serializer zum Erstellen eines Produkts.
    Erwartet IDs für zugehörige Märkte und Verkäufer.
    """
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    seller = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def validate_markets(self, value):
        """
        Validiert die Existenz aller angegebenen Market-IDs.
        """
        markets = Market.objects.filter(id__in=value)
        if len(markets) != len(value):
            raise serializers.ValidationError("One or more Market IDs not found.")
        return value

    def validate_seller(self, value):
        """
        Validiert die Existenz aller angegebenen Seller-IDs.
        """
        sellers = Seller.objects.filter(id__in=value)
        if len(sellers) != len(value):
            raise serializers.ValidationError("One or more Seller IDs not found.")
        return value

    def create(self, validated_data):
        """
        Erstellt ein Produkt und verknüpft es mit Märkten und Verkäufern.
        """
        market_ids = validated_data.pop('markets')
        seller_ids = validated_data.pop('seller')
        product = Product.objects.create(**validated_data)
        product.markets.set(Market.objects.filter(id__in=market_ids))
        product.seller.set(Seller.objects.filter(id__in=seller_ids))
        return product
