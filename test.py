#!/usr/bin/env python
# -*- coding:utf-8 -*- 

# File for library testing

from enclib import *

content="testtesttest"*2
#print content
key="frguy348ybuci3q4bv783h7nv8hyeuytwi47ehyf78wh57veuy5gynsdhgfway"

enc=Enclibv1()
test = enc.encrypt(key, content)
print test.encode('hex')
test = enc.decrypt(key, test)
print test

