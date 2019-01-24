import sys
sys.path.append("..")
from circuit_app.component import *
import sqlite3
conn = sqlite3.connect('circuit_database.db',check_same_thread=False)
c = conn.cursor()
import json
from graphviz import *
class Circuit():
	def __init__(self,name):
		res = c.execute("SELECT * FROM Circuits C WHERE C.name = ?",(name,))
		result = res.fetchall()
		if result == []:
			self.name = name
			self.components = {}
			self.connections = {}
			self.lastID = 0
			self.ins = {}
			self.outs={}
			self.swins = {}
			self.ledouts = {}
		else:
			data = result[0]
			self.name = data[0]

			comp_str = data[1]
			components = json.loads(comp_str)
			self.components = {}
			for key in components.keys():
				comp = components[key].split("-")

				if(comp[0] == "AND"):
					C = AND(int(comp[1]))
					C.id = int(key)
					self.components[int(key)] = C
				elif(comp[0] == "OR"):
					C = OR(int(comp[1]))
					C.id = int(key)
					self.components[int(key)] = C					
				elif(comp[0] == "XOR"):
					C = XOR(int(comp[1]))
					C.id = int(key)
					self.components[int(key)] = C					
				elif(comp[0] == "NOT"):
					C = NOT()
					C.id = int(key)
					self.components[int(key)] = C					
				elif(comp[0] == "NOR"):
					C = NOR(int(comp[1]))
					C.id = int(key)
					self.components[int(key)] = C					
				elif(comp[0] == "NAND"):
					C = NAND(int(comp[1]))
					C.id = int(key)
					self.components[int(key)] = C					
				elif(comp[0] == "EQUIV"):
					C = EQUIV()
					C.id = int(key)
					self.components[int(key)] = C
				elif(comp[0]=="SWITCH"):
					C = SWITCH(int(comp[1]))
					C.id = int(key)
					self.components[int(key)]=C
				elif(comp[0]=="LED"):
					C=LED(int(comp[1]))
					C.id = int(key)
					self.components[int(key)]=C

			conn_str = data[2]
			conn = json.loads(conn_str)
			swins = json.loads(data[3])
			self.swins = {}
			for val in swins:
				key = (val[0][0],val[0][1])
				self.swins[key] = (val[1][0],val[1][1])
			self.ledouts = json.loads(data[4])
			self.connections = {}
			for val in conn:
				key = (val[0][0],val[0][1])
				self.connections[key] = (val[1][0],val[1][1])
			self.lastID = data[5]
			self.ins={}
			self.outs={}

	def save(self,name='no name'):
		if name == 'no name':
			name = self.name

		result = c.execute('''SELECT * 
								FROM Circuits C 
								WHERE C.name = ?''', (name,)).fetchall()
		if result == []:
			sql = "INSERT INTO Circuits VALUES (?,?,?,?,?,?); "

			compList = {}
			for key in self.components.keys():
				compList[key] = self.components[key].getName()+'-'+str(self.components[key].no)

			compStr = json.dumps(compList)
			theList = []
			for key in self.connections.keys():
				t = (key,self.connections[key])
				theList.append(t)
			connList = json.dumps(theList)
			swins = []
			for key in self.swins.keys():
				t = (key,self.swins[key])
				swins.append(t)	
			swins = json.dumps(swins)
			ledout = json.dumps(self.ledouts)
			task = (name,compStr,connList,swins,ledout,self.lastID)
			c.execute(sql,task)

		else:
			sql = '''UPDATE Circuits 
						SET components = ?, connections = ?,swins = ?,ledouts = ?, lastID = ? 
						WHERE name = ? '''
			compList = {}			
			for key in self.components.keys():
				compList[key] = self.components[key].getName()+'-'+str(self.components[key].no)

			compStr = json.dumps(compList)
			theList = []
			for key in self.connections.keys():
				t = (key,self.connections[key])
				theList.append(t)
			connList = json.dumps(theList)
			swins = []
			for key in self.swins.keys():
				t = (key,self.swins[key])
				swins.append(t)	
			swins = json.dumps(swins)

			ledout = json.dumps(self.ledouts)
			task = (compStr,connList,swins,ledout,self.lastID,name)	
			c.execute(sql,task)
		conn.commit()
	def addComponent(self,component):
		self.lastID = self.lastID + 1
		self.components[self.lastID] = component
		component.id = self.lastID

	def getComponent(self,cid):
		return self.components[cid]

	def delComponent(self,cid):
		for key in list(self.connections.keys()):
			value = self.connections[key]
			if key[0] == cid:
				del self.connections[key]
			elif value[0] == cid:
				del self.connections[key]


		if self.components[cid].getName()== "SWITCH":
			comp = self.components[cid]
			for i in self.swins.keys():
				if i[0] == comp.id:
					del self.swins[i]
		del self.components[cid]		

	def connect(self,cidA, outid, cidB, inid):
		outTuple = (cidA,outid)
		inputTuple = (cidB,inid)
		
		if inputTuple in self.connections.values():
			print("Input pin already connected. Cannot connect the input pin "+str(inputTuple)+" to more than one output pin")
			return
		val = self.getComponent(cidA)
		if val.getName() == "SWITCH":
			self.swins[inputTuple] = outTuple
		self.connections[outTuple] = inputTuple

	def disconnect(self,cidA, outid, cidB, inid):
		outTuple = (cidA,outid)
		inputTuple = (cidB,inid)
		if inputTuple not in self.connections.values():
			print("Not connected")
			return
		val = self.getComponent(cidA)
		if val.getName() == "SWITCH":
			del self.swins[inputTuple]

		del self.connections[outTuple]


	def freeinpins(self):
		inpList = []
		for key in self.components.keys():
			val = self.components[key]
			if val.getName() == "SWITCH" or val.getName() == "LED":
				continue;
			for i in range(len(val.getInputs())):
				inpList.append((key,i))


		
		for value in self.connections.values():
			
			if value in inpList:
				inpList.remove(value) 

		return inpList		
	
	def freeoutpins(self):
		outList = []
		for key in self.components.keys():
			val = self.components[key]
			if val.getName() == "SWITCH" :
				continue;
			for i in range(len(val.getOutputs())):
				outList.append((key,i+len(val.getInputs())))
		
		for key in self.connections.keys():
			if key in outList:
				outList.remove(key)				
		return outList						



	def setinput(self,inputList):
		self.ins = {}
		self.outs ={}
		tins ={}
		temps = self.freeinpins()
		tswins = {}
		for i in range(len(inputList)):
			self.ins[temps[i]] = inputList[i]

		for i in self.swins.keys():
			val = self.getComponent(self.swins[i][0])
			if val.get()[self.swins[i][1]] == '1':
				tswins[i] = True
			else:
				tswins[i] = False
		self.ins.update(tswins)
		for count in range(self.lastID+1):
			flag = 0

			self.ins.update(tins)
			tins ={}
			for i in self.ins.keys():
				
				comp = self.components[i[0]]
				if comp.getName() == "SWITCH":
					continue
				if comp.getName() == "LED":
					if self.ins[i] == True:
						comp.state[i[1]] = '1'
					else:
						comp.state[i[1]] = '0'
					continue
				if(len(comp.getInputs())==1):
					if (i[0],1) not in self.outs.keys():
						comp.calculate([self.ins[i]])
						self.outs[(i[0],1)] = comp.out
						
						flag = 1
						if (i[0],1) in self.connections.keys():
							pin = self.connections[(i[0],1)]
							tins[pin]= comp.out

				else:
					if (i[0],comp.no) not in self.outs.keys():
						inputList=[]
						for j in self.ins.keys():							
							if j[0] == i[0]:
								inputList.append(self.ins[j])
						if len(inputList) == comp.no:
							comp.calculate(inputList)
							self.outs[(i[0],comp.no)] = comp.out
							flag =1
							if (i[0],comp.no) in self.connections.keys():
								pin = self.connections[(i[0],comp.no)]
								tins[pin] = comp.out
			if flag == 0:
				break
		for i in self.ins.keys():
			val = self.getComponent(i[0])
			if val.getName() == "LED":
				if self.ins[i] == True:
					val.state[i[1]] = '1'
				else:
					val.state[i[1]] = '0'

	def getoutput(self):
		temps = self.freeoutpins()
		res = []
		
		for i in temps:
			res.append(self.outs[i])
		return res
	def viewGraph(self, arg = "source"):
		fins = self.freeinpins()
		fouts = self.freeoutpins()
		dot = Graph(name = "Circuit", node_attr={'shape':'none','label':'','fontsize':'10'})
		dot.graph_attr['rankdir'] = 'LR'
		#dot.graph_attr['fontsize'] = '6'
		cnt = 1
		gcons = {}
		for i in fins:
			c = i[1]
			name = 'INP'+str(cnt)
			dot.node(name,name)
			cname = self.getComponent(i[0]).getName()
			gcons[name] = cname+str(i[0])
			cnt += 1
		cnt = 1
		for i in fouts:
			c = i[1]
			name = 'OUT'+str(cnt)
			dot.node(name,name)
			cname = self.getComponent(i[0]).getName()
			gcons[name] = cname+str(i[0])
			cnt += 1

		for i in self.components.keys():
			val  = self.components[i]
			name = val.getName()+str(i)
			if(val.getName() == "LED"):
				dot.attr('node', image = 'LEDOFF.png')
				dot.node(name,name+" "+val.get())
			elif val.getName() == "SWITCH":
				dot.attr('node', image = 'SWITCHON.png')
				dot.node(name,name+" "+val.get())

			else:
				dot.attr('node',image = val.getName()+'.png')
				dot.node(name,name)
			dot.attr('node',image = 'none')
		used = True
		for i in self.connections.keys():
			val = self.connections[i]
			o = self.getComponent(i[0]).getName()+str(i[0])+':e'
			d = 'sw'
			if used == True:
				d = 'nw'
			used = not used
			j = self.getComponent(val[0]).getName()+str(val[0])+':'+d
			dot.edge(o,j)

		used = True
		for i in gcons.keys():
			val = gcons[i]
			if i[0] == 'O':
				dot.edge(val+':e',i)
				continue
			d = 'nw'
			if used == True:
				d = 'sw'
			used = not used
			
			dot.edge(i+':e',val+':'+d)

		#if arg == "render":
		return dot.render('circuit_app/static/circuit', format = 'jpg')
		#else:
		#	return dot.source 
conn.commit()
"""CREATE TABLE Circuits(
	name VARCHAR(20),
	components VARCHAR(2000),
	connections VARCHAR(2000),
	swins VARCHAR(2000),
	ledouts VARCHAR(2000),
	lastID INT,
	PRIMARY KEY(name));"""