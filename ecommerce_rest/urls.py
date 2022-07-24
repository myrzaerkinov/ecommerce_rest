from django.contrib import admin
from django.urls import path, include
from products import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="API Docs",
      default_version='v1',
      description="Ecommerce",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@xyz.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/test/', views.test),
    path('api/v1/products/', views.product_list_view),
    path('api/v1/products/<int:id>/', views.product_detail_view),
    path('api/v1/login/', views.authorization),
    path('api/v1/register/', views.register),
    path('api/v1/user/reviews/', views.user_reviews),
    path('api/v1/cbv/', include('main_class.urls')),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]

