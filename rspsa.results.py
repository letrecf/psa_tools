# -*- coding: utf-8 -*-
import codecs
import os
from . import helpers as h

UTF8 = "utf-8"


class mcs(object):
    def __init__(self):
        self.analysis = ""
        self.position = 0
        self.value = 0.0
        self.origin = ""
        self.events = []


class reader(object):

    def __init__(self, model, path):
        self.work_dir = path
        self.encoding = UTF8
        self.model = model

    def __iter_files(self, fu, ext):
        for f in os.listdir(self.work_dir):
            if f.endswith(ext):
                print(("Reading %s..." % f))
                with codecs.open(
                        os.path.join(self.work_dir, f),
                        "r",
                        encoding=self.encoding
                        ) as fo:
                    fu(fo)

    def __read_fre_file(self, f):
        # skip until *EVENTS* line
        s = ""
        while not(s == "*EVENTS*"):
            s = f.readline().strip()
        while True:
            s = f.readline()
            if (not s) or (s.strip() == ""):
                break
            name = s[:20].strip()
            value = h.get_float(s[20:].strip())
            origin = os.path.basename(f.name)
            yield (name, value, origin)

    def get_event_data(self):
        self.__iter_files(self.__read_fre_file, ".FRE")

    EventValues = property(
        fget=get_event_data,
        doc="Event probability/frequency values via iterator"
        )

    def parse_mcs_row(self, s):
        return [i.strip() for i in [s[0:6], s[6:17], s[24:46], s[46:69]]]

    def read_mcs_file(self, f):
        skip = lambda x: h.skip_read(f, x)
        # header
        skip(4)
        prj = h.get_value(f.readline(), "Project        : ")
        # check if result belongs to the expected model
        if prj != self.model:
            print("WARNING: file <%s> is ignored because it belongs to different model '%s'" % (f.name,prj))
            return
        skip(1)
        aname = h.get_value(f.readline(), "Top event    : ")
        skip(2)
        avalue = h.get_float(h.get_value(f.readline(), "Frequency = "))
        skip(4)
        # mcs
        mcs_count = 0
        mcs_add = []
        o = mcs()
        isInit = False
        while True:
            try:
                sline = next(f)
                if not(sline):
                    if isInit:
                        yield o
                    break
                expr = self.parse_mcs_row(sline)
                if expr[0] == "" and expr[2] == "":
                    if isInit:
                        yield o
                    break
                if expr[0] == "":
                    mcs_add = expr[2:]
                else:
                    # emit cached
                    if isInit:
                        yield o
                    # new mcs
                    mcs_count += 1
                    if int(expr[0]) == mcs_count:
                        o = mcs()
                        o.position = mcs_count
                        o.value = float(expr[1])
                        o.analysis = aname
                        o.origin = os.path.basename(f.name)
                        isInit = True
                        mcs_add = [m for m in expr[2:] if m]
                    else:
                        raise RuntimeError("MCS index is out of sync")
                    o.events += mcs_add
            except StopIteration:
                if isInit:
                    yield o
                break
        print(("--> found %i" % mcs_count))

    def get_mcs(self):
        self.__iter_files(self.read_mcs_file, ".MCS")

    MCS = property(
        fget=get_mcs,
        doc="MCS via iterator"
        )