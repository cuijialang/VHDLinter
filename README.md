# VHDLinter

## Table of contents
* [General info](#general-info)
* [How to Use](#setup)
* [Features](#features)
    * [Code checking](#checking)
    * [Formatting](#formatting)
* [Preview](#preview)
* [Source](#source)
* [License](#license)

## General info
VHDLinter is a smart linter for the VHDL language, which looks for programming errors and helps enforcing a coding standard.

## How to Use
To launch the app, save the repository folder unter the same directory like your VHDL design files and open the *VHDLinter.py* script via the console.

## Features
VHDLinter supports code check and formatting options for VHDL Design Files (.vhd).<br />

#### Code check
Verification of the following naming and coding conventions is supported:
##### General
- [x] VHDL file names are derived by their entity name
- [x] Each line must contain only one VHDL statement
- [x] Source code must not exceed 80 characters per line
- [x] No tab characters should be used for indentation
- [ ] Lines must be properly indented with 2 spaces per level of indentation
- [x] Source code should be lower case, except for constant declarations

##### Signals, Variables and Constants
- [x] Signal and variable names must not exceed 24 characters
- [x] Vector range should be *MSB downto LSB*
- [x] Constant names should be upper-case

##### Entities
- [x] Ports shoud be ordered by their type (in, out)
- [ ] Functionality of entities should be commented
- [ ] Functionality of generics should be commented

##### Architectures
- [x] Arcitecture names are derived by their entity name and *_arc*-suffix
- [ ] Port maps and generic maps should use named association
- [ ] Maps should contain only one port or generic per line

##### Packages
- [x] Package should be indicated by suffixing *_pkg* to their name
- [X] Self-defined types (except for FSM types) should be in libraries
- [ ] Self-defined types should be commented

#### Formatting
Automatic correction of the following flaws is possible:
- [x] Removal of trailing whitespace
- [x] Removal of bad whitespaces
- [x] Replacing tabs (Tab2Space)
- [ ] Deletion of unused signals or variables

## Preview
<img src="images/preview.png" width="500">

## Source
The supported checks and formatting options are based on [**VHDL coding style**](http://www.tkt.cs.tut.fi/kurssit/1212/S08/Harjoitukset/vhdl_coding.html) by Tampere University of Technology and [**VHDL Style Guide**](https://www.ims-chips.de/content/pdftext/VHDL_Style_Guide.pdf) by IMS CHIPS.

## License
Licensed under the [GNU GPLv3 License](LICENSE).
