# coding: cp1252
import sys
import os

import cx_Freeze
from cx_Freeze import setup, Executable
base = None

os.environ['TCL_LIBRARY']=r'C:\Python310\tcl\tcl8.6'

os.environ['TK_LIBRARY']=r'C:/Python310/tcl/tk8.6'

if sys.platform=='win32':
    base='Win32GUI'

executables= [cx_Freeze.Executable("TestService.py",base=base)]
# build_exe_options = {"packages": ["os"]}
# if sys.platform == 'win32':
#     base = "Win32GUI"



setup(
    name="RPL",
    version="0.1",
    description="An example wxPython script",
    options={"build_exe": {"packages":["tkinter","threading","time","datetime","json","psycopg2","servicemanager","win32event","win32service","win32serviceutil"]}},
    executables=executables
    )