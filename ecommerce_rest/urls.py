from django.contrib import admin
from django.urls import path, include
from products import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/test/', views.test),
    path('api/v1/products/', views.product_list_view),
    path('api/v1/products/<int:id>/', views.product_detail_view),
    path('api/v1/login/', views.authorization),
    path('api/v1/register/', views.register),
    path('api/v1/user/reviews/', views.user_reviews),
    path('api/v1/cbv/', include('main_class.urls'))
]
