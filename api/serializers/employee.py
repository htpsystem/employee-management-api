from rest_framework import serializers
from api.models.employee import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    qualification_display = serializers.SerializerMethodField()
    marital_status_display = serializers.SerializerMethodField()
    gender_display = serializers.SerializerMethodField()

    def get_qualification_display(self, obj):
        return obj.get_qualification_display()
    
    def get_marital_status_display(self, obj):
        return obj.get_marital_status_display()
    
    def get_gender_display(self, obj):
        return obj.get_gender_display()
    
    class Meta:
        model = Employee
        # fields = sorted([field.name for field in Employee._meta.fields] + ['qualification_display', 'marital_status_display', 'gender_display'])
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