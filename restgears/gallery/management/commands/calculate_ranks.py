import logging

from django.core.management import BaseCommand
from django.db.models import F

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
            rank = 1
            for photo_id in Photo.objects.filter(gallery=gallery_id).values_list('id',flat=True).order_by('-votes','-views','-uploaded_on',):
                Photo.objects.filter(pk=photo_id).update(rank=rank)
                log.info('Set ID %s to Rank %s'%(photo_id, rank))
                rank+=1
                
            


