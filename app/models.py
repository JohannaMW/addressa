import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

PLAN = ((1, '500/Monat (20 Euro)'),
            (2, '1000/Monat (30 Euro)'),
            (3, '5000/Monat (50 Euro)'),
            (4, '10000/Monat (80 Euro)'),
            (5, '25000/Monat (150 Euro)'),
            (6, '50000/Monat (280 Euro)'),
            (7, '100000/Monat (450 Euro)'),
            (8, 'unlimited (900)')
        )

STATUS = ((1, 'abgelaufen'),
            (2, 'aktiv'))

# Create your models here.
class Client(AbstractUser):
    website = models.CharField(max_length=250)
    company = models.CharField(max_length=200)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    class Meta:
        db_table = 'auth_user'

    def __unicode__(self):
        return u"{}".format(self.username)


class Subscription(models.Model):
    plan = models.IntegerField(choices=PLAN, null=True, blank=True)
    status = models.IntegerField(choices=STATUS, null=True, blank=True)
    usage = models.IntegerField()
    start = models.DateField()
    end = models.DateField()
    owner = models.ForeignKey(Client, related_name="subscription")

    def __unicode__(self):
        return u"{}".format(self.plan)


class AccountContact(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=250)
    company = models.CharField(max_length=250)
    account_holder = models.ForeignKey(Client, related_name="account_contact")

    def __unicode__(self):
        return u"{}".format(self.first_name)


class SecretKey(models.Model):
    label = models.CharField(max_length=250)
    auth_id = models.CharField(max_length=250)
    auth_token = models.CharField(max_length=250)
    owner = models.ForeignKey(Client, related_name="secret_key")

    def __unicode__(self):
        return u"{}".format(self.label)


class WebsiteKey(models.Model):
    auth_id = models.CharField(max_length=250)
    host = models.CharField(max_length=250)
    owner = models.ForeignKey(Client, related_name="website_key")

    def __unicode__(self):
        return u"{}".format(self.host)
