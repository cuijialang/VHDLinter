# VHDLint

## Table of contents
* [General info](#general-info)
* [How to Use](#setup)
* [Features](#features)
* [Preview](#preview)
* [To Do](#to-do)
* [Source](#source)

## General info
*VHDLint* is a small linter for the VHDL language, which looks for programming errors and helps enforcing a coding standard.

## How to Use
To launch the app, open the *VHDLint.py* script via the console.
If the repository *VHDLint* folder is not in the same directory like your VHDL files, edit the configuration settings in *config.py* first.

## Features
*VHDLint* supports code check and formatting options for VHDL Design Files (.vhd).
Checks and/or formatting options for the following naming and coding conventions are supported:

#### General
- [x] Source code must not exceed 80 characters per line
- [ ] Each line must contain only one VHDL statement
- [x] No TAB characters should be used for indentation
- [ ] Each line must be properly indented with 2 spaces per level of indentation
- [x] Source code has to be written in lower case, except for constant declarations

#### Signals, Variables and Constants
- [x] Signal and variable names should be short, not exceeding 24 characters
- [ ] If the signal is a vector, the range is defined as *msb downto lsb*
- [ ] Constants should be written in upper-case

#### Entities
- [ ] The functionality of an entity should be commented
- [ ] Ports shoud be ordered by their function
- [ ] Ports can only be one of the following types: *in*, *out* or *inout*
- [ ] If generics are preset, their function should be commented

#### Architectures
- [ ] The arcitecture name is derived from the entity name by suffixing it with *_arc*
- [ ] Port maps and generic maps should use named association
- [ ] Maps should contain only one port or generic per line

#### Packages
- [x] Package should be indicated by suffixing *_pkg* to their name
- [ ] All defined types that are in the package should be commented
- [ ] Self-defined types (except for state-machine states) should be defined in a library


## Preview
<img src="images/preview.png" width="500">

## To Do
Some ideas to improve the functionality:
* Support more features!
* Add configuration settings
* Support multiple directories
* Ignore lines with ignore comment
* Implement code rating ?
* GUI ?

## Source
The functionality is based on the idea of having something like *Pylint* for VHDL code; *VHDLint*.
All suported checks for the listed coding conventions in VHDL are based on [**VHDL Style Guide**](https://www.ims-chips.de/content/pdftext/VHDL_Style_Guide.pdf) by IMS CHIPS.
