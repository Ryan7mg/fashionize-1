from django.db import models
from django.conf import settings


def user_directory_path(instance, filename):
    # upload MEDIA_ROOT/username/clothing_type/filename
    return '{0}/{1}/{2}'.format(instance.owner.username, instance.type, filename)
class Clothing(models.Model):

    TYPE_CHOICES = (
        ('top', 'Top'),
        ('bottom', 'Bottom'),
        ('shoe', 'Shoe'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clothings')
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=user_directory_path)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

