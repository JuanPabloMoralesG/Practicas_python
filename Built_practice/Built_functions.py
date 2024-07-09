#math buildt-ins

def bool_fun(data):
    return bool(data)

def int_fun(data):
    return int(data)

def float_fun(data):
    return  float(data)

def complex_fun(real_Part,complex_Part):
    return complex(real_Part,complex_Part)

def max_fun(data):
    return max(data)

def min_fun(data):
    return min(data)

def divmod_fun(num1,num2):
    return divmod(num1,num2)

def abs_fun(num):
    return abs(num)

def pow_fun(bas,exp,mod=None):
    return pow(bas,exp,mod)

def round_fun(num,n=None):
    return round(num,n)

def sum_fun(data): #__add__
    return sum(data)


#Collections

dict()# elemenots agrupados por clave-valor
list()#secuencia
tuple()# secuencia inmutable
set() #elementos unicos
frozenset() #elementos unicos inmutables

#string-byte
data = bytes(b"Hola")
#print(data[0])
#print("Hola".encode())

bytearray() #Byte mutable
str()
# memoryview() # crea una vista de un objeto a partir de un buffer de datos
open("./hola.txt","w") #abre un archivo
chr(1) #convierte de asci a caracter
ord("w") #convierte un caracter a asci
bin(10)
oct(10) #representar numeros en otras bases
hex(10)

def format_fun(name,age):
    formated_user = "Name:{}, Age:{}".format(name,age)
    formated_user = f"Name:{name},Age:{age:x}"
    return formated_user

#input()
ascii("æ")
repr("æ")

#Iteration

iterator = iter([1,2,3]) # crea un iterador
assert next(iterator) == 1 # 

enumList = enumerate(["uno","dos","tres"]) #Indexa la lista

l1=[1,2,3]
l2=["a","b","c"]
zipped = list(zip(l1,l2))
revZipped = list(reversed(zipped))
sortZipped = sorted(revZipped)
filter #salta elementdos dependiendo si cumplen la condicion
map #aplicauna funcion a cada elemento de una lista
all([1,1,1]) #Valida que todo es verdad
any([0,0,1]) # Valida que algo es verdad
range(1,10) #devuelve los valores incluyendo el inicio pero no el fin
slice(1,4)# inclute el final pero no el inicio

async def ex_aiter():
    async def async_generator():
        yield 1
        yield 2
        yield 3
    async_gen = async_generator()
    async_iter = aiter(async_gen)

    assert await anext(async_iter)==1

    #async for x in async_generator():

#ex_aiter()

#Debugging

import sys
#breakpoint()
#help()
#print("hola",file=sys.stderr)

#Object

obj =object()
assert obj is not None

class Example:
    def __init__(self):
        self.attribute = 42
class Sub_Example(Example):
    def __init__(self):
        return super()
instance = Example()

assert getattr(instance,"attribute","default")==42
setattr(instance,"new_attribute","hola")
hasattr(instance,"new_attribute")
delattr(instance,"attribute")
dir([1,2,3]) #lista alfabetica no se garantisa que sea correcta o completa
id(instance) # numero que identifica cada objeto en python
var = "hola"
print("1" if hash("hola")== hash(var) else "2")
len("2")
assert isinstance(instance,Example)
assert issubclass(Example,object)
callable #metodos, clases, funciones son llamables (ej. string no lo es)
super #tomar algo de la clase padre
type #te dece el tipo de objeto o crea un nuevo tipo de objeto

NewType = type("NewType",(object,),{"name":"Hola"})
instance =NewType()
assert instance.name == "Hola"

#Descriptor

class Descriptor:
    def __init__(self,value):
        self.value = value
    
    @property
    def value(self):
        return self.value
    @value.setter
    def value(self,val):
        self._value = val
    @value.getter
    def value(self):
        return self.value

    @classmethod
    def class_method(cls):
        return cls.__name__
    
    @staticmethod
    def static_method():
        return "Hola"
    
descriptorIstance = Descriptor()
#dinamic/code
x = 1
code = 'print("Hola mundo")'
assert eval("x+1") #evalua una exprecion(str) como codigo
compiled_code = compile(code, "<string>","exec") #puede servir para precompilar codigo que se use mucho
exec(compiled_code) #Ejecuta una exprecion(str) como codigo
globals() #diccionario de variables globales, se puede modificar
print(locals()) #diccionario de variables locales, no modifica variables locales
vars_dic = vars(descriptorIstance) #retorna un diccionario de las variables del objeto
math = __import__("math")  #importa un modulo