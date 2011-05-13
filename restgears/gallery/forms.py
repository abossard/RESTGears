from django.forms import ModelForm
from restgears.gallery.models import Photo


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
