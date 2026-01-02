from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.organization.models import Organization

class UserProfile(AbstractUser):
    
    ROLE_ADMIN = "ADMIN"
    ROLE_MANAGER = "MANAGER"
    ROLE_EMPLOYEE = "EMPLOYEE"

    ROLE_CHOICES = (
        (ROLE_ADMIN, "Admin"),
        (ROLE_MANAGER, "Manager"),
        (ROLE_EMPLOYEE, "Employee"),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_EMPLOYEE,
    )

    organization=models.ForeignKey(to=Organization,on_delete=models.CASCADE,null=False)
    profile_picture=models.ImageField(upload_to='profile_picture/')
    created_by=models.ForeignKey("self",on_delete=models.SET_NULL,related_name="user_created",null=True,blank=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by=models.ForeignKey("self",on_delete=models.SET_NULL,related_name="user_updated",null=True,blank=True)


    class Meta:
        db_table='inventory_user'
        constraints=[models.UniqueConstraint(fields=["organization","username"],name="unique_username_per_organization")]
