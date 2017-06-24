#!/usr/bin/python

from optparse import OptionParser
import sys

parser = OptionParser()
parser.add_option("-f", "-o", "--file", "--output", type="string", dest="filename")
parser.add_option("-r", "--resolution", type="string", dest="resolution")
parser.add_option("-s", "--samples", type="int", dest="samples")
parser.add_option("-d", "--depth", type="int", dest="depth")
parser.add_option("-S", "--seed", type="int", dest="seed")

options, args = parser.parse_args()
print(options)
print(args)
