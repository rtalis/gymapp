# -*- coding: utf-8 -*-

import appuifw
import e32
import os
import csv
import time
import itertools
import shutil
 
MAIN_DIR = u"E:\\data\\gymapp"
MENU_ENTRIES = [u""]
SELECTED = 1
CSV_DATA = []
FILE = None

def file_selector():
    csvdir = u"E:\\"
    selected_file = u""
    selected_path = csvdir + selected_file
    while os.path.isfile(selected_path) == False:
        if os.path.isdir(selected_path):
            csvdir = csvdir + selected_file
        files = map(unicode, os.listdir(csvdir))
        index = appuifw.selection_list(files)
        if index == None:
            break
        else:
            selected_file = files[index]

        if csvdir[-1] != "\\":
            csvdir = csvdir + "\\"

        selected_path = csvdir + selected_file
    return selected_path

def open_data():
    reader = ""
    global FILE
    try:
        csvdir = u"E:\\data\\gymapp\\workouts.csv"
        FILE = open(csvdir, 'rb')
        lines = itertools.islice(FILE, 1, None)
        reader = csv.reader(lines)
        
    except:
        appuifw.note(u"Error opening data, choose a new csv file", "error")
        selected_path = file_selector()

        shutil.copy2(selected_path, csvdir)
        appuifw.note(u"Saved in E: > data > gymapp", "conf")
        open_data()
    return reader

def csv_writter():
    print('TODO saved')
    
def details(exercices, series, load, repetitions):
    data = [(u'Exercices','text', exercices.decode('utf-8')),
            (u'Series','text', series.decode('utf-8')),
            (u'Load','text', load.decode('utf-8')),
            (u'Repetitions','text', repetitions.decode('utf-8'))]
    flags = appuifw.FFormEditModeOnly
    f = appuifw.Form(data, flags)
    f.save_hook = csv_writter
    f.execute()
    

def handle_selected():
    counter = 0
    index = lb.current()
    for workout in CSV_DATA:
        if int(workout[0]) == SELECTED:
            if index == counter:
                try:
                    details(workout[1], workout[2], workout[3], workout[4])
                except:
                    appuifw.note(u"Not able to show the details of the selected entry", "error")
                break
            counter = counter + 1


def refresh_menu():
    #os.makedirs(MAIN_DIR, mode=0o777, exist_ok=False)
    #if not os.path.exists(MAIN_DIR + "workouts.csv"):
    MENU_ENTRIES = []
    for workout in CSV_DATA:
        if int(workout[0]) == SELECTED:    
            MENU_ENTRIES.append(workout[1].decode('utf-8'))
    lb.set_list(MENU_ENTRIES, 0)

def exit_key_handler():
    app_lock.signal()

def handle_tab(tab_index):
    global SELECTED
    SELECTED = tab_index + 1 #exercices start from 1; tabs index start from 0
    refresh_menu()

def create_tabs():
    tabs = []
    tabs.append(unicode(1))
    check = '1'
    for workout in CSV_DATA:
        if not str(workout[0]).decode('utf-8') == check:
            tabs.append(unicode(str(workout[0])))
            check = str(workout[0])
    return tabs

def data_update():
    global FILE
    FILE.close()
    shutil.move(unicode(os.path.join(MAIN_DIR, 'workouts.csv')), unicode(os.path.join(MAIN_DIR, 'workouts.csv.bk')))
    appuifw.note(u"Sucessully copied to workouts.csv.bk", "conf")
    open_data()
    
def print_about(): 
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    time.sleep(6)
    refresh_menu()


appuifw.app.screen = "normal"
app_lock = e32.Ao_lock()
data = open_data()
for d in data:
    CSV_DATA.append(d)
tabs = create_tabs()
appuifw.app.set_tabs(tabs, handle_tab)
appuifw.app.title = u'Gymapp'
lb = appuifw.Listbox(MENU_ENTRIES, handle_selected)
appuifw.app.body = lb
appuifw.app.exit_key_handler = exit_key_handler
appuifw.app.menu = [ (u"About", print_about), (u"Update training", data_update),(u"Exit", exit_key_handler)]
refresh_menu()

app_lock.wait()
FILE.close()


