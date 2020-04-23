# VHDLinter Config

#DIRECTORY = "../"
DIRECTORY = "../my_VHDL_project/"

MAX_LINE_LENGTH = 80
MAX_SIGNAL_NAME_LENGTH = 24
MAX_VARIABLE_NAME_LENGTH = 24
SPACES_PER_TAB = 4

# Filename check
FILE_NAME_CHECK = True

# Print to console
CODE_CHECK = True

BACKUP = True
BAK_DIRECTORY = "./.bak/"

# PERSONAL SETTINGS
PRINT = True
PRINT2CONSOLE = True

PRINT2FILE = True
FILE_OUT_NAME = "VHDLinter_out.txt"
FILE_OUT_DIR = "./testing/"

COLORS = ["yellow", "cyan", "magenta", "blue", "green", "white"]
COLOR_FILENAME = COLORS[0]
COLOR_WARNING = COLORS[0]

# Caution: File modifications can't be undone!
FORMATING = False
RM_BAD_WHITESPACES = False
TAB2SPACE = False
PRETTY_COMMENTS = False
