APP_FOLDER = "/var/www/picture-scavenger-hunt/"

import os
import sys
sys.path.insert(0, APP_FOLDER)

activate_this = os.path.join(APP_FOLDER, 'venv/bin/activate_this.py')
#execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(), dict(__file__=activate_this))

from picture_hunt import app as application
