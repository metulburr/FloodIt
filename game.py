#!/usr/bin/env python

import pygame as pg
from data.main import main
import data.tools
import argparse
import sys

CAPTION = 'Flood It'

parser = argparse.ArgumentParser(description='{} Arguments'.format(CAPTION))
parser.add_argument('-c','--clean', action='store_true', 
    help='Remove all .pyc files and __pycache__ directories')
parser.add_argument('-f' , '--fullscreen', action='store_true',
    help='start program with fullscreen')
parser.add_argument('-d' , '--difficulty', default='medium',
    help='where DIFFICULTY is one of the strings [hard, medium, easy], set AI difficulty, default is medium, ')
parser.add_argument('-s' , '--size', nargs=2, default=[500,400], metavar=('WIDTH', 'HEIGHT'),
    help='set window size to WIDTH HEIGHT, defualt is 800 600')
args = vars(parser.parse_args())

if __name__ == '__main__':
    accepted_difficulty = ['hard', 'medium', 'easy']
    
    if args['difficulty']:
        diff = args['difficulty'].lower()
        if diff in accepted_difficulty:
            difficulty = diff
        else:
            print('{} is not a valid difficulty option, {}'.format(diff, accepted_difficulty))
            sys.exit()
    if args['size']:
        size = args['size']
        
    if args['clean']:
        data.tools.clean_files()
    else:
        settings = { #dict gets update to control class
            'fullscreen':args['fullscreen'],
            'difficulty':difficulty,
            'size'      :size,
            'caption'   :CAPTION,
            'resizable' :False,
        }
        print(settings)
        main(**settings)
    pg.quit()

