import os

RRDPATH = 'rrdtool/'
PRERIODS = {'1d': ['end-1d','Daily'], '1w': ['end-1w','Weekly'], '1m': ['end-1m','Monthly']}
METRICS = ['cpu','mem','task']
SERVICES = ['blocs-pro']