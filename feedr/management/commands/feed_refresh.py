# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from feedr.feedrefresh import refresh

class Command(BaseCommand):
   help = 'Refresh command to fecth new feeds by scheduling cron jobs'

   '''
   def add_arguments(self, parser):
      parser.add_argument('feed_id', nargs='+', type=int)
   '''

   def handle(self, *args, **options):
      r = refresh()
      #print(r)
      #source = Source.objects.all()
   
      #for s in source:
         #print(s.url)
         
      
