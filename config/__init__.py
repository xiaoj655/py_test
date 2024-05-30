import configparser
import sys, os

cfg = configparser.ConfigParser()
cfg.read(os.path.join(os.path.dirname(__file__) , 'settings.cfg'))
