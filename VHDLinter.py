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

    def print_banner(self, f_dir):
        print("Checking VHDL files in " + f_dir + "\n")


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


if __name__ == "__main__":

    # Check OS
    if platform.platform().find("Linux") == -1:
        os.system('color')

    # Configurations
    VHDLinter_config = "config.yml"
    try:
        with open(VHDLinter_config, "r") as stream:
            cfg = yaml.safe_load(stream)

            print("Using config " + VHDLinter_config +"\n")

            f_dir = cfg["directory"]

            CODE_CHECK = cfg["CODE_CHECK"]
            f_name_check = cfg["file_name_check"]
            max_line_length = cfg["max_line_length"]
            max_signal_name_length = cfg["max_signal_name_length"]
            max_var_name_length = cfg["max_var_name_length"]

            FORMATING = cfg["FORMATING"]
            rm_bad_ws = cfg["rm_bad_whitespaces"]
            tab2space = cfg["tab2space"]
            spaces_per_tab = cfg["spaces_per_tab"]
            pretty_comments = cfg["pretty_comments"]

            BACKUP = cfg["BACKUP"]
            bak_dir = cfg["bak_directory"]

            print2console = cfg["print2console"]
            print2file = cfg["print2file"]
            f_out_dir = cfg["file_out_dir"]
            f_out_name = cfg["file_out_name"]

            color_warning = cfg["colors"]["warning"]
            color_fname = cfg['colors']['filename']
    except:
        print(colored("No config file found, using default configuration", "yellow"))

        f_dir = "../"

        CODE_CHECK = True
        f_name_check = True
        max_line_length = 80
        max_signal_name_length = 24
        max_var_name_length = 24

        FORMATING = False
        rm_bad_ws = True
        tab2space = False
        spaces_per_tab = 2
        pretty_comments = True

        BACKUP = False
        bak_dir = "./bak"

        print2console = True
        print2file = False
        f_out_dir = "./.VHDLinter"
        f_out_name = "CodeCheck_Info"

        color_warning = "yellow"
        color_fname = "white"

    # Get Files
    VHDLinter = VHDLinter()
    VHDLinter.print_banner(f_dir)
    Files = VHDLinter.get_files(f_dir, color_warning)


    if BACKUP:
        VHDLinter.make_backup_copies(bak_dir)

    if print2file:
        VHDLinter.make_output_file(f_out_dir, f_out_name)

    # Looping through files and lines #TODO
    for f_name in Files:

        CC = CodeCheck(f_dir, f_name)
        CF = CodeFormating(f_dir, f_name)

        if FORMATING:
            if rm_bad_ws:
                CF.rm_bad_whitespaces()
            if tab2space:
                CF.tab2space(spaces_per_tab)
            if pretty_comments:
                CF.make_pretty_comment()
            CF.edit_file()


        if CODE_CHECK:
            if f_name_check:
                CC.check_file_name()

            # General
            CC.check_statements_per_line()
            CC.check_line_length(max_line_length)
            CC.check_tabs()
            #CC.check_indenation()
            CC.check_constant_names()
            CC.check_lower_case()

            # Signals, Variables and Constants
            CC.check_signal_names(max_signal_name_length)
            CC.check_var_names(max_var_name_length)
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

            if print2console:
                CC.print2console(color_fname)

            if print2file:
                CC.print2file(f_out_dir, f_out_name)
