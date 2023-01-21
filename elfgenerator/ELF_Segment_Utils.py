"""       size alignment
Elf32_Addr 4 4 Unsigned program address
Elf32_Half 2 2 Unsigned medium integer
Elf32_Off 4 4 Unsigned file offset
Elf32_Sword 4 4 Signed large integer
Elf32_Word 4 4 Unsigned large integer
unsigned char 1 1 Unsigned small integer
"""
from enum import Enum
from elfgenerator.Binary import Binary
class p_type(Enum):
    """
    This member tells what kind of segment this array element describes or how to
    interpret the array element's information. Type values and their meanings appear
    below.
    """
    PT_NULL = 0
    PT_LOAD = 1
    PT_DYNAMIC = 2
    PT_INTERP = 3
    PT_NOTE = 4
    PT_SHLIB = 5
    PT_PHDR = 6
    PT_LOPROC = 0x70000000
    PT_HIPROC = 0x7fffffff

    def binary(self):
        return Binary(self.value, 4, 4)

class p_offset():
    """
    This member gives the offset from the beginning of the file at which the first byte
    of the segment resides.
    """
    def __init__(self, value):
        self.value = value

    def binary(self):
        size = 8
        alignment = 8
        return Binary(self.value, size, alignment)


class p_vaddr():
    """
    This member gives the virtual address at which the first byte of the segment resides
    in memory.
    """
    def __init__(self, value):
        self.value = value

    def binary(self):
        size = 8
        alignment = 8
        return Binary(self.value, size, alignment)


class p_paddr():
    """
    On systems for which physical addressing is relevant, this member is reserved for
    the segment's physical address. This member requires operating system specific
    information, which is described in the appendix at the end of Book III.

    On systems for which physical addressing is relevant, this member is reserved for
    the segment's physical address. Because System V ignores physical addressing for
    application programs, this member has unspecified contents for executable files and
    shared objects.
    """
    def __init__(self, value):
        print("WARNING: p_paddr: Requires OS specific information, refer to Book 3 of Specification")
        self.value = value

    def binary(self):
        size = 8
        alignment = 8
        return Binary(self.value, size, alignment)


class p_filesz():
    """
    This member gives the number of bytes in the file image of the segment; it may be
    zero.
    """
    def __init__(self, value):
        self.value = value

    def binary(self):
        size = 8
        alignment = 8
        return Binary(self.value, size, alignment)

class p_memsz():
    """
    This member gives the number of bytes in the memory image of the segment; it
    may be zero.
    """
    def __init__(self, value):
        self.value = value

    def binary(self):
        size = 8
        alignment = 8
        return Binary(self.value, size, alignment)


class p_flags():
    """
    This member gives flags relevant to the segment. Defined flag values appear below.

    Since processor dependent. I think, simply input correct value
    For Unix x86 systems at least
    0x1 is Execute
    0x2 is Write
    0x4 is Read
    0x6 is Read and Write
    You can mix and match. 
    The above are bits essentially so you can do all simultaneously by adding? the numbers
    """
    
    def __init__(self, value):
        self.value = value

    def binary(self):
        size = 4
        alignment = 4
        return Binary(self.value, size, alignment)


class p_align():
    """
    Loadable process segments must have congruent values for p_vaddr and
    p_offset, modulo the page size.This member gives the value to which the
    segments are aligned in memory and in the file. Values 0 and 1 mean that no
    alignment is required. Otherwise, p_align should be a positive, integral power of
    2, and p_addr should equal p_offset, modulo p_align.
    """
    def __init__(self, value):
        """
        Values 0 and 1 mean that no
        alignment is required. Otherwise, p_align should be a positive, integral power of
        2, and p_addr should equal p_offset, modulo p_align.
        """
        self.value = value

    def binary(self):
        size = 8
        alignment = 8
        return Binary(self.value, size, alignment)

class Segment_32():
    def __init__(self, type, offset, vaddr, paddr, filesz, memsz, flags, align):
        self.p_type = p_type(type)
        self.p_offset = p_offset(offset)
        self.p_vaddr = p_vaddr(vaddr)
        self.p_paddr = p_paddr(paddr)
        self.p_filesz = p_filesz(filesz)
        self.p_memsz = p_memsz(memsz)
        self.p_flags = p_flags(flags)
        self.p_align = p_align(align)
    
    def binary(self):
        segment_vals = [self.p_type, self.p_offset, self.p_vaddr,
                        self.p_paddr, self.p_filesz, self.p_memsz,
                        self.p_flags, self.p_align]
        result = Binary(0,0,0)
        for val in segment_vals:
            result += val.binary()
        return result

class Segment():

    def __init__(self, type, offset, vaddr, paddr, filesz, memsz, flags, align):
        self.p_type = p_type(type)
        self.p_flags = p_flags(flags)
        self.p_offset = p_offset(offset)
        self.p_vaddr = p_vaddr(vaddr)
        self.p_paddr = p_paddr(paddr)
        self.p_filesz = p_filesz(filesz)
        self.p_memsz = p_memsz(memsz)
        self.p_align = p_align(align)
    
    def binary(self):
        segment_vals = [self.p_type, self.p_flags, self.p_offset, 
                        self.p_vaddr, self.p_paddr, self.p_filesz, 
                        self.p_memsz, self.p_align]
        result = Binary(0,0,0)
        for val in segment_vals:
            result += val.binary()
        return result
    
    def __repr__(self):
        string = f"\np_type = {self.p_type.binary()}    -> {self.p_type.value}\n"
        string += f"p_flags = {self.p_flags.binary()}   -> {self.p_flags.value}\n"
        string += f"p_offset = {self.p_offset.binary()} -> {self.p_offset.value}\n"
        string += f"p_vaddr = {self.p_vaddr.binary()}   -> {self.p_vaddr.value}\n"
        string += f"p_paddr = {self.p_paddr.binary()}   -> {self.p_paddr.value}\n"
        string += f"p_filesz = {self.p_filesz.binary()} -> {self.p_filesz.value}\n"
        string += f"p_memsz = {self.p_memsz.binary()}   -> {self.p_memsz.value}\n"
        string += f"p_align = {self.p_align.binary()}   -> {self.p_align.value}\n"
        return string