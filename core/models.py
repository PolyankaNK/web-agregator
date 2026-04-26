from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

KYIV_DISTRICT_CHOICES = [
    ("holosiivskyi", "Голосіївський"),
    ("darnytskyi", "Дарницький"),
    ("desnianskyi", "Деснянський"),
    ("dniprovskyi", "Дніпровський"),
    ("obolonskyi", "Оболонський"),
    ("pecherskyi", "Печерський"),
    ("podilskyi", "Подільський"),
    ("sviatoshynskyi", "Святошинський"),
    ("solomianskyi", "Солом’янський"),
    ("shevchenkivskyi", "Шевченківський"),
]

class ServiceCenter(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Опис")
    city = models.CharField(max_length=100, verbose_name="Місто")
    district = models.CharField(max_length=50, choices=KYIV_DISTRICT_CHOICES, verbose_name="Район", blank=True)
    address = models.CharField(max_length=255, verbose_name="Адреса")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Телефон")
    website = models.URLField(blank=True, verbose_name="Сайт")
    working_hours = models.CharField(max_length=255, blank=True, verbose_name="Години роботи")
    latitude = models.DecimalField(max_digits=18, decimal_places=16, null=True, blank=True, verbose_name="Широта")
    longitude = models.DecimalField(max_digits=18, decimal_places=16, null=True, blank=True, verbose_name="Довгота")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Сервісний центр"
        verbose_name_plural = "Сервісні центри"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while ServiceCenter.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва категорії")

    class Meta:
        verbose_name = "Категорія сервісу"
        verbose_name_plural = "Категорії сервісів"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ServiceCenterImage(models.Model):
    service_center = models.ForeignKey(
        ServiceCenter,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Сервісний центр"
    )
    image = CloudinaryField(folder="service_centers", verbose_name="Фото")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Фото сервісного центру"
        verbose_name_plural = "Фото сервісних центрів"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.service_center.name} - фото"


class ServiceOffer(models.Model):
    service_center = models.ForeignKey(
        ServiceCenter,
        on_delete=models.CASCADE,
        related_name="offers",
        verbose_name="Сервісний центр"
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="offers",
        verbose_name="Категорія"
    )
    title = models.CharField(max_length=255, verbose_name="Назва послуги")
    description = models.TextField(blank=True, verbose_name="Опис послуги")
    price_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Ціна від")
    price_to = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Ціна до")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Послуга сервісного центру"
        verbose_name_plural = "Послуги сервісних центрів"
        ordering = ["title"]

    def __str__(self):
        return f"{self.service_center.name} - {self.title}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Користувач"
    )
    service_center = models.ForeignKey(
        ServiceCenter,
        on_delete=models.CASCADE,
        related_name="favorited_by",
        verbose_name="Сервісний центр"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Обране"
        verbose_name_plural = "Обране"
        unique_together = ("user", "service_center")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} -> {self.service_center.name}"

class ServiceReview(models.Model):
    service_center = models.ForeignKey(
        ServiceCenter,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Сервісний центр"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="service_reviews",
        verbose_name="Користувач"
    )
    service_rating = models.PositiveSmallIntegerField(verbose_name="Оцінка обслуговування")
    price_rating = models.PositiveSmallIntegerField(verbose_name="Оцінка ціни")
    quality_rating = models.PositiveSmallIntegerField(verbose_name="Оцінка якості")
    comment = models.TextField(blank=True, verbose_name="Коментар")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} -> {self.service_center.name}"

class ServiceCenterSubmission(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="service_submissions",
        verbose_name="Користувач"
    )
    name = models.CharField(max_length=255, verbose_name="Назва")
    description = models.TextField(blank=True, verbose_name="Опис")
    city = models.CharField(max_length=100, verbose_name="Місто")
    district = models.CharField(
        max_length=50,
        choices=KYIV_DISTRICT_CHOICES,
        blank=True,
        verbose_name="Район"
    )
    address = models.CharField(max_length=255, verbose_name="Адреса")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Телефон")
    website = models.URLField(blank=True, verbose_name="Сайт")
    working_hours = models.CharField(max_length=255, blank=True, verbose_name="Години роботи")
    latitude = models.DecimalField(max_digits=20, decimal_places=16, null=True, blank=True, verbose_name="Широта")
    longitude = models.DecimalField(max_digits=20, decimal_places=16, null=True, blank=True, verbose_name="Довгота")
    services_note = models.TextField(blank=True, verbose_name="Послуги сервісу")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заявка на додавання сервісу"
        verbose_name_plural = "Заявки на додавання сервісів"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class ServiceCenterSubmissionImage(models.Model):
    submission = models.ForeignKey(
        ServiceCenterSubmission,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Заявка"
    )
    image = CloudinaryField(folder="service_submissions", verbose_name="Фото")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Фото заявки"
        verbose_name_plural = "Фото заявок"
        ordering = ["created_at"]

    def __str__(self):
        return f"Фото заявки: {self.submission.name}"