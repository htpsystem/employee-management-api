from django.db import models
from .employee import Employee
    
class Address(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='addresses')
    type = models.CharField(max_length=1, choices=[('C', 'Current'), ('P', 'Permanent')])
    add_1 = models.CharField(max_length=255)
    add_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type} Address for {self.employee.name}"
    
    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        ordering = ['employee', 'type']

    def save(self, *args, **kwargs):
        if self.type not in dict(self._meta.get_field('type').choices):
            raise ValueError("Invalid address type. Choose 'C' for Current or 'P' for Permanent.")
        super().save(*args, **kwargs)

    def clean(self):
        if not self.add_1:
            raise ValueError("Address line 1 cannot be empty.")
        if not self.city:
            raise ValueError("City cannot be empty.")
        if not self.state:
            raise ValueError("State cannot be empty.")
        if not self.pincode.isdigit() or len(self.pincode) != 6:
            raise ValueError("Pincode must be a 6-digit number.")
        super().clean()

    def get_full_address(self):
        full_address = f"{self.add_1}"
        if self.add_2:
            full_address = f"{self.add_2}, {full_address}"
        full_address = f"{full_address}, {self.city}, {self.state} - {self.pincode}"
        return full_address
    
    # def get_address_type_display(self):
    #     return dict(self._meta.get_field('type').choices).get(self.type, "Unknown")
    
