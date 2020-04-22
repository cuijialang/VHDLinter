# VHDLinter Config

#DIRECTORY = "../"
DIRECTORY = "../monitoring/"

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
FILE_OUT_NAME = "VHDLint_out.txt"
FILE_OUT_DIR = "./"

COLORS = ["yellow", "cyan", "magenta", "blue", "green"]
COLOR_FILENAME = COLORS[1]

# Caution: File modifications can't be undone!
FORMATTING = True
RM_BAD_WHITESPACES = True
TAB2SPACE = True
PRETTY_COMMENTS = True
