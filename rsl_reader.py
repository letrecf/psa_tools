import codecs
import logging

import hanging_indent_data
import unstructured_text

class rsl_reader(object):

  def __init__(self,filepath,logger):
    self.filepath = filepath
    self.logger = logger

  def read_logic(self):
    try:
      input = unstructured_text(self.filepath,self.logger).get_section(anchor=["FAULT TREE LOGIC"],skip=3)
      columns = [
          ("id",  True, 0,13,True),
          ("name",True,13,34,True),
          ("type",True,34,39,True),
          ("item",False,39,61,False),
          ("item",False,61,83,False),
          ("item",False,83,200,False)
        ]
      dat = hanging_indent_data(input,columns,self.logger)
      for item in dat.parse():
        yield item
    except:
      self.logger.exception("Error parsing logic in RSL file")

  def read_events(self):
    equalline = "="*105
    try:
      input = unstructured_text(self.filepath,self.logger).get_section(anchor=[equalline,"EVENTS"],skip=3,terminator=equalline)
      columns = [
          ("name", 0,23),
          ("value",23,36),
          ("model",49,66),
          ("ccf_model",66,200)
        ]
      for line in input:
        o = {}
        for c in self.columns:
          t = (line[c[1]:c[2]]).strip()
          if t:
            o[c[0]]=float(t) if c[0]=="value" else t
        yield o
    except:
      self.logger.exception("Error parsing events in RSL file")
