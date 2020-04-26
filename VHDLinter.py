import platform
from LinterUtil import LinterUtil
from CodeCheck import CodeCheck
from CodeFormating import CodeFormating

class VHDLinter(LinterUtil):

    def __init__(self):

        self.files = []
        self.file_dirs = []
        self.check_platform()
        super(VHDLinter, self).__init__(self.os)


    def check_platform(self):

        if platform.platform().find("Linux") != -1:
            self.os = "linux"
        else:
            self.os = "win"


    def load_linter(self, config_name):

        self.load_config(config_name)
        self.files = self.get_files(self.f_dir, self.color_warning)

        if self.backup:
            self.make_backup_copies(self.bak_dir)

        if self.print2file:
            self.make_output_file(self.f_out_dir, self.f_out_name)


    def lint_files(self):

        # Looping through files and lines
        for f_name in self.files:

            lines = self.get_lines(self.f_dir, f_name)
            content = self.get_content(self.f_dir, f_name)

            cc = CodeCheck(self.f_dir, f_name)
            cf = CodeFormating(self.f_dir, f_name, lines, content)

            if self.formating:
                if self.rm_bad_ws:
                    cf.rm_bad_whitespaces()
                if self.tab2space:
                    cf.tab2space(self.spaces_per_tab)
                if self.pretty_comments:
                    cf.make_pretty_comment()
                cf.edit_file()


            if self.code_check:

                if self.f_name_check:
                    cc.check_file_name(lines)

                for j, line in enumerate(lines):
                    i = j+1

                    # General checks
                    cc.check_statements_per_line(line, i)
                    cc.check_line_length(line, i, self.max_line_length)
                    cc.check_tabs(line, i)
                    cc.check_constant_names(line, i)
                    cc.check_lower_case(line, i)

                    # Signals, Variables and Constants
                    cc.check_signal_names(line, i, self.max_signal_name_length)
                    cc.check_var_names(line, i, self.max_var_name_length)
                    cc.check_msb_to_lsb(line, i)

                    # Architectures
                    cc.check_arc_name(line, i)

                    # Packages
                    cc.check_pkg_name(line, i)
                    cc.check_user_def_types(line, i)

                    # Others
                    #cc.find_reports(line, i)
                    cc.check_comments(line, i)
                    cc.check_semicolons(line, i)
                    cc.check_time_units(line, i)
                    cc.trailing_whitespace(line, i)

                # Entities
                cc.check_port_order(lines)
                cc.check_spaces_in_ports(lines)

                if self.print2console:
                    cc.print2console(self.os, self.color_fname)

                if self.print2file:
                    cc.print2file(self.f_out_dir, self.f_out_name)


if __name__ == "__main__":

    LINTER = VHDLinter()
    LINTER.load_linter("config.yml")
    LINTER.lint_files()
