from django.db import models
from django.contrib.auth.models import User

class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"{self.user.username} booking for {self.listing.title}"


class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.user.username} for {self.listing.title}"
