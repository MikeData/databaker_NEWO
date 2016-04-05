# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 17:48:22 2015

@author: Mike
"""

import tkFileDialog
import Tkinter as tk


def get_file1():
    global file1 
    path = tkFileDialog.askopenfilename(filetypes=[("Excel Spreadsheet","*.xls")])
    file1.set(path)    
        
def run():
    runfiles(file1.get())

def runfiles(source):
    
    import shutil
    import os    

    # Get the directory of the selected file
    # Compare length with both \ and / to cover possible other os use
    filepath = source[: source.rfind('\\')]
    if len(source[: source.rfind('/')]) < len(filepath):
        filepath = source[: source.rfind('/')]
    filepath = filepath.replace('/', '\\')    # Swap / for \ so we can compare the two

    # Compare the current working directory with the above.
    # If its the same, we dont want to move or split anything - the files already in the working directory!
    if filepath != os.getcwd():    
        shutil.move(source, os.getcwd())    
    
    # now get the name out of it    

    filename = source.split('/')
    filename = filename[len(filename)-1]
    filename = '"' + filename + '"'

    """
    Now the flename is sorted. This part is just bulding a list of commands, then executing them
    """
    linestolaunch = []
    
    # databaking
    linestolaunch.append('bake --preview ConstNOT1.py ' + filename)
    linestolaunch.append('bake --preview ConstNOT234.py ' + filename)
    linestolaunch.append('bake --preview ConstNOT5.py ' + filename)
    linestolaunch.append('bake --preview ConstNOT6.py ' + filename) 
    
    # Take the quotes back off
    filename = filename[1:-1]  
    
    #Get rid of file extension
    filename = filename[:-4]
    
    print linestolaunch
    
    linestolaunch.append('python transform1.py "data-' + filename + '-ConstNOT1-.csv" NOT1')
    linestolaunch.append('python transform234.py "data-' + filename + '-ConstNOT234-.csv" NOT234')
    linestolaunch.append('python transform5.py "data-' + filename +  '-ConstNOT5-.csv" NOT5')
    linestolaunch.append('python transform6.py "data-' + filename +  '-ConstNOT6-.csv" NOT6')    

    # Run the commands in turn
    import subprocess as sp     
    for each in linestolaunch:
                p = sp.Popen(each, shell=True)
                p.communicate()

    print ''    
    print ''
    print '*************'
    print ''
    print 'Processing Complete. Either select another file of close this window to exit.'
    print ''
    
    
    
"""
THE FOLLOWING CODE IS JUST FOR THE GUI
"""
            
root = tk.Tk()
file1 = tk.StringVar()

description = 'TRANSFORM TOOL - New Orders in Construction, V1.0'
label = tk.Label(root, text=description)
label.pack()

description = 'INFO - Just works, nothing of note out of the ordinary.'
label = tk.Label(root, text=description)
label.pack()

tk.Button(text='Select Source File', command=get_file1).pack()
tk.Label(root, textvariable=file1).pack()

tk.Button(text='Databake, Transform & Validates Files', command=run).pack()
# tk.Button(text='Compare', command=convert).pack()
root.mainloop()



