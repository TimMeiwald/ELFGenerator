from elfgenerator.ELF_Header_Utils import *
from elfgenerator.ELF_Segment_Utils import *
from Binary import Binary
from os import getcwd
from os.path import join


class x86_64():

    def __init__(self):
        EI_CLASS = 2
        self.e_ident = e_ident(EI_CLASS=EI_CLASS, EI_DATA=1, EI_OSABI=0, EI_ABIVERSION=0) #64 bit, LSB, Linux, Unsure
        self.e_type = e_type.ET_EXEC
        self.e_machine = e_machine.EM_X86_64
        self.e_version = e_version.EV_CURRENT
        self.e_entry = e_entry(0, EI_CLASS=EI_CLASS) # 0 is placeholder # TODO MODIFY FOR 64BIT
        self.e_phoff = e_phoff(0, EI_CLASS=EI_CLASS) # 0 is placeholder # TODO MODIFY FOR 64BIT
        self.e_shoff = e_shoff(0, EI_CLASS=EI_CLASS) # 0 is placeholder # TODO MODIFY FOR 64BIT
        self.e_flags = e_flags()
        self.e_ehsize = e_ehsize(64) #0 is placeholder
        self.e_phentsize = e_phentsize(0) # 0 is placeholder
        self.e_phnum = e_phnum(0) # 0 is placeholder
        self.e_shentsize = e_shentsize(0) # 0 is placeholder
        self.e_shnum = e_shnum(0) # 0 is placeholder
        self.e_shstrndx = e_shstrndx(0) # 0 is placeholder
        self.program_header = []
        self.segments = []


    def _generate_ELF_header(self):
        header_vals = [self.e_ident, self.e_type, self.e_machine, self.e_version,
        self.e_entry, self.e_phoff, self.e_shoff, self.e_flags, self.e_ehsize,
        self.e_phentsize, self.e_phnum, self.e_shentsize, self.e_shnum, self.e_shstrndx]
        ELF_HEADER = Binary(0,0,0)
        for val in header_vals:
            ELF_HEADER += val.binary()       
        return ELF_HEADER

    def write_to_file(self, filename):
        cwd = getcwd()
        filename = join(cwd,filename)
        with open(filename, "wb") as fp:
            for byte in self._generate_file():
                byte = int(byte, 16)
                byte = byte.to_bytes(1, "big")
                fp.write(byte)
        return 0
    
    def _generate_file(self):
        ELF_HEADER = self._generate_ELF_header()
        #print(ELF_HEADER.hex_value)
        p_header_table = self._generate_program_header_table()
        segments = self._generate_segments()
        #print("p_header table = ", p_header_table.hex_value)
        #print("segments = ", segments.hex_value)

        binary = ELF_HEADER + p_header_table 
        padding = (4096 - binary.size)
        padding = Binary(0, padding, padding)
        binary = binary + padding
        print(binary.size)
        #print("HEADER SIZE = ", binary.size)
        binary += segments 
        #print(binary.size)
        binary = binary.hex_value
        return binary

    def _generate_program_header_table(self):
        header_table = Binary(0,0,0)
        for p_header in self.program_header:
            header_table += p_header
        return header_table
        
    def _generate_segments(self):
        segments = Binary(0,0,0)
        for segment in self.segments:
            padding = 4096 - segment.size 
            padding = Binary(0, padding, padding)
            segment = segment + padding
            segments += segment
        return segments

    def add_program_segment(self, program):
        program_header, program_code = program
        if(self.e_phentsize.value == 0):
            self.e_phentsize.value = program_header.size
        elif(self.e_phentsize.value != 0):
            if(self.e_phentsize.value != program_header.size):
                raise ValueError("Program Headers must have the same size. Check you are not using mismatched 32 bit or 64 bit segments")
        self.e_phnum.value += 1 
        self.e_phoff.value = 64 # p_header after ELF header
        #self.e_entry.value = self.e_phoff.value + self.e_phentsize.value*self.e_phnum.value # entry after p_header #If I figure it out
        self.e_entry.value = 0x401000
        self.segments.append(program_code)
        self.program_header.append(program_header)

        print(f"Number of p_headers: {self.e_phnum.value}")
        print(f"Size of p_headers: {self.e_phentsize.value}")
        print(f"Offset of p_headers: {self.e_phoff.value}")

        print(f"Programme entry point: {self.e_entry.value}")



        """Shit need to set all the values correctly in ELF header and
        program header etc"""





if __name__ == "__main__":
    """
    MyELF = x86_64()
    
    # tiny42.prg below, literally just returns 42 as error code
    # Use ./[file_name] ; echo $? to test output
    aka 
    mov rdi, 0x2a ; 0x2a 42 is the return code
    mov rax, 0x3c ; 60 as first arg implies exit
    syscall
    "48 c7 c7 2a 00 00 00" #-> Int 20485856540229632
    "48 c7 c0 3c 00 00 00" #-> Int 20485826777448448
    "0f 05 c3"
    binary = Binary(0x48c7c72a00000048c7c03c0000000f05, 16, 16)
    print(binary.hex_value)
    binary.hex_value = binary.hex_value[::-1]
    print(binary.hex_value)
    segment_text = binary
    p_header_text = Segment(1, 0x001000,0x401000,0x401000,0x001000, 0x001000, 0x5, 2**12)
    MyELF.add_program_segment([p_header_text.binary(), segment_text])
    MyELF.write_to_file("TestELF2")
    #Working
    """

    
    MyELF = x86_64()

    
    # helloworld below
    """ mov rax, 1 ; 1 is write 
        mov rdi, 1
        mov rsi, 0x402000 ; Memory address of data segment, need to track positions for compiler
        mov rdx, 13
        syscall

        mov rax, 60 ; 60 is exit
        mov rdi, 0 ; Return value of 0
        syscall
        """

    
    binary = Binary(0x48C7C00100000048C7C70100000048C7C60020400048C7C20D0000000F0548C7C03C00000048C7C7000000000F05, 46, 46)
    binary.hex_value = binary.hex_value[::-1]
    segment_text = binary
    segment_data = Binary("Hello World.\n", 13, 13)
    p_header_text = Segment(1, 0x001000,0x401000,0x401000,0x001000, 0x001000, 0x5, 2**12)
    p_header_data = Segment(1, 0x002000,0x402000,0x402000,0x001000, 0x001000, 0x4, 2**12)
    #print("header size = ", p_header.binary().size)
    MyELF.add_program_segment([p_header_text.binary(), segment_text])
    MyELF.add_program_segment([p_header_data.binary(), segment_data])
    #MyELF.add_programn_segment([p_header.binary(), segment])
    #print(MyELF.e_phentsize.value, MyELF.e_phnum.value)
    #print(MyELF._generate_ELF_header().hex_value)
    #MyELF._generate_file()
    #print(MyELF.e_shoff.binary().hex_value, MyELF.e_shentsize.binary().hex_value)
    #print(MyELF.e_phoff.binary().hex_value, MyELF.e_phnum.binary().hex_value, MyELF.e_phentsize.binary().hex_value)
    binary = MyELF._generate_file()
    #for index in range(0,4150):
    #    print(index, binary[index])
    MyELF.write_to_file("TestELF3")
    