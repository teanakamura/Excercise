#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot

print(matplotlib.__dict__.keys())
print(len(matplotlib.__dict__.keys())) # 190
print(len(matplotlib.pyplot.__dict__.keys())) #254
print(len(matplotlib.pyplot.matplotlib.__dict__.keys())) #190
#print(len(matplotlib.pyplot.pyplot.__dict__.keys())) #error
print(len(matplotlib.pyplot.cycler.__dict__.keys())) #0
print(len(matplotlib.pyplot.np.__dict__.keys())) #621
print(globals())
print(locals())


# from matplotlib import pyplot
#
# print(len(pyplot.__dict__.keys())) #254
# print(len(pyplot.matplotlib.__dict__.keys())) #190
# #print(len(pyplot.matplotlib.cycler__dict__.keys())) #error
# print(len(pyplot.cycler.__dict__.keys())) #0
# print(globals())
# print(locals())


# import matplotlib
#
# print(globals())
# print(locals())
# print(__package__)
