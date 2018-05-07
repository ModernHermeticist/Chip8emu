import os
import msvcrt as m


class Chip8(object):

    def __init__(self):

        self.general_registers = [0x00] * 16  # V0-VF

        self.vI = [0]  # two bytes

        self.delay_timer = [0]
        self.sound_timer = [0]

        self.pc = 0x200  # two bytes
        self.sp = [0]

        self.file_size = 0

        self.SCREEN_SIZE = [32, 64]

        self.memory = [0] * 4096

        self.firstnib = 0x00
        self.secondnib = 0x00
        self.next_byte = 0x00
        self.next_byte_firstnib = 0x00
        self.next_byte_secondnib = 0x00
        self.code = 0x00

    def bytes_from_file(self):
        with open("PONG", "rb") as f:
            self.file_size = os.path.getsize("PONG")
            while True:
                chunk = f.read(200)
                if chunk:
                    for b in chunk:
                        yield b
                else:
                    break

    def load_file_to_memory(self):
        i = 0x200
        for b in self.bytes_from_file():
            self.memory[i] = hex(b)
            i += 0x01
        i = 0x200
        while i < self.file_size + 0x200:
            self.memory[i] = int(self.memory[i], 16)
            i += 0x01

    def opcodes(self):
        if self.firstnib == 0x0:
            if self.next_byte == 0xE0:
                self.clear_display()
                self.pc += 2
            elif self.next_byte == 0xEE:
                self.return_from_subroutine()
                self.pc += 2
            else:
                print("{:03X}  {:02X}{:02X}  UNKNOWN 0".format(
                    self.pc, self.code, self.next_byte))
                self.pc += 2
        elif self.firstnib == 0x1:
            self.jump_address()
        elif self.firstnib == 0x2:
            self.call_address()
            self.pc += 2
        elif self.firstnib == 0x3:
            self.skip_if_reg_equal()
        elif self.firstnib == 0x4:
            self.skip_if_not_equal()
        elif self.firstnib == 0x5:
            self.skip_if_equal()
        elif self.firstnib == 0x6:
            self.load()
            self.pc += 2
        elif self.firstnib == 0x7:
            self.add()
            self.pc += 2

        elif self.firstnib == 0x8:
            if self.next_byte_secondnib == 0x0:
                self.load_register_with_register()
                self.pc += 2
            elif self.next_byte_secondnib == 0x1:
                self.logical_or()
                self.pc += 2
            elif self.next_byte_secondnib == 0x2:
                self.logical_and()
                self.pc += 2
            elif self.next_byte_secondnib == 0x3:
                self.logical_xor()
                self.pc += 2
            elif self.next_byte_secondnib == 0x4:
                self.add_registers()
                self.pc += 2
            elif self.next_byte_secondnib == 0x5:
                self.sub_registers_x_y()
                self.pc += 2
            elif self.next_byte_secondnib == 0x6:
                self.shift_right()
                self.pc += 2
            elif self.next_byte_secondnib == 0x7:
                self.sub_registers_y_x()
                self.pc += 2
            elif self.next_byte_secondnib == 0xE:
                self.shift_left()
                self.pc += 2
            else:
                print("{:03X}  {:02X}{:02X}  UNKNOWN 8".format(
                    self.pc, self.code, self.next_byte))
                self.pc += 2

        elif self.firstnib == 0x9:
            self.skip_next_instruction()
        elif self.firstnib == 0xA:
            self.set_i()
            self.pc += 2
        elif self.firstnib == 0xB:
            self.jump_with_offset()

        elif self.firstnib == 0xC:
            self.random_byte_plus_kk()
            self.pc += 2
        elif self.firstnib == 0xD:
            self.draw_sprites()
            self.pc += 2

        elif self.firstnib == 0xE:
            if self.next_byte == 0x9E:
                self.skip_next_on_key_press()
            elif self.next_byte == 0xA1:
                self.skip_next_on_not_key_press()
            else:
                print("{:03X}  {:02X}{:02X}  UNKNOWN E".format(
                    self.pc, self.code, self.next_byte))
                self.pc += 2

        elif self.firstnib == 0xF:
            if self.next_byte == 0x07:
                self.set_register_delay_timer()
                self.pc += 2
            elif self.next_byte == 0x0A:
                self.set_register_value_of_key()
                self.pc += 2
            elif self.next_byte == 0x15:
                self.load_delay_timer()
                self.pc += 2
            elif self.next_byte == 0x18:
                self.load_sound_timer()
                self.pc += 2
            elif self.next_byte == 0x1E:
                self.add_i_and_register()
                self.pc += 2
            elif self.next_byte == 0x29:
                self.load_f_in_register()
                self.pc += 2
            elif self.next_byte == 0x33:
                self.load_b_in_register()
                self.pc += 2
            elif self.next_byte == 0x55:
                self.store_in_memory()
                self.pc += 2
            elif self.next_byte == 0x65:
                self.read_from_memory()
                self.pc += 2
            else:
                print("{:03X}  {:02X}{:02X}  UNKNOWN F".format(
                    self.pc, self.code, self.next_byte))
                self.pc += 2

    # 6xkk LD
    def load(self):
        self.general_registers[self.secondnib] = self.next_byte
        # print("{:03X}  {:02X}{:02X}  LD V{:01X} {:02X}".format(
        # self.pc, self.code, self.next_byte, self.secondnib, self.next_byte))
        print("{:03X}  LD  V{:01X}: {:02X}".format(self.pc, self.secondnib,
                                                   self.general_registers[self.secondnib]))
    # 7xkk ADD

    def add(self):
        self.general_registers[self.secondnib] += self.next_byte
        if self.general_registers[self.secondnib] > 255:
            self.general_registers[self.secondnib] -= 255
        # print("{:03X}  {:02X}{:02X}  ADD V{:01X} {:02X}".format(
        # self.pc, self.code, self.next_byte, self.secondnib, self.next_byte))
        print("{:03X}  ADD  V{:01X}: {:02X}".format(
            self.pc, self.secondnib, self.next_byte))
    # 1nnn JMP

    def jump_address(self):
        temp = int(hex((self.secondnib << 8) | self.next_byte), 16)
        print("{:03X}  JMP {:03X}".format(self.pc, temp))
        self.pc = temp
        # print("{:03X}  {:02X}{:02X}  JMP {:01X}{:02X}".format(
        # self.pc, self.code, self.next_byte, self.secondnib, self.next_byte))

    def call_address(self):
        print("{:03X}  {:02X}{:02X}  CALL {:01X}{:02X}".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte))

    def skip_if_reg_equal(self):
        print("{:03X}  {:02X}{:02X}  SE V{:01X} {:02X}".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte))

    def skip_if_not_equal(self):
        print("{:03X}  {:02X}{:02X}  SNE V{:01X} {:02X}".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte))

    def skip_if_equal(self):
        print("{:03X}  {:02X}{:02X}  SE V{:01X} V{:01X}".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte_firstnib))

    def skip_next_instruction(self):
        print("{:03X}  {:02X}{:02X}  SNE V{:01X} V{:01X}".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte_firstnib))

    def set_i(self):
        print("{:03X}  {:02X}{:02X}  LD I {:01X}{:02X}".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte))

    def jump_with_offset(self):
        print("{:03X}  {:02X}{:02X}  JMP V0 + {:01X}{:02X}".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte))

    def random_byte_plus_kk(self):
        print("{:03X}  {:02X}{:02X}  RND V{:01X} AND {:02X}".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte))

    def draw_sprites(self):
        print("{:03X}  {:02X}{:02X}  DRW Starting at memory location V{:01X}, V{:01X},".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte_firstnib),
            " sprites are XORed onto the screen, set VF = collision")

    def skip_next_on_key_press(self):
        print("{:03X}  {:02X}{:02X}  SKP V{:01X}".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def skip_next_on_not_key_press(self):
        print("{:03X}  {:02X}{:02X}  SKNP V{:01X}".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    # 8xxx...
    def load_register_with_register(self):
        print("{:03X}  {:02X}{:02X}  LD V{:01X} V{:01X}".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte_firstnib))

    def logical_or(self):
        print("{:03X}  {:02X}{:02X}  OR V{:01X} V{:01X}".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte_firstnib))

    def logical_and(self):
        print("{:03X}  {:02X}{:02X}  AND V{:01X} V{:01X}".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte_firstnib))

    def logical_xor(self):
        print("{:03X}  {:02X}{:02X}  XOR V{:01X} V{:01X}".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte_firstnib))

    def add_registers(self):
        print("{:03X}  {:02X}{:02X}  ADD V{:01X} V{:01X}".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte_firstnib))

    def sub_registers_x_y(self):
        print("{:03X}  {:02X}{:02X}  SUB V{:01X} V{:01X}".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte_firstnib))

    def shift_right(self):
        print("{:03X}  {:02X}{:02X}  SHR V{:01X} 1".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def sub_registers_y_x(self):
        print("{:03X}  {:02X}{:02X}  SUBN V{:01X} V{:01X}".format(
            self.pc, self.code, self.next_byte, self.next_byte_firstnib, self.secondnib))

    def shift_left(self):
        print("{:03X}  {:02X}{:02X}  SHL V{:01X} 1".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    # TODO OBSOLETE
    # def jump_to_sys_address(self):
    #    print("{:03X}    SYS {:01X}{:02X}".format(self.pc, self.secondnib, self.next_byte))
    # TODO OBSOLETE

    def clear_display(self):
        print("{:03X}  {:02X}{:02X}  CLS".format(
            self.pc, self.code, self.next_byte))

    def return_from_subroutine(self):
        print("{:03X}  {:02X}{:02X}  RET".format(
            self.pc, self.code, self.next_byte))

    # Fxxx....
    def set_register_delay_timer(self):
        print("{:03X}  {:02X}{:02X}  LD V{:02X}, DT".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def set_register_value_of_key(self):
        print("{:03X}  {:02X}{:02X}  LD V{:02X}, K".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def load_delay_timer(self):
        print("{:03X}  {:02X}{:02X}  LD DT, V{:02X}".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def load_sound_timer(self):
        print("{:03X}  {:02X}{:02X}  LD ST, V{:02X}".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def add_i_and_register(self):
        print("{:03X}  {:02X}{:02X}  ADD I, V{:02X}".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def load_f_in_register(self):
        print("{:03X}  {:02X}{:02X}  LD F, V{:02X}".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def load_b_in_register(self):
        print("{:03X}  {:02X}{:02X}  LD B, V{:02X}".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def store_in_memory(self):
        print("{:03X}  {:02X}{:02X}  LD [I], V{:02X}".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def read_from_memory(self):
        print("{:03X}  {:02X}{:02X}  LD V{:02X}, [I]".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def disassembler(self, current_byte, next_byte):
        self.code = current_byte
        # print("{:02X}".format(self.code))
        self.firstnib = self.code >> 4
        # print("{:02X}".format(self.firstnib))
        self.secondnib = self.code & 0x0F
        # print("{:02X}".format(self.secondnib))
        self.next_byte = next_byte
        self.next_byte_firstnib = self.next_byte >> 4
        self.next_byte_secondnib = self.next_byte & 0x0F
        self.opcodes()
        # self.pc += 2


def wait():
    m.getch()


def main():

    current_byte = 0
    next_byte = 0

    chip8 = Chip8()

    chip8.load_file_to_memory()

    while chip8.pc < (chip8.file_size + 0x200):
        next_byte = chip8.memory[chip8.pc + 0x01]
        current_byte = chip8.memory[chip8.pc]
        chip8.disassembler(current_byte, next_byte)
        wait()

if __name__ == "__main__":
    main()
