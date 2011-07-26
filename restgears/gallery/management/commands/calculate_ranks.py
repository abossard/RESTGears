import logging

from django.core.management import BaseCommand

log = logging.getLogger(__name__)

from gallery.models import Gallery, Photo

class Command(BaseCommand):
    args = ''
    help = 'Calculate all Ranks on all galleries'
    #values = {'s' : sys.argv[1] }
    #data = urllib.urlencode(values)
    def handle(self, *args, **options):
        log.info('Starting to calculate the ranks...\n')
        gallery_ids = Gallery.objects.values_list('id',flat=True)
        for gallery_id in gallery_ids:
            photo_ids = Photo.objects.filter(gallery=gallery_id).values_list('id',flat=True).order_by('-votes','-views','-uploaded_on',)
            log.info(photo_ids)


