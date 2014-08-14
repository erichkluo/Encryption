#!/usr/bin/env python
# -*- coding:utf-8 -*- 

# Encryption Library for all version.

# 更抽象化一点, 加密逻辑过程、Key生成过程分离! 这样对不同类型的文件再调用不同的类!

# 如果这个类将无法解密的话返回什么错误? 上一级不应该出错而是应该调用新的类!

import sys
import os
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, RIPEMD, MD5
from Crypto.Protocol.KDF import PBKDF2

class DecryptError(Exception): pass

class StandardOne:
    """
    Encryption Methods & Algorithms Standard Version One.
    13 Aug 2014
    Exception:
        DecryptError
        EncryptError
    """
    
    STRENGTH=32
    SALT_LENGTH=64
    HEADER_LENGTH=512
    ENCRYPTED_HEADER_LENGTH=560 # @TODO: Compute is right away.
    SD_VERSION="01"
    salt=""
    content_length=""

    def strong_random(self, length=STRENGTH):
        # @TODO: Make it system-independent.
        return os.urandom(length)

    def hash_SHA256(self, key, salt):
        h = SHA256.new()
        h.update(key+salt)
        return h.hexdigest()  

    def hash_RIPEMD(self, key, salt):
        h = RIPEMD.new()
        h.update(key+salt)
        return h.hexdigest()

    def strong_hash(self, key, salt, method):
        iterations = 20001
        return PBKDF2(key, salt, dkLen=self.STRENGTH*4, count=iterations, prf=method)

    class AESCipher:
        def __init__(self, key):
            self.bs = 32
            if len(key) >= 32:
                self.key = key[:32]
            else:
                self.key = self._pad(key)
        def encrypt(self, raw):
            raw = self._pad(raw)
            iv = os.urandom(AES.block_size)  ##HOW
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            # cipher=AES.new(self.key, AES.MODE_ECB)
            return iv + cipher.encrypt(raw)
            # return cipher.encrypt(raw)
        def decrypt(self, enc):
            iv = enc[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            # cipher=AES.new(self.key, AES.MODE_ECB)
            return self._unpad(cipher.decrypt(enc[AES.block_size:]))
            # return self._unpad(cipher.decrypt(enc))
        def _pad(self, s):
            return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
        def _unpad(self, s):
            return s[:-ord(s[len(s)-1:])]

    def get_header(self, key, filename):
        header="TRUE"+self.SD_VERSION+"FILE$"+filename+"$"
        if len(header)<self.HEADER_LENGTH:
            header=header+self.strong_random(self.HEADER_LENGTH-len(header)) # 到这里 Header 应该为 512 bytes
        h=self.AESCipher(key)
        header=h.encrypt(header) # 加密后的 Header 应该为 560 bytes ADJUSTED
        header=self.salt+header
        return header

    def wipe_file(self, filename):
        wipe_handle=open(filename, 'wb')
        for i in xrange(self.content_length % 16):
            wipe_handle.write(self.strong_random(16))
        wipe_handle.close()
        os.remove(filename)

    def encrypt(self, key, inputfile, outputfile=""):
        # Initialization
        self.salt=self.strong_random(self.SALT_LENGTH)
        key=self.strong_hash(key, self.salt, self.hash_SHA256) # NOW WE HAVE 128 bytes Key
        operation_key=key[0:16]
        key1 = key[32:64]
        key2 = key[64:96]
        key3 = key[96:128]
        # File handling
        if outputfile=="":
            outputfile=inputfile+".lock"
        inputfile_handle=open(inputfile,'rb')
        outputfile_handle=open(inputfile+'.lock','wb')
        inputfile_name=inputfile.split('/')[-1]
        header=self.get_header(key1, inputfile_name)
        content=inputfile_handle.read()
        self.content_length=len(content)+self.ENCRYPTED_HEADER_LENGTH
        # Encryption Process
        e=self.AESCipher(key1)
        content=e.encrypt(content)
        outputfile_handle.write(header)
        outputfile_handle.write(content)
        inputfile_handle.close()
        outputfile_handle.close()

        # Wipe Input file
        self.wipe_file(inputfile)
        return True

    def decrypt(self, key, inputfile, outputfile=""):
        status = self.verify_file(key, inputfile, outputfile)
        self.wipe_file(inputfile)
        return status

    def decrypt_content(self, key, inputfile_handle, outputfile_handle):
        # Key spliting
        operation_key=key[0:16]
        key1 = key[32:64]
        key2 = key[64:96]
        key3 = key[96:128]
        e=self.AESCipher(key1)
        content=inputfile_handle.read()
        self.content_length=len(content)+self.ENCRYPTED_HEADER_LENGTH
        content=e.decrypt(content)
        outputfile_handle.write(content)
        inputfile_handle.close()
        outputfile_handle.close()
        # Wipe File
        return True

    def verify_file(self, key, inputfile, outputfile=""):
        inputfile_handle=open(inputfile,'rb')
        self.salt=inputfile_handle.read(self.SALT_LENGTH)
        key=self.strong_hash(key, self.salt, self.hash_SHA256)
        header=inputfile_handle.read(self.ENCRYPTED_HEADER_LENGTH)
        # Key spliting
        operation_key=key[0:16]
        key1 = key[32:64]
        key2 = key[64:96]
        key3 = key[96:128]
        # Decrypt the header
        h=self.AESCipher(key1)
        header=h.decrypt(header)
        if header[:4]!="TRUE":
            raise DecryptError
        if outputfile=="":
            outputfile_name=header.split('$')[1]
            outputfile_path=inputfile[:len(inputfile)-len(inputfile.split('/')[-1])]
            outputfile=outputfile_path+outputfile_name
        outputfile_handle=open(outputfile,'wb') # ORIGINAL FILE NAME
        return self.decrypt_content(key, inputfile_handle, outputfile_handle)

    def hash_keyfile(self, keyfile):
        keyfile_handle=open(keyfile,'rb')
        keyfile_content=keyfile_handle.read()
        key=self.salt+self.hash_SHA256(keyfile_content, "")
        return key

