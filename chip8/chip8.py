import os
import msvcrt as m
import random
import pygame
from pygame.locals import *
from chip8screen import Chip8Screen


BLACK = [0,0,0]

class Chip8(object):

    def __init__(self, screen):

        self.general_registers = [0x00] * 16  # V0-VF

        self.vI = 0x00  # two bytes

        self.delay_timer = 0x00
        self.sound_timer = 0x00

        self.pc = 0x200  # two bytes
        self.sp = []

        self.file_size = 0

        self.SCREEN_SIZE = [320,160]

        self.memory = [0] * 4096

        self.firstnib = 0x00
        self.secondnib = 0x00
        self.next_byte = 0x00
        self.next_byte_firstnib = 0x00
        self.next_byte_secondnib = 0x00
        self.code = 0x00

        self.screen = screen


        ####KEYS####
        K_1 = 0x01
        K_2 = 0x02
        K_3 = 0x03
        K_4 = 0x0C
        K_q = 0x04
        K_w = 0x05
        K_e = 0x06
        K_r = 0x0D
        K_a = 0x07
        K_s = 0x08
        K_d = 0x09
        K_f = 0x0E
        K_z = 0x0A
        K_x = 0x00
        K_c = 0x0B
        K_v = 0x0F

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
            else:
                print("{:03X}  {:02X}{:02X}  UNKNOWN 0".format(
                    self.pc, self.code, self.next_byte))
                self.pc += 2
        elif self.firstnib == 0x1:
            self.jump_address()
        elif self.firstnib == 0x2:
            self.call_address()
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
            elif self.next_byte_secondnib == 0x1:
                self.logical_or()
            elif self.next_byte_secondnib == 0x2:
                self.logical_and()
            elif self.next_byte_secondnib == 0x3:
                self.logical_xor()
            elif self.next_byte_secondnib == 0x4:
                self.add_registers()
            elif self.next_byte_secondnib == 0x5:
                self.sub_registers_x_y()
            elif self.next_byte_secondnib == 0x6:
                self.shift_right()
            elif self.next_byte_secondnib == 0x7:
                self.sub_registers_y_x()
            elif self.next_byte_secondnib == 0xE:
                self.shift_left()
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
        self.sp.append(self.pc)
        print("{:03X}  CALL {:01X}{:02X}".format(
            self.pc, self.secondnib, self.next_byte))
        self.pc = int(hex((self.secondnib << 8) | self.next_byte), 16)

    def skip_if_reg_equal(self):
        print("{:03X}  SE V{:01X} {:02X}".format(
            self.pc, self.secondnib, self.next_byte))
        if self.general_registers[self.secondnib] == self.next_byte:
            self.pc += 4
        else:
            self.pc += 2

    def skip_if_not_equal(self):
        print("{:03X}  SNE V{:01X} {:02X}".format(
            self.pc, self.secondnib, self.next_byte))
        if self.general_registers[self.secondnib] != self.next_byte:
            self.pc += 4
        else:
            self.pc += 2

    def skip_if_equal(self):
        print("{:03X}  SE V{:01X} V{:01X}".format(
            self.pc, self.secondnib, self.next_byte_firstnib))
        if self.general_registers[self.secondnib] == self.general_registers[self.next_byte_firstnib]:
            self.pc += 4
        else:
            self.pc += 2

    def skip_next_instruction(self):
        print("{:03X}  SNE V{:01X} V{:01X}".format(
            self.pc, self.secondnib, self.next_byte_firstnib))
        if self.general_registers[self.secondnib] != self.general_registers[self.next_byte_firstnib]:
            self.pc += 4
        else:
            self.pc += 2

    def set_i(self):
        temp = int(hex((self.secondnib << 8) | self.next_byte), 16)
        self.vI = temp
        print("{:03X}  LD I {:01X}{:02X}".format(
            self.pc, self.secondnib, self.next_byte))

    def jump_with_offset(self):
        print("{:03X}  JMP V0 + {:01X}{:02X}".format(
            self.pc, self.secondnib, self.next_byte))
        temp = int(hex((self.secondnib << 8) | self.next_byte), 16)
        temp += self.general_registers[0x00]
        self.pc += temp

    def random_byte_plus_kk(self):
        print("{:03X}  RND V{:01X} AND {:02X}".format(
            self.pc, self.secondnib, self.next_byte))
        rand = random.randint(0x00, 0xFF)
        temp = rand & self.next_byte
        self.general_registers[self.secondnib] = temp
        self.pc += 2

    def draw_sprites(self):
        print("{:03X}  DRW V{:01X}, V{:01X},".format(
            self.pc, self.secondnib, self.next_byte_firstnib))
        x_pos = self.general_registers[self.secondnib]
        y_pos = self.general_registers[self.next_byte_firstnib]
        num_bytes = self.next_byte_secondnib
        self.general_registers[0x0F] = 0x00
        self.draw_normal(x_pos,y_pos,num_bytes)

    def draw_normal(self, x_pos, y_pos, num_bytes):
        for y_index in range(num_bytes):
            color_byte = bin(self.vI + y_index)
            color_byte = color_byte[2:].zfill(8)
            y_coord = y_pos + y_index
            y_coord = y_coord % self.screen.height

        for x_index in range(8):

            x_coord = x_pos + x_index
            x_coord = x_coord % self.screen.width

            color = int(color_byte[x_index])
            current_color = self.screen.get_pixel(x_coord, y_coord)

            if color == 1 and current_color == 1:
                self.general_registers[0x0F] = self.general_registers[0x0F] | 1
                color = 0

            elif color == 0 and current_color == 1:
                color = 1

            self.screen.draw_pixel(x_coord, y_coord, color)

        self.screen.update()

    def skip_next_on_key_press(self):
        print("{:03X}  SKP V{:01X}".format(
            self.pc, self.secondnib))
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
                    
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys == self.secondnib:
            self.pc += 4
        else: self.pc += 2

    def skip_next_on_not_key_press(self):
        print("{:03X}  SKNP V{:01X}".format(
            self.pc, self.secondnib))
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
                    
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys != self.secondnib:
            self.pc += 4
        else: self.pc += 2

    # 8xxx...
    def load_register_with_register(self):
        print("{:03X}  LD V{:01X} V{:01X}".format(
            self.pc, self.secondnib, self.next_byte_firstnib))
        self.general_registers[self.secondnib] = self.general_registers[self.next_byte_firstnib]
        self.pc += 2

    def logical_or(self):
        print("{:03X}  OR V{:01X} V{:01X}".format(
            self.pc, self.secondnib, self.next_byte_firstnib))
        temp = self.general_registers[self.secondnib] | self.general_registers[self.next_byte_firstnib]
        self.general_registers[self.secondnib] = temp
        self.pc += 2

    def logical_and(self):
        print("{:03X}  AND V{:01X} V{:01X}".format(
            self.pc, self.secondnib, self.next_byte_firstnib))
        temp = self.general_registers[self.secondnib] & self.general_registers[self.next_byte_firstnib]
        self.general_registers[self.secondnib] = temp
        self.pc += 2

    def logical_xor(self):
        print("{:03X}  XOR V{:01X} V{:01X}".format(
            self.pc, self.secondnib, self.next_byte_firstnib))
        temp = self.general_registers[self.secondnib] ^ self.general_registers[self.next_byte_firstnib]
        self.general_registers[self.secondnib] = temp
        self.pc += 2

    def add_registers(self):
        print("{:03X}  ADD V{:01X} V{:01X}".format(
            self.pc, self.secondnib, self.next_byte_firstnib))
        temp = self.general_registers[self.secondnib] + self.general_registers[self.next_byte_firstnib]
        if temp > 0xFF:
            self.general_registers[0x0F] = 0x01
            temp = temp - 256
        else: self.general_registers[0x0F] = 0x00
        self.general_registers[self.secondnib] = temp
        self.pc += 2

    def sub_registers_x_y(self):
        print("{:03X}  SUB V{:01X} V{:01X}".format(
            self.pc, self.secondnib, self.next_byte_firstnib))
        if self.general_registers[self.secondnib] > self.general_registers[self.next_byte_firstnib]:
            self.general_registers[0x0F] = 0x01
            temp = self.general_registers[self.secondnib] - self.general_registers[self.next_byte_firstnib]
            self.general_registers[self.secondnib] = temp
        else: 
            self.general_registers[0x0F] = 0x00
            temp = 256 + self.general_registers[self.secondnib] - self.general_registers[self.next_byte_firstnib]
            self.general_registers[self.secondnib] = temp

        self.pc += 2

    def shift_right(self):
        print("{:03X}  SHR V{:01X} 1".format(
            self.pc, self.secondnib))
        bit_zero = self.general_registers[self.secondnib] & 0x01
        self.general_registers[0x0F] = bit_zero

        self.general_registers[self.secondnib] = self.general_registers[self.secondnib] >> 1
        self.pc += 2

    def sub_registers_y_x(self):
        print("{:03X}  SUBN V{:01X} V{:01X}".format(
            self.pc, self.next_byte_firstnib, self.secondnib))
        if self.general_registers[self.next_byte_firstnib] > self.general_registers[self.secondnib]:
            self.general_registers[0x0F] = 0x01
            temp = self.general_registers[self.next_byte_firstnib] - self.general_registers[self.secondnib]
            self.general_registers[self.secondnib] = temp
        else: 
            self.general_registers[0x0F] = 0x00
            temp = 256 + self.general_registers[self.next_byte_firstnib] - self.general_registers[self.secondnib]
            self.general_registers[self.secondnib] = temp
        self.pc += 2

    def shift_left(self):
        print("{:03X}  SHL V{:01X} 1".format(
            self.pc, self.secondnib))
        bit_seven = (self.general_registers[self.secondnib] & 0x80) >> 8
        self.general_registers[0x0F] = bit_seven

        self.general_registers[self.secondnib] = self.general_registers[self.secondnib] << 1
        self.pc += 2

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
        self.pc = self.sp[-1]
        self.sp.pop()
        self.pc += 2

    # Fxxx....
    def set_register_delay_timer(self):
        print("{:03X}  LD V{:02X}, DT".format(
            self.pc, self.secondnib))
        self.general_registers[self.secondnib] = self.delay_timer

    def set_register_value_of_key(self):
        print("{:03X}  {:02X}{:02X}  LD V{:02X}, K".format(
            self.pc, self.code, self.next_byte, self.secondnib))

    def load_delay_timer(self):
        print("{:03X}  LD DT, V{:01X}".format(
            self.pc, self.secondnib))
        self.delay_timer = self.general_registers[self.secondnib]

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

    def timers(self):
        if self.delay_timer != 0x00:
            self.delay_timer -= 0x01
        if self.sound_timer != 0x00:
            self.sound_timer -= 0x01

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
        self.timers()


def wait():
    m.getch()


def main():

    TIMER = pygame.USEREVENT+1
    current_byte = 0
    next_byte = 0
    clock = pygame.time.Clock()
    pygame.init()
    screen = Chip8Screen(scale_factor=10)
    screen.init_display()
    chip8 = Chip8(screen)
    pygame.time.set_timer(TIMER,17)


    chip8.load_file_to_memory()
    running = True
    while running:
        pygame.time.wait(1)
        next_byte = chip8.memory[chip8.pc + 0x01]
        current_byte = chip8.memory[chip8.pc]
        chip8.disassembler(current_byte, next_byte)
        #wait()

        for event in pygame.event.get():
            if event.type == TIMER:
                chip8.timers()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_q]:
                    running = False
        if current_byte == 0xFD:
            running = False

if __name__ == "__main__":
    main()
