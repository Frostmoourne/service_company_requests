from rest_framework import generics
from .models import ServiceRequest
from .serializers import ServiceRequestSerializer
from .services import RequestService


class ServiceRequestList(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer


class ServiceRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

    def save(self, request):
        service_data = request.data
        urgency = RequestService().get_urgency(service_data)




