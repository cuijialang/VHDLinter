import os
import platform
import shutil
import pyfiglet
from termcolor import colored
import config as cfg

class VHDLint:

    def __init__(self):

        self.dir = cfg.DIRECTORY
        self.max_line_length = cfg.MAX_LINE_LENGTH
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

    def get_lines(self, my_file):
        self.lines = []
        line_no = 0
        f = open(self.dir+my_file, "r")
        if f.mode == "r":
            f_lines = f.readlines()
            for line in f_lines:
                line_no += 1
                self.lines.append(line)
            f.close()

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

    def check_semicolons(self):

        info = "Space before semicolon"
        i = 1
        for line in self.lines:
            chk1 = line.lower().find(" ;", 0)
            if chk1 != -1:
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

    def find_tabs(self):

        info = "TabError"
        i = 1
        for line in self.lines:
            chk1 = line.lower().find("\t", 0)
            if chk1 != -1:
                print(str(i) + ", " + info + ": " + line.lstrip())
            i += 1

    def check_linelength(self):

        info = "Line too long"
        i = 1
        for line in self.lines:
            line_length = len(line)
            if line_length > self.max_line_length:
                hint = " (" + str(line_length) + "/" + str(self.max_line_length) + ")"
                print(str(i) + ", " + info + hint + ": " + line.lstrip())
            i += 1

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


    def edit_file(self, my_file):

        content = ""
        for line in self.lines:
            content += line.rstrip()+"\n"

        f = open(self.dir + my_file, "w")
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

    for my_file in FILES:

        if platform.platform().find("Linux") == -1:
            os.system('color')
        print(colored("************ " + my_file, cfg.COLOR_FILENAME))

        LNTR.get_lines(my_file)

        if cfg.CODE_CHECK:

            LNTR.check_comments()
            LNTR.check_semicolons()
            LNTR.check_linelength()
            LNTR.check_time_units()
            LNTR.trailing_spaces()
            #LNTR.find_tabs()
            #LNTR.find_reports()

        if cfg.FORMATTING:

            if cfg.TAB2SPACE:
                LNTR.tab2space()

            if cfg.PRETTY_COMMENTING:
                LNTR.make_pretty_comment()

            # edit file and delete whitespaces
            LNTR.edit_file(my_file)
