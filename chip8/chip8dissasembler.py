import os


class Chip8Disassembler(object):

    def __init__(self):

        self.pc = 0x200
        self.buffer = 0x00
        self.firstnib = 0
        self.secondnib = 0
        self.next_byte = 0
        self.next_byte_firstnib = 0
        self.next_byte_secondnib = 0
        self.code = 0

    def opcodes(self):
        if self.firstnib == 0x0:
            print("0 not handled yet")
        elif self.firstnib == 0x1:
            self.jump_address()
        elif self.firstnib == 0x2:
            self.call_address()
        elif self.firstnib == 0x3:
            self.skip_if_reg_equal()
        elif self.firstnib == 0x4:
            self.skip_if_not_equal()
        elif self.firstnib == 0x5:
            self.skip_if_equal
        elif self.firstnib == 0x6:
            self.load()
        elif self.firstnib == 0x7:
            self.add()
        elif self.firstnib == 0x8:
            print("8 not handled yet")
        elif self.firstnib == 0x9:
            self.skip_next_instruction()
        elif self.firstnib == 0xA:
            self.set_i()
        elif self.firstnib == 0xB:
            self.jump_with_offset()
        elif self.firstnib == 0xC:
            self.random_byte_plus_kk()
        elif self.firstnib == 0xD:
            print("D not handled yet")
        elif self.firstnib == 0xE:
            print("E not handled yet")
        elif self.firstnib == 0xF:
            print("F not handled yet")

    def move_value_to_reg(self):
        pass

    def load(self):
        print("LD V{:01X} {:02X}".format(self.secondnib, self.next_byte))

    def add(self):
        print("ADD V{:01X} {:02X}".format(self.secondnib, self.next_byte))

    def jump_address(self):
        print("JMP {:01X}{:02X}".format(self.secondnib, self.next_byte))

    def call_address(self):
        print("CALL {:01X}{:02X}".format(self.secondnib, self.next_byte))

    def skip_if_reg_equal(self):
        print("SE V{:01X} {:02X}".format(self.secondnib, self.next_byte))

    def skip_if_not_equal(self):
        print("SNE V{:01X} {:02X}".format(self.secondnib, self.next_byte))

    def skip_if_equal(self):
        print("SE V{:01X} V{:01X}".format(
            self.secondnib, self.next_byte_firstnib))

    def skip_next_instruction(self):
        print("SNE V{:01X} V{:01X}".format(
            self.secondnib, self.next_byte_firstnib))

    def set_i(self):
        print("LD I {:01X}{:02X}".format(self.secondnib, self.next_byte))

    def jump_with_offset(self):
        print("JMP V0 + {:01X}{:02X}".format(self.secondnib, self.next_byte))

    def random_byte_plus_kk(self):
        print("RND V{:01X} AND {:02X}".format(self.secondnib, self.next_byte))

    def disassembler(self, value, next_byte):
        self.code = value
        # print("{:02X}".format(self.code))
        self.firstnib = self.code >> 4
        # print("{:02X}".format(self.firstnib))
        self.secondnib = self.code & 0x0F
        # print("{:02X}".format(self.secondnib))
        self.next_byte = next_byte
        self.next_byte_firstnib = self.next_byte >> 4
        self.next_byte_secondnib = self.next_byte & 0x0F
        self.opcodes()


def bytes_from_file(filename, chunksize=8192):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    yield b
            else:
                break


def main():

    dis = Chip8Disassembler()

    a = []
    next_byte = 0

    for b in bytes_from_file("Fishie.ch8"):
        a.append(hex(b))
        # print(b)

    l = len(a)
    for index, item in enumerate(a):
        if index < (l - 1):
            next_byte = a[index + 1]
            next_byte = int(next_byte, 16)
        item = a[index]
        item = int(item, 16)
        dis.disassembler(item, next_byte)
        index += 2


main()
