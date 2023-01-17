from rest_framework import serializers

from .models import Order, OrderItem

from product.serializers import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
	items = OrderItemSerializer(many=True)

	class Meta:
		model = Order
		fields = (
			'id',
			'first_name',
			'last_name',
			'email',
			'address',
			'zipcode',
			'place',
			'phone',
			'stripe_token',
			'items'
		)

	# Separate List[OrderItem] and Order from serializer and save them to their class
	def create(self, validated_data):
		items_data = validated_data.pop('items')
		order = Order.objects.create(**validated_data)

		for item_data in items_data:
			OrderItem.objects.create(order=order, **item_data)

		return order

class OrderItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderItem
		fields = (
			'price',
			'product',
			'quantity',
		)