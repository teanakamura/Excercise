#!/usr/bin/env python
# -*- coding: utf-8 -*-

def templete(x, y, z):
    print(str(x)+"時の"+str(y)+"は"+str(z))
    print("{}時の{}は{}".format(x,y,z))

templete(12, "気温", 22.4)
