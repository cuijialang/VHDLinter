import os
import platform
import shutil
import pyfiglet
from termcolor import colored
import config as cfg

class VHDLint:

    def __init__(self):

        self.dir = cfg.DIRECTORY
        self.content = ""
        self.lines = []

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
            i += 1

    def get_content(self, f_name):

        f = open(self.dir+f_name, "r")
        if f.mode == "r":
            self.content = f.read()
        f.close()

    def get_lines(self, f_name):

        line_no = 0
        f = open(self.dir+f_name, "r")
        if f.mode == "r":
            self.lines = []
            f_lines = f.readlines()
            for line in f_lines:
                line_no += 1
                self.lines.append(line)
        f.close()

    def check_file_name(self, f_name):

        info = "Bad file or entity name (entity_name.vhd)"
        i = 1
        entity_keys = ["entity ", " is"]
        for line in self.lines:
            if all(k in line for k in entity_keys):
                if line.lower().find(f_name[:-4]) == -1:
                    print(str(i) + ", " + info + ": " + f_name)
            i += 1

    def check_line_length(self, max_line_length):

        info = "Line too long"
        i = 1
        for line in self.lines:
            line_length = len(line)
            if line_length > max_line_length:
                hint = " (" + str(line_length) + "/" + str(max_line_length) + ")"
                print(str(i) + ", " + info + hint + ": " + line.lstrip())
            i += 1

    def check_statements_per_line(self):

        info = "Each line must contain only one VHDL statement"
        i = 1
        for line in self.lines:

            # ignore comments
            comment_bgn = line.find("--")
            if comment_bgn != -1:
                l_code = line[:comment_bgn].strip()
            else:
                l_code = line.strip()

            chk = l_code.find(";", 0)

            if l_code.find(";", chk+1) > chk:
                print("yesss")
                print(str(i) + ", " + info + ": " + line.lstrip())
            i += 1

    def check_tabs(self):

        info = "TAB found"
        i = 1
        for line in self.lines:
            chk1 = line.lower().find("\t", 0)
            if chk1 != -1:
                print(str(i) + ", " + info + ": " + line.lstrip())
            i += 1

    def check_indenation(self):

        info = "TODO"

    def check_constant_names(self):

        info = "constant names must be upper case"
        i = 1
        constant_keys = ["constant ", ":", ";"]
        for line in self.lines:
            if all(k in line for k in constant_keys):
                bgn = line.find("constant") + len("constant")
                end = line.find(":")
                constant_name = line[bgn:end]

                upper_case = True
                for c in range(0, len(constant_name)):
                    if constant_name[c].isalpha() and constant_name[c].islower():
                        upper_case = False

                if not upper_case:
                    print(str(i) + ", " + info + ": constant" + constant_name)
            i += 1



    def check_lower_case(self):

        info = "Use lower case"
        i = 1

        # TODO: add constant_names list
        exceptions = [" N"," T", "N_", "T_"]

        for line in self.lines:

            excep_name = False
            for ex in exceptions:
                ex_chk = line.find(ex)
                if ex_chk != -1:
                    excep_name = True
                    break;

            # ignore comments
            comment_bgn = line.find("--")
            if comment_bgn != -1:
                l_code = line[:comment_bgn].strip()
            else:
                l_code = line.strip()

            lower_case = True
            for pos in range(0, len(l_code)):
                if l_code[pos].isalpha() and l_code[pos].isupper():
                    lower_case = False

            if not lower_case and not excep_name:
                print(str(i) + ", " + info + ": " + l_code)
            i += 1


    def check_signal_names(self):

        info = "Bad naming style for signal"
        i = 1
        for line in self.lines:
            name_bgn = line.lower().find("signal")
            chk_comment = line.find("--")
            if name_bgn != -1 and (name_bgn < chk_comment or chk_comment == -1):
                l_ss = line[name_bgn+len("signal"):].strip()
                signal_name = l_ss[:l_ss.find(" ")]
                if len(signal_name) > 24:
                    print(str(i) + ", " + info + ": " + signal_name)
            i += 1

    def check_var_names(self):

        info = "Bad naming style for variable"
        i = 1
        for line in self.lines:
            name_bgn = line.lower().find("variable")
            chk_comment = line.find("--")
            if name_bgn != -1 and (name_bgn < chk_comment or chk_comment == -1):
                l_ss = line[name_bgn+len("variable"):].strip()
                var_name = l_ss[:l_ss.find(" ")]
                if len(var_name) > 24:
                    print(str(i) + ", " + info + ": " + var_name)
            i += 1

    def check_pkg_name(self):

        info = "Bad naming style for package (_pkg)"
        i = 1
        pack_keys = ["package ", " is"]
        for line in self.lines:
            if all(k in line for k in pack_keys):
                if line.lower().find("_pkg ") == -1:
                    print(str(i) + ", " + info + ": " + line.lstrip())
            i += 1

    def check_arc_name(self):

        info = "Bad naming style for architecture (_arc)"
        i = 1
        arch_keys = ["architecture ", " of ", " is"]
        for line in self.lines:
            if all(k in line for k in arch_keys):
                if line.lower().find("_arc") == -1:
                    print(str(i) + ", " + info + ": " + line.lstrip())
            i += 1

    def check_port_order(self):
        info = "Wrong port order"
        i = 1
        entity=""
        entity_dec = False
        for line in self.lines:
            if line.lower().find("entity ") != -1 or entity_dec:
                entity += line
                entity_dec = True
                if line.lower().find("end ") != -1:
                    entity_dec = False
                    break;
            i += 1
        #TODO: Check port order
        print(entity)

    def check_time_units(self):

        info = "Add space before time unit!"
        i = 1
        for line in self.lines:
            for unit in ["ns", "ms", "ps"]:
                chk1 = line.lower().find(unit + ";", 0)
                chk2 = line.lower().find(unit + " ", 0)
                chk_correct = line.lower().find(" " + unit, 0)
                if (chk1 != -1 or chk2 != -1) and chk_correct == -1:
                    print(str(i) + ", " + info + ": " + line.lstrip())
            i += 1

    def trailing_spaces(self):

        info = "Trailing Spaces"
        i = 1
        for line in self.lines:
            line = line.lstrip()
            chk = line.find("  ", 0)
            chk_e1 = line.find(":", 0)
            chk_e2 = line.find("=>", 0)
            if chk != -1 and (chk_e1 == -1 and chk_e2 == -1):
                print(str(i) + ", " + info + ": " + line.lstrip())
            i += 1

    def check_comments(self):

        info = "Ugly comment"
        i = 1
        for line in self.lines:
            chk1 = line.lower().find("xxx", 0)
            if chk1 != -1:
                print(str(i) + ", " + info + ": " + line.lstrip())
            chk2 = line.lower().find("todo", 0)
            chk3 = line.lower().find("to do", 0)
            if chk2 != -1 or chk3 != -1:
                print(str(i) + ", " + info + ": " + line.lstrip())
            i += 1

    def find_reports(self):

        info = "Debugging code"
        i = 1
        for line in self.lines:
            chk1 = line.lower().find("report", 0)
            if chk1 != -1:
                print(str(i) + ", " + info + ": " + line.lstrip())
            i += 1

    def check_semicolons(self):

        info = "Space before semicolon"
        i = 1
        for line in self.lines:
            chk1 = line.lower().find(" ;", 0)
            if chk1 != -1:
                print(str(i) + ", " + info + ": " + line.lstrip())
            i += 1

    def tab2space(self):

        i = 0
        for line in self.lines:
            chk = line.find("\t")
            if chk != -1:
                space = cfg.SPACES_PER_TAB * " "
                self.lines[i] = line.replace("\t", space)
            i += 1

    def make_pretty_comment(self):

        i = 0
        for line in self.lines:
            chk = line.lstrip().find("--")
            if chk != -1 and chk != 0:

                # remove multiple spaces at commentbegin
                chk = line.find("--  ")
                while chk != -1:
                    line = line.replace("--  ", "-- ")
                    chk = line.find("--  ")

                # remove space before colon
                chk = line.find(" ;")
                while chk != -1:
                    line = line.replace(" ;", ";")
                    chk = line.find(" ;")

                # check correctness
                chk = line.find("; -- ")
                if chk == -1:

                    # add space between ; and --
                    chk = line.find(";--")
                    if chk != -1:
                        line = line.replace(";--", "; --")

                    # remove multiple spaces between ; and --
                    chk = line.find("  --")
                    while chk != -1:
                        line = line.replace("  --", " --")
                        chk = line.find("  --")

                    # add space between -- and comment
                    chk = line.find("-- ")
                    if chk == -1:
                        line = line.replace("--", "-- ")
                self.lines[i] = line
            i += 1


    def edit_file(self, f_name):

        content = ""
        for line in self.lines:
            content += line.rstrip()+"\n"

        f = open(self.dir + f_name, "w")
        f.write(content)
        f.close()


if __name__ == "__main__":

    BANNER = pyfiglet.figlet_format("VHDLint")
    print("\n" + BANNER)
    print("No config file found, using default configuration \n")

    LNTR = VHDLint()


    FILES, FILE_DIRS = LNTR.get_files()

    if cfg.BACKUP:
        LNTR.make_backup_copies(cfg.BAK_FOLDER, FILES, FILE_DIRS)

    for f_name in FILES:

        if platform.platform().find("Linux") == -1:
            os.system('color')
        print(colored("************ " + f_name, cfg.COLOR_FILENAME))

        LNTR.get_content(f_name)
        LNTR.get_lines(f_name)

        if cfg.FILE_NAME_CHECK:
            LNTR.check_file_name(f_name)

        if cfg.CODE_CHECK:

            LNTR.check_line_length(cfg.MAX_LINE_LENGTH)
            LNTR.check_statements_per_line()
            #LNTR.check_tabs()
            #LNTR.check_indenation()
            LNTR.check_constant_names()
            LNTR.check_lower_case()
            LNTR.check_signal_names()
            LNTR.check_var_names()
            LNTR.check_pkg_name()
            LNTR.check_arc_name()

            LNTR.check_port_order() #TODO
            LNTR.check_msb_to_lsb() #TODO

            LNTR.check_comments()
            LNTR.check_semicolons()
            LNTR.check_time_units()
            LNTR.trailing_spaces()
            #LNTR.find_reports()

        if cfg.FORMATTING:

            if cfg.TAB2SPACE:
                LNTR.tab2space()

            if cfg.PRETTY_COMMENTING:
                LNTR.make_pretty_comment()

            # edit file and delete whitespaces
            LNTR.edit_file(f_name)
