from termcolor import colored
from LinterUtil import *

class CodeCheck():

    def __init__(self, f_dir, f_name):

        self.f_dir = f_dir
        self.f_name = f_name
        self.linter_out = ""
        self.constants = []


    def check_file_name(self, lines):

        info = "Bad file or entity name (entity_name.vhd)"
        entity_keys = ["entity ", " is"]

        for x in range(len(lines)):
            line = lines[x]
            i = x+1

            if all(k in line for k in entity_keys):
                if line.lower().find(self.f_name[:-4]) == -1:
                    self.linter_out += str(i) + ", " + info + ": " + self.f_name +"\n"

    def check_line_length(self, line, i, max_line_length):
        info = "Line too long"
        line_length = len(line)
        if line_length > max_line_length:
            hint = " (" + str(line_length) + "/" + str(max_line_length) + ")"
            self.linter_out += str(i) + ", " + info + hint + ": " + line.strip() + "\n"

    def rm_comment(self, line):

        # ignore comments
        comment_bgn = line.find("--")
        if comment_bgn != -1:
            line = line[:comment_bgn].strip()
        return line.strip()

    def check_statements_per_line(self, line, i):
        info = "Lines must not contain multiple statements"
        # ignore comments
        line_ic = self.rm_comment(line)

        chk = line_ic.find(";", 0)

        if line_ic.find(";", chk+1) > chk:
            self.linter_out += str(i) + ", " + info + ": " + line_ic + "\n"

    def check_tabs(self, line, i):

        info = "TAB found"
        chk = line.lower().find("\t", 0)
        if chk != -1:
            self.linter_out += str(i) + ", " + info + ": " + line.strip() + "\n"

    def check_indentation(self, line, i):
        print("Indentation check is not supported yet")
        info = "Bad indentation"

    def check_constant_names(self, line, i):

        info = "Constant name should be upper case"
        self.constants = []
        constant_keys = ["constant ", ":", ";"]
        if all(k in line for k in constant_keys):
            bgn = line.find("constant") + len("constant")
            end = line.find(":")
            constant_name = line[bgn:end]
            self.constants.append(constant_name.strip())

            upper_case = True
            for c in range(0, len(constant_name)):
                if constant_name[c].isalpha() and constant_name[c].islower():
                    upper_case = False

            if not upper_case:
                self.linter_out += str(i) + ", " + info + ": " + constant_name + "\n"


    def check_lower_case(self, line, i):

        info = "Upper case only in constant names and comments"

        exceptions = [" N", " T", "N_", "T_"]
        exceptions.extend(self.constants)

        excep_name = False
        for ex in exceptions:
            ex_chk = line.find(ex)
            if ex_chk != -1:
                excep_name = True
                break

        # ignore comments
        line_ic = self.rm_comment(line)

        lower_case = True
        for pos in range(0, len(line_ic)):
            if line_ic[pos].isalpha() and line_ic[pos].isupper():
                lower_case = False

        if not lower_case and not excep_name:
            self.linter_out += str(i) + ", " + info + ": " + line_ic + "\n"


    def check_signal_names(self, line, i, max_name_length):

        info = "Signal name too long"
        name_bgn = line.lower().find("signal")
        chk_comment = line.find("--")
        if name_bgn != -1 and (name_bgn < chk_comment or chk_comment == -1):
            l_ss = line[name_bgn+len("signal"):].strip()
            signal_name = l_ss[:l_ss.find(" ")-1]
            if len(signal_name) > max_name_length:
                hint = " ("+str(len(signal_name)) + "/" + str(max_name_length)+")"
                self.linter_out += str(i) + ", " + info + hint + ": " + signal_name + "\n"

    def check_var_names(self, line, i, max_name_length):

        info = "Variable name too long"
        name_bgn = line.lower().find("variable")
        chk_comment = line.find("--")
        if name_bgn != -1 and (name_bgn < chk_comment or chk_comment == -1):
            l_ss = line[name_bgn+len("variable"):].strip()
            var_name = l_ss[:l_ss.find(" ")]
            if len(var_name) > max_name_length:
                hint = " ("+str(len(var_name)) + "/" + str(max_name_length)+")"
                self.linter_out += str(i) + ", " + info + hint +": " + var_name + "\n"

    def check_pkg_name(self, line, i):

        info = "Bad naming style for package (_pkg)"
        pack_keys = ["package ", " is"]
        if all(k in line for k in pack_keys):
            if line.lower().find("_pkg ") == -1:
                self.linter_out += str(i) + ", " + info + ": " + line.strip() + "\n"

    def check_arc_name(self, line, i):

        info = "Bad naming style for architecture (_arc)"

        arch_keys = ["architecture ", " of ", " is"]
        if all(k in line for k in arch_keys):
            if line.lower().find("_arc ") == -1:
                self.linter_out += str(i) + ", " + info + ": " + line.strip() + "\n"

    def check_port_order(self, lines):
        info = "Wrong port order"
        i = 1
        entity_dec_keys = ["entity ", " is"]
        entity_lines = []
        entity_found = False

        for line in lines:

            if all(k in line for k in entity_dec_keys):
                entity_found = True
                j = i

            if entity_found:
                entity_lines.append(line.strip())
                if line.lower().find("end") != -1:
                    break
            i += 1

        in_pos = False
        out_pos = False

        for line in entity_lines:

            in_chk = line.find("in ")
            if in_chk != -1:
                in_pos = True

            out_chk = line.find("out ")
            if out_chk != -1:
                out_pos = True

            if out_pos and in_chk != -1:
                self.linter_out += str(j) + ", " + info + ": " + line + "\n"
            j += 1

    def check_spaces_in_ports(self, lines):

        info = "Add space before"
        i = 1
        entity_dec_keys = ["entity ", " is"]
        entity_lines = []
        entity_found = False

        for line in lines:

            if all(k in line for k in entity_dec_keys):
                entity_found = True
                j = i

            if entity_found:
                entity_lines.append(line.strip())
                if line.lower().find("end") != -1:
                    break
            i += 1

        for line in entity_lines:

            if line.find("in ") != -1 and line.find(": in") == -1:
                self.linter_out += str(j) + ", " + info + " in port : " + line + "\n"

            if line.find("out ") != -1 and line.find(": out") == -1:
                self.linter_out += str(j) + ", " + info + " out port : " + line + "\n"

            if line.find("inout ") != -1 and line.find(": inout") == -1:
                self.linter_out += str(j) + ", " + info + " inout port : " + line  + "\n"
            j += 1

    def check_msb_to_lsb(self, line, i):

        info = "Vector range should be MSB to LSB"
        if line.lower().find("std_logic_vector") != -1:

            chk_to = line.lower().find(" to ")
            chk_downto = line.lower().find(" downto ")

            if chk_downto == -1 and chk_to != -1:
                self.linter_out += str(i) + ", " + info + ": " + line.strip() + "\n"

    def check_user_def_types(self, line, i):

        info = "Self-defined type not in library file"
        type_keys = ["type ", " is"]
        if all(k in line for k in type_keys):
            if self.f_name.find("_pkg") == -1 and line.lower().find("fsm") == -1:
                self.linter_out += str(i) + ", " + info + ": " + line.strip() + "\n"

    def check_time_units(self, line, i):

        info = "Add space before time unit"
        time_keys = ["ns;", "ms;", "ps"]
        for key in time_keys:
            chk = line.lower().find(key, 0)
            if chk != -1 and line[chk-1].isnumeric() and not line[chk+len(key)-1].isalpha():
                self.linter_out += str(i) + ", " + info + ": " + line.strip() + "\n"

    def trailing_whitespace(self, line, i):

        info = "Trailing whitespace"
        line = line.lstrip()
        chk = line.find("  ", 0)
        chk_e1 = line.find(":", 0)
        chk_e2 = line.find("=>", 0)
        if chk != -1 and (chk_e1 == -1 and chk_e2 == -1):
            self.linter_out += str(i) + ", " + info + ": " + line.strip() + "\n"

    def check_comments(self, line, i):

        info = "Ugly comment"
        key = ["xxx", "to do", "todo", "delete", "check", "?"]
        chk = line.find("--")
        if chk != -1:
            comment = line[chk:].strip()
            if any(k in comment.lower() for k in key):
                self.linter_out += str(i) + ", " + info + ": "+ comment + "\n"

    def find_reports(self, line, i):

        info = "Debugging code"
        chk = line.lower().find("report", 0)
        if chk != -1:
            self.linter_out += str(i) + ", " + info + ": " + line.strip() + "\n"

    def check_semicolons(self, line, i):

        info = "Remove space before semicolon"
        chk = line.lower().find(" ;", 0)
        if chk != -1:
            self.linter_out += str(i) + ", " + info + ": " + line.strip() + "\n"

    def print2console(self, color):

        if platform.platform().find("Linux") == -1:
            os.system('color')
        print(colored("*************** " + self.f_name, color))
        print(self.linter_out)

    def print2file(self, f_out_dir, f_out_name):

        file_content = "\n*************** " + self.f_name + "\n" + self.linter_out
        f_out_path = f_out_dir + f_out_name
        f_cc = open(f_out_path, "a")
        f_cc.write(file_content)
        f_cc.close()
