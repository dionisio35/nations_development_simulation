from sly import Lexer, Parser

class NDSLexer(Lexer):
    tokens = {'NATION', 'PROVINCE', 'SEA', 'NEUTRAL', 'EVENT', 'DISTRIBUTION',
            'NAME',
            'NUMBER',
            'ASSIGN',
            'FOR', 'WHILE', 'IF', 'ELSE',
            'GREATER', 'LESS', 'XPLUS', 'XMINUS',
            'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS'}
    
    literals = { '(', ')', '{', '}', '[', ']', ';', ',' }

    ignore = "\t "

    newline = r'\n+'
    def newline(self, t):
        self.lineno += t.value.count('\n')

    #ELEMENTS
    NATION= r'nation\s+'
    def NATION(self, t):
        t.value = str(t.value).strip()
        return t
    
    PROVINCE= r'province\s+'
    def PROVINCE(self, t):
        t.value = str(t.value).strip()
        return t
    
    SEA= r'sea\s+'
    def SEA(self, t):
        t.value = str(t.value).strip()
        return t
    
    NEUTRAL= r'neutral\s+'
    def NEUTRAL(self, t):
        t.value = str(t.value).strip()
        return t
    
    EVENT= r'event\s+'
    def EVENT(self, t):
        t.value = str(t.value).strip()
        return t
    
    DISTRIBUTION= r'distribution\s+'
    def DISTRIBUTION(self, t):
        t.value = str(t.value).strip()
        return t
    
    #PARAMETERS
    #todo: add parameters if needed


    #LOOPS
    FOR= r'for\s+'
    def FOR(self, t):
        t.value = str(t.value).strip()
        return t
    
    WHILE= r'while\s+'
    def WHILE(self, t):
        t.value = str(t.value).strip()
        return t
    
    #CONDITIONS
    IF= r'if\s+'
    def IF(self, t):
        t.value = str(t.value).strip()
        return t
    
    ELSE= r'else\s+'
    def ELSE(self, t):
        t.value = str(t.value).strip()
        return t
    
    #VARIABLES
    NAME= r'[a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9]*'
    #CONSTANTS
    NUMBER = r'\d+'

    # Special symbols
    ASSIGN = r':'


    XPLUS= r'\+\+'
    XMINUS= r'--'

    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'

    EQUALS= r'='
    GREATER= r'>'
    LESS= r'<'

    # Ignored pattern
    ignore_comment = r'\#.*'

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1




class NDSParser(Parser):
    tokens = NDSLexer.tokens
    debugfile = 'parser.out'

    precedence = (
        # ('left', 'PLUS', 'MINUS'),
        # ('left', 'TIMES', 'DIVIDE'),
        # ('right', 'UMINUS'),
        )

    def __init__(self):
        self.elements = {
            'nations': {},
            'provinces': {},
            'seas': {},
            'neutrals': {},
        }
    
    @_('script ";" script')
    def script(self, p):
        return p.script0 + p.script1
    
    @_('script ";"')
    def script(self, p):
        return p.script
    
    @_('element')
    def script(self, p):
        return p.element

    @_('NATION NAME params', 'PROVINCE NAME params', 'SEA NAME params', 'NEUTRAL NAME params')
    def element(self, p):
        # print(1, p.NAME, p.params)
        if p[0] == 'nation':
            self.elements['nations'][p.NAME] = p.params
            return p.NAME
        elif p[0] == 'province':
            self.elements['provinces'][p.NAME] = p.params
            return p.NAME
        elif p[0] == 'sea':
            self.elements['seas'][p.NAME] = p.params
            return p.NAME
        elif p[0] == 'neutral':
            self.elements['neutrals'][p.NAME] = p.params
            return p.NAME
    

    @_('"(" param ")"')
    def params(self, p):
        # print(2, p.param)
        return p.param

    @_('param "," param')
    def param(self, p):
        # print(3, p.param0, p.param1)
        return p.param0 + p.param1
        
    @_('NUMBER')
    def param(self, p):
        # print(4, p.NUMBER)
        return [int(p.NUMBER)]





def compile(code: str):
    lexer = NDSLexer()
    parser = NDSParser()

    tokens = lexer.tokenize(code)
    parser.parse(tokens)
    print(parser.elements)

compile(
    '''
    nation a(2, 3,
    5);
    nation b(3);
    province c(4);
    nation d(5);
    nation e(6);
    neutral f(7);
    '''
)