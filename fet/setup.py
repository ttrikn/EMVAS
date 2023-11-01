from cx_Freeze import setup, Executable
import sys

sys.setrecursionlimit(100000)
setup(name = "MMSAFET" ,
      version = "0.1" ,
      description = "" ,
      executables = [Executable("silence.py")],
)