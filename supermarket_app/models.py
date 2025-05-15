from django.db import models

# Create your models here.


class Market(models.Model):
    """
    Repräsentiert einen Marktstandort.

    Felder:
    - name: Der Name des Marktes (z.B. "Wochenmarkt Berlin").
    - location: Die physische Adresse oder Stadt, wo der Markt liegt.
    - description: Eine Beschreibung des Marktes.
    - net_worth: Der geschätzte Marktwert in Dezimalzahl (z.B. 1000000.00).
    """
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    net_worth = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        """
        Gibt den Namen des Marktes als String-Repräsentation zurück.
        Wird z.B. in der Admin-Oberfläche angezeigt.
        """
        return self.name


class Seller(models.Model):
    """
    Repräsentiert einen Verkäufer, der auf einem oder mehreren Märkten tätig ist.

    Felder:
    - name: Name des Verkäufers oder des Standes.
    - contact_info: Kontaktinformationen (z.B. Telefonnummer, E-Mail).
    - markets: Many-to-Many-Beziehung zu Market (ein Verkäufer kann auf mehreren Märkten verkaufen).
    """
    name = models.CharField(max_length=255)
    contact_info = models.TextField()
    markets = models.ManyToManyField(Market, related_name="sellers")

    def __str__(self):
        """
        Gibt den Namen des Verkäufers als String zurück.
        """
        return self.name


class Product(models.Model):
    """
    Repräsentiert ein Produkt, das verkauft wird.

    Felder:
    - name: Der Produktname (z.B. "Äpfel").
    - description: Beschreibung des Produkts.
    - price: Preis des Produkts als Dezimalwert (z.B. 2.99).
    - markets: Many-to-Many-Beziehung zu Märkten, auf denen das Produkt verkauft wird.
    - seller: Many-to-Many-Beziehung zu Verkäufern, die das Produkt anbieten.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=50, decimal_places=2)
    markets = models.ManyToManyField(Market, related_name="products")
    seller = models.ManyToManyField(Seller, related_name="products")

    def __str__(self):
        """
        Gibt den Produktnamen zusammen mit dem Preis als String zurück.
        Beispiel: "Äpfel (2.99)"
        """
        return f"{self.name} ({self.price})"
