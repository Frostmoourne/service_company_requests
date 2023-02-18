from django.db import models


class ServiceRequest(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.PositiveIntegerField(unique=True)
    customer = models.IntegerField()
    request_type = models.CharField(max_length=100)
    request_details = models.TextField()
    status = models.CharField(max_length=100)
    urgency = models.CharField(max_length=100)
    request_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    request_origin = models.CharField(max_length=100)
    customer_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        # Добавляем номер заявки
        if self.pk is None:
            self.request_number = ServiceRequest.objects.aggregate(models.Max('number'))['number__max'] + 1

        super().save(*args, **kwargs)
