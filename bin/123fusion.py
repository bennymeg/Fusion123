#!/usr/bin/env python

import sys
import fusion123

args = sys.argv
filepath = args[1] if len(args) == 2 else ''

fusion123.main(filepath)