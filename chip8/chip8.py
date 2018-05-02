import os


class Chip8(object):

    def __init__(self):

        self.v0 = [0] * 8
        self.v1 = [0] * 8
        self.v2 = [0] * 8
        self.v3 = [0] * 8
        self.v4 = [0] * 8
        self.v5 = [0] * 8
        self.v6 = [0] * 8
        self.v7 = [0] * 8
        self.v8 = [0] * 8
        self.v9 = [0] * 8
        self.vA = [0] * 8
        self.vB = [0] * 8
        self.vC = [0] * 8
        self.vD = [0] * 8
        self.vE = [0] * 8
        self.vF = [0] * 8

        self.vI = [0] * 16

        self.delay_timer = [0] * 8
        self.sound_timer = [0] * 8

        self.pc = [0] * 16
        self.sp = [0] * 8

        self.SCREEN_SIZE = [32, 64]

        self.memory = [0] * 4096



    def bytes_from_file(self):
        with open("PONG", "rb") as f:
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
        i = 0
        while i < 200:
            self.memory[i] = int(self.memory[i], 16)
            print("{:02X}".format(self.memory[i]))
            i += 1

def main():

    chip8 = Chip8()

    chip8.load_file_to_memory()

if __name__ == "__main__":
    main()


