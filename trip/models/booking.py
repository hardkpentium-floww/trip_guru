from django.db import models

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey("Hotel", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    destination = models.ForeignKey("Destination", on_delete=models.CASCADE)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    tariff = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name