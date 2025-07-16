#!/bin/bash
mkdir -p workdir

{ 
    ./license_1
    ./license_1 ABC
    ./license_1 AAAA-Z10N-42-OK
} > workdir/orig_output

# This never works cuz GDB prints the filename and the two filenames will be different.
echo disassemble main | gdb ./license_1 > workdir/orig_gdb