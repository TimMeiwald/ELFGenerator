from elfgenerator.ELF_Header_Utils import *
from elfgenerator.ELF_Segment_Utils import *
from elfgenerator.Binary import Binary
from os import getcwd
from os.path import join


# class x86_64():

#     def __init__(self, entry_point: int):
#         EI_CLASS = 2
#         self.e_ident = e_ident(EI_CLASS=EI_CLASS, EI_DATA=1, EI_OSABI=0, EI_ABIVERSION=0) #64 bit, LSB, Linux, Unsure
#         self.e_type = e_type.ET_EXEC
#         self.e_machine = e_machine.EM_X86_64
#         self.e_version = e_version.EV_CURRENT
#         self.e_entry = e_entry(0, EI_CLASS=EI_CLASS) # 0 is placeholder # TODO MODIFY FOR 64BIT
#         self.e_entry.value = entry_point
#         self.e_phoff = e_phoff(0, EI_CLASS=EI_CLASS) # 0 is placeholder # TODO MODIFY FOR 64BIT
#         self.e_shoff = e_shoff(0, EI_CLASS=EI_CLASS) # 0 is placeholder # TODO MODIFY FOR 64BIT
#         self.e_flags = e_flags()
#         self.e_ehsize = e_ehsize(64) #0 is placeholder
#         self.e_phentsize = e_phentsize(0) # 0 is placeholder
#         self.e_phnum = e_phnum(0) # 0 is placeholder
#         self.e_shentsize = e_shentsize(0) # 0 is placeholder
#         self.e_shnum = e_shnum(0) # 0 is placeholder
#         self.e_shstrndx = e_shstrndx(0) # 0 is placeholder

#         self.program_header = []
#         self.segments = []

#     def _generate_ELF_header(self):
#         header_vals = [self.e_ident, self.e_type, self.e_machine, self.e_version,
#         self.e_entry, self.e_phoff, self.e_shoff, self.e_flags, self.e_ehsize,
#         self.e_phentsize, self.e_phnum, self.e_shentsize, self.e_shnum, self.e_shstrndx]
#         ELF_HEADER = Binary(0,0,0)
#         for val in header_vals:
#             ELF_HEADER += val.binary()       
#         return ELF_HEADER

#     def _generate_program_header_table(self):
#         header_table = Binary(0,0,0)
#         for p_header in self.program_header:
#             header_table += p_header
#         return header_table
        
#     def _generate_segments(self):
#         segments = Binary(0,0,0)
#         for segment in self.segments:
#             padding = 4096 - segment.size 
#             padding = Binary(0, padding, padding)
#             segment = segment + padding
#             segments += segment
#         return segments

#     def add_program_segment(self, program):
#         program_header, program_code = program
#         if(self.e_phentsize.value == 0):
#             self.e_phentsize.value = program_header.size
#         elif(self.e_phentsize.value != 0):
#             if(self.e_phentsize.value != program_header.size):
#                 raise ValueError("Program Headers must have the same size. Check you are not using mismatched 32 bit or 64 bit segments")
#         self.e_phnum.value += 1 
#         self.e_phoff.value = 64 # p_header after ELF header
#         self.segments.append(program_code)
#         self.program_header.append(program_header)

#         print(f"Number of p_headers: {self.e_phnum.value}")
#         print(f"Size of p_headers: {self.e_phentsize.value}")
#         print(f"Offset of p_headers: {self.e_phoff.value}")

#         print(f"Programme entry point: {self.e_entry.value}")



#         """Shit need to set all the values correctly in ELF header and
#         program header etc"""




class x86_64():
    
    def __init__(self):
        """Entry Point needs to be the virtual address of the TEXT segment aka the segment that actually runs the code"""
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
        self.e_phentsize = e_phentsize(56) # Program headers are 56 bytes for x86-64
        self.e_phnum = e_phnum(0) # 0 is placeholder
        self.e_shentsize = e_shentsize(0) # 0 is placeholder
        self.e_shnum = e_shnum(0) # 0 is placeholder
        self.e_shstrndx = e_shstrndx(0) # 0 is placeholder

        self.program_header = []
        self.segments = []

    def set_entry_point(self, entry_point: int):
        """Entry point is the virtual address of the code, so usually the TEXT segment"""
        self.e_entry.value = entry_point

    def add_segment(self, flags, size_physical: int, size_virtual: int, code: Binary =None):
        """ p_type This member tells what kind of segment this array element describes or how to
            interpret the array element's information. Type values and their meanings appear
            below.
            p_offset This member gives the offset from the beginning of the file at which the first byte
            of the segment resides.
            p_vaddr This member gives the virtual address at which the first byte of the segment resides
            in memory.
            p_paddr On systems for which physical addressing is relevant, this member is reserved for
            the segment's physical address. This member requires operating system specific
            information, which is described in the appendix at the end of Book III.
            p_filesz This member gives the number of bytes in the file image of the segment; it may be
            zero.
            p_memsz This member gives the number of bytes in the memory image of the segment; it
            may be zero.
            p_flags This member gives flags relevant to the segment. Defined flag values appear below.
            It's a bitmap so the combo can give you all three or any 2
            0x1 Execute
            0x2 Write
            0x4 Read
            p_align Loadable process segments must have congruent values for p_vaddr and
            p_offset, modulo the page size.This member gives the value to which the
            segments are aligned in memory and in the file. Values 0 and 1 mean that no
            alignment is required. Otherwise, p_align should be a positive, integral power of
            2, and p_addr should equal p_offset, modulo p_align."""
        if(size_physical == 0 and code == None):
            raise Exception("If physical size is not 0 then you must have code to write.")
        else:
            if(len(code) != size_physical):
                raise Exception("Physical size must be the same length as the Binary passed to it.")
            if(len(code) != size_virtual):
                raise Exception("Virtual size must be the same length as the Binary passed to it.")
        
        if(len(self.segments) == 0):
            offset = 64
            type = 1 # Loadable segment
            vaddr = self.e_entry.value
            paddr = offset
            align = 0 # No alignment
            flags = flags
            filesz = size_physical # Bytes needed on disk
            memsz = size_virtual # Bytes needed virtually, e.g BSS may allocate a lot of data but doesn't use any physical space. 
            self.program_header.append(Segment(type, offset, vaddr, paddr, filesz, memsz, flags, align))
            self.segments.append(code)
        else:
            last_segment = self.program_header[-1]

            offset = last_segment.p_paddr.value + last_segment.p_filesz.value # Since p_paddr is counting up physical addresses.
            type = 1
            vaddr = last_segment.p_vaddr.value + last_segment.p_memsz.value
            paddr = last_segment.p_paddr.value + last_segment.p_filesz.value
            align = 0
            flags = flags
            filesz = size_physical
            memsz = size_virtual
            self.program_header.append(Segment(type, offset, vaddr, paddr, filesz, memsz, flags, align))
            self.segments.append(code)

        
    def _generate_ELF_header(self):
        header_vals = [self.e_ident, self.e_type, self.e_machine, self.e_version,
        self.e_entry, self.e_phoff, self.e_shoff, self.e_flags, self.e_ehsize,
        self.e_phentsize, self.e_phnum, self.e_shentsize, self.e_shnum, self.e_shstrndx]
        ELF_HEADER = Binary(0,0,0)
        for val in header_vals:
            ELF_HEADER += val.binary()       
        return ELF_HEADER

    def _generate_program_header_table(self):
        last_segment_header = self.program_header[-1] 
        self.e_phoff.value = last_segment_header.p_paddr.value + last_segment_header.p_filesz.value # Location of start of program header. 
        self.e_phnum.value = len(self.segments)
        print(self.e_phoff.value, self.e_phnum.value)
        header_table = Binary(0,0,0)
        for p_header in self.program_header:
            header_table += p_header.binary()
        return header_table
    
    def generate_executable(self):
        program_header = self._generate_program_header_table() # So that stuff gets set before ELF header is generated
        code = self._generate_ELF_header()
        for segment in self.segments:
             code += segment
        code += program_header
        print(f"Header Length = {len(program_header)}")
        return code
  