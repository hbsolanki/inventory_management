from django.db import models


class Organization(models.Model):
    name=models.CharField(max_length=70)
    description=models.CharField(max_length=200)    

    class Meta:
        db_table="inventory_organization"
        