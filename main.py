#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
gas - 2021 - por jero98772
gas - 2021 - by jero98772
"""
from flask import Flask, render_template, request, flash, redirect ,session
from tools.dbInteracion import dbInteracion
from tools.tools import *
app = Flask(__name__)
app.secret_key = str(enPassowrdHash(generatePassword()))
DBPATH = "data/"
DBNAMEGAS = DBPATH + "gas_db"
TABLEGAS = "gastos"
GASLOGINTABLE = "logingastos"
DATANAMEGAS = ["item","category","thread","price","amount","date"]
class gas():
	WEBPAGE = "/"
	@app.route(WEBPAGE+"user_register.html", methods = ['GET','POST'])
	def register():
		if request.method == 'POST':
			pwd = request.form["pwd"]
			pwd2 = request.form["pwd2"]
			if pwd == pwd2 :
				usr = request.form["usr"]
				db = dbInteracion(DBNAMEGAS)
				db.connect(GASLOGINTABLE)
				if db.userAvailable(usr,"usr") :
					encpwd = enPassowrdStrHex(pwd+usr) 
					db.saveUser(usr,enPassowrdStrHex(pwd))
					try:
						db.createUser(usr)
						session['loged'] = True
						session['user'] = usr
						session['encpwd'] = encpwd
					except db.userError():
						return "invalid user , please try with other username and password"		
		return render_template("user_register.html")
	@app.route(WEBPAGE)
	def gasinfo():
		return render_template("gasinfo.html")
	@app.route(WEBPAGE+"gas.html", methods = ['GET','POST'])
	def gas():
		priceCol = "price"
		data = []
		db = dbInteracion(DBNAMEGAS)
		timenow = hoyminsStr()
		if not session.get('loged'):
			return render_template('gas_login.html')	
		else:
			user = session.get('user')
			encpwd = session.get('encpwd')
			db.connect(TABLEGAS+user)
			item_id =  db.getID()
			rows = db.getDataGas()
			keys = len(DATANAMEGAS)*[encpwd]
			pricesum = 0
			decdata =[]
			i = 0
			for row in rows:
				decdata.append([concatenateStrInList(item_id[i])]+list(map(decryptAES,row,keys)))
				pricesum += float(decdata[i][4])*float(decdata[i][5])
				i += 1
			try :
				priceavg = pricesum / len(rows)
			except :
				priceavg = "no data" 
			if request.method == 'POST':
				data = multrequest(DATANAMEGAS)
				data = list(map(encryptAES , data, keys))
				data = list(map(str , data))
				db.addGas(DATANAMEGAS,data)
				return redirect("gas.html")
			return render_template("gas.html",purchases = decdata,now=timenow,sum=pricesum,avg=priceavg)	
	"""
	@app.route(WEBPAGE+'gas/threads.html', methods = ['GET','POST'])
	def gasThreads():
		threadsNames = []
		user = session.get('user')
		encpwd = session.get('encpwd')
		keys = len(DATANAMEGAS)*[encpwd]
		db = dbInteracion(DBNAMEGAS)
		db.connect(TABLEGAS+user)
		threads = db.getDistinctColumnGAS("thread")
		threads = list(map(decryptAES,threads,keys))
		for thread in threads:
			if thread not in threadsNames:
				threadsNames.append(thread)
		return render_template("gas_threads.html" , threads = threadsNames)
	@app.route(WEBPAGE+'gas/filter<string:thread>', methods = ['GET','POST'])
	def gasFilter(thread):
		user = session.get('user')
		db = dbInteracion(DBNAMEGAS)
		db.connect(TABLEGAS+user)
		threads = db.getDistinctWhere(thread)
		pricesum = db.getSum(priceCol)
		priceavg = db.getAvg(priceCol)
		threadName = thread
		return render_template("thread.html" ,threads = threads , threadName = threadName)
	"""
	@app.route(WEBPAGE+"gas_login.html", methods=['GET', 'POST'])
	def gaslogin():	
		usr = request.form['username']
		pwd = request.form["password"]
		encpwd = enPassowrdStrHex(pwd+usr)
		protectpwd = enPassowrdStrHex(pwd)
		db = dbInteracion(DBNAMEGAS)
		db.connect(GASLOGINTABLE)
		if db.findUser(usr) and db.findPassword(protectpwd)  :
			session['loged'] = True
			session['user'] = usr
			session['encpwd'] = encpwd
			return redirect("/gas.html")
		else:
			flash('wrong password!')
		return gas.gas()
	@app.route(WEBPAGE+'gas/actualisar<string:id>', methods = ['GET','POST'])
	def update_gas(id):
		user = session.get('user')
		db = dbInteracion(DBNAMEGAS)
		db.connect(TABLEGAS+user)
		key = session.get('encpwd')
		keys = len(DATANAMEGAS)*[key]
		if request.method == 'POST':
			data = multrequest(DATANAMEGAS)
			encdata = list(map(encryptAES , data, keys))
			encdata = list(map(str,encdata))
			del key,keys,data
			sentence = setUpdate(DATANAMEGAS,encdata)
			db.updateGas(sentence,id)
			flash(' Updated Successfully')
		return redirect('/gas.html')
	@app.route(WEBPAGE+'gas/editar<string:id>', methods = ['POST', 'GET'])
	def get_gas(id):
		user = session.get('user')
		db = dbInteracion(DBNAMEGAS)
		db.connect(TABLEGAS+user)
		key = session.get('encpwd')
		keys = len(DATANAMEGAS)*[key]
		rows = db.getDataGasWhere("item_id",id)[0]
		idData = [id]+list(map(decryptAES,rows,keys))
		del key,keys , user , rows
		return render_template('gas_update.html', purchase = idData )
	@app.route(WEBPAGE+"gas/eliminar/<string:id>", methods = ['GET','POST'])
	def gassdelete(id):
		user = session.get('user')
		db = dbInteracion(DBNAMEGAS)
		db.connect(TABLEGAS+user)
		db.deleteWhere("item_id",id)
		#flash('you delete that')
		return redirect('/gas.html')
if __name__=='__main__':
	app.run(debug=True,host="0.0.0.0",port=9600)