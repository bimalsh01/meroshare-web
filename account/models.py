from django.db import models
from django.contrib.auth.models import User

class Meroshare(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    dp = models.CharField(max_length=100)
    uname = models.CharField(max_length=100)
    pword = models.CharField(max_length=100)
    crn = models.CharField(max_length=100)
    pin = models.CharField(max_length=100)
    linked_to = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
    
class History(models.Model):
    id = models.AutoField(primary_key=True)
    appliedby_name = models.CharField(max_length=100)
    applied_company = models.CharField(max_length=100)
    applied_on = models.DateTimeField(auto_now_add=True)
    linked_to = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.linked_to
    
class IPOList(models.Model):
    company_option = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.company_name