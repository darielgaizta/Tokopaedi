from django.http import Http404
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status, authentication, permissions

import stripe

from .models import Order, OrderItem
from .serializers import OrderSerializer

# Create your views here.
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
	serializer = OrderSerializer(data=request.data)

	# Check if data submitted from the form is valid and match to the serializer
	if serializer.is_valid():
		stripe.api_key = settings.STRIPE_SECRET_KEY
		paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])

		try:
			# Amount is multiplied by 100 because Stripe accepts in cents (USD)
			charge = stripe.Charge.create(
				amount=int(paid_amount*100),
				currency='USD',
				description='Charge from Tokopaedi',
				source=serializer.validated_data['stripe_token']
			)

			serializer.save(user=request.user, paid_amount=paid_amount)

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		except Exception as e:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)