from LinterUtil import *

class CodeFormatting(LinterUtil):

    def __init__(self, f_name):

        self.f_name = f_name

        f_dir = cfg.DIRECTORY
        LinterUtil.__init__(self, f_dir, f_name)


    def tab2space(self, spaces_per_tab):

        i = 0
        for line in self.lines:
            chk = line.find("\t")
            if chk != -1:
                space = spaces_per_tab * " "
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

    def rm_bad_whitespaces(self):

        i = 0
        for line in self.lines:
            # Colon without space
            chk1 = line.lstrip().find(":")
            chk2 = line.lstrip().find(": ")
            if chk1 != -1 and chk2 == -1:
                line = line.replace(":", ": ")
            self.lines[i] = line
            i += 1

    def edit_file(self, f_dir, f_name):

        content = ""
        for line in self.lines:
            content += line.rstrip()+"\n"

        f_out_path = f_dir + f_name
        f_cf = open(f_out_path, "w")
        f_cf.write(content)
        f_cf.close()
