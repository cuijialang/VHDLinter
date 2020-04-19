import os
import pyfiglet
import config as cfg
from termcolor import colored

class VHDLint:

    def __init__(self):

        self.dir = cfg.DIRECTORY
        self.max_line_length = cfg.MAX_LINE_LENGTH


    def get_files(self):

        files = []
        for f in os.listdir(self.dir):
            if f.endswith(".vhd"):
                files.append(f)
        return files


    def read_files(self, file):
        line_no = 0
        f_path = self.dir+file
        f = open(f_path, "r")
        if f.mode == "r":
            lines = []
            my_file = f.readlines()
            for line in my_file:
                line_no += 1
                lines.append(line)
            f.close()
            return lines

    def check_comments(self, lines):

        type123 = "Ugly comment"
        i = 1

        for line in lines:
            chk1 = line.lower().find("xxx", 0)
            if chk1 != -1:
                print(str(i) + ", " + type123 + ": " + line.lstrip())

            chk2 = line.lower().find("todo", 0)
            chk3 = line.lower().find("to do", 0)
            if chk2 != -1 or chk3 != -1:
                print(str(i) + ", " + type123 + ": " + line.lstrip())
            i += 1

    def check_semicolons(self, lines):

        type1 = "Space before semicolon"
        i = 1

        for line in lines:
            chk1 = line.lower().find(" ;", 0)
            if chk1 != -1:
                print(str(i) + ", " + type1 + ": " + line.lstrip())
            i += 1

    def find_reports(self, lines):

        type1 = "Debugging code"
        i = 1

        for line in lines:
            chk1 = line.lower().find("report", 0)
            if chk1 != -1:
                print(str(i) + ", " + type1 + ": " + line.lstrip())
            i += 1

    def find_tabs(self, lines):

        type1 = "TabError"
        i = 1

        for line in lines:
            chk1 = line.lower().find("\t", 0)
            if chk1 != -1:
                print(str(i) + ", " + type1 + ": " + line.lstrip())
            i += 1

    def check_linelength(self, lines):

        type1 = "Line too long"
        i = 1

        for line in lines:
            line_length = len(line)
            if line_length > self.max_line_length:
                hint = " (" + str(line_length) + "/" + str(self.max_line_length) + ")"
                print(str(i) + ", " + type1 + hint + ": " + line.lstrip())
            i += 1

    def check_time_units(self, lines):

        type1 = "Add space before time unit!"
        i = 1

        for line in lines:
            for unit in ["ns", "ms", "ps"]:
                chk1 = line.lower().find(unit + ";", 0)
                chk2 = line.lower().find(unit + " ", 0)
                chk_correct = line.lower().find(" " + unit, 0)
                if (chk1 != -1 or chk2 != -1) and chk_correct == -1:
                    print(str(i) + ", " + type1 + ": " + line.lstrip())
            i += 1

    def trailing_spaces(self, lines):

        type1 = "Trailing Spaces"
        i = 1

        for line in lines:
            line = line.lstrip()
            chk = line.find("  ", 0)
            chk_e1 = line.find(":", 0)
            chk_e2 = line.find("=>", 0)
            if chk != -1 and (chk_e1 == -1 and chk_e2 == -1):
                print(str(i) + ", " + type1 + ": " + line.lstrip())
            i += 1

    def tab2space(self, file):

        f = open(self.dir + file, "r")
        content = f.read()
        f.close()

        chk = content.find("\t", 0)
        while chk != -1:
            content = content.replace("\t", "    ")
            chk = content.find("\t", 0)

        f = open(self.dir + file, "w")
        f.write(content)
        f.close()


    def rm_eol_spaces(self, file):

        f = open(self.dir + file, "r")
        content = f.read()
        f.close()

        # then
        chk = content.find(" then ", 0)    
        while chk != -1:
            content = content.replace(" then ", " then")
            chk = content.find(" then ", 0)

        # # loop, Problem: loop L1
        # chk = content.find(" loop ", 0)
        # while chk != -1:
            # content = content.replace(" loop ", " loop")
            # chk = content.find(" loop ", 0)


        # Remove all spaces after semicolons
        chk = content.find("; ", 0)
        while chk != -1:
            content = content.replace("; ", ";")
            chk = content.find("; ", 0)

        # Insert space between semicolon and comment
        chk = content.find(";--", 0)
        if chk != -1:    
            content = content.replace(";--", "; --")

        f = open(self.dir + file, "w")
        f.write(content)
        f.close()



if __name__ == "__main__":

    ascii_banner = pyfiglet.figlet_format("VHDLint")
    print("\n" + ascii_banner)
    print("No config file found, using default configuration \n")

    o = VHDLint()

    files = o.get_files()

    for my_file in files:

        # print filename
        os.system('color')
        print(colored("********** " + my_file, "magenta"))

        # Code check and formatting
        if cfg.check:

            lines = o.read_files(my_file)

            o.check_comments(lines)
            o.check_semicolons(lines)
            o.check_linelength(lines)
            o.check_time_units(lines)
            o.trailing_spaces(lines)
            #o.find_tabs(lines)
            #o.find_reports(lines)

        if cfg.tab2space:
            o.tab2space(my_file)

        if cfg.tab2space:
            o.rm_eol_spaces(my_file)
