import re

RULES = [
            ('MULTILINE_COMMENT', r'/\*[\s\S]*?\*/'), ('SINGLELINE_COMMENT', r'\/\/([^\/]+)'),
            ('MAIN', r'main'), ('AUTO', r'auto'), ('BREAK', r'break'), ('CASE', r'case'), 
            ('CHAR', r'char'), ('CONST', r'const'), ('CONTINUE', r'continue'), ('DEFAULT', r'default'), 
            ('DO', r'do'), ('DOUBLE', r'double'), ('ELSE', r'else'), ('ENUM', r'enum'), 
            ('EXTERN', r'extern'), ('FLOAT', r'float'), ('FOR', r'for'), ('GOTO', r'goto'),
            ('IF', r'if'), ('INT', r'int'), ('LONG', r'long'), ('REGISTER', r'register'),
            ('RETURN', r'return'), ('SHORT', r'short'), ('SIGNED', r'signed'), ('SIZEOF', r'sizeof'),
            ('STATIC', r'static'), ('STRUCT', r'struct'), ('SWITCH', r'switch'), ('TYPEDEF', r'typedef'),
            ('UNION', r'union'), ('UNSIGNED', r'unsigned'), ('VOID', r'void'), ('VOLATILE', r'volatile'),
            ('WHILE', r'while'), ('INCLUDE', r'include'), ('READ', r'read'), ('PRINT', r'print'),
            ('LBRACKET', r'\('), ('RBRACKET', r'\)'), ('LBRACE', r'\{'), ('RBRACE', r'\}'),
            ('COMMA', r','), ('PCOMMA', r';'), ('NEWLINE', r'\n'), ('SKIP', r'[ \t]+'),
            ('EQ', r'=='), ('NE', r'!='), ('LE', r'<='), ('GE', r'>='), ('LT', r'<'), ('GT', r'>'), 
            ('OR', r'\|\|'), ('AND', r'&&'), ('ATTR', r'\='), ('PLUS', r'\+'), ('MINUS', r'-'),
            ('MULT', r'\*'), ('DIV', r'\/'), ('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]*'),
            ('INTEGER', r'[1-9][0-9]*[uU]?[lL]?[lL]?|0x[0-9a-fA-F]+[uU]?[lL]?[lL]?|(0[0-7]*[uU]?[lL]?[lL]?)|[0-9]'),
            ('FLOAT_NUMERAL', r'[-+]?[0-9]+\.?[0-9]+([eE][-+]?[0-9]+)?'), 
            ('CHARACTER_LITERAL', r'[\'].[\']'), ('STRING', r'["]([^"\\\n]|\\.|\\\n)*["]'),
            ('PREPROCESSOR_DIRECTIVES', r'([#!][A-z]{2,}[ ]*[\<|\"]?[ A-z.\(\,\)\>\?\:\<\'\]*[ ]*[\d]*[\>]?)'),
            ('ERROR', r'.')
    ]

tokens = '|'.join('(?P<%s>%s)' % rule for rule in RULES)