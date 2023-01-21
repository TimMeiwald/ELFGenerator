from elfgenerator.ELF import x86_64
from elfgenerator.Binary import Binary
from elfgenerator.ELF_Segment_Utils import Segment
def test_ELF_x86_64_header():
    x = x86_64()
    header = x._generate_ELF_header()
    b = header.binary()
    from os import getcwd
    from os.path import join
    # with open(join(getcwd(), "tests", "testELF", "TestELFHEADER"), "wb") as fp:
    #     fp.write(b)
    assert len(header) == 64     
    assert header.__repr__() == "7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 02 00 3e 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 40 00 38 00 00 00 00 00 00 00 00 00"
    

def test_ELF_x86_64_prog():
    "mov rdi, 0x2a -> 48 c7 c7 2a 00 00 00"
    "mov rax, 0x3c -> 48 c7 c0 3c 00 00 00"
    "syscall -> 0f 05"
    prog = 0x48c7c03c00000048c7c72a0000000f05

    prog_bin = Binary(prog, 16, 16, endianness="big") # Big since code was already in correct order. Don't need to invert anything for LSB
    x = x86_64()
    x.set_entry_point(0x401000 + 64)
    x.add_segment(7, 16, 16, prog_bin)

    b = x.generate_executable().binary()
    print(f"Lenght is {len(b)}")
    from os import getcwd
    from os.path import join
    # with open(join(getcwd(), "tests", "testELF", "TestExecutable"), "wb") as fp: # Can be used to write it out as a binary file
    #     fp.write(b)
    assert b == b'\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00>\x00\x01\x00\x00\x00@\x10@\x00\x00\x00\x00\x00P\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x008\x00\x01\x00\x00\x00\x00\x00\x00\x00H\xc7\xc0<\x00\x00\x00H\xc7\xc7*\x00\x00\x00\x0f\x05\x01\x00\x00\x00\x07\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00@\x10@\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


def test_ELF_x86_64_prog2():
    """ mov rax, 1 ; 1 is write 
        mov rdi, 1
        mov rsi, 0x401000 ; Memory address of data segment, need to track positions for compiler
        mov rdx, 13
        syscall
        mov rax, 60 ; 60 is exit
        mov rdi, 0 ; Return value of 0
        syscall
        """
    prog = 0x48C7C00100000048C7C70100000048C7C66E10400048C7C20D0000000F0548C7C03C00000048C7C7000000000F05
    data = Binary("Hello World.\n", 13, 13)
    prog = Binary(prog, 46, 46, endianness="big") # Big since code was already in correct order. Don't need to invert anything for LSB
    print(prog)
    x = x86_64()
    x.set_entry_point(0x401000 + 64)
    x.add_segment(7, 46, 46, prog)
    x.add_segment(7, 13, 13, data)
    for header in x.program_header:
        print("HEADER: ", header)
    for segment in x.segments:
        print("SEGMENT: ", segment)
    b = x.generate_executable().binary()
    print(f"Lenght is {len(b)}")
    from os import getcwd
    from os.path import join
    with open(join(getcwd(), "tests", "testELF", "TestExecutable2"), "wb") as fp: # Can be used to write it out as a binary file
        fp.write(b)
    assert 0 == 1