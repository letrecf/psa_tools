import codecs
import logging

class multiline_data(object):

  def __init__(self,iter_obj,logger):
    self.iterator = iter_obj
    self.logger = logger

  def parse(self,is_head_line):
    try:
      o = []
      isInit = False
      for line in self.iterator:
        if is_head_line(line):
          if isInit:
            yield o
          o=[line]
          isInit=True
        else:
          o.append(line)
      if isInit:
        yield o
    except:
      self.logger.exception("Error parsing multi-line data")
