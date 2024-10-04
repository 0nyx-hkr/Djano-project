# inventory/views.py
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import InventoryItem
from .serializers import InventoryItemSerializer
from django.http import HttpResponse
from django.core.cache import cache

import logging

# Create a logger instance for this module
logger = logging.getLogger(__name__)



# Registration View
@api_view(['POST'])
def register_user(request):
    try:
        data = request.data
        user = User.objects.create(
            username=data['username'],
            email=data['email'],
            password=make_password(data['password']),
        )
        logger.info(f"New user registered: {user.username}")  # Log user registration
        return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")  # Log error
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Login View to get JWT tokens
@api_view(['GET','POST'])
def login_user(request):
    # if request.method == 'GET':
    #     return render(request, 'login.html')
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            logger.info(f"User logged in: {username}")  # Log user login
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            logger.warning(f"Failed login attempt for user: {username}")  # Log failed login
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        logger.warning(f"Login failed, user not found: {username}")  # Log warning for user not found
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)



 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    try:
        serializer = InventoryItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Item created: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Item creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error in create_item: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_item(request, item_id):
    # print("item ID",item_id)
    cache_key = f"item_{item_id}"
    # print("cahe key",cache_key)
    item = cache.get(cache_key)
    # print("Item : Item",item)
    if not item:
        try:
            # If not in cache, fetch from the database
            item = InventoryItem.objects.get(id=item_id)
            serializer = InventoryItemSerializer(item)
            
            # Cache the item for future requests (example: cache for 5 minutes)
            cache.set(cache_key, serializer.data, timeout=300)  # 300 seconds = 5 minutes
            
            logger.info(f"Item fetched from database and cached: {item_id}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except InventoryItem.DoesNotExist:
            logger.warning(f"Item not found: {item_id}")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        # If in cache, return the cached item
        logger.info(f"Item fetched from cache: {item_id}")
        return Response(item, status=status.HTTP_200_OK)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_item(request, item_id):
    try:
        item = InventoryItem.objects.get(id=item_id)
        serializer = InventoryItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Item updated: {item_id}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error(f"Item update failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except InventoryItem.DoesNotExist:
        logger.warning(f"Item not found: {item_id}")
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item(request, item_id):
    try:
        item = InventoryItem.objects.get(id=item_id)
        item.delete()
        logger.info(f"Item deleted: {item_id}")
        return Response({"message": "Item deleted successfully"}, status=status.HTTP_200_OK)
    except InventoryItem.DoesNotExist:
        logger.warning(f"Item not found: {item_id}")
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_items(request):
    items = InventoryItem.objects.all()
    serializer = InventoryItemSerializer(items, many=True)
    logger.info("Fetched all items from the database")
    return Response(serializer.data, status=status.HTTP_200_OK)
