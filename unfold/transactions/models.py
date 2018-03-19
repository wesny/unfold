from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from unfold.users import models as user_models

class Article(models.Model):

    url = models.URLField()
    external_id = models.CharField(max_length=255)
    publisher = models.ForeignKey(user_models.User, on_delete=models.PROTECT, limit_choices_to={'is_publisher': True})
    price = models.DecimalField(max_digits=8, decimal_places=2)
    title = models.CharField(max_length=255)

    # class Meta:
    #     unique_together = (("publisher", "external_id"),)

    def __str__(self):
        return '{}'.format(self.external_id)
      

class Purchase(models.Model):

    buyer = models.ForeignKey(user_models.User, on_delete=models.PROTECT, related_name='%(class)s_buyer')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    article = models.ForeignKey(Article, on_delete=models.PROTECT,)

    class Meta:
        unique_together = (("buyer", "article"),)

    def __str__(self):
        return '{}'.format(self.article)

