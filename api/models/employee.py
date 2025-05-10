from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class EmployeeManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
class Employee(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    aadhar = models.CharField(max_length=12, unique=True)
    pan = models.CharField(max_length=10, unique=True)
    role = models.CharField(max_length=100)
    join_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if not self.mobile.isdigit() or len(self.mobile) < 10:
            raise ValueError("Mobile number must be a valid 10-digit number.")
        if not self.aadhar.isdigit() or len(self.aadhar) != 12:
            raise ValueError("Aadhar number must be a 12-digit number.")
        if not self.pan.isalnum() or len(self.pan) != 10:
            raise ValueError("PAN number must be a valid 10-character alphanumeric string.")
        super().save(*args, **kwargs)

    def clean(self):
        if not self.name:
            raise ValueError("Name cannot be empty.")
        if not self.email:
            raise ValueError("Email cannot be empty.")
        if not self.role:
            raise ValueError("Role cannot be empty.")
        if not self.join_date:
            raise ValueError("Join date cannot be empty.")
        if self.end_date and self.end_date < self.join_date:
            raise ValueError("End date cannot be earlier than join date.")
        super().clean()

    def get_full_name(self):
        return f"{self.name} ({self.role})"
    
    def get_age(self):
        from datetime import date
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age
    
    def get_mobile(self):
        return f"{self.mobile[:3]}-{self.mobile[3:6]}-{self.mobile[6:]}"
    
    def get_email_domain(self):
        return self.email.split('@')[1] if '@' in self.email else None  
    
    def get_aadhar_last_four(self):
        return self.aadhar[-4:] if len(self.aadhar) >= 4 else self.aadhar
    
    def get_pan_first_three(self):
        return self.pan[:3] if len(self.pan) >= 3 else self.pan
    
    def get_pan_last_three(self):
        return self.pan[-3:] if len(self.pan) >= 3 else self.pan
    
    def get_join_date_formatted(self):
        return self.join_date.strftime("%d-%m-%Y") if self.join_date else None
    
    def get_end_date_formatted(self):
        return self.end_date.strftime("%d-%m-%Y") if self.end_date else None
    
    def get_employee_status(self):
        return "Active" if self.is_active else "Inactive"
    
    def get_employee_details(self):
        return {
            "name": self.name,
            "dob": self.dob.strftime("%d-%m-%Y"),
            "mobile": self.get_mobile(),
            "email": self.email,
            "aadhar": f"****{self.get_aadhar_last_four()}",
            "pan": f"{self.get_pan_first_three()}***{self.get_pan_last_three()}",
            "role": self.role,
            "join_date": self.get_join_date_formatted(),
            "end_date": self.get_end_date_formatted(),
            "status": self.get_employee_status()
        }
    
    def get_employee_summary(self):
        return {
            "name": self.name,
            "role": self.role,
            "status": self.get_employee_status(),
            "join_date": self.get_join_date_formatted()
        }