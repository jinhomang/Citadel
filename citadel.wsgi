# -*- coding: utf-8 -*-

activate_this = '/Users/jinho/Citadel/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, '/Users/jinho/Citadel')

from main import app as application