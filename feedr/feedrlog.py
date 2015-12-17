# -*- coding: utf-8 -*-

import logging
import logging.handlers

class Flogger:
   LOG_FILENAME='feedr.log'
   formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   
   def __init__(self):
      # Set up a specific logger with our desired output level
      self.flogger = logging.getLogger('feedr')
      self.flogger.setLevel(logging.DEBUG)   
      
      # Add the log message handler to the logger
      self.handler = logging.handlers.RotatingFileHandler(self.LOG_FILENAME, maxBytes=20000, backupCount=10)
      self.handler.setLevel(logging.DEBUG)

      # create a logging format
      self.handler.setFormatter(self.formatter)
            
   def __del__(self):
      pass
      #print(self)
      #logging.shutdown()
   
   #remember to pass self otherwise you will get an error...
   def info(self, message):
      self.flogger.addHandler(self.handler)      
      
      self.flogger.info(message)
      
      self.flogger.removeHandler(self.handler)
      #self.handler.close()      
      
   def warning(self, message):
      self.flogger.addHandler(self.handler)      
      
      self.flogger.warning(message)

      self.flogger.removeHandler(self.handler)         
      #self.handler.close()
            
   def debug(self, message):
      self.flogger.addHandler(self.handler)      
      
      self.flogger.debug(message)
      
      self.flogger.removeHandler(self.handler)
      #self.handler.close()        
   
