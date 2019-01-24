from abc import ABC


class Component(ABC):
    

    def getName(self):
        pass

    def getInputs(self):
        pass

    def getOutputs(self):
        pass

    def getPicture(self):
        pass



    def calculate(self,inputList):
        pass

class AND(Component):
    def __init__(self,no):
        self.no = no
        self.inp = []
        for i in range(no):
            self.inp.append(False)
        self.out = True
        self.id = -1

    def getName(self):
        return "AND"

    def getInputs(self):
        res = []
        for i in range(self.no):
            res.append("i"+str(i))
        return res

    def getOutputs(self):
        return ["out"]

    def getPicture(self):
        return """<svg height="52" width="70">
                  <path fill = "none" stroke="black" 
                      d="m 50,0
                      q 25,25  0,50
                      " />
                  <path fill = "none" stroke="black"
                      d="m 50,0
                        l -30,0
                        "/>
                  <path fill = "none" stroke ="black"
                      d = "m 50,50
                        l -30,0
                        "/>
                   <path fill = "none" stroke ="black"
                      d = "m 20,0
                        l 0,50
                        "/>

                </svg>"""


    def calculate(self,inputList):
        
        self.out = inputList[self.no-1]
        self.inp[self.no-1] = inputList[self.no-1]
        for i in range(len(inputList)-1):
            self.inp[i] = inputList[i]
            self.out = self.out and inputList[i]
        return self.out

class OR(Component):
    def __init__(self,no):
        self.no = no
        self.inp = []
        for i in range(no):
            self.inp.append(False)
        self.out = False
        self.id = -1

    def getName(self):
        return "OR"

    def getInputs(self):
        res = []
        for i in range(self.no):
            res.append("i"+str(i))
        return res

    def getOutputs(self):
        return ["out"]

    def getPicture(self):
        return """<svg height="52" width="70">
                  <path fill = "none" stroke="black" 
                      d="m 20,0
                      q 35,0  50,25
                      " />
                  
                  
                   <path fill = "none" stroke ="black"
                      d = "m 20,0
                        q 25,25 0,50
                        "/>
                  <path fill = "none" stroke="black" 
                      d="m 20,50
                      q 35,0  50,-25
                      " />
                </svg>"""



    def calculate(self,inputList):
        self.out = inputList[self.no-1]
        self.inp[self.no-1] = inputList[self.no-1]
        for i in range(len(inputList)-1):
            self.inp[i] = inputList[i]
            self.out = self.out or inputList[i]
        return self.out

class XOR(Component):
    def __init__(self,no):
        self.no = no
        self.inp = []
        for i in range(no):
            self.inp.append(False)
        self.out = False
        self.id = -1

    def getName(self):
        return "XOR"

    def getInputs(self):
        res = []
        for i in range(self.no):
            res.append("i"+str(i))
        return res

    def getOutputs(self):
        return ["out"]

    def getPicture(self):
        return """<svg height="52" width="70">
                  <path fill = "none" stroke="black" 
                      d="m 20,0
                      q 35,0  50,25
                      " />
                  
                  
                   <path fill = "none" stroke ="black"
                      d = "m 20,0
                        q 25,25 0,50
                        "/>
                  <path fill = "none" stroke="black" 
                      d="m 20,50
                      q 35,0  50,-25
                      " />
                    <path fill = "none" stroke = "black"
                      d= "m 15,0
                        q 25,25 0,50
                        "/>
                </svg>"""



    def calculate(self,inputList):
        self.out = inputList[self.no-1]
        self.inp[self.no-1] = inputList[self.no-1]
        for i in range(len(inputList)-1):
            self.inp[i] = inputList[i]
            self.out = (not self.out and inputList[i]) or (not inputList[i] and self.out)
        return self.out
        

class NOT(Component):
    def __init__(self):
        self.i0 = False
        self.no = 1
        self.out = True
        self.id = -1

    def getName(self):
        return "NOT"

    def getInputs(self):
        return ["i0"]

    def getOutputs(self):
        return ["out"]

    def getPicture(self):
        return """<svg height="52" width="70">
                  <path fill = "none" stroke="black" 
                      d="m 20,0
                      l 0,50  
                      " />
                  
                  
                   <path fill = "none" stroke ="black"
                      d = "m 20,0
                        l 25,25
                        "/>
                  <path fill = "none" stroke="black" 
                      d="m 20,50
                      l 25,-25
                      " />
                    <circle fill = "none" stroke="black" cx = "49" cy="25" r ="4"/>
                </svg>"""


    def calculate(self,inputList):
        self.i0 = inputList[0]
        self.out = not self.i0
        return self.out

class NOR(Component):
    def __init__(self,no):
        self.no = no
        self.inp = []
        for i in range(no):
            self.inp.append(False)
        self.out = True
        self.id = -1

    def getName(self):
        return "NOR"

    def getInputs(self):
        res = []
        for i in range(self.no):
            res.append("i"+str(i))
        return res

    def getOutputs(self):
        return ["out"]

    def getPicture(self):
        return """<svg height="52" width="70">
                  <path fill = "none" stroke="black" 
                      d="m 20,0
                      q 35,0  50,25
                      " />
                  
                  
                   <path fill = "none" stroke ="black"
                      d = "m 20,0
                        q 25,25 0,50
                        "/>
                  <path fill = "none" stroke="black" 
                      d="m 20,50
                      q 35,0  50,-25
                      " />
                  <circle fill = "none" stroke = "black" cx = "74" cy = "25" r ="4"/>    
                  
                </svg>"""


    def calculate(self,inputList):
        self.out = inputList[self.no-1]
        self.inp[self.no-1] = inputList[self.no-1]
        for i in range(len(inputList)-1):
            self.inp[i] = inputList[i]
            self.out = not (self.out or inputList[i])
        return self.out
        

class NAND(Component):
    def __init__(self,no):
        self.no = no
        self.inp = []
        for i in range(no):
            self.inp.append(False)
        self.out = True
        self.id = -1

    def getName(self):
        return "NAND"

    def getInputs(self):
        res = []
        for i in range(self.no):
            res.append("i"+str(i))
        return res

    def getOutputs(self):
        return ["out"]

    def getPicture(self):
        return """<svg height="52" width="70">
                  <path fill = "none" stroke="black" 
                      d="m 50,0
                      q 25,25  0,50
                      " />
                  <path fill = "none" stroke="black"
                      d="m 50,0
                        l -30,0
                        "/>
                  <path fill = "none" stroke ="black"
                      d = "m 50,50
                        l -30,0
                        "/>
                   <path fill = "none" stroke ="black"
                      d = "m 20,0
                        l 0,50
                        "/>
                  <circle fill = "none" stroke = "black" cx = "68" cy = "25" r ="4"/>    
                  
                </svg>"""


    def calculate(self,inputList):
        self.out = inputList[self.no-1]
        self.inp[self.no-1] = inputList[self.no-1]
        for i in range(len(inputList)-1):
            self.inp[i] = inputList[i]
            self.out = not (self.out and inputList[i])
        return self.out
        

class EQUIV(Component):
    def __init__(self):
        self.i0 = False
        self.no = 1
        self.out = False
        self.id = -1

    def getName(self):
        return "EQUIV"

    def getInputs(self):
        return ["i0"]

    def getOutputs(self):
        return ["out"]

    def getPicture(self):
        return """<svg height="52" width="70">
                  <path fill = "none" stroke="black" 
                      d="m 20,0
                      l 0,50  
                      " />
                  
                  
                   <path fill = "none" stroke ="black"
                      d = "m 20,0
                        l 25,25
                        "/>
                  <path fill = "none" stroke="black" 
                      d="m 20,50
                      l 25,-25
                      " />
                    
                </svg>"""

    def calculate(self,inputList):
        self.i0 = inputList[0]
        self.out = self.i0
        return self.out
        


class SWITCH(Component):
    def __init__(self,no):
        self.no = no
        self.state = '0'*self.no
        
        self.id = -1

    def getName(self):
        return "SWITCH"

    def getInputs(self):
        return []

    def getOutputs(self):
        res = []
        for i in range(self.no):
            res.append("out"+str(i))
        return res
        

    def getPicture(self):
        return '''<svg width="100" height="100">
	<rect x = "10" y = "10" width = "80" height = "80" fill= "none" stroke = "black" stroke-width = "4"/>
   <circle cx="50" cy="50" r="40" stroke="black" stroke-width="4" fill="red" />
</svg> '''
    
    def get(self):
        return self.state

    def set(self,i):
        self.state = bin(i)[2:]
        if len(self.state) != self.no:
        	temp = '0'*(self.no-len(self.state))
        	self.state = temp+self.state


    def calculate(self,inputList):
        pass

class LED(Component):
    def __init__(self,no):
        self.no = no
        
        self.state = ['0']*self.no
        self.id = -1

    def getName(self):
        return "LED"

    def getInputs(self):
        res = []
        for i in range(self.no):
            res.append("i"+str(i))
        return res

    def getOutputs(self):
        return []

    def getPicture(self):
        return '''<svg width="52" height="70">
   <circle cx="50" cy="50" r="40" stroke="black" stroke-width="4" fill="none" />
</svg> '''

    def get(self):
        return ''.join(self.state)

    def set(self):
        pass

    def calculate(self,inputList):
        pass

