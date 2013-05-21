#!/usr/bin/env python

import os
from custom_configparser import MyConfigParser 
import subprocess
import gobject
import gtk
import appindicator
import re

menu = gtk.Menu()
app_dir = os.path.dirname(os.path.abspath(__file__))
config_file =  app_dir + '/config'

# checks if config file exists or not, if not then creates one in app dir.
if not os.path.exists(config_file):
    with open(config_file, 'w+') as cf:
        header = """# Use 'README' for help on how to setup configuration.
        
[files]


[scripts]"""
        cf.write(header)

config = MyConfigParser()
config.read(config_file)
file_list = config.valid_items('files')
script_list = config.valid_items('scripts')

def menu_item_creator(item_list, action):
    global menu
    for item in item_list:
        menu_item = gtk.MenuItem(item[0])
        menu_item.connect('activate', action, item[1])
        menu.append(menu_item)

def file_action(widget, file):
    subprocess.call(['gvim', file])

def script_action(widget, script):
    subprocess.call(script)

def indicator_quit(widget, data=None):
    gtk.main_quit()

def run():
    global menu

    indicator = appindicator.Indicator('scripts-indicator',
                                app_dir + '/ui/indicator-icon.png',
                                appindicator.CATEGORY_APPLICATION_STATUS)
    indicator.set_status(appindicator.STATUS_ACTIVE)

    if file_list:
        menu_item_creator(file_list, file_action)
        sep = gtk.SeparatorMenuItem()
        menu.append(sep)

    if script_list:
        menu_item_creator(script_list, script_action)
        sep = gtk.SeparatorMenuItem()
        menu.append(sep)

    # create quit menu item
    quit_menu_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    quit_menu_item.connect('activate', indicator_quit)
    menu.append(quit_menu_item)

    menu.show_all()

    indicator.set_menu(menu)

    gtk.main()
