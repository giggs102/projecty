'''
Created on Aug 22, 2015

@author: dsingh
'''

import ConfigParser

def read_cfg_file():
    config_parser = ConfigParser.RawConfigParser()
    config_file_path = 'cfg.txt'
    config_parser.read(config_file_path)
    return config_parser

if __name__ == '__main__':
    pass