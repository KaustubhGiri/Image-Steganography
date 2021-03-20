from django.db import models
from django.core.validators import MaxValueValidator
from django.conf import settings
class Document(models.Model):
    message = models.CharField(max_length=255, blank=True)
    image_path = models.ImageField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    encoded_img = models.CharField(max_length=255, blank=True)
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    pin = models.IntegerField(
        
        default=None,
        validators=[
            MaxValueValidator(6),
        ],null=True)
        

    def __str__(self):
        return self.message

class img_steg_enc(models.Model):
    main_img = models.CharField(max_length=255, blank=True)
    cover_img =models.CharField(max_length=255, blank=True)
    user_id_img = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    pin_img = models.IntegerField(
        blank=True,
        validators=[
            MaxValueValidator(6),
           
        ])
    enc_img_steg = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.main_img
