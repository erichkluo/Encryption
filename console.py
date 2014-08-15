#!/usr/bin/env python
# -*- coding:utf-8 -*- 

import sys
import os
import base64
import getpass
from enclib import *

# @TODO: 是否替换文件的通知!
# @TODO: 在运算的过程中随机执行一些没用的运算!
# @TODO: 参数化! 没有参数的就在命令行问!
# @TODO: 超大文件处理!
# @TODO: Add key-file support.
# @TODO: 清除密码内存变量!
# @TODO: 待捕捉错误: KeyboardInterrupt, CannotDecrypt, IOError
# @TODO: 文件伪装功能! (内容, 后缀等!)
# @TODO: 混淆文件生成器!

# @PLAN: MODE: FILE, CONT, 
# @PLAN: TEAM FILE ENCRYPTING SHATING

# Version = 0.01
# Author = Exted Luo (extedluo.com)

# Pre-defined contants

FILE_EXT=".lock"
SW_VERSION="0.1"
SD_VERSION="01"
LANGUAGE="zh-CN"
f=""
# Command-line Interface

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
T_UNAVAILABLE="""
This feature is currently unavailable.
"""
# 

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_file(filename):
    return os.path.isfile(filename)

def get_file():
    inputfile=raw_input(T_GET_ORDER).rstrip()
    clear_screen()
    return inputfile

def get_order():
    order=raw_input(T_GET_ORDER).rstrip()
    return order

def get_password():
    t_key = getpass.getpass(T_GET_PASS)  # Need a pop-up windows
    return t_key

def get_keyfile():
    keyfile=raw_input(T_GET_KEYFILE).rstrip()
    return keyfile
    
def please_wait():
    print "Processing..."
    # How to estimate the time?

def can_not_decrypt():
    print "Cannot be decrypted. Press [Enter] to exit."
    notice=raw_input()
    sys.exit(0)

def show_file_operations(f):
    
    # 输入保证是可以读取的文件!
    clear_screen()
    print(T_HEADER)
    mode=raw_input(T_MODE_LIST)
    if mode=="1":
        encrypt_file_password(f)
    elif mode=="2":
        decrypt_file_password(f)
    elif mode=="3":
        encrypt_file_keyfile(f)
    elif mode=="4":
        decrypt_file_keyfile(f)
    elif mode=="5":
        pass
    elif mode=="6":
        clear_screen()
        sys.exit(0)
    else:
        print(T_UNKNOWN)

def encrypt_file_password(f):
    
    key=get_password()

    please_wait() # 这个怎么

    new_instance=StandardOne()
    new_instance.encrypt(key, f, "")

    print(T_FINISHED)
    notice=raw_input()
    clear_screen()
    show_main_menu("")

def encrypt_file_keyfile(f):
    
    keyfile=get_keyfile()
    please_wait()
    new_instance=StandardOne()
    key=new_instance.hash_keyfile(keyfile)
    new_instance.encrypt(key, f, "")
    
    print(T_FINISHED)
    notice=raw_input()
    clear_screen()
    show_main_menu("")

def decrypt_file_password(f):

    key=get_password()
    please_wait()
    
    new_instance=StandardOne()
    new_instance.decrypt(key, f, "")
    
    print(T_FINISHED)
    notice=raw_input()
    clear_screen()
    show_main_menu("")

def decrypt_file_keyfile(f):
    
    keyfile=get_keyfile()
    please_wait()
    new_instance=StandardOne()
    key=new_instance.hash_keyfile(keyfile)
    new_instance.decrypt(key, f, "")

    print(T_FINISHED)
    notice=raw_input()
    clear_screen()
    show_main_menu("")

def show_main_menu(f):
    if check_file(f):
        show_file_operations(f)
    elif f=="2":
        print(T_UNAVAILABLE)
        notice=raw_input()
        show_main_menu("")
    elif f=="3":
        print(T_UNAVAILABLE)
        notice=raw_input()
        show_main_menu("")
    elif f=="4":
        clear_screen()
        sys.exit(0)
    else:
        clear_screen()
        print(T_HEADER)
        f=get_order()
        show_main_menu(f)

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
        print(T_DECRYPT_ERROR)
        notice=raw_input()
        clear_screen()
        show_main_menu("")
    except IOError:
        print(T_IOERROR)
        show_main_menu("")
    except KeyboardInterrupt:
        clear_screen()
        print(T_EXIT)