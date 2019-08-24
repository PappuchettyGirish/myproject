from django.db import models
from datetime import datetime
from datetime import date

class userinfo(models.Model):
	website=models.CharField(max_length=30)
	mail=models.CharField(max_length=30)
	name=models.CharField(max_length=30)
	phonenumber=models.IntegerField()


class Userdata(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    status=models.CharField(max_length=50,default="waiting")
    image=models.ImageField(upload_to="profile_image",blank=True,default="profile_image/download.png")
class Messages(models.Model):
	from_username=models.CharField(max_length=50)
	to_username=models.CharField(max_length=50)
	message=models.CharField(max_length=500)
	send_time=models.DateTimeField(auto_now_add=True)
class Friends(models.Model):
	requested_from=models.CharField(max_length=50)
	requested_to=models.CharField(max_length=50)
	status=models.CharField(max_length=50,default="waiting")
