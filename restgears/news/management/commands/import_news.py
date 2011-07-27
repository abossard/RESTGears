import urllib
import re
import urllib2
import string
import sys
from BeautifulSoup import BeautifulSoup
import datetime
from django.core.management.base import BaseCommand
from django.utils.encoding import smart_str, smart_unicode
from django.template.defaultfilters import slugify
import logging
log = logging.getLogger(__name__)

from news.models import Entry

user_agent = 'Mozilla/5 (Solaris 10) Gecko'
headers = { 'User-Agent' : user_agent }
site_url = 'http://www.powerfood.ch/'
day_length = datetime.timedelta(1)-datetime.timedelta(microseconds=1)

def get_the_soup(uri, headers=headers):
    return BeautifulSoup(get_the_bytes(uri, headers))

def get_the_bytes(uri, headers=headers):
    request = urllib2.Request(uri, None, headers)
    response = urllib2.urlopen(request)
    return response.read()

def absolutize_url(base, url):
    if url.startswith('http'):
        return url
    if url.startswith('/'):
        return '/'.join(base.split('/')[:3]) + url
    return '/'.join(base.split('/')[:-1])+'/' + url 
        

class Command(BaseCommand):
    args = ''
    help = 'Import news Items from the Powerfood Website'
    #values = {'s' : sys.argv[1] }
    #data = urllib.urlencode(values)
    def handle(self, *args, **options):
        log.info('Loading News form "%s"...\n' % site_url)
        soup = get_the_soup(site_url)
        result = soup.find('td',text=re.compile('Latest News'))
        for newslink in result.parent.parent.parent.parent.findAll('a'):
            external_key = href = absolutize_url(site_url, newslink['href'].strip().split('?')[0])
            
            date, title = smart_unicode(newslink.string).split(' - ') 
            day, month, year = date.split('.')
            day_start = datetime.datetime(int(year), int(month), int(day))
            #day_end = day_start + day_length
            #print day_start, day_end, title, href
            #newsentry = Entry.objects.filter(publish_on__range=(day_start, day_end))
            
            #load content
            content_soup = get_the_soup(href)
            content_td = content_soup.find('td', {'class':'main'})
            content = ''
            for node in content_td.contents:
                content += str(node)
            content = smart_str(content)
              
                
            attrs = {'name': title, 
                     'content': content, 
                     'publish_on':day_start,
                     'slug': slugify(title)[:50],}
            
            #find images
            images = content_td.findAll('img',)
            if images:
                image_url = absolutize_url(href, images[0]['src'])
                attrs.update({
                              'image_url': '',
                              'thumb_image_url':image_url,
                              })

            filter_attrs = { 'external_key':external_key,}
            rows = Entry.objects.filter(**filter_attrs).update(**attrs)
            
            if not rows:
                attrs.update(filter_attrs)
                obj = Entry.objects.create(**attrs)
                obj.save()
                log.info('Successfully created News Entry "%s" (%s)' % (title, day_start))
            else:
                log.info('Successfully updated News Entry "%s" (%s)' % (title, day_start))


