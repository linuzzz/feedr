# -*- coding: utf-8 -*-

import feedparser
import json


from .models import Source, Feed

from datetime import datetime

from feedr.feedrlog import Flogger

def refresh():
   flogger = Flogger()
   flogger.info("refreshing...")
      
   source = Source.objects.all()
         
   news = 0   
   for s in source:
      url = s.url 
      
      #bandwidth saving with etag and last-modified (http headers)
      if s.etag != "":
         feed = feedparser.parse(url, etag=s.etag)
      elif s.modified != "":
         feed = feedparser.parse(url, modified=s.modified)
      else:
         feed = feedparser.parse(url)
           
      if feed.has_key('etag'):
         s.etag = feed.etag
         s.save()
      if feed.has_key('modified'):
         s.modified = feed.modified
         s.save()

                     
      #feed status == 200 to load new items
      #feed status == 301 permanently moved
      if feed.has_key('status'):
         if feed.status == 301:
            flogger.warning("feed url permanently moved, please check new url:" + feed.href)
         elif feed.status != 200:
      	   flogger.debug("feed already loaded - {} - {} ".format(feed.href,feed.status))
      	   continue
      else:
         flogger.warning("Error loading source feed, please check url:" + feed.href)
         
      for f in feed.entries:
         #some feeds doesn't have a link...pass
         if f.has_key('link'):
            pass
         else:
            continue
            
         #verifico che l'articolo non sia gia presente
         try:
            old = Feed.objects.get(link=f.link)
            #already in db...go to next article
            continue
         except:
            news = news + 1
         
         #datetime in formato che sqlite gradisce
         if f.has_key('published_parsed'):         
            p = f.published_parsed
            pdate = datetime(p[0], p[1], p[2], p[3], p[4])
            pubDate = datetime.strftime(pdate,"%Y-%m-%dT%H:%M")
         elif f.has_key('updated_parsed'):
            p = f.updated_parsed
            pdate = datetime(p[0], p[1], p[2], p[3], p[4])
            pubDate = datetime.strftime(pdate,"%Y-%m-%dT%H:%M")
         else:
            pubDate = datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M")
                        
         mylist = []
         mylist.append(f.description)
         mylist.append(f.summary)
         try:
            mylist.append(f.content[0]['value'])
         except:
            mylist.append("")
            
         #get the longest text between summary, description and content: differents feeds has different fields         
         contenuto = max(mylist, key=len)
            
         feed = Feed(source=s, title=f.title, summary=f.summary, content=contenuto, link=f.link, pubDate=pubDate, read=False, favorite=False)
         feed.save()
   
   flogger.info(str(news) + ' new feeds!!!')
   
   response_data = {}
   response_data['result'] = 'True'
   response_data['news'] = str(news)
   json_data = json.dumps(response_data)
   return json_data
