from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from supermarket_app.models import Market, Seller, Product
from .serializers import (
    MarketSerializer,
    ProductDetailSerializer, 
    ProductCreateSerializer, 
    SellerSerializer
)

@api_view(['GET', 'POST'])
def markets_view(request):
    """
    API-Endpunkt für das Abrufen aller Märkte (GET)
    und das Erstellen eines neuen Marktes (POST).
    """
    if request.method == 'GET':
        markets = Market.objects.all()
        serializer = MarketSerializer(markets, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = MarketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'DELETE', 'PUT'])
def market_single_view(request, pk):
    """
    API-Endpunkt für einzelne Märkte:
    - GET: Gibt Details eines Markts zurück.
    - PUT: Aktualisiert einen Markt (teilweise erlaubt mit partial=True).
    - DELETE: Löscht den Markt und gibt ihn zurück.
    """
    try:
        market = Market.objects.get(pk=pk)
    except Market.DoesNotExist:
        return Response({"error": "Market not found"}, status=404)

    if request.method == 'GET':
        serializer = MarketSerializer(market)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = MarketSerializer(market, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        serializer = MarketSerializer(market)
        market.delete()
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def sellers_view(request):
    """
    API-Endpunkt für Verkäufer:
    - GET: Gibt alle Verkäufer mit Detailinformationen zurück.
    - POST: Erstellt einen neuen Verkäufer, erwartet Market-IDs.
    """
    if request.method == 'GET':
        sellers = Seller.objects.all()
        serializer = SellerSerializer(sellers, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'POST'])
def products_view(request):
    """
    API-Endpunkt für Produkte:
    - GET: Gibt alle Produkte zurück, inkl. Märkten und Verkäufern.
    - POST: Erstellt ein neues Produkt mit Market- und Seller-IDs.
    """
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductDetailSerializer(products, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
