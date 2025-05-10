from rest_framework import serializers
from api.models.employee import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'phone': {'required': True, 'allow_blank': False},
            'department': {'required': True, 'allow_blank': False},
            'designation': {'required': True, 'allow_blank': False},
            'joining_date': {'required': True, 'allow_null': False},
            'is_active': {'required': False, 'default': True}
        }
