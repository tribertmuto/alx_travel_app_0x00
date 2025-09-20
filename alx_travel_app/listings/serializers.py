from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']


class ListingSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'location', 'price_per_night',
            'available', 'max_guests', 'created_at', 'updated_at',
            'reviews', 'average_rating', 'total_reviews'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 2)
        return None
    
    def get_total_reviews(self, obj):
        return obj.reviews.count()


class BookingSerializer(serializers.ModelSerializer):
    listing = ListingSerializer(read_only=True)
    listing_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_id', 'user', 'check_in', 'check_out',
            'status', 'total_price', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'total_price', 'created_at', 'updated_at']
    
    def validate(self, data):
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        return data
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
