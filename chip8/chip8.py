import os


class Chip8(object):

    def __init__(self):

        self.general_registers = [0] * 16  # V0-VF

        self.vI = [0] * 2

        self.delay_timer = [0]
        self.sound_timer = [0]

        self.pc = [0] * 2
        self.sp = [0]

        self.file_size = 0

        self.SCREEN_SIZE = [32, 64]

        self.memory = [0] * 4096

        self.firstnib = 0
        self.secondnib = 0
        self.next_byte = 0
        self.next_byte_firstnib = 0
        self.next_byte_secondnib = 0
        self.code = 0

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
        i = 200
        for b in self.bytes_from_file():
            self.memory[i] = hex(b)
            i += 1
        i = 200
        while i < self.file_size + 200:
            self.memory[i] = int(self.memory[i], 16)
            print("{:02X}".format(self.memory[i]))
            i += 1

    # 6xkk LD
    def load(self):
        print("{:03X}  {:02X}{:02X}  LD V{:01X} {:02X}".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte))
    # 7xkk ADD

    def add(self):
        print("{:03X}  {:02X}{:02X}  ADD V{:01X} {:02X}".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte))
    # 1nnn JMP

    def jump_address(self):
        print("{:03X}  {:02X}{:02X}  JMP {:01X}{:02X}".format(
            self.pc, self.code, self.next_byte, self.secondnib, self.next_byte))

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
        print("{:03X}  {:02X}{:02X}  LD V{:02}, DT".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def set_register_value_of_key(self):
        print("{:03X}  {:02X}{:02X}  LD V{:02}, K".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def load_delay_timer(self):
        print("{:03X}  {:02X}{:02X}  LD DT, V{:02}".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def load_sound_timer(self):
        print("{:03X}  {:02X}{:02X}  LD ST, V{:02}".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def add_i_and_register(self):
        print("{:03X}  {:02X}{:02X}  ADD I, V{:02}".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def load_f_in_register(self):
        print("{:03X}  {:02X}{:02X}  LD F, V{:02}".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def load_b_in_register(self):
        print("{:03X}  {:02X}{:02X}  LD B, V{:02}".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def store_in_memory(self):
        print("{:03X}  {:02X}{:02X}  LD [I], V{:02}".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def read_from_memory(self):
        print("{:03X}  {:02X}{:02X}  LD V{:02}, [I]".format(
            self.pc, self.code, self.next_byte, self.secondnib))


def main():

    chip8 = Chip8()

    chip8.load_file_to_memory()

if __name__ == "__main__":
    main()
