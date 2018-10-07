# # -*- coding: utf-8 -*-
# from setuptools import setup
# import py2exe

# # name, description, version등의 정보는 일반적인 setup.py와 같습니다.
# setup(name="test_syncn",
#       description="SyncN Windows Program",
#       version="0.0.1",
#       windows=[{"script": "SyncN.py"}],
#       options={
#           "py2exe": {
#               # PySide 구동에 필요한 모듈들은 포함시켜줍니다.
#               "includes": ["PyQt5.QtCore",
#                            "PyQt5.QtGui",
#                            "PyQt5.QtWidgets",
#                            "sys",
#                            "os",
#                            "json",
#                            "requests",
#                            "time",
#                            "Lib",
#                            "pydash",
#                            "sqlite3",
#                            "uuid",
#                            "re",
#                           ],
#           }
#       })
# setup.py (filename은 편할대로 하세요.)
import sys
from cx_Freeze import setup, Executable

setup(
		name="Demo",
		version="1.0",
		description = "SyncN test version",
		author = "syncn",
		executables = [Executable("E:\\Project\\Agent\\SyncN.py")])