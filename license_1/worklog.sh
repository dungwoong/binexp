# -------------------------------------------------
# Compile the program
# -------------------------------------------------
gcc -o license_1 license_1.c

# -------------------------------------------------
# Basic GDB
# -------------------------------------------------
gdb license_1
set disassembly-flavor intel # use intel symbols when displaying assembly
disassemble main

# -------------------------------------------------
# Run and set breakpoints
# -------------------------------------------------
break *main
run AAA # run with args
info registers
si # step into
ni # step over
disassemble main
info registers

# eax is the first 32 bits of rax, you can check with print $eax
set $eax = 0
continue

# ASLR: address space layout randomization
# makes your addresses different everytime, to make exploits harder
# you can do setarch x86_64 -R gdb ./your_program

# quick exploit here with main+88 for address
break *main+88
set $eax=0
continue

# -------------------------------------------------
# Extract the license
# -------------------------------------------------
break *main+83 # strcmp
# strcmp compares rdi vs rsi apparently
# I guess maybe if we looked at the earlier instructions we could guess that but ok
x/s $rdi
x/s $rsi # string they're comparing to
# x - examine memory /s - format memory as a string
# so x/s ADDRESS, or in our case x/s $register

# alternative
print (char *)$rdi
print (char *)$rsi