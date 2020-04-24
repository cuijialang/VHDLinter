import os
import platform
import yaml
import shutil
from termcolor import colored

class LinterUtil:

    def __init__(self):

        self.content = ""
        self.lines = []


    def get_files(self, f_dir, color):

        try:
            for f_name in os.listdir(f_dir):
                if f_name.endswith(".vhd"):
                    self.files.append(f_name)
                    self.file_dirs.append(f_dir+f_name)
        except:
            print(colored("Directory " + f_dir + " not found!", color))

        if len(self.files) == 0:
            if platform.platform().find("Linux") == -1:
                os.system('color')
            print(colored("No VHDL files found in " + f_dir , color))
        else:
            print("Loading VHDL files in " + f_dir + "\n")
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


    def make_output_file(self, f_out_dir, f_out_name):

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

                self.CODE_CHECK = cfg["CODE_CHECK"]
                self.f_name_check = cfg["file_name_check"]
                self.max_line_length = cfg["max_line_length"]
                self.max_signal_name_length = cfg["max_signal_name_length"]
                self.max_var_name_length = cfg["max_var_name_length"]

                self.FORMATING = cfg["FORMATING"]
                self.rm_bad_ws = cfg["rm_bad_whitespaces"]
                self.tab2space = cfg["tab2space"]
                self.spaces_per_tab = cfg["spaces_per_tab"]
                self.pretty_comments = cfg["pretty_comments"]

                self.BACKUP = cfg["BACKUP"]
                self.bak_dir = cfg["bak_directory"]

                self.print2console = cfg["print2console"]
                self.print2file = cfg["print2file"]
                self.f_out_dir = cfg["file_out_dir"]
                self.f_out_name = cfg["file_out_name"]

                self.color_warning = cfg["colors"]["warning"]
                self.color_fname = cfg['colors']['filename']
        except:

            print(colored("No config file found, using default configuration", "white"))

            self.f_dir = "../"

            self.CODE_CHECK = True
            self.f_name_check = True
            self.max_line_length = 80
            self.max_signal_name_length = 24
            self.max_var_name_length = 24

            self.FORMATING = False
            self.rm_bad_ws = True
            self.tab2space = False
            self.spaces_per_tab = 2
            self.pretty_comments = True

            self.BACKUP = False
            self.bak_dir = "./bak"

            self.print2console = True
            self.print2file = False
            self.f_out_dir = "./.VHDLinter"
            self.f_out_name = "CodeCheck_Info"

            self.color_warning = "red"
            self.color_fname = "white"
