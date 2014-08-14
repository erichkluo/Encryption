#!/usr/bin/env python
# -*- coding:utf-8 -*- 

import sys
import os
import base64
import getpass
from enclib import *
from easygui import *

# Version = 0.01
# Author = Exted Luo (extedluo.com)

# Pre-defined contants

FILE_EXT=".lock"
SW_VERSION="0.1"
SD_VERSION="01"
LANGUAGE="zh-CN"
f=""
# Command-line Interface
T_NAME="Encryption PREVIEW"
T_HEADER="""
Encryption 0.1.PREVIEW
Design by Extedluo.com
THIS VERSION IS FOR PREVIEW ONLY. NO BACKWARD COMPATIBILITY SUPPORT WILL BE PROVIDED.
DO NOT USE IT ON YOUR IMPORTANT FILE OR ON PRODUCTION.
"""
T_MODE_LIST="""
File was selected.
1. Encrypt file using password
2. Decrypt file using password
3. Encrypt file using keyfile
4. Decrypt file using keyfile
5. Encrypt file with Strong Password Generator
6. Exit
Please enter the mode number (1/2/3/4/5/6):
"""
T_GET_PASS="""
Enter your password (will not be shown):
"""
T_GET_FILE="""
Please drag your file here.
"""
T_GET_ORDER="""
[1 Open]  2 Create  3 Signature  4 Exit 
To start, drag/type the file here or enter mode code:
"""
T_GET_KEYFILE="""
Please drag the keyfile or type the location of your file here:
"""
T_FINISHED="""
Finished.
"""
T_UNKNOWN="""
Sorry, we can't interpret your input now. 
"""
T_DECRYPT_ERROR="""
File cannot be decrypted. Please try again.
"""
T_IOERROR="""
File cannot be opened. Please try again.
Note: Filename including non-ASCII characters is not supported yet.
"""
T_EXIT="""
Terminated.
"""
T_UNAVAILABLE="Sorry, this feature is currently unavailable."
T_SELECT_FUNCTION="Please select the function"


T_MAIN_OPEN = "1 - Open a file"
T_MAIN_CREATE = "2 - Create a container"
T_MAIN_TOOLS = "3 - Tools"
T_MAIN_EXIT = "4 - Exit"

T_FILE_ENCRYPT_PASSWORD="1 - Encrypt file using password"
T_FILE_DECRYPT_PASSWORD="2 - Decrypt file using password"
T_FILE_ENCRYPT_KEYFILE="3 - Encrypt file using keyfile"
T_FILE_DECRYPT_KEYFILE="4 - Decrypt file using keyfile"
T_FILE_ENCRYPT_WITH_PASSWORD_GENERATOR="5 - Encrypt file with Strong Password Generator"
T_FILE_EXIT="6 - Exit"

import Tkinter, tkFileDialog

def file_dialog():
    # I don't know why easygui's openfilebox doesn't work, so I write this one.
    root = Tkinter.Tk()
    root.withdraw()
    file_path = tkFileDialog.askopenfilename()
    return file_path

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_file(filename):
    return os.path.isfile(filename)

def get_file():
    #inputfile=fileopenbox(msg=T_GET_FILE, title="Open", default="*.*")
    inputfile=file_dialog()
    return inputfile

def get_password():
    password=passwordbox(msg=T_GET_PASS)
    return password

def get_keyfile():
    #inputfile=fileopenbox(msg=T_GET_KEYFILE, title="Open")
    inputfile=file_dialog()
    return keyfile
    
def please_wait():
    pass

def function_unavailable():
    msgbox(T_UNAVAILABLE)

def unknown_input():
    msgbox(T_UNKNOWN)

def finished():
    msgbox(T_FINISHED)

def show_file_operations(f):

    choices = [T_FILE_ENCRYPT_PASSWORD, T_FILE_DECRYPT_PASSWORD, T_FILE_ENCRYPT_KEYFILE, T_FILE_DECRYPT_KEYFILE, T_FILE_ENCRYPT_WITH_PASSWORD_GENERATOR, T_FILE_EXIT]
    mode = choicebox(T_SELECT_FUNCTION, T_NAME, choices) 
    if mode==T_FILE_ENCRYPT_PASSWORD:
        encrypt_file_password(f)
    elif mode==T_FILE_DECRYPT_PASSWORD:
        decrypt_file_password(f)
    elif mode==T_FILE_ENCRYPT_KEYFILE:
        encrypt_file_keyfile(f)
    elif mode==T_FILE_DECRYPT_KEYFILE:
        decrypt_file_keyfile(f)
    elif mode==T_FILE_ENCRYPT_WITH_PASSWORD_GENERATOR:
        function_unavailable()
    elif mode==T_FILE_EXIT:
        sys.exit(0)
    else:
        unknown_input()

def encrypt_file_password(f):
    
    key=get_password()

    new_instance=StandardOne()
    new_instance.encrypt(key, f, "")

    finished()

    show_main_menu("")

def encrypt_file_keyfile(f):
    
    keyfile=get_keyfile()
    please_wait()
    new_instance=StandardOne()
    key=new_instance.hash_keyfile(keyfile)
    new_instance.encrypt(key, f, "")
    
    finished()
    show_main_menu("")

def decrypt_file_password(f):

    key=get_password()
    please_wait()
    
    new_instance=StandardOne()
    new_instance.decrypt(key, f, "")
    
    finished()
    show_main_menu("")

def decrypt_file_keyfile(f):
    
    keyfile=get_keyfile()
    please_wait()
    new_instance=StandardOne()
    key=new_instance.hash_keyfile(keyfile)
    new_instance.decrypt(key, f, "")

    finished()
    show_main_menu("")

def show_main_menu(f):

    if check_file(f):
        show_file_operations(f)
    elif f==T_MAIN_OPEN:
        filename = get_file()
        show_main_menu(filename)
    elif f==T_MAIN_CREATE:
        function_unavailable()
        show_main_menu("")
    elif f==T_MAIN_TOOLS:
        function_unavailable()
        show_main_menu("")
    elif f==T_MAIN_EXIT:
        sys.exit(0)
    else:
        msg ="Please select the function:"
        title = T_NAME
        choices = [T_MAIN_OPEN, T_MAIN_CREATE, T_MAIN_TOOLS, T_MAIN_EXIT]
        choice = choicebox(msg, title, choices)
        show_main_menu(choice)

def main():

    # Get argument first.
    if len(sys.argv) == 1:
        f=""
    else:
        f=sys.argv[1]
    show_main_menu(f)    

if __name__ == '__main__':
    try:
        main()
    except DecryptError:
        msgbox(T_DECRYPT_ERROR, T_NAME)
        show_main_menu("")
    except IOError:
        msgbox(T_IOERROR, T_NAME)
        show_main_menu("")
    except KeyboardInterrupt:
        clear_screen()
        print(T_EXIT)