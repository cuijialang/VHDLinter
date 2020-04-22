import config as cfg

class LinterUtil:

    def __init__(self, f_dir, f_name):

        self.f_name = f_name
        self.get_content(f_dir, f_name)
        self.get_lines(f_dir, f_name)

    def get_content(self, f_dir, f_name):

        f = open(f_dir + f_name, "r")
        if f.mode == "r":
            self.content = f.read()
        f.close()

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
