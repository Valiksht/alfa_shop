import json
from django.core.management.base import BaseCommand
from api.models import MainCategiry, LastCategiry, Prodact

class Command(BaseCommand):
    help = "Создание фиктур для базы данных"

    def handle(self, *args, **kwargs):
        data = []
        for category in MainCategiry.objects.all():
            data.append({
                "model": "api.maincategiry",
                "pk": category.id,
                "fields": {
                    "name": category.name,
                    "slug": category.slug,
                    "image": category.image.url if category.image else None
                }
            })
        for subcategory in LastCategiry.objects.all():
            data.append({
                "model": "api.lastcategiry",
                "pk": subcategory.id,
                "fields": {
                    "name": subcategory.name,
                    "slug": subcategory.slug,
                    "image": subcategory.image.url if subcategory.image else None,
                    "main_categiry": subcategory.main_categiry.id
                }
            })
        for product in Prodact.objects.all():
            data.append({
                "model": "api.prodact",
                "pk": product.id,
                "fields": {
                    "name": product.name,
                    "slug": product.slug,
                    "price": str(product.price),
                    "category": product.category.id
                }
            })
        with open('api/fixtures/fixtures.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        self.stdout.write(self.style.SUCCESS('Фиктуры успешно созданы!'))
