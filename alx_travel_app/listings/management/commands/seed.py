from django.core.management.base import BaseCommand
from listings.models import Listing
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(10):
            Listing.objects.create(
                title=fake.sentence(nb_words=3),
                description=fake.text(),
                location=fake.city(),
                price_per_night=round(random.uniform(50, 300), 2),
                available=True
            )
        self.stdout.write(self.style.SUCCESS('Successfully seeded listings'))
