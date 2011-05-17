from django.forms import ModelForm
from gallery.models import Photo


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
