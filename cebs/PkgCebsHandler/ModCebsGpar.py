'''
Created on 2018/7/21

@author: Administrator
'''

####!/usr/bin/python3.6
#### -*- coding: UTF-8 -*-

import random
import sys
import time
import json
import os
import re
import urllib
import http
import socket

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot

#Local include
from cebsMain import *
from PkgCebsHandler import ModCebsCom
from PkgCebsHandler import ModCebsCfg
from PkgCebsHandler import ModCebsVision
from PkgCebsHandler import ModCebsMoto
from PkgCebsHandler import ModCebsCtrl


class classGparProcess(object):
    def __init__(self, father):
        super(classGparProcess, self).__init__()
        self.identity = None;
        self.gparForm = father
        self.objInitCfg=ModCebsCfg.ConfigOpr();
    

    