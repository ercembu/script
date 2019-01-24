from django.shortcuts import render
from circuit_app.circuits import Circuit 
from circuit_app.component import * 
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import transaction
from django.forms import ModelForm
from circuit_app.forms import *
from circuit_app.models import *
from django.http import HttpResponse
from django.http import JsonResponse
import json
import sys
#sys.path.append('..')
import pickle
# Create your views here.
class CreateCircuitView(CreateView):
	model = Circuit_hold
	template_name_suffix = '_create_form'
	form_class = CircuitForm
	fields = ['name']
	def post(self,request):
		form = CircuitForm(request.POST)
		list_form = CircuitListForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			Circuit_hold.objects.filter(name=name).delete()
			form.save()
			x = Circuit_hold.objects.latest('id')
			components = {}
			c = Circuit(name)
			mes = pickle.dumps(c)
			mes2 = pickle.dumps(components)
			x.circuit = mes
			x.components = mes2			
			x.save()
			return redirect('/web_app/circuit/'+str(name)+'/')
		elif list_form.is_valid():
			name = form.cleaned_data['circuit']
			"""circuit = Circuit_hold.objects.select_for_update().get(name=name)
			c = Circuit(name)
			print(c.components)
			mes = pickle.dumps(c)
			circuit.circuit = mes
			circuit.save()"""
			return redirect('/web_app/circuit/'+str(name)+'/')		

	def get(self,request):
		l = Circuit_hold.objects.filter(flag = 1)
		for i in l:
			name = i.name
			temp = Circuit(name)
			mes = pickle.dumps(temp)
			i.circuit = mes
			i.save()
		return render(request, "circuit_create_form.html",{'form':CircuitForm(),
															'circuit_list': Circuit_hold.objects.filter(flag = 1)})		


class UpdateCircuitView(View):
	@classmethod
	def post(self,request,name):
		component_form = ComponentForm(request.POST,request.FILES)
		connect_form = ConnectForm(request.POST,request.FILES)
		disConnect_form = disConnectForm(request.POST,request.FILES)
		del_form = delComponentForm(request.POST,request.FILES)
		setinput = setInputForm(request.POST,request.FILES)
		switch_form = switchSet(request.POST, request.FILES)
		flag = 0
		with transaction.atomic():

			circuit = (Circuit_hold.objects.select_for_update().get(name=name))
			file = 'x.txt'
			c = circuit.circuit
			with open(file, 'wb') as output:
				output.write(c)		
			f = open(file, 'rb')
			cir = pickle.load(f)
			f.close()
			open(file, 'w').close()

			if component_form.is_valid():
				inp = int(request.POST.get('input_number', None))
				component_name = request.POST.get('component_name', None)
				#component_name = component_form.cleaned_data['component_name']
				#inp = component_form.cleaned_data['input_number']
				if component_name == "AND":
					a = AND(inp)
					#circuit.lastID = circuit.lastID + 1
					#components[circuit.lastID] = a
					cir.addComponent(a)				
				elif component_name == "OR":
					a = OR(inp)
					cir.addComponent(a)
					#circuit.lastID = circuit.lastID + 1
					#components[circuit.lastID] = a				
				elif component_name == "XOR":
					a = XOR(inp)
					cir.addComponent(a)
					#circuit.lastID = circuit.lastID + 1
					#components[circuit.lastID] = a				
				elif component_name == "NOT":
					a = NOT()
					cir.addComponent(a)
					#circuit.lastID = circuit.lastID + 1
					#components[circuit.lastID] = a				
				elif component_name == "NOR":
					a = NOR(inp)
					cir.addComponent(a)
					#circuit.lastID = circuit.lastID + 1
					#components[circuit.lastID] = a					
				elif component_name == "NAND":
					a = NAND(inp)
					cir.addComponent(a)
					#circuit.lastID = circuit.lastID + 1
					#components[circuit.lastID] = a				
				elif component_name == "EQUIV":
					a = EQUIV()
					cir.addComponent(a)
					#circuit.lastID = circuit.lastID + 1
					#components[circuit.lastID] = a				
				elif component_name == "SWITCH":
					a = SWITCH(inp)
					cir.addComponent(a)
					#circuit.lastID = circuit.lastID + 1
					#components[circuit.lastID] = a				
				elif component_name == "LED":
					a = LED(inp)
					cir.addComponent(a)
					#circuit.lastID = circuit.lastID + 1
					#components[circuit.lastID] = a						
				flag = 1
				mes = pickle.dumps(cir)
				circuit.circuit = mes	
				circuit.save()				
				response_data = {}
				components = []
				connections = []
				for comp in cir.components:
					component = cir.components[comp]
					l = []
					name = component.getName()
					if name == "AND" or name == "OR" or name == "XOR" or name == "NOT" or name == "NOR" or name == "NAND" or name == "EQUIV": 
						l.append(component.id)
						l.append(component.getName())
						l.append(component.no)
							
						components.append(l)
					else:
						l.append(component.id)
						l.append(component.getName())
						l.append(component.no)
						l.append(component.get())
						components.append(l)
				for key in cir.connections:
					tup1 = cir.connections[key]
					l = []
					l.append(key)
					l.append(tup1)
					connections.append(l)
				o = []
				if circuit.input_set == True:
					o = cir.getoutput()	
					print("GIRDIM")
					circuit.save()				
				response_data['connections'] = connections
				response_data['components'] = components
				response_data['freeinpins'] = cir.freeinpins()
				response_data['freeoutpins'] = cir.freeoutpins()
				response_data['output'] = o
				print(connections)
				return JsonResponse(response_data)				
			elif connect_form.is_valid():
				component1 = int(request.POST.get('component1', None))
				connection1 = int(request.POST.get('connection1', None))
				component2 = int(request.POST.get('component2', None))
				connection2 = int(request.POST.get('connection2', None))
				cir.connect(component1,connection1,component2,connection2)
				mes = pickle.dumps(cir)
				circuit.circuit = mes	
				circuit.save()
				flag = 1
				mes = pickle.dumps(cir)
				circuit.circuit = mes	
				circuit.save()				
				response_data = {}
				components = []
				connections = []
				for comp in cir.components:
					component = cir.components[comp]
					l = []
					name = component.getName()
					if name == "AND" or name == "OR" or name == "XOR" or name == "NOT" or name == "NOR" or name == "NAND" or name == "EQUIV": 
						l.append(component.id)
						l.append(component.getName())
						l.append(component.no)
							
						components.append(l)
					else:
						l.append(component.id)
						l.append(component.getName())
						l.append(component.no)
						l.append(component.get())
						components.append(l)
				for key in cir.connections:
					tup1 = cir.connections[key]
					l = []
					l.append(key)
					l.append(tup1)
					connections.append(l)
				o = []
				if circuit.input_set == True:
					o = cir.getoutput()	
					circuit.save()				
				response_data['connections'] = connections
				response_data['components'] = components
				response_data['freeinpins'] = cir.freeinpins()
				response_data['freeoutpins'] = cir.freeoutpins()
				response_data['output'] = o
				return JsonResponse(response_data)								
			elif disConnect_form.is_valid():
				component1 = int(request.POST.get('comp1', None))
				connection1 = int(request.POST.get('conn1', None))
				component2 = int(request.POST.get('comp2', None))
				connection2 = int(request.POST.get('conn2', None))				
				cir.disconnect(component1,connection1,component2,connection2)
				mes = pickle.dumps(cir)
				circuit.circuit = mes	
				circuit.save()
				flag = 1
				mes = pickle.dumps(cir)
				circuit.circuit = mes	
				circuit.save()				
				response_data = {}
				components = []
				connections = []
				for comp in cir.components:
					component = cir.components[comp]
					l = []
					name = component.getName()
					if name == "AND" or name == "OR" or name == "XOR" or name == "NOT" or name == "NOR" or name == "NAND" or name == "EQUIV": 
						l.append(component.id)
						l.append(component.getName())
						l.append(component.no)
							
						components.append(l)
					else:
						l.append(component.id)
						l.append(component.getName())
						l.append(component.no)
						l.append(component.get())
						components.append(l)
				for key in cir.connections:
					tup1 = cir.connections[key]
					l = []
					l.append(key)
					l.append(tup1)
					connections.append(l)
				o = []
				if circuit.input_set == True:
					o = cir.getoutput()	
					circuit.save()				
				response_data['connections'] = connections
				response_data['components'] = components
				response_data['freeinpins'] = cir.freeinpins()
				response_data['freeoutpins'] = cir.freeoutpins()
				response_data['output'] = o
				return JsonResponse(response_data)								
			elif del_form.is_valid():	
				component1 = int(request.POST.get('del1', None))
				cir.delComponent(component1)
				mes = pickle.dumps(cir)
				circuit.circuit = mes	
				circuit.save()
				flag = 1
				mes = pickle.dumps(cir)
				circuit.circuit = mes	
				circuit.save()				
				response_data = {}
				components = []
				connections = []
				for comp in cir.components:
					component = cir.components[comp]
					l = []
					name = component.getName()
					if name == "AND" or name == "OR" or name == "XOR" or name == "NOT" or name == "NOR" or name == "NAND" or name == "EQUIV": 
						l.append(component.id)
						l.append(component.getName())
						l.append(component.no)
							
						components.append(l)
					else:
						l.append(component.id)
						l.append(component.getName())
						l.append(component.no)
						l.append(component.get())
						components.append(l)
				for key in cir.connections:
					tup1 = cir.connections[key]
					l = []
					l.append(key)
					l.append(tup1)
					connections.append(l)
				o = []
				if circuit.input_set == True:
					o = cir.getoutput()	
					circuit.save()				
				response_data['connections'] = connections
				response_data['components'] = components
				response_data['freeinpins'] = cir.freeinpins()
				response_data['freeoutpins'] = cir.freeoutpins()
				response_data['output'] = o
				return JsonResponse(response_data)			
			elif setinput.is_valid():

				inputs = request.POST.get('inputs', None)
				inp = inputs.split(" ")
				print(inp)
				l = []
				for i in inp:
					if i == "True":
						l.append(True)
					elif i == "False":
						l.append(False)

		
				cir.setinput(l)
				circuit.input_set = True
				flag = 1
				mes = pickle.dumps(cir)
				circuit.circuit = mes	
				circuit.save()				
				response_data = {}
				components = []
				connections = []
				for comp in cir.components:
					component = cir.components[comp]
					l = []
					name = component.getName()
					if name == "AND" or name == "OR" or name == "XOR" or name == "NOT" or name == "NOR" or name == "NAND" or name == "EQUIV": 
						l.append(component.id)
						l.append(component.getName())
						l.append(component.no)
							
						components.append(l)
					else:
						l.append(component.id)
						l.append(component.getName())
						l.append(component.no)
						l.append(component.get())
						components.append(l)
				for key in cir.connections:
					tup1 = cir.connections[key]
					l = []
					l.append(key)
					l.append(tup1)
					connections.append(l)
				o = []
				if circuit.input_set == True:
					o = cir.getoutput()	
					circuit.input_set = False
					circuit.save()				
				response_data['connections'] = connections
				response_data['components'] = components
				response_data['freeinpins'] = cir.freeinpins()
				response_data['freeoutpins'] = cir.freeoutpins()
				response_data['output'] = o
				return JsonResponse(response_data)					
			elif switch_form.is_valid():
				switchNo = int(request.POST.get('switchNo', None))
				setNo = int(request.POST.get('setNo', None))
				comp = cir.getComponent(switchNo)
				comp.set(setNo)
				mes = pickle.dumps(cir)
				circuit.circuit = mes	
				circuit.save()
				flag = 1
				mes = pickle.dumps(cir)
				circuit.circuit = mes	
				circuit.save()				
				response_data = {}
				components = []
				connections = []
				for comp in cir.components:
					component = cir.components[comp]
					l = []
					name = component.getName()
					if name == "AND" or name == "OR" or name == "XOR" or name == "NOT" or name == "NOR" or name == "NAND" or name == "EQUIV": 
						l.append(component.id)
						l.append(component.getName())
						l.append(component.no)
							
						components.append(l)
					else:
						l.append(component.id)
						l.append(component.getName())
						l.append(component.no)
						l.append(component.get())
						components.append(l)
				for key in cir.connections:
					tup1 = cir.connections[key]
					l = []
					l.append(key)
					l.append(tup1)
					connections.append(l)
				o = []
				if circuit.input_set == True:
					o = cir.getoutput()	
					circuit.save()				
				response_data['connections'] = connections
				response_data['components'] = components
				response_data['freeinpins'] = cir.freeinpins()
				response_data['freeoutpins'] = cir.freeoutpins()
				response_data['output'] = o
				return JsonResponse(response_data)	
			
			if flag == 0:
				if request.method == "POST":
					print("sena")
					if(request.POST.get('del',None) == '1'):
						component1 = int(request.POST.get('del1', None))
						cir.delComponent(component1)
						mes = pickle.dumps(cir)
						circuit.circuit = mes	
						circuit.save()
						flag = 1
						mes = pickle.dumps(cir)
						circuit.circuit = mes	
						circuit.save()				
						response_data = {}
						components = []
						connections = []
						for comp in cir.components:
							component = cir.components[comp]
							l = []
							name = component.getName()
							if name == "AND" or name == "OR" or name == "XOR" or name == "NOT" or name == "NOR" or name == "NAND" or name == "EQUIV": 
								l.append(component.id)
								l.append(component.getName())
								l.append(component.no)
									
								components.append(l)
							else:
								l.append(component.id)
								l.append(component.getName())
								l.append(component.no)
								l.append(component.get())
								components.append(l)
						for key in cir.connections:
							tup1 = cir.connections[key]
							l = []
							l.append(key)
							l.append(tup1)
							connections.append(l)
						o = []
						if circuit.input_set == True:
							o = cir.getoutput()	
							circuit.save()				
						response_data['connections'] = connections
						response_data['components'] = components
						response_data['freeinpins'] = cir.freeinpins()
						response_data['freeoutpins'] = cir.freeoutpins()
						response_data['output'] = o
						return JsonResponse(response_data)
					elif(request.POST.get('del',None) == '2'):
						response_data = {}
						components = []
						connections = []
						for comp in cir.components:
							component = cir.components[comp]
							l = []
							name = component.getName()
							if name == "AND" or name == "OR" or name == "XOR" or name == "NOT" or name == "NOR" or name == "NAND" or name == "EQUIV": 
								l.append(component.id)
								l.append(component.getName())
								l.append(component.no)
									
								components.append(l)
							else:
								l.append(component.id)
								l.append(component.getName())
								l.append(component.no)
								l.append(component.get())
								components.append(l)
						for key in cir.connections:
							tup1 = cir.connections[key]
							l = []
							l.append(key)
							l.append(tup1)
							connections.append(l)
						o = []
						if circuit.input_set == True:
							o = cir.getoutput()	
							circuit.save()				
						response_data['connections'] = connections
						response_data['components'] = components
						response_data['freeinpins'] = cir.freeinpins()
						response_data['freeoutpins'] = cir.freeoutpins()
						response_data['output'] = o
						return JsonResponse(response_data)
				circuit.flag = 1
				cir.save()				
			mes = pickle.dumps(cir)
			circuit.circuit = mes	
			circuit.save()				
			response_data = {}
			components = []
			connections = []
			for comp in cir.components:
				component = cir.components[comp]
				l = []
				name = component.getName()
				if name == "AND" or name == "OR" or name == "XOR" or name == "NOT" or name == "NOR" or name == "NAND" or name == "EQUIV": 
					l.append(component.id)
					l.append(component.getName())
					l.append(component.no)
						
					components.append(l)
				else:
					l.append(component.id)
					l.append(component.getName())
					l.append(component.no)
					l.append(component.get())
					components.append(l)
			for key in cir.connections:
				tup1 = cir.connections[key]
				l = []
				l.append(key)
				l.append(tup1)
				connections.append(l)
			o = []
			if circuit.input_set == True:
				o = cir.getoutput()	
				circuit.input_set = False
				circuit.save()				
			response_data['connections'] = connections
			response_data['components'] = components
			response_data['freeinpins'] = cir.freeinpins()
			response_data['freeoutpins'] = cir.freeoutpins()
			response_data['output'] = o
			return redirect('/web_app/circuit/'+str(name)+'/')
		
	def save_circuit(self,request,name):
		circuit = Circuit_hold.objects.get(name=name)
		circuit.circuit.save()
		circuit.flag = True		
		return redirect('/web_app/circuit/')

	def get(self,request,name):
		circuit = Circuit_hold.objects.get(name=name)
		c = circuit.circuit
		file = 'x.txt'
		with open(file, 'wb') as output:
			output.write(c)		
		f = open(file, 'rb')
		cir = pickle.load(f)
		f.close()	
		open(file, 'w').close()	
		inp = cir.freeinpins()
		out = cir.freeoutpins()
		conns = cir.connections
	
		components = []
		connections = []
		for comp in cir.components:
			component = cir.components[comp]
			l = []
			name = component.getName()
			if name == "AND" or name == "OR" or name == "XOR" or name == "NOT" or name == "NOR" or name == "NAND" or name == "EQUIV": 
				l.append(component.id)
				l.append(component.getName())
				l.append(component.no)
					
				components.append(l)
			else:
				l.append(component.id)
				l.append(component.getName())
				l.append(component.no)
				l.append(component.get())
				components.append(l)
		for key in cir.connections:
			tup1 = cir.connections[key]
			l = []
			l.append(key)
			l.append(tup1)
			connections.append(l)
		o = []
		if circuit.input_set == True:
			o = cir.getoutput()	
			circuit.input_set = False
			circuit.save()		
		return render(request, "circuit_form.html",{'component_form': ComponentForm(),
												'switch_form':switchSet(),
												'connect_form' : ConnectForm(),
												'disConnect_form' : disConnectForm(),
												'del_form' : delComponentForm(),
												'setinput': setInputForm(),
												'output' : o,
												'conns' : connections,
												'inp' : cir.freeinpins(),
												'out' : cir.freeoutpins(),
												'comps': components})	
