import os
import sys
import shutil
import yaml
from termcolor import colored

class LinterUtil:

    def __init__(self, os):

        self.content = ""
        self.files = []
        self.file_dirs = []
        self.lines = []
        self.os = os

        # default config
        self.f_dir = "../"
        self.code_check = True
        self.f_name_check = True
        self.max_line_length = 80
        self.max_signal_name_length = 24
        self.max_var_name_length = 24
        self.formating = False
        self.rm_bad_ws = True
        self.tab2space = False
        self.spaces_per_tab = 2
        self.pretty_comments = True
        self.backup = False
        self.bak_dir = "./bak"
        self.print2console = True
        self.print2file = False
        self.f_out_dir = "./.VHDLinter"
        self.f_out_name = "CodeCheck_Info"
        self.color_warning = "red"
        self.color_fname = "white"


    def get_files(self, f_dir, color):

        try:
            for f_name in os.listdir(f_dir):
                if f_name.endswith(".vhd"):
                    self.files.append(f_name)
                    self.file_dirs.append(f_dir+f_name)
            if len(self.files) == 0:
                if self.os == "win":
                    os.system('color')
                print(colored("No VHDL files found in " + f_dir, color))
                sys.exit(1)
            else:
                print("Loading VHDL files in " + f_dir + "\n")
        except FileNotFoundError:
            print(colored("Directory " + f_dir + " not found!", color))
            sys.exit(1)

        return self.files

    def make_backup_copies(self, bak_dir):

        try:
            os.mkdir(bak_dir)
        except:
            pass

        i = 0
        for original in self.file_dirs:
            target = bak_dir + self.files[i]
            shutil.copyfile(original, target)
            i += 1

    @staticmethod
    def make_output_file(f_out_dir, f_out_name):

        try:
            os.mkdir(f_out_dir)
        except:
            pass
        file_content = "VHDLinter\n"
        f_out_path = f_out_dir + f_out_name
        f_cc = open(f_out_path, "w+")
        f_cc.write(file_content)
        f_cc.close()


    def get_content(self, f_dir, f_name):

        f = open(f_dir + f_name, "r")
        if f.mode == "r":
            self.content = f.read()
        f.close()
        return self.content


    def get_lines(self, f_dir, f_name):

        line_no = 0
        f = open(f_dir + f_name, "r")
        if f.mode == "r":
            self.lines = []
            f_lines = f.readlines()
            for line in f_lines:
                line_no += 1
                self.lines.append(line)
        f.close()
        return self.lines


    def load_config(self, config_name):

        try:
            with open(config_name, "r") as stream:

                cfg = yaml.safe_load(stream)
                print("Loading " + config_name)

                self.f_dir = cfg["directory"]

                # Code checks
                self.code_check = cfg["CODE_CHECK"]
                self.f_name_check = cfg["file_name_check"]
                self.max_line_length = cfg["max_line_length"]
                self.max_signal_name_length = cfg["max_signal_name_length"]
                self.max_var_name_length = cfg["max_var_name_length"]
                # Code formating
                self.formating = cfg["FORMATING"]
                self.rm_bad_ws = cfg["rm_bad_whitespaces"]
                self.tab2space = cfg["tab2space"]
                self.spaces_per_tab = cfg["spaces_per_tab"]
                self.pretty_comments = cfg["pretty_comments"]
                # Code backups
                self.backup = cfg["BACKUP"]
                self.bak_dir = cfg["bak_directory"]
                # Linter output
                self.print2console = cfg["print2console"]
                self.print2file = cfg["print2file"]
                self.f_out_dir = cfg["file_out_dir"]
                self.f_out_name = cfg["file_out_name"]
                self.color_warning = cfg["colors"]["warning"]
                self.color_fname = cfg['colors']['filename']

        except FileNotFoundError:
            print(colored("No config file found, using default configuration", "white"))
