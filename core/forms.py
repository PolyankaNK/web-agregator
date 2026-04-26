from django import forms
from .models import ServiceReview, ServiceCenterSubmission


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

class ServiceCenterSubmissionForm(forms.ModelForm):
    class Meta:
        model = ServiceCenterSubmission
        fields = [
            "name",
            "description",
            "city",
            "district",
            "address",
            "phone",
            "website",
            "working_hours",
            "services_note",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-500"
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-500 h-32 resize-none"
            }),
            "city": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-500"
            }),
            "district": forms.Select(attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-500"
            }),
            "address": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-500"
            }),
            "phone": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-500"
            }),
            "website": forms.URLInput(attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-500"
            }),
            "working_hours": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-500"
            }),
            "services_note": forms.Textarea(attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-500 h-32 resize-none",
                "placeholder": "Послуги, які надає сервісний центр - ціна, якість, гарантія тощо"
            }),
        }