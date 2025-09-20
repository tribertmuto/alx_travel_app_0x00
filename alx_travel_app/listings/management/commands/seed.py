from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review
from faker import Faker
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Seed the database with sample listings, bookings, and reviews'

    def add_arguments(self, parser):
        parser.add_argument(
            '--listings',
            type=int,
            default=20,
            help='Number of listings to create (default: 20)'
        )
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create (default: 10)'
        )

    def handle(self, *args, **options):
        fake = Faker()
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # Create users
        self.stdout.write('Creating users...')
        users = []
        for _ in range(options['users']):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password='password123'
            )
            users.append(user)
        
        # Create listings
        self.stdout.write('Creating listings...')
        listings = []
        property_types = ['Apartment', 'House', 'Villa', 'Condo', 'Studio', 'Loft', 'Cottage']
        locations = [
            'New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX',
            'Phoenix, AZ', 'Philadelphia, PA', 'San Antonio, TX', 'San Diego, CA',
            'Dallas, TX', 'San Jose, CA', 'Austin, TX', 'Jacksonville, FL',
            'Fort Worth, TX', 'Columbus, OH', 'Charlotte, NC', 'San Francisco, CA',
            'Indianapolis, IN', 'Seattle, WA', 'Denver, CO', 'Washington, DC'
        ]
        
        for _ in range(options['listings']):
            listing = Listing.objects.create(
                title=f"{random.choice(property_types)} in {random.choice(locations)}",
                description=fake.text(max_nb_chars=500),
                location=random.choice(locations),
                price_per_night=round(random.uniform(50, 500), 2),
                available=random.choice([True, True, True, False]),  # 75% available
                max_guests=random.randint(1, 8)
            )
            listings.append(listing)
        
        # Create bookings
        self.stdout.write('Creating bookings...')
        statuses = ['pending', 'confirmed', 'completed', 'cancelled']
        for _ in range(50):
            listing = random.choice(listings)
            user = random.choice(users)
            
            # Generate random dates
            start_date = fake.date_between(start_date='-30d', end_date='+60d')
            end_date = start_date + timedelta(days=random.randint(1, 14))
            
            booking = Booking.objects.create(
                listing=listing,
                user=user,
                check_in=start_date,
                check_out=end_date,
                status=random.choice(statuses)
            )
        
        # Create reviews
        self.stdout.write('Creating reviews...')
        review_comments = [
            "Great place to stay! Highly recommended.",
            "Beautiful location and excellent amenities.",
            "Perfect for a weekend getaway.",
            "Clean and comfortable, exactly as described.",
            "Amazing views and great service.",
            "Would definitely stay here again.",
            "Nice place but could use some improvements.",
            "Good value for money.",
            "Excellent location, close to everything.",
            "Very comfortable and well-equipped."
        ]
        
        for _ in range(80):
            listing = random.choice(listings)
            user = random.choice(users)
            
            # Check if user already reviewed this listing
            if not Review.objects.filter(listing=listing, user=user).exists():
                Review.objects.create(
                    listing=listing,
                    user=user,
                    rating=random.randint(1, 5),
                    comment=random.choice(review_comments)
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded database with:\n'
                f'- {len(users)} users\n'
                f'- {len(listings)} listings\n'
                f'- {Booking.objects.count()} bookings\n'
                f'- {Review.objects.count()} reviews'
            )
        )
