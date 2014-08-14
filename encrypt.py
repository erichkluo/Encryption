#!/usr/bin/env python
# -*- coding:utf-8 -*- 

import sys
import os
import base64
import getpass
from enclib import *

# @TODO: Class 化!
# @TODO: 是否替换文件的通知!
# @TODO: 在运算的过程中随机执行一些没用的运算!
# @TODO: 参数化! 没有参数的就在命令行问!
# @TODO: 超大文件处理!
# @TODO: Add key-file support.
# @TODO: 清除密码内存变量!
# @TODO: 文件头, 需要的最低版本!
# @TODO: 抹掉文件!
# @TODO: 先 Decrypt Header, 读取需要的版本号, 再调用相关的 class!

# @PLAN: MODE: File-encrypting, Floder-encrypting, Encrypted Volumes, Encrypted Notes/Vault.
# @PLAN: TEAM FILE ENCRYPTING SHATING


# Version = 0.01
# Author = Exted Luo (extedluo.com)

# Pre-defined contants



FILE_EXT=".lock"
SW_VERSION="0.1.1"
SD_VERSION="01"

def it_is_a_valid_file(filename):
    return os.path.isfile(filename)

def require_file():
    # @TODO: Show Error First!
    return raw_input("Error! Please select a file again:")

def require_key():
    t_key = getpass.getpass("Enter your passcode (will not be shown):")  # Need a pop-up windows
    return t_key
    
def please_wait():
    print "Please wait..."
    # How to estimate the time?

def can_not_decrypt():
    print "Cannot be decrypted. Press [Enter] to exit."
    notice=raw_input()
    sys.exit(0)

def encrypt_file(f):
    
    key=require_key()

    please_wait() # 这个怎么

    new_instance=StandardOne()
    new_instance.encrypt(key, f, "")

    print "Finished. Press [Enter] to exit."
    notice=raw_input()

def decrypt_file(f):

    key=require_key()
    please_wait()
    
    new_instance=StandardOne()
    new_instance.decrypt(key, f, "")
    
    print "Finished. Press [Enter] to exit."
    notice=raw_input()

def main():

    if len(sys.argv) == 1:
        f=require_file()
    f=sys.argv[1]

    while not(it_is_a_valid_file(f)):
        f=require_file()
        
    # Check whether it is .lock file
    if f[-len(FILE_EXT):]==FILE_EXT:
        decrypt_file(f)
    else:
        mode=raw_input("[E]ncrypt or [D]ecrypt?")
        if (mode.upper() == "E") or (mode.lower() == "encrypt"):
            encrypt_file(f)
        elif (mode.upper() == "D") or (mode.lower() == "decrypt"):
            decrypt_file(f)
        else:
            "Sorry, we can't interpret your input. "
    
    # @TODO: CHECK REPLACE FILE OR NOT!

if __name__ == '__main__':
    main()
