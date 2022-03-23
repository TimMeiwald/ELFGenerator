import enum
from Binary import Binary
from enum import Enum

class e_type(Enum):
    """ Identifies object file type"""
    ET_NONE = 0 # No file type
    ET_REL = 1 # Relocatable file
    ET_EXEC = 2 # Executable file
    ET_DYN = 3 # Shared object file
    ET_CORE = 4 # Core file
    ET_LOPROC = 0xff00 # Processor specific 
    ET_HIPROC = 0xffff #Processor specific
    
    def binary(self):
        """Creates binary object that both checks size, pads values and contains size and alignment info for a given thing
        
        E.g e_type.ET_CORE.binary().size = 2 because it's a 2 byte obj 
            e_type.ET_CORE.binary().alignment = 2 because it's aligned on a 2 byte boundary
            e_type.ET_CORE.binary().hex_value = [0x00, 0x04] because it's 4 in a 2 bytes so it's been padded to add more 0s 
        """
        return Binary(self.value, 2,2)

class e_machine(Enum):
    """ Specifies required architechture for file
    
    Add as a pull request if I haven't done so
    """
    EM_NONE = 0
    EM_M32 = 1
    EM_SPARC = 2
    EM_386 = 3
    EM_68K = 4
    EM_88K = 5
    EM_860 = 7
    EM_MIPS = 8
    EM_X86_64 = 62
    
    def binary(self):
        return Binary(self.value, 2,2)


class e_version(Enum):
    """ Identifies Object file version"""
    EV_NONE = 0 # Invalid version
    EV_CURRENT = 1 # Current version

    
    def binary(self):
        return Binary(self.value, 4,4)

class e_entry():
    """Virtual address to which system transfers control,
     if the file has no associated entry point return 0"""
    def __init__(self, value, *, EI_CLASS=0):
        if(EI_CLASS == 1):
            self.size = 4
            self.alignment = 4
        elif(EI_CLASS == 2):
            self.size = 8
            self.alignment = 8
        elif(EI_CLASS == 0):
            raise ValueError("You need to specify whether it's a 32 bit or 64 bit value using EI_CLASS")
        else:
            raise NotImplementedError("Anything other than 32 bit or 64 bit was not defined when this was written.")
        self.value = value
    
    def binary(self):
        return Binary(self.value, self.size, self.alignment)


class e_phoff():
    """Holds the program header tables file offset in bytes
    if no program header then its zero"""
    def __init__(self, value, *, EI_CLASS=0):
        if(EI_CLASS == 1):
            self.size = 4
            self.alignment = 4
        elif(EI_CLASS == 2):
            self.size = 8
            self.alignment = 8
        elif(EI_CLASS == 0):
            raise ValueError("You need to specify whether it's a 32 bit or 64 bit value using EI_CLASS")
        else:
            raise NotImplementedError("Anything other than 32 bit or 64 bit was not defined when this was written.")
        self.value = value
    
    def binary(self):
        return Binary(self.value, self.size, self.alignment)

class e_shoff():
    """Holds the section header tables file offset in bytes
    if no section header then its zero"""
    def __init__(self, value, *, EI_CLASS=0):
        if(EI_CLASS == 1):
            self.size = 4
            self.alignment = 4
        elif(EI_CLASS == 2):
            self.size = 8
            self.alignment = 8
        elif(EI_CLASS == 0):
            raise ValueError("You need to specify whether it's a 32 bit or 64 bit value using EI_CLASS")
        else:
            raise NotImplementedError("Anything other than 32 bit or 64 bit was not defined when this was written.")
        self.value = value
    
    def binary(self):
        return Binary(self.value, self.size, self.alignment)

class e_flags():
    """Holds architechture specific flags"""
    def __init__(self, value=0):
        self.size = 4
        self.alignment = 4
        self.value = value
    
    def binary(self):
        return Binary(self.value, self.size, self.alignment)



class e_ehsize():
    """Holds ELF header's size in bytes"""
    def __init__(self, value):
        self.size = 2
        self.alignment = 2
        self.value = value
    
    def binary(self):
        return Binary(self.value, self.size, self.alignment)

class e_phentsize():
    """Holds the size of bytes in one entry of the files program header table, 
    all entries are teh same size"""
    def __init__(self, value):
        self.size = 2
        self.alignment = 2
        self.value = value
    
    def binary(self):
        return Binary(self.value, self.size, self.alignment)

class e_phnum():
    """Holds the number of entreis in the program header table, If no header
    is zero"""
    def __init__(self, value):
        self.size = 2
        self.alignment = 2
        self.value = value
    
    def binary(self):
        return Binary(self.value, self.size, self.alignment)

class e_shentsize():
    """Holds the size in bytes of one section header"""
    def __init__(self, value):
        self.size = 2
        self.alignment = 2
        self.value = value
    
    def binary(self):
        return Binary(self.value, self.size, self.alignment)

class e_shnum():
    """Holds the number of entreis in section header table, if no header
    then 0"""
    def __init__(self, value):
        self.size = 2
        self.alignment = 2
        self.value = value
    
    def binary(self):
        return Binary(self.value, self.size, self.alignment)

class e_shstrndx():
    """Holds the section header table index of the entry associated
    with the section name string table, if the file doesn't have one it holds the value
    SHN_UNDEF(0x00)"""
    def __init__(self, value=0):
        self.size = 2
        self.alignment = 2
        self.value = value
    
    def binary(self):
        return Binary(self.value, self.size, self.alignment)


class e_ident():
    """Holds the initial bytes that mark the file as an object file
    and provides machine independent data needed to decode and 
    interpret the ELF files content"""

    def __init__(self,*, EI_CLASS, EI_DATA, EI_OSABI, EI_ABIVERSION):
        print("WARNING LSB OR MSB DOENS'T DO ANYTHING YET, NEEDS TO AFFECT PADDING")
        self.EI_MAG = Binary(0x7f, 1, 1)
        self.EI_MAG_13 = Binary("ELF", 3, 3)
        self.EI_CLASS = Binary(EI_CLASS, 1, 1) # 0 is invalid, 1 32 bit, 2 64 bit
        self.EI_DATA = Binary(EI_DATA, 1, 1) # 0 is invalid, 1 is Least Sig bit/byte not sure, 2 is Most sig bit
        self.EI_VERSION = Binary(1, 1, 1) # Just like e_version always 1
        self.EI_OSABI = Binary(EI_OSABI, 1, 1) #OS verison
        self.EI_ABIVERSION = Binary(EI_ABIVERSION, 1, 1) # unsure what
        self.EI_PAD = Binary(0x00, 7, 7) #Marks start of unused bytes in e_ident can change in future

    
    def binary(self):
        return self.EI_MAG + self.EI_MAG_13 + self.EI_CLASS + self.EI_DATA + self.EI_VERSION + self.EI_OSABI + self.EI_ABIVERSION + self.EI_PAD



if __name__ == "__main__":
    x = e_ident(EI_CLASS=2, EI_DATA=1, EI_OSABI=0, EI_ABIVERSION=0)
    print(x.binary().size)
