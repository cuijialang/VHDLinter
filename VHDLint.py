import os
import platform
import pyfiglet
import shutil
import config as cfg
from termcolor import colored

class VHDLint:

    def __init__(self):

        self.dir = cfg.DIRECTORY
        self.max_line_length = cfg.MAX_LINE_LENGTH


    def get_files(self):

        files = []
        file_dirs = []
        for f in os.listdir(self.dir):
            if f.endswith(".vhd"):
                files.append(f)
                file_dirs.append(self.dir+f)
        return files, file_dirs
        
        
    def make_backup_copies(self, target_dir, file_names, file_paths):
        
        try:
            os.mkdir(target_dir)
        except:
            pass
        
        i = 0
        for original in file_paths:
            target = target_dir + "/" + file_names[i]
            shutil.copyfile(original, target)
            i+=1

    def read_files(self, my_file):

        line_no = 0
        f = open(self.dir+my_file, "r")
        if f.mode == "r":
            self.lines = []
            f_lines = f.readlines()
            for line in f_lines:
                line_no += 1
                self.lines.append(line)
            f.close()

    def check_comments(self):

        type123 = "Ugly comment"
        i = 1
        for line in self.lines:
            chk1 = line.lower().find("xxx", 0)
            if chk1 != -1:
                print(str(i) + ", " + type123 + ": " + line.lstrip())
            chk2 = line.lower().find("todo", 0)
            chk3 = line.lower().find("to do", 0)
            if chk2 != -1 or chk3 != -1:
                print(str(i) + ", " + type123 + ": " + line.lstrip())
            i += 1

    def check_semicolons(self):

        type1 = "Space before semicolon"
        i = 1
        for line in self.lines:
            chk1 = line.lower().find(" ;", 0)
            if chk1 != -1:
                print(str(i) + ", " + type1 + ": " + line.lstrip())
            i += 1

    def find_reports(self):

        type1 = "Debugging code"
        i = 1
        for line in self.lines:
            chk1 = line.lower().find("report", 0)
            if chk1 != -1:
                print(str(i) + ", " + type1 + ": " + line.lstrip())
            i += 1

    def find_tabs(self):

        type1 = "TabError"
        i = 1
        for line in self.lines:
            chk1 = line.lower().find("\t", 0)
            if chk1 != -1:
                print(str(i) + ", " + type1 + ": " + line.lstrip())
            i += 1

    def check_linelength(self):

        type1 = "Line too long"
        i = 1
        for line in self.lines:
            line_length = len(line)
            if line_length > self.max_line_length:
                hint = " (" + str(line_length) + "/" + str(self.max_line_length) + ")"
                print(str(i) + ", " + type1 + hint + ": " + line.lstrip())
            i += 1

    def check_time_units(self):

        type1 = "Add space before time unit!"
        i = 1
        for line in self.lines:
            for unit in ["ns", "ms", "ps"]:
                chk1 = line.lower().find(unit + ";", 0)
                chk2 = line.lower().find(unit + " ", 0)
                chk_correct = line.lower().find(" " + unit, 0)
                if (chk1 != -1 or chk2 != -1) and chk_correct == -1:
                    print(str(i) + ", " + type1 + ": " + line.lstrip())
            i += 1

    def trailing_spaces(self):

        type1 = "Trailing Spaces"
        i = 1
        for line in self.lines:
            line = line.lstrip()
            chk = line.find("  ", 0)
            chk_e1 = line.find(":", 0)
            chk_e2 = line.find("=>", 0)
            if chk != -1 and (chk_e1 == -1 and chk_e2 == -1):
                print(str(i) + ", " + type1 + ": " + line.lstrip())
            i += 1

    def tab2space(self, my_file):


        # TODO: edit lines[], not content
        f = open(self.dir + my_file, "r")
        content = f.read()
        f.close()
        chk = content.find("\t", 0)
        while chk != -1:
            content = content.replace("\t", "    ")
            chk = content.find("\t", 0)
#        f = open(self.dir + my_file, "w")
#        f.write(content)
#        f.close()


    def add_comment_space(self, my_file):

        # TODO: edit lines[], not content
        # Delete white spaces at end of lines
        f = open(self.dir + my_file, "r")
        content = f.read()
        f.close()

        # Insert space between semicolon and comment
        chk = content.find(";--", 0)
        if chk != -1:  
            content = content.replace(";--", "; --")
#        f = open(self.dir + my_file, "w")
#        f.write(content)
#        f.close()


    def delete_wspaces(self, my_file):

        i = 0
        for line in self.lines:
            line_length = len(line.lstrip())

            if line_length == 0:
                #empty line
                self.lines[i] += "\n"
            else:
                # TODO
                # should be right stripped to remove whitespaces at eol
                # content += line.rstrip()
                self.lines[i] += line
            i += 1


    def edit_file(self, my_file):

        content = ""
        for line in self.lines:
            content += line

        f = open(self.dir + my_file, "w")
        f.write(content)
        f.close()        


if __name__ == "__main__":

    ascii_banner = pyfiglet.figlet_format("VHDLint")
    print("\n" + ascii_banner)
    print("No config file found, using default configuration \n")

    o = VHDLint()


    FILES, FILE_DIRS = o.get_files()
    
    if cfg.BACKUP:
        bak_folder = cfg.bak_folder
        o.make_backup_copies(bak_folder, FILES, FILE_DIRS)

    for my_file in FILES:

        if platform.platform().find("Linux") == -1:
            os.system('color')
        print(colored("************ " + my_file, cfg.color_filename))
        
        o.read_files(my_file)

        if cfg.CODE_CHECK:

            o.check_comments()
            o.check_semicolons()
            o.check_linelength()
            o.check_time_units()
            o.trailing_spaces()
            #o.find_tabs()
            #o.find_reports()
            
        if cfg.FORMATTING:
                
            if cfg.delete_wspaces:
                pass
                #o.delete_wspaces(my_file)
            
            if cfg.tab2space:
                pass
                #o.tab2space(my_file)

            if cfg.comment_space:
                pass
                #o.add_comment_space(my_file)
                
            o.edit_file(my_file)
