from rest_framework import serializers
from .models import ServiceReview


class ServiceReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceReview
        fields = ["service_rating", "price_rating", "quality_rating", "comment"]

    def validate_service_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Оцінка обслуговування має бути від 1 до 5.")
        return value

    def validate_price_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Оцінка ціни має бути від 1 до 5.")
        return value

    def validate_quality_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Оцінка якості має бути від 1 до 5.")
        return value
    
