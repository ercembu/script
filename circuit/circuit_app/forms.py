from django import forms
from circuit_app.models import *
#from circuit_app.circuits import Circuit
#from circuit_app.component import Component
COMPONENTS = [('AND','AND'),('OR','OR'),('NOR','NOR'),('NAND','NAND'),('EQUIV','EQUIV'),('XOR','XOR'),('NOT','NOT'),('LED','LED'),('SWITCH','SWITCH')]

class CircuitForm(forms.ModelForm):
	class Meta:
		model = Circuit_hold
		fields = ['name',]
		labels = {
					'name': 'Circuit name',
				 }
class CircuitListForm(forms.Form):				 
	circuit = forms.ModelChoiceField(queryset=Circuit_hold.objects.all(), label='Circuits')

class ComponentForm(forms.Form):
	component_name = forms.ChoiceField(choices=COMPONENTS)
	input_number = forms.IntegerField()

class ConnectForm(forms.Form):
	component1 = forms.IntegerField()
	connection1 = forms.IntegerField()
	component2 = forms.IntegerField()
	connection2 = forms.IntegerField()

class disConnectForm(forms.Form):
	comp1 = forms.IntegerField()
	conn1 = forms.IntegerField()
	comp2 = forms.IntegerField()
	conn2 = forms.IntegerField()
	
class delComponentForm(forms.Form):
	del1 = forms.IntegerField()

class setInputForm(forms.Form):
	inputs = forms.CharField(max_length=1000) 

class switchSet(forms.Form):
	switchNo = forms.IntegerField()
	setNo = forms.IntegerField()