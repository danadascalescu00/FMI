import os
import sys
from helpers import *
from copy import deepcopy

class AnalizatorLexical:
    def __init__(self):
        self.base_dir = 'C:/Users/Dana/Desktop/University/Anul 3/TC/AnalizatorLexical/data/'
        self.input_file_name = 'test1.c'
        self.input_file_path = os.path.join(self.base_dir, self.input_file_name)
        self.dir_save_files = os.path.join(self.base_dir, 'salveazaFisiere')

        try:
            if not os.path.exists(self.dir_save_files):
                os.makedirs(self.dir_save_files)
                print('directory created: {}'.format(self.dir_save_files))
            else:
                print('directory {} exists'.format(self.dir_save_files))
        except:
            print('Unexpected error: ', sys.exc_info()[0])

        self.output_file_name = None


    def validate_extension(self):
        try:
            file_name, extension = self.input_file_name.split('.')
        except ValueError:
            return False
        
        if extension.replace("\\r\\n", "").replace(" ", "") == "c":
            self.output_file_name = file_name + '_out.txt'
            self.output_file_path = os.path.join(self.dir_save_files, self.output_file_name)
            return True
        return False


    def read_line(self):
        input_file = open(self.input_file_path, 'r')

        while True:
            line = input_file.readline()
            yield line


    def run(self):
        try:
            if self.validate_extension():
                output_file = open(self.output_file_path, 'w+')

                row, current_pointer, length = 1, 0 ,0
                for line in self.read_line():
                    if line == "":
                        print('EOF')
                        output_file.close()
                        break
                    else:
                        for match in re.finditer(tokens,line):
                            token_type = match.lastgroup
                            token = match.group(token_type)
                            length = len(token)

                            if token_type == 'NEWLINE':
                                row += 1
                            elif token_type == 'SKIP' or token_type == 'SINGLELINE_COMMENT' or token_type == 'MULTILINE_COMMENT' or token_type == 'PREPROCESSOR_DIRECTIVES':
                                continue
                            elif token_type == 'ERROR':
                                print('Unexpected error at line {} and position {}: {}'.format(row,current_pointer,token))
                            else:
                                output_file.writelines('Token = {0}, Lexeme = \'{1}\', Line = {2}, Position = {3}, Length = {4}\n'.format(token_type, token, row, current_pointer, length))
                            current_pointer += length          
            else:
                print('NOT A C FILE!')
                sys.exit(1)
        except:
            print("Unexpected error: ", sys.exc_info()[1])