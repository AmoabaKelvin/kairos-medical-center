from django.db import models
from django.urls import reverse
from django.utils import timezone


class LabTests(models.Model):
    """
    The tests performed at the laboratory and their respective prices
    """
    name = models.CharField(max_length=200, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=1000)
    date_added = models.DateTimeField(auto_now_add=timezone.now)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
    
    @staticmethod
    def get_price(test_name):
        return LabTests.objects.get(name=test_name).price
    
    def get_absolute_url(self):
        return reverse('edit_test', kwargs={"pk":self.pk})