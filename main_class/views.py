from rest_framework.generics import ListCreateAPIView,\
    RetrieveUpdateDestroyAPIView, GenericAPIView
from products.models import Review
from products.serializers import ReviewSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    filter_fields = ['product']
    search_fields = ['text']


class ReviewUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCreateSerializer


class RegisterAPIView(GenericAPIView):
    serializer_class = UserCreateSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # username = request.data.get('username')
        # password = request.data.get('password')
        User.objects.create_user(**serializer.validated_data)
        return Response(data={'MESSAGE': serializer.errors},
                        status=status.HTTP_201_CREATED)
