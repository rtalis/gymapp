# -*- coding: utf-8 -*-

import appuifw
import e32
import os
import csv
from graphics import *
import itertools
 
MAIN_DIR = "E:\\data\\gymapp"
MENU_ENTRIES = [u""]
SELECTED = 1
CSV_DATA = []


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
    try:
        csvdir = u"E:\\data\\gymapp\\workouts.csv"
        f = open(csvdir, 'rb')
        lines = itertools.islice(f, 1, None)
        reader = csv.reader(lines)
    except:
        appuifw.note(u"Error opening data, choose a new csv file", "error")
        selected_path = file_selector()
        f = open(selected_path, 'rb')
        lines = itertools.islice(f, 1, None)
        reader = csv.reader(lines)
        #header = ['treino','nome','series','repetições','carga','biset','intervalo','anotação']
        w = open(selected_path, 'wb')
        writer = csv.writer(w)
        #writer.writerow(header)
        writer.writerows(reader)
        w.close()
        appuifw.note(u"Saved in E: > data > gymapp", "conf")
        #shutil.copy(selected_path, csvdir)
    return reader

def details(exercices, series, load, repetitions):
    data = [(u'Exercices','text', exercices),
            (u'Series','text', series),
            (u'Load','text', load),
            (u'Repetitions','text', repetitions)]
    flags = appuifw.FFormEditModeOnly
    f = appuifw.Form(data, flags)
    #f.save_hook = csv_writter
    f.execute()
    

def handle_selected():
    counter = 0
    index = lb.current()
    for workout in CSV_DATA:
        if workout[0] == SELECTED:
            if index == counter:
                details(workout[1], workout[2], workout[3], workout[4])
        counter += counter


def refresh_menu():
    #os.makedirs(MAIN_DIR, mode=0o777, exist_ok=False)
    #if not os.path.exists(MAIN_DIR + "workouts.csv"):
    for workout in CSV_DATA:
        if int(workout[0]) == SELECTED:
            MENU_ENTRIES.append(workout[1].decode('utf-8'))
    lb.set_list(MENU_ENTRIES)

def exit_key_handler():
    app_lock.signal()

def handle_tab(tab_index):
    global SELECTED
    SELECTED = tab_index
    refresh_menu()

def create_tabs():
    counter = 1
    tabs = []
    tabs.append(unicode(str(counter)))
    check = '1'
    for workout in CSV_DATA:
        if not str(workout[0]) == check:
            counter += counter
            check = str(workout[0])
            tabs.append(unicode(str(counter)))
    print(tabs)
    return tabs


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
refresh_menu()

app_lock.wait()

