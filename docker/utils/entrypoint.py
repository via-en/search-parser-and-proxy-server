#!/usr/bin/python3
# -*- coding: utf-8 -*-
from time import sleep

import sys
sys.path.append("/usr/src/app/")
sys.path.append("/usr/src/app/project")
from proccess.main import SomeTaskManager
from crawler_base.run import main

if __name__ =="__main__":

    main(SomeTaskManager)

    while True:
        sleep(10)
