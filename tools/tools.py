#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
gas - 2021 - por jero98772
gas - 2021 - by jero98772
"""
from flask import request
from hashlib import  sha256
import base64
from Crypto import Random
from Crypto.Cipher import AES

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
def enPassowrdHash(password):
	password = str(password)
	hashPassowrd = sha256(password.encode("utf-8")).digest()
	return hashPassowrd
def unpad(txt):
	return txt[:-ord(txt[len(txt) - 1:])]
def pad(txt):
	size = 16
	txt = str(txt)
#	return txt + (size - len(txt) % size) * chr(size - len(txt) % size)
	return bytes(txt + (size - len(txt) % size) * chr(size - len(txt) % size), 'utf-8')
#pad = lambda s: bytes(s + (size - len(s) % size) * chr(BS - len(s) % BS), 'utf-8')
def encryptAES(text, password):
	private_key = enPassowrdHash(password)
	text = pad(text)
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(private_key, AES.MODE_CBC, iv)
	return base64.b64encode(iv + cipher.encrypt(text))
def decryptAES(text, password):
	private_key = enPassowrdHash(password)
	text = base64.b64decode(eval(text))
	iv = text[:16]
	cipher = AES.new(private_key, AES.MODE_CBC, iv)
	mensaje =  unpad(cipher.decrypt(text[16:]))
	return mensaje.decode()
def concatenateStrInList(arr):
	"""
	concatenates the numbers of a string, the elements of an array : return  integer
	"""
	intAsString = ""
	for i in arr:
		intAsString += i
	return int(intAsString)