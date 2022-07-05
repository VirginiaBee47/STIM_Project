import sys
import argparse

parser = argparse.ArgumentParser(description='Test the arghook module')

parser.add_argument('-a', '--archive', action='store_true', help='Test the archive flag')
parser.add_argument('-v', '--verbose', action='store_true', help='Test the verbose flag')