import random
import os

RANDOM_BYTE_NUMBER = None
RANDOM_BYTE = None

os.system("cp license_1 license_1_fuzz") # ensure execute permission on the file

# don't touch ELF header(not sure what that is)
def flip_byte(in_bytes, safe_offset=0x100):
    """Copy bytes but change 1 byte"""
    global RANDOM_BYTE_NUMBER, RANDOM_BYTE
    i = random.randint(safe_offset, len(in_bytes) - 1)
    c = bytes([random.randint(0, 0xFF)])
    RANDOM_BYTE_NUMBER = i
    RANDOM_BYTE = c
    return in_bytes[:i] + c + in_bytes[i+1:]

def copy_binary(name_orig="license_1", name_new="license_1_fuzz"):
    with open(name_orig, "rb") as orig_f, open(name_new, "wb") as new_f:
        new_f.write(flip_byte(orig_f.read()))

def compare(fn1, fn2):
    try:
        with open(fn1) as f1, open(fn2) as f2:
            # f1_text = f1.read()
            # f2_text = f2.read()
            # print(f"{f1_text}\n\n{f2_text}")
            # print(f"Equal={f1_text == f2_text}")
            return f1.read() == f2.read()
    except UnicodeDecodeError:
        return False

def check_output():
    os.system("{ ./license_1_fuzz; ./license_1 ABC; ./license_1_fuzz AAAA-Z10N-42-OK; } > workdir/fuzz_output")
    return compare("workdir/orig_output", "workdir/fuzz_output")

def check_gdb():
    os.system("echo disassemble main | gdb ./license_1_fuzz > workdir/fuzz_gdb")
    with open("workdir/fuzz_gdb") as f:
        if "Dump of assembler code" in f.read():
            return True
    return compare("workdir/orig_gdb", "workdir/fuzz_gdb")

def run():
    copy_binary()
    if check_output():
        print("FOUND EQUIV OUTPUT")
        # input()
        if not check_gdb():
            print(f"FOUND POSSIBLE FAIL {RANDOM_BYTE_NUMBER=} {RANDOM_BYTE=}")
            os.system("cat workdir/fuzz_gdb")
            input()
    else:
        # print("Pass :(")
        pass

if __name__ == "__main__":
    # FOUND POSSIBLE FAIL RANDOM_BYTE_NUMBER=15961 RANDOM_BYTE=b'\xd9'
    for i in range(100):
        run()