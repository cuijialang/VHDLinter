import os
import shutil
import pyfiglet
import config as cfg
from CodeCheck import *
from CodeFormating import *

class VHDLinter:

    def __init__(self):

        self.dir = cfg.DIRECTORY
        self.bak_dir = cfg.BAK_DIRECTORY
        self.files = []
        self.file_dirs = []

    def get_files(self):

        for f_name in os.listdir(self.dir):
            if f_name.endswith(".vhd"):
                self.files.append(f_name)
                self.file_dirs.append(self.dir+f_name)
        return self.files

    def make_backup_copies(self):

        try:
            os.mkdir(self.bak_dir)
        except:
            pass

        i = 0
        for original in self.file_dirs:
            target = self.bak_dir + self.files[i]
            shutil.copyfile(original, target)
            i += 1

    def print_banner(self):

        #print("\n" + pyfiglet.figlet_format("VHDLinter"))
        print("No config file found, using default configuration\n")

    def make_output_file(self, f_out_dir, f_out_name):

        try:
            os.mkdir(f_out_dir)
        except:
            pass
        file_content = "VHDLinter\n"
        file_content += "No config file found, using default configuration\n"
        f_out_path = f_out_dir + f_out_name
        f_cc = open(f_out_path, "w")
        f_cc.write(file_content)
        f_cc.close()


if __name__ == "__main__":

    VHDLinter = VHDLinter()
    Files = VHDLinter.get_files()

    if cfg.BACKUP:
        VHDLinter.make_backup_copies()

    if cfg.PRINT and cfg.PRINT2CONSOLE:
        VHDLinter.print_banner()

    if cfg.PRINT and cfg.PRINT2FILE:
        # create or empty output file
        VHDLinter.make_output_file(cfg.FILE_OUT_DIR, cfg.FILE_OUT_NAME)

    for f_name in Files:

        CC = CodeCheck(f_name)
        CF = CodeFormating(f_name)

        if cfg.FORMATING:

            if cfg.RM_BAD_WHITESPACES:
                CF.rm_bad_whitespaces()
            if cfg.TAB2SPACE:
                CF.tab2space(cfg.SPACES_PER_TAB)
            if cfg.PRETTY_COMMENTS:
                CF.make_pretty_comment()

            # edit file and delete whitespaces
            CF.edit_file(cfg.DIRECTORY, f_name)

        if cfg.FILE_NAME_CHECK:
            CC.check_file_name()

        if cfg.CODE_CHECK:

            # General
            CC.check_statements_per_line()
            CC.check_line_length(cfg.MAX_LINE_LENGTH)
            CC.check_tabs()
            #CC.check_indenation()
            CC.check_constant_names()
            CC.check_lower_case()

            # Signals, Variables and Constants
            CC.check_signal_names(cfg.MAX_SIGNAL_NAME_LENGTH)
            CC.check_var_names(cfg.MAX_VARIABLE_NAME_LENGTH)
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

            if cfg.PRINT:
                if cfg.PRINT2CONSOLE:
                    CC.print2console(cfg.COLOR_FILENAME)

                if cfg.PRINT2FILE:
                    CC.print2file(cfg.FILE_OUT_DIR, cfg.FILE_OUT_NAME)
