


from typing import Type


class Binary():

    def __init__(self, value, size, alignment):
        self.alignment = alignment # Boundary Alignment, aka 4 will align on a 4 byte boundary
        self.size = size # Size in Bytes
        if(size != 0):
            self.value, hex_value = self.__check_value(value)   # Value to be written, keep value for readability prior to binary conversion
            self.hex_value = self.__add_padding(hex_value)
        else:
            self.value = [] # Simply allows null Binary objects to make other code neater e.g in loops adding them
            self.hex_value = []

    def __check_value(self, value):
        if(type(value) == str):
            if(len(value) < 1):
                raise Exception("String input must be at least one char.")
            hex_value = list(map(hex, map(ord, value))) #Gets a list of hex values of the ord of each char in the string
            hex_value = hex_value[::-1]
            if(len(hex_value) > self.size):
                size = len(hex_value)
                raise ValueError(f"""Input: '{value}' is {size} bytes of data.  
This is larger than the {self.size} bytes specified.""")
            value = list(value)
            return value, hex_value 
        elif(type(value) == int):
            hex_value = hex(value)
            hex_value = self.__hex_bytes_to_hex_byte_array(hex_value)
            return [value], hex_value
        else:
            raise TypeError(f"Type {value} is not a valid input.")

    def __hex_bytes_to_hex_byte_array(self, hex_value):
        hex_value = hex_value[2:]
        length = len(hex_value)
        byte_array = []
        if(len(hex_value) % 2 == 0):
            pass
        else:
            hex_value = "0" + hex_value
        for index in range(0, length, 2):
            byte_array.append("0x" + hex_value[index:index+2])
        hex_value = byte_array
        return hex_value

    def __add_padding(self, hex_value):
        bytes_to_pad = self.size - len(hex_value)
        if(bytes_to_pad != 0):
            padding = bytes_to_pad*["0x00"]
            hex_value =  padding + hex_value 
        return hex_value[::-1]

    def __add__(self, other):
        if(type(other) != Binary):
            raise TypeError("Can only add Binary objects to other Binary objects")
        self.size = self.size + other.size
        self.value = self.value + other.value
        self.alignment = self.alignment + other.alignment
        self.hex_value = self.hex_value + other.hex_value #Order will depend on endianness
        return self
    
    def __repr__(self):
        response = ""
        for i in self.hex_value:
            response += i + " "
        return response

if __name__ == "__main__":
    x3 = Binary(0,0,0)
    x1 = Binary(0x7F, 1, 1)
    x2 = Binary("ELF", 3, 3)
    print((x3+x1+x2).hex_value)
    x = Binary(0x4010000000, 8, 8)
    print(x.value, x.hex_value)
    print(0x401000)

