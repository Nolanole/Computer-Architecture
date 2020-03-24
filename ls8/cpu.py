"""CPU functionality."""

import sys

LDI = 0b10000010 #Set the value of a register to an integer
PRN = 0b01000111 #Print numeric value stored in the given register
HLT = 0b00000001 #Halt the CPU (and exit the emulator)
MUL = 0b10100010 #Multiply the values in two registers together and store the result in registerA.

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.halt = False
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[MUL] = self.handle_MUL

    def handle_LDI(self, pc):
        operand_a = self.ram_read(pc+1)
        operand_b = self.ram_read(pc+2)
        self.reg[operand_a] = operand_b

    def handle_PRN(self, pc):
        operand_a = self.ram_read(pc+1)
        print(self.reg[operand_a])

    def handle_HLT(self, pc):
        self.halt = True

    def handle_MUL(self, pc):
        operand_a = self.ram_read(pc+1)
        operand_b = self.ram_read(pc+2)
        self.alu('MUL', operand_a, operand_b)
    
    def load(self):
        """Load a program into memory."""

        if len(sys.argv) != 2:
            print('Usage: cpu.py filename')
            sys.exit(1)

        filename = sys.argv[1]
        address = 0

        with open(filename) as f:
            for line in f:
                #ignore everything after the '#' and strip whitespace
                instruction = line.split('#')[0].strip()
                #ignore blank lines
                if instruction == '':
                    continue
                #convert string to int (base 2)
                val = int(instruction, 2)
                #store the value in memory (RAM)
                self.ram[address] = val
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
    
    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
        while not self.halt:
            ir = self.ram_read(self.pc) #Instruction Register
            #bitwise shift to grab the first 2 digits of the instruction
            num_operands = ir >> 6
            #access the branchtable to handle the instruction (function call)
            self.branchtable[ir](self.pc)
            #increment the pc
            self.pc += num_operands + 1