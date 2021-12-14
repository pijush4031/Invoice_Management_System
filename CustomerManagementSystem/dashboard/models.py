from django.db import models

class Customer(models.Model):
    name=models.CharField(max_length=100,null=False,blank=False)
    email=models.EmailField(blank=False)
    address=models.CharField(max_length=50,null=True,blank=False)
    country=models.CharField(max_length=50,null=True,blank=False)
    
    def __str__(self):
        return self.name

class Invoice(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False)
    invoice_number=models.CharField(max_length=50, blank=False)
    applicable_taxes=models.IntegerField()
    gst_number=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number
