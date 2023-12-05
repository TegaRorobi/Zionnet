from .models import MarketPlace,Store,Product

class ProductQuerysetMixin():
     def custom_queryset(self,market_place_id):
        market_place = MarketPlace.objects.get(id=market_place_id)
        stores_in_marketplace = Store.objects.filter(marketplace=market_place)
        products_in_marketplace = Product.objects.filter(store__in= stores_in_marketplace )
        return products_in_marketplace