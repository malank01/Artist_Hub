from django.db import models
from django.utils import timezone


# Create your models here.
class User(models.Model):
	name=models.CharField(max_length=100)
	email=models.EmailField()
	password=models.CharField(max_length=100)
	permission=models.BooleanField(default=False)
	usertype=models.CharField(max_length=100,default="customer")

	def __str__(self):
		return self.name

class Artist(models.Model):
	artist_type=(
			("singer","singer"),
			("dancer","dancer"),
			("photographer","photographer"),
			("Writer","writer"),
			("standup","standup"),
			("influencer","influencer")
		)
	artist_artist=models.ForeignKey(User,on_delete=models.CASCADE)
	artist_name=models.CharField(max_length=100)
	artist_price=models.PositiveIntegerField()
	artist_desc=models.TextField()
	artist_pic=models.ImageField(upload_to="artist_pic/")
	artist_type=models.CharField(max_length=100,choices=artist_type)

	def __str__(self):
		return self.artist_name

class Contacts(models.Model):
	contact_customer=models.ForeignKey(User,on_delete=models.CASCADE)
	contact_name=models.CharField(max_length=100)
	contact_email=models.EmailField()
	contact_subject=models.CharField(max_length=100)
	contact_message=models.TextField()

	def __str__(self):
		return self.contact_name


class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('Kishor%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)


class Booking(models.Model):

	user=models.ForeignKey(User,on_delete=models.CASCADE)
	artist=models.ForeignKey(Artist,on_delete=models.CASCADE)
	artist_price=models.PositiveIntegerField()
	artist_name=models.CharField(max_length=100)
	date=models.DateTimeField(default=timezone.now)
	payment_status=models.BooleanField(default=False)

	def __str__(self):
		return  self.user.name