import datetime

from django.core.validators import MinValueValidator
from django.db import models

from app.utils import validate_past_order_date


class Color(models.Model):
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=100, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.title


class ModelType(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='model_type')

    class Meta:
        verbose_name = 'Модель автомобиля'
        verbose_name_plural = 'Модели автомобилей'
        constraints = [
            models.UniqueConstraint(fields=['title', 'brand'], name='model_brand need to be unique')
        ]

    def __str__(self):
        return self.title + '__' + self.brand.title


class Order(models.Model):
    color = models.ForeignKey('Color', on_delete=models.PROTECT, related_name='order')
    model = models.ForeignKey('ModelType', on_delete=models.PROTECT, related_name='order')
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    date = models.DateField(default=datetime.date.today, validators=[validate_past_order_date])

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-date']

    def brand(self):
        return self.model.brand.title
