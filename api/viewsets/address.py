from rest_framework import viewsets
from api.models.address import Address
from api.serializers.address import AddressSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
