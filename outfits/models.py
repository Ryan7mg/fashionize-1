from django.db import models
from django.conf import settings

def user_directory_path(instance, filename):
    # upload MEDIA_ROOT/username/outfit_images
    return '{0}/outfit_images/{1}'.format(instance.owner.username, filename)
class Outfit(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='outfits')
    name = models.CharField(max_length=100)
    top = models.ForeignKey('closet.Clothing', on_delete=models.SET_NULL, null=True, related_name='outfit_tops', limit_choices_to={'type': 'top'})
    bottom = models.ForeignKey('closet.Clothing', on_delete=models.SET_NULL, null=True, related_name='outfit_bottoms', limit_choices_to={'type': 'bottom'})
    shoe = models.ForeignKey('closet.Clothing', on_delete=models.SET_NULL, null=True, related_name='outfit_shoes', limit_choices_to={'type': 'shoe'})
    image = models.ImageField(upload_to=user_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

