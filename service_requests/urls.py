from django.urls import path
from .views import ServiceRequestList, ServiceRequestDetail

urlpatterns = [
    path('service_requests/', ServiceRequestList.as_view(), name='service_request-list'),
    path('service_requests/<int:pk>/', ServiceRequestDetail.as_view(), name='service_request-detail'),
]
