from rest_framework import serializers

from app.models import Brand, Color, ModelType, Order


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('title',)


class ColorReportSerializer(serializers.Serializer):
    color = serializers.CharField(source='color__title')
    quantity = serializers.IntegerField()


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('title',)


class BrandReportSerializer(serializers.Serializer):
    brand = serializers.CharField(source='model__brand__title')
    quantity = serializers.IntegerField()


class ModelTypeSerializer(serializers.ModelSerializer):
    model = serializers.CharField(source='title')
    brand = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Brand.objects.all()
    )

    class Meta:
        model = ModelType
        fields = ('model', 'brand',)


class OrderReadSerializer(serializers.ModelSerializer):
    color = serializers.CharField(source='color.title')
    model = serializers.CharField(source='model.title')

    class Meta:
        model = Order
        fields = ('date', 'brand', 'model', 'color', 'quantity',)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('date', 'color', 'model', 'quantity',)

    def to_representation(self, instance):
        return OrderReadSerializer(
            instance,
        ).data


"""
В задании нет уточнения, что должен принимать на вход сериализатор, но
при необходимости, можно написать сериализатор, который принимает более человеко-читаемые данные:
например, он может принимать не первичные ключи color, model, а их str значения и разбирать их + создавать
необходимые сущности. Пример:
"""


# class OrderSerializer(serializers.ModelSerializer):
#     color = serializers.CharField(max_length=100)
#     model = serializers.CharField(max_length=100)
#     brand = serializers.CharField(max_length=100)
#
#     class Meta:
#         model = Order
#         fields = ('date', 'color', 'model', 'brand', 'quantity',)
#
#     def create(self, validated_data):
#         color, _ = Color.objects.get_or_create(title=validated_data.pop('color'))
#         brand, _ = Brand.objects.get_or_create(title=validated_data.pop('brand'))
#         model, _ = ModelType.objects.get_or_create(
#             title=validated_data.pop('model'),
#             brand=brand
#         )
#         return Order.objects.create(**validated_data, color=color, model=model)
#
#     def update(self, instance, validated_data):
#         brand, model = validated_data.get('brand', None), validated_data.get('model', None)
#         color = validated_data.get('color', None)
#         if brand and model:
#             brand_inst, _ = Brand.objects.get_or_create(title=validated_data.pop('brand'))
#             validated_data['model'], _ = ModelType.objects.get_or_create(
#                 title=model,
#                 brand=brand_inst
#             )
#         if color:
#             validated_data['color'], _ = Color.objects.get_or_create(title=color)
#         return super().update(instance, validated_data)
#
#     def to_representation(self, instance):
#         return OrderReadSerializer(
#             instance,
#         ).data
