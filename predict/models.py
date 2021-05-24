from django.db import models


class History(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    corona = models.CharField(max_length=50)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name + ' ' + self.email+ ' ' + self.corona