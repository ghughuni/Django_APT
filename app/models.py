from django.db import models


class Links(models.Model):
    name = models.CharField(max_length=220, blank=True)
    url = models.URLField()
    img_url = models.URLField()
    current_price = models.FloatField(blank=True)
    old_price = models.FloatField(default=0)
    price_difference = models.FloatField(default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
