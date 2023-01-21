from elfgenerator.Binary import Binary


def test_Binary1():
    value = 0
    alignment = 4
    size = 4
    test = Binary(value, size, alignment)
    assert test.__repr__() == "00 00 00 00"

def test_Binary5():
    value = 17
    alignment = 4
    size = 4
    test = Binary(value, size, alignment)
    assert test.__repr__() == "11 00 00 00"

def test_Binary2():
    value = "ELF"
    alignment = 3
    size = 3
    test = Binary(value, size, alignment)
    assert test.__repr__() == "45 4c 46"

def test_Binary3():
    value = 0x4300002B
    alignment = 4
    size = 4
    test = Binary(value, size, alignment, endianness="big")
    assert test.__repr__() == "43 00 00 2b"

def test_Binary4():
    value = 0x4300002B
    alignment = 4
    size = 4
    test = Binary(value, size, alignment, endianness="little")
    assert test.__repr__() == "2b 00 00 43"


def test_Binary6():
    value = 0x4300002B
    alignment = 4
    size = 4
    test = Binary(value, size, alignment, endianness="little")
    value = "ELF"
    alignment = 3
    size = 3
    test2 = Binary(value, size, alignment)
    print(type(test), type(test2))
    test = test + test2
    assert test.__repr__() == "2b 00 00 43 45 4c 46"


