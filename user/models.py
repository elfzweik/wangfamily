from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatar', blank=True,
    )
    
    def __str__(self):
        return "<Profile>: for %s" % (self.user.username)
    
def get_fullname_or_username(self):
    if self.first_name.encode('utf-8').isalpha() and self.last_name.encode('utf-8').isalpha():
        return "%s %s" % (self.first_name, self.last_name) if (self.first_name !='' or self.last_name != '') else self.username
    return "%s%s" % (self.last_name, self.first_name) if (self.first_name !='' or self.last_name != '') else self.username
User.get_fullname_or_username = get_fullname_or_username

def is_moderator(self):
    return self.has_perm('wagtailadmin.access_admin')
User.is_moderator = is_moderator
        