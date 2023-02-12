


from typing import Type


class Binary():

    def __init__(self, value: str | int, size: int, alignment: int, endianness = "little"):
        """Accepts hex, ascii string or int values, can specify 'little' or 'big' endian with 'little' as default

        Note that strings create bytes left to right regardless of endiannness, mainly useful for magic numbers and the like. 
        """
        self.endianness = endianness
        self.alignment = alignment
        self.size = size
        self.value = []
        self._check_type(value)

    def _check_type(self, value):
        if(type(value) == int):
            self._handle_int(value)
        elif(type(value) == str):
            self._handle_string(value)
        elif(type(value) == list):
            for val in value:
                self._check_type()
        else:
            raise ValueError("Invalid type of input.")

    def _handle_int(self, value):
        self.value = value.to_bytes(self.size, self.endianness)
        if(len(self.value) > self.size):
            raise ValueError("Value requires too many bytes to represent")

    def _handle_string(self, value):
        self.value = bytes(bytearray(value, encoding="ASCII"))
        if(len(self.value) > self.size):
            raise ValueError("Value requires too many bytes to represent")

    def __repr__(self):
        hex_strings = ""
        for val in self.value.copy():
            val = hex(val)
            if(len(val) == 3):
                val = "0" + val[2]
            else:
                val = val[2:]
            hex_strings += val + " "
        hex_strings = hex_strings[:-1]
        return hex_strings

    def binary(self):
        return self.value.copy()

    def __add__(self, other):
        if(type(other) != Binary):
            raise TypeError("Can only add Binary objects to other Binary objects")
        self.size = self.size + other.size
        self.value = self.value + other.value
        self.alignment = self.alignment + other.alignment
        return self

    def __len__(self):
        return len(self.value)
