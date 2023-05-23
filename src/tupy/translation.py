import gettext
import os

_translation = gettext.translation('tupy', localedir=os.path.join(os.path.dirname(__file__), 'locale'), 
        languages=['en', 'pt_BR'])
_ = _translation.gettext