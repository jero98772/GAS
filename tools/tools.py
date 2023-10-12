#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
gas - 2021 - por jero98772
gas - 2021 - by jero98772
"""
from flask import request
from hashlib import  sha256
import os
from Crypto import Random
from Crypto.Cipher import AES
import base64
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
def multrequest(items):	
	values = []
	for item in items:		
		item = request.form.get(item)
		try:
			item = float(item)
		except:	
			item = str(item)
		values.append(item)
	return values
def generatePassword():
	"""generatePassword(),return srtring
	generate random string 
	"""
	genPassowrd = ""
	for i in range(0,16):
		if len(genPassowrd) >= 16 and len(genPassowrd)-len(hexStr) <= 16:
			num = rnd.randint(0,9999)
			if 32 > num >126:
				char = chr(num)
				genPassowrd += char
			else:
				hexStr = str(hex(hexStr))
				genPassowrd += hexStr
		else:
			break
	return genPassowrd
def hoyminsStr():
	import datetime
	"""
	return date and hours and minutes as string
	"""
	hoy = datetime.datetime.today().strftime("%m/%d/%Y, %H:%M")
	return hoy
def setUpdate(dataname, data):
	"""
	generate update sentece for sqlite3 
	"""
	sentence = dataname[0]+" = "+ '"'+data[0]+'"'
	for i ,ii in zip(dataname[1:] , data[1:]):
		sentence += ','+i+" = "+ '"'+ii+'"'
	return sentence
def enPassowrdStrHex(password):
	password = str(password)
	hashPassowrd = str(sha256(password.encode('utf-8')).hexdigest())
	return hashPassowrd
def enPasswordHash(password):
	password = str(password)
	hashPassowrd = sha256(password.encode("utf-8")).digest()
	return hashPassowrd

def generate_key_from_password(password, salt=None, iterations=100000, length=32):
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=iterations,
        salt=salt,
        length=length
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt
def pad(text):
    size = 32
    text = str(text)
    padding = size - (len(text) % size)
    text += chr(padding) * padding
    return text.encode('utf-8')

def unpad(text):
    padding = text[-1]
    return text[:-padding]


def encryptAES(text, password):
    private_key = enPasswordHash(password)  # Assuming 'enPasswordHash' is defined elsewhere.
    text = pad(text)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(text))

def decryptAES(text, password):
    private_key = enPasswordHash(password)  # Assuming 'enPasswordHash' is defined elsewhere.
    text = base64.b64decode(text)
    iv = text[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    
    decrypted_data = cipher.decrypt(text[16:])
    unpadded_data = unpad(decrypted_data)
    
    return unpadded_data.decode()
def concatenateStrInList(arr):
	"""
	concatenates the numbers of a string, the elements of an array : return  integer
	"""
	intAsString = ""
	for i in arr:
		intAsString += i
	return int(intAsString)