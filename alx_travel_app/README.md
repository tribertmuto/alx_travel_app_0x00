# alx_travel_app_0x00

## Database Models

This project includes three main models:

### Listing
- **title**: Property title
- **description**: Detailed property description
- **location**: Property location
- **price_per_night**: Price per night (with validation)
- **available**: Availability status
- **max_guests**: Maximum number of guests
- **created_at/updated_at**: Timestamps

### Booking
- **listing**: Foreign key to Listing
- **user**: Foreign key to User
- **check_in/check_out**: Booking dates
- **status**: Booking status (pending, confirmed, cancelled, completed)
- **total_price**: Automatically calculated based on nights and price
- **created_at/updated_at**: Timestamps

### Review
- **listing**: Foreign key to Listing
- **user**: Foreign key to User
- **rating**: Rating from 1-5 (with validation)
- **comment**: Review text
- **created_at/updated_at**: Timestamps
- **unique_together**: One review per user per listing

## API Serializers

The project includes comprehensive serializers for API data representation:

- **ListingSerializer**: Includes nested reviews, average rating, and total review count
- **BookingSerializer**: Includes validation and automatic total price calculation
- **ReviewSerializer**: Includes user information and timestamps

## Database Seeder

To populate the database with sample data, run:

```bash
python manage.py seed
```

### Seeder Options

You can customize the seeder with options:

```bash
# Create 50 listings and 20 users
python manage.py seed --listings 50 --users 20

# Use default values (20 listings, 10 users)
python manage.py seed
```

### What the seeder creates:

- **Users**: Sample users with realistic names and emails
- **Listings**: Various property types in different US cities
- **Bookings**: Random bookings with different statuses and date ranges
- **Reviews**: Reviews with ratings and comments (ensuring one review per user per listing)

### Dependencies

Make sure to install the required packages:

```bash
pip install faker
pip install djangorestframework
```

### Running the seeder

1. Make sure your Django project is set up and migrations are applied
2. Run the seeder command
3. The seeder will clear existing data and create fresh sample data
4. Check the console output for confirmation of created records
