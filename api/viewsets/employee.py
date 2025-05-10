from rest_framework import viewsets
from api.models.employee import Employee
from api.serializers.employee import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
