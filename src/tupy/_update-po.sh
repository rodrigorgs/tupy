#!/bin/bash

xgettext -d tupy -o locale/tupy.pot gui.py
msgmerge -U locale/pt_BR/LC_MESSAGES/tupy.po locale/tupy.pot
msgmerge -U locale/en/LC_MESSAGES/tupy.po locale/tupy.pot
msgfmt locale/pt_BR/LC_MESSAGES/tupy.po --output-file=locale/pt_BR/LC_MESSAGES/tupy.mo
msgfmt locale/en/LC_MESSAGES/tupy.po --output-file=locale/en/LC_MESSAGES/tupy.mo