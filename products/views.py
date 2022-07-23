from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from products.models import Product, Review
from products.serializers import ProductSerializers, ProductCreateUpdateSerializer,\
    ReviewSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def test(request):
    print(request.user)
    context = {
        'int': 123,
        'str': 'Hello',
        'bool': True,
        'list': [
            1, 2, 3
        ]
    }
    return Response(data=context)

@api_view(['GET', 'POST'])
def product_list_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = ProductSerializers(products, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = ProductCreateUpdateSerializer(data=request.data) #Validation for create and update product method "POST"
        if not serializer.is_valid():
            return Response(data={'Error': serializer.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')
        product = Product.objects.create(title=title, description=description,
                               price=price, category_id=category_id)
        for i in request.data.get('reviews', []): #Creating fake reviews
            Review.objects.create(
                stars=i['stars'],
                text=i['text'],
                product=product
            )
        return Response(data=ProductSerializers(product).data,
                        status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_view(request, id):
        try:
            products = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'Message': 'PRODUCT NOT FOUND'})
        if request.method == 'GET':
            data = ProductSerializers(products, many=False).data
            return Response(data=data)
        elif request.method == 'DELETE':
            products.delete()
            return Response(ProductSerializers(products).data)
        elif request.method == 'PUT':
            products.title = request.data.get('title')
            products.description = request.data.get('description')
            products.price = request.data.get('price')
            products.category_id = request.data.get('category_id')
            products.save()
            return Response(ProductSerializers(products).data)

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def authorization(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        return Response(data={'key': token.key})
    return Response(data={'ERROR': 'USER NOT FOUND'},
                    status=status.HTTP_404_NOT_FOUND)


from django.contrib.auth.models import User

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    User.objects.create_user(username=username, password=password)
    return Response(data={'MESSAGE': "USER CREATED"},
                    status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_reviews(request):
    reviews = Review.objects.filter(author=request.user)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(data=serializer.data)

