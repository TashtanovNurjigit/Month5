from django.contrib import admin
from django.urls import path, include
from product import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/test/', views.test),
    path('api/v1/products/', views.products_view),
    path('api/v1/products/<int:id>/', views.product_detail_view),
    path('api/v1/profiles/', include('profiles.urls')),
    path('api/v1/categories/', views.CategoryListAPIView.as_view()),
    path('api/v1/categories/<int:id>/', views.CategoryDetailAPIView.as_view()),
    path('api/v1/tags/', views.TagModelViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/v1/tags/<int:id>/', views.TagModelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
