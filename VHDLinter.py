from CodeCheck import *
from CodeFormating import *

class VHDLinter(LinterUtil):

    def __init__(self):

        super(VHDLinter, self).__init__()
        self.files = []
        self.file_dirs = []


    def load_linter(self, config_name):

        self.load_config(config_name)
        self.Files = self.get_files(self.f_dir, self.color_warning)

        if self.BACKUP:
            self.make_backup_copies(self.bak_dir)

        if self.print2file:
            self.make_output_file(self.f_out_dir, self.f_out_name)


    def lint_files(self):

        # Looping through files and lines
        for f_name in self.Files:

            lines = self.get_lines(self.f_dir, f_name)
            content = self.get_content(self.f_dir, f_name)

            CC = CodeCheck(self.f_dir, f_name)
            CF = CodeFormating(self.f_dir, f_name, lines, content)

            if self.FORMATING:
                if self.rm_bad_ws:
                    CF.rm_bad_whitespaces()
                if self.tab2space:
                    CF.tab2space(self.spaces_per_tab)
                if self.pretty_comments:
                    CF.make_pretty_comment()
                CF.edit_file()


            if self.CODE_CHECK:

                if self.f_name_check:
                    CC.check_file_name(lines)

                for x in range(len(lines)):
                    line = lines[x]
                    i = x+1

                    # General checks
                    CC.check_statements_per_line(line, i)
                    CC.check_line_length(line, i, self.max_line_length)
                    CC.check_tabs(line, i)
                    #CC.check_indentation(line, i)
                    CC.check_constant_names(line, i)
                    CC.check_lower_case(line, i)

                    # Signals, Variables and Constants
                    CC.check_signal_names(line, i, self.max_signal_name_length)
                    CC.check_var_names(line, i, self.max_var_name_length)
                    CC.check_msb_to_lsb(line, i)

                    # Architectures
                    CC.check_arc_name(line, i)

                    # Packages
                    CC.check_pkg_name(line, i)
                    CC.check_user_def_types(line, i)

                    # Others
                    #CC.find_reports(line, i)
                    CC.check_comments(line, i)
                    CC.check_semicolons(line, i)
                    CC.check_time_units(line, i)
                    CC.trailing_whitespace(line, i)

                # Entities
                CC.check_port_order(lines)
                CC.check_spaces_in_ports(lines)

                if self.print2console:
                    CC.print2console(self.color_fname)

                if self.print2file:
                    CC.print2file(self.f_out_dir, self.f_out_name)


if __name__ == "__main__":

    VHDLinter = VHDLinter()
    VHDLinter.load_linter("config.yml")
    VHDLinter.lint_files()
