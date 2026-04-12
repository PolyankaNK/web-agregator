from django import forms
from .models import ServiceReview


RATING_CHOICES = [
    (5, "5 - Відмінно"),
    (4, "4 - Добре"),
    (3, "3 - Середньо"),
    (2, "2 - Погано"),
    (1, "1 - Жахливо"),
]


class ServiceReviewForm(forms.ModelForm):
    service_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={
            "class": "w-full border border-gray-300 rounded-lg px-3 py-2"
        }),
        label="Обслуговування"
    )
    price_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={
            "class": "w-full border border-gray-300 rounded-lg px-3 py-2"
        }),
        label="Ціна"
    )
    quality_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={
            "class": "w-full border border-gray-300 rounded-lg px-3 py-2"
        }),
        label="Якість"
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "w-full border border-gray-300 rounded-lg px-3 py-2 h-28 resize-none",
            "placeholder": "Напишіть ваш відгук..."
        }),
        label="Коментар"
    )

    class Meta:
        model = ServiceReview
        fields = ["service_rating", "price_rating", "quality_rating", "comment"]