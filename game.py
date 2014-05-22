#!/usr/bin/env python

import pygame as pg
from data.main import main
import data.tools
import argparse
import sys
from data.tools import DB

ACCEPTED = ['hard', 'medium', 'easy']
DEFAULT = { 
    'fullscreen':False,
    'difficulty':'medium',
    'size'      :(500, 400),
    'caption'   :'Flood It',
    'resizable' :False,
}

parser = argparse.ArgumentParser(description='{} Arguments'.format(DEFAULT['caption']))
parser.add_argument('-c','--clean', action='store_true', 
    help='Remove all .pyc files and __pycache__ directories')
'''
parser.add_argument('-f' , '--fullscreen', action='store_true',
    help='start program with fullscreen')
parser.add_argument('-d' , '--difficulty', default='medium',
    help='where DIFFICULTY is one of the strings [hard, medium, easy], set AI difficulty, default is medium, ')
parser.add_argument('-s' , '--size', nargs=2, default=[500,400], metavar=('WIDTH', 'HEIGHT'),
    help='set window size to WIDTH HEIGHT, defualt is 800 600')
'''
args = vars(parser.parse_args())

if __name__ == '__main__':
    '''
    if args['difficulty']:
        diff = args['difficulty'].lower()
        if diff in ACCEPTED:
            difficulty = diff
        else:
            print('{} is not a valid difficulty option, {}'.format(diff, ACCEPTED))
            sys.exit()
    if args['size']:
        size = args['size']
    '''
    if args['clean']:
        data.tools.clean_files()
    else:
        if not DB.exists():
            DB.save('settings', DEFAULT)
            d = DEFAULT
        else:
            d = DB.load('settings')
        print(d)
        main(**d)
    pg.quit()

