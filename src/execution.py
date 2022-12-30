from elements.map import Map
from elements.elements import *
from compiler.compiler import *

#todo: get the execution list
#todo: generar codigo de funciones
#todo: terminar value method
class Code:
    def __init__(self) -> None:
        self.elements= dict()
        self.vars= dict()

        self.execution_list = list()
        self.compiled_list= list[obj]

        self.map= Map()

    def compile(self, code: str):
        self.compiled_list= compile(code)
        for compiled in self.compiled_list:

            #ELEMENTS
            #todo: params with vars. ex: nation a(provinces: [b])
            if compiled.type == 'element':
                self.add_element(compiled.subtype, **self.params(compiled))
            
            #VARS
            elif compiled.type == 'var':
                self.add_var(compiled.name, self.value(compiled.value))
            
            #FUNCTIONS
            elif compiled.type == 'function':
                ...
            
            else:
                print(self.value(compiled))

    def value(self, object: obj):
        if type(object) == obj:
            if object.type == 'arithmetic':
                left= self.value(object.left)
                right= self.value(object.right)

                if object.subtype == '+':
                    return left + right
                if object.subtype == '*':
                    return left * right
                if object.subtype == '/':
                    return left / right
                if object.subtype == '-':
                    return left - right

            elif object.type == 'list':
                return [self.value(value) for value in object.value]
            
            elif object.type == 'expr':
                return self.value(object.value)
            
            elif object.get('name') and object.name in self.vars:
                return self.vars[object.name]
            
            elif object.get('name') and  object.name in self.map.mapelementsdict:
                return self.map.mapelementsdict[object.name]
            
            else:
                return object.value
        
        else:
            return object
    
    def params(self, object: obj):
        params= dict()
        params['name']= object.name
        for param in object.params:
            params[param.name]= self.value(param.value)
        return params
    
    
    def add_element(self, element: str, **kwargs):
        '''
        Add an element to the map
        :param element: the element to add
        '''
        elements={
            'nation': self.map.add_nation,
            'province': self.map.add_province,
            'sea': self.map.add_sea,
            'neutral': self.map.add_neutral,
            'trait': self.map.add_trait,
        }
        if element in elements:
            elements[element](**kwargs)
        else:
            raise Exception('The element is not recognized')
    
    #todo: dynamic var type
    def add_var(self, name: str, value):
        '''
        Add a variable to the code
        :param name: the name of the variable
        :param value: the value of the variable
        '''
        self.vars[name]= value
    
    def add_function(self):
        ...
        

    
    
a= Code()
a.compile(
    '''
    province a(extension: 10, development: 20, population: 30);
    a= 1;
    a= 'pollo';
    nation b(provinces: [a]);

    '''
)
print(a.map.mapelementsdict['b'].provinces['a'].extension)
print(a.vars)

