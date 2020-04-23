import os
import yaml
import shutil
from CodeCheck import *
from CodeFormating import *

class VHDLinter:

    def __init__(self):

        self.files = []
        self.file_dirs = []

    def get_files(self, f_dir, color):

        try:
            for f_name in os.listdir(f_dir):
                if f_name.endswith(".vhd"):
                    self.files.append(f_name)
                    self.file_dirs.append(f_dir+f_name)

            if len(self.files) == 0:
                if platform.platform().find("Linux") == -1:
                    os.system('color')
                print(colored("No VHDL files found!", color))
        except:
            print(colored("Directory " + f_dir + " not found!", color))
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

    def print_banner(self, f_dir, color):

        if platform.platform().find("Linux") == -1:
            os.system('color')
        print(colored("No config file found, using default configuration", color))
        print("Checking VHDL files in " + f_dir + "\n")


    def make_output_file(self, f_out_dir, f_out_name):

        try:
            os.mkdir(f_out_dir)
        except:
            pass
        file_content = "VHDLinter\n"
        file_content += "No config file found, using default configuration\n"
        f_out_path = f_out_dir + f_out_name
        f_cc = open(f_out_path, "w+")
        f_cc.write(file_content)
        f_cc.close()


if __name__ == "__main__":

    # Configurations
    with open("config.yml", "r") as stream:
        try:
            cfg = yaml.safe_load(stream)
            f_dir = cfg["directory"]
        except yaml.YAMLError as exc:
            print(exc)

    # Get Files
    VHDLinter = VHDLinter()
    VHDLinter.print_banner(f_dir, cfg["colors"]["warning"])
    Files = VHDLinter.get_files(f_dir, cfg["colors"]["warning"])


    if cfg["BACKUP"]:
        VHDLinter.make_backup_copies(cfg["bak_directory"])

    if cfg["print2file"]:
        VHDLinter.make_output_file(cfg["file_out_dir"], cfg["file_out_name"])

    # Looping through files
    for f_name in Files:

        CC = CodeCheck(f_dir, f_name)
        CF = CodeFormating(f_dir, f_name)

        if cfg["FORMATING"]:

            if cfg["rm_bad_whitespaces"]:
                CF.rm_bad_whitespaces()
            if cfg["tab2space"]:
                CF.tab2space(cfg["spaces_per_tab"])
            if cfg["pretty_comments"]:
                CF.make_pretty_comment()
            CF.edit_file()


        if cfg["CODE_CHECK"]:

            if cfg["file_name_check"]:
                CC.check_file_name()

            # General
            CC.check_statements_per_line()
            CC.check_line_length(cfg["max_line_length"])
            CC.check_tabs()
            #CC.check_indenation()
            CC.check_constant_names()
            CC.check_lower_case()

            # Signals, Variables and Constants
            CC.check_signal_names(cfg["max_signal_name_length"])
            CC.check_var_names(cfg["max_var_name_length"])
            CC.check_msb_to_lsb()

            # Entities
            CC.check_port_order()

            # Architectures
            CC.check_arc_name()

            # Packages
            CC.check_pkg_name()
            CC.check_user_def_types()

            # Others
            #CC.find_reports()
            CC.check_comments()
            CC.check_semicolons()
            CC.check_time_units()

            CC.check_spaces_in_ports()
            CC.trailing_whitespace()

            if cfg["print2console"]:
                CC.print2console(cfg['colors']['filename'])

            if cfg["print2file"]:
                CC.print2file(cfg["file_out_dir"], cfg["file_out_name"])
