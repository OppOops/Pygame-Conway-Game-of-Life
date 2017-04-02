#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import glob, sys
from distutils.core   import setup
from py2exe import build_exe

class py2exe_MyPatch(build_exe.py2exe, object):
	def plat_prepare(self):
		super(py2exe_MyPatch, self).plat_prepare()
		self.dlls_in_exedir.extend(["tcl85.dll","tk85.dll"])


revision = "1.1.0.0"
if sys.platform == 'win32':
  if len(sys.argv) == 1:
      sys.argv.append("py2exe_MyPatch")
      sys.argv.append("-q")
 
  setup(
	cmdclass={"py2exe_MyPatch" : py2exe_MyPatch},	
    platforms        = ['Windows'],
    version          = revision,
    description      = "Conway's Game of Life",
    name             = "Conway's Game of Life", 
    long_description = "Conway's Game of Life",
    url              = "https://github.com/OppOops/",     
    maintainer       = 'oppoops',
    maintainer_email = 'oppoops@gmail.com',
    zipfile          = None, 
    windows = [
      {
        "script": "Main.py",
      }
    ],
    data_files = [],
    options = {
      "py2exe_MyPatch":{
        "compressed"  : 1,
        "includes"    : ["sip", "Queue", "Tkinter", "pygubu.builder.tkstdwidgets",
                                              "pygubu.builder.ttkstdwidgets",
                                              "pygubu.builder.widgets.dialog",
                                              "pygubu.builder.widgets.editabletreeview",
                                              "pygubu.builder.widgets.scrollbarhelper",
                                              "pygubu.builder.widgets.scrolledframe",
                                              "pygubu.builder.widgets.tkscrollbarhelper",
                                              "pygubu.builder.widgets.tkscrolledframe",
                                              "pygubu.builder.widgets.pathchooserinput"],
        "optimize"    : 2,
        "excludes": ["readline"],
        "bundle_files": 1 
      },
    }
  )
