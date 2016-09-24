import codecs
import logging

class unstructured_text(object):

  def __init__(self,filepath,logger):
    self.filepath = filepath
    self.logger = logger
    self.encoding = "cp1252"

  def get_header_lines(self,count):
    with open(self.filepath,"r") as fi:
      head = [next(fi).decode(self.encoding) for x in xrange(count)]
    return head

  def idynslice(self,start,terminator_func):
    with open(self.filepath,"r") as fi:
      skipped=0
      while True:
        v=next(fi).decode(self.encoding)
        if skipped<start:
          skipped += 1
        else:
          if terminator_func(v):
            break
          else:
            yield v

  def get_section(self,anchor,skip=0,terminator=""):
    try:
      with open(self.filepath,"r") as fi:
        # find anchor
        anchor_matches=0
        for line in fi:
          decoded_line = line.decode(self.encoding)
          if decoded_line[:len(anchor[anchor_matches])]==anchor[anchor_matches]:
            anchor_matches += 1
            if anchor_matches==len(anchor):
              break 
          elif decoded_line[:len(anchor[0])]==anchor[0]:
            anchor_matches=1
          else:
            anchor_matches=0
        # skip lines after the anchor is found
        skipped=0
        for line in fi:
          if skipped==skip:
            break
          else:
            skipped += 1
        # return if not terminator
        for line in fi:
          decoded_line = line.decode(self.encoding)
          if decoded_line[:len(terminator)]==terminator:
            break
          else:
            yield decoded_line
    except:
      self.logger.exception(("File <%s> cannot be read." % self.filepath))
