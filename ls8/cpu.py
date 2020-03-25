"""CPU functionality."""

import sys

ADD = 0b10100000 
AND = 0b10101000 
CALL = 0b01010000 
CMP = 0b10100111 
DEC = 0b01100110 
DIV = 0b10100011 
HLT = 0b00000001 
INC = 0b01100101 
INT = 0b01010010 
IRET = 0b00010011 
JEQ  = 0b01010101 
JGE = 0b01011010 
JGT = 0b01010111 
JLE = 0b01011001 
JLT = 0b01011000 
JMP = 0b01010100 
JNE = 0b01010110 
LD = 0b10000011 
LDI = 0b10000010 
MOD = 0b10100100 
MUL = 0b10100010 
NOP = 0b00000000 
NOT = 0b01101001 
OR = 0b10101010 
POP = 0b01000110 
PRA = 0b01001000 
PRN = 0b01000111 
PUSH = 0b01000101 
RET = 0b00010001 
SHL = 0b10101100
SHR = 0b10101101
ST = 0b10000100
SUB = 0b10100001
XOR = 0b10101011

SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[SP] = 0xF4
        self.halt = False
        self.flag = 0b00000000 #8bit flag 00000LGE
        self.branchtable = {}
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[AND] = self.handle_AND
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[DEC] = self.handle_DEC
        self.branchtable[DIV] = self.handle_DIV
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[INC] = self.handle_INC
        self.branchtable[INT] = self.handle_INT
        self.branchtable[IRET] = self.handle_IRET
        self.branchtable[JEQ] = self.handle_JEQ
        self.branchtable[JGE] = self.handle_JGE
        self.branchtable[JGT] = self.handle_JGT
        self.branchtable[JLE] = self.handle_JLE
        self.branchtable[JLT] = self.handle_JLT
        self.branchtable[JMP] = self.handle_JMP
        self.branchtable[JNE] = self.handle_JNE
        self.branchtable[LD] = self.handle_LD
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[MOD] = self.handle_MOD
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[NOP] = self.handle_NOP
        self.branchtable[NOT] = self.handle_NOT
        self.branchtable[OR] = self.handle_OR
        self.branchtable[POP] = self.handle_POP
        self.branchtable[PRA] = self.handle_PRA
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[RET] = self.handle_RET
        self.branchtable[SHL] = self.handle_SHL
        self.branchtable[SHR] = self.handle_SHR
        self.branchtable[ST] = self.handle_ST
        self.branchtable[SUB] = self.handle_SUB
        self.branchtable[XOR] = self.handle_XOR

    # def print_stuff(self):
    #     '''Debugging helper funct'''
    #     print(f'pc: {self.pc}')
    #     print(f'Registers: {self.reg}')
    #     print(f'RAM: {self.ram}\n')

    def get_operands(self, pc, num_operands=2):
        if num_operands == 1:
            return self.ram_read(pc+1)
        elif num_operands == 2:
            return self.ram_read(pc+1), self.ram_read(pc+2)
        else:
            print('Error: Number of operands must be 1 or 2')
            self.halt = True
    
    def handle_ADD(self, pc):
        '''Add the value in two registers and store the result in registerA.'''
        operand_a, operand_b = self.get_operands(pc)
        self.alu('ADD', operand_a, operand_b)

    def handle_AND(self, pc):
        '''Bitwise-AND the values in registerA and registerB, then store the result in registerA.'''
        operand_a, operand_b = self.get_operands(pc)
        #ALU instruction
        self.alu('AND', operand_a, operand_b)
    
    def handle_CALL(self, pc):
        '''Calls a subroutine (function) at the address stored in the register.'''
        #Decrement the SP
        self.reg[SP] -= 1

        #The address of the instruction directly after CALL is pushed onto the stack. 
        #This allows us to return to where we left off when the subroutine finishes executing.
        self.ram[self.reg[SP]] = pc + 2

        #The PC is set to the address stored in the given register. 
        #We jump to that location in RAM and execute the first instruction in the subroutine. 
        #The PC can move forward or backwards from its current location.
        reg_num = self.get_operands(pc, 1)
        self.pc = self.reg[reg_num]

    def handle_CMP(self, pc):
        '''Compare the values in two registers.'''
        operand_a, operand_b = self.get_operands(pc)
        #ALU instruction
        self.alu('CMP', operand_a, operand_b)
    
    def handle_DEC(self, pc):
        '''Decrement (subtract 1 from) the value in the given register.'''
        reg_num = self.get_operands(pc, 1)
        self.alu('DEC', reg_num, reg_num)
    
    def handle_DIV(self, pc):
        '''Divide the value in the first register by the value in the second, storing the result in registerA.'''
        operand_a, operand_b = self.get_operands(pc)
        #If the value in the second register is 0, the system should print an error message and halt.
        if operand_b == 0:
            print('Error, cannot divide by zero!')
            self.halt = True
        else:
            #ALU instruction
            self.alu('DIV', operand_a, operand_b)
    
    def handle_HLT(self, pc):
        '''Halt the CPU (and exit the emulator).'''
        self.halt = True
    
    def handle_INC(self, pc):
        '''Increment (add 1 to) the value in the given register.'''
        reg_num = self.get_operands(pc, 1)
        self.alu('INC', reg_num, reg_num)

    def handle_INT(self, pc):
        '''Issue the interrupt number stored in the given register.'''
        #This will set the _n_th bit in the IS register to the value in the given register.
        pass

    def handle_IRET(self, pc):
        #Registers R6-R0 are popped off the stack in that order.
        #The FL register is popped off the stack.
        #The return address is popped off the stack and stored in PC.
        #Interrupts are re-enabled
        pass

    def handle_JEQ(self, pc):
        '''If equal flag is set (true), jump to the address stored in the given register.'''
        pass

    def handle_JGE(self, pc):
        '''If greater-than flag or equal flag is set (true), jump to the address stored in the given register.'''
        pass

    def handle_JGT(self, pc):
        '''If greater-than flag is set (true), jump to the address stored in the given register.'''
        pass

    def handle_JLE(self, pc):
        '''If less-than flag or equal flag is set (true), jump to the address stored in the given register.'''
        pass

    def handle_JLT(self, pc):
        '''If less-than flag is set (true), jump to the address stored in the given register.'''
        pass

    def handle_JMP(self, pc):
        '''Jump to the address stored in the given register'''
        #Set the PC to the address stored in the given register.
        reg_num = self.get_operands(pc, 1)
        self.pc = self.reg[reg_num]

    def handle_JNE(self):
        '''If E flag is clear (false, 0), jump to the address stored in the given register.'''
        pass
    
    def handle_LD(self, pc):
        '''Loads registerA with the value at the memory address stored in registerB.'''
        #This opcode reads from memory.
        pass

    def handle_LDI(self, pc):
        '''Set the value of a register to an integer.'''
        operand_a, operand_b = self.get_operands(pc)
        self.reg[operand_a] = operand_b

    def handle_MOD(self, pc):
        '''Divide the value in the first register by the value in the second, storing the remainder of the result in registerA.'''
        operand_a, operand_b = self.get_operands(pc)
        #If the value in the second register is 0, the system should print an error message and halt.
        if operand_b == 0:
            print('Error, cannot divide by zero!')
            self.halt = True
        else:
            #ALU instruction
            self.alu('MOD', operand_a, operand_b)

    def handle_MUL(self, pc):
        '''Multiply the values in two registers together and store the result in registerA.'''
        operand_a, operand_b = self.get_operands(pc)
        #ALU instruction
        self.alu('MUL', operand_a, operand_b)
    
    def handle_NOP(self, pc):
        '''No operation. Do nothing for this instruction.'''
        pass

    def handle_NOT(self, pc):
        '''Perform a bitwise-NOT on the value in a register, storing the result in the register.'''
        operand_a = self.get_operands(pc, 1)
        #ALU instruction:
        self.alu('NOT', operand_a, operand_a)

    def handle_OR(self, pc):
        '''Perform a bitwise-OR between the values in registerA and registerB, storing the result in registerA.'''
        operand_a, operand_b = self.get_operands(pc)
        #ALU instruction
        self.alu('OR', operand_a, operand_b)

    def handle_POP(self, pc):
        '''Pop the value at the top of the stack into the given register'''
        #Copy the value from the address pointed to by SP to the given register
        val = self.ram_read(self.reg[SP])
        reg_num = self.ram_read(pc+1)
        #save the value into the register argument:
        self.reg[reg_num] = val
        #Increment SP
        self.reg[SP] += 1
    
    def handle_PRA(self, pc):
        '''PRA register pseudo-instruction
        Print alpha character value stored in the given register.'''
        #Print to the console the ASCII character corresponding to the value in the register.   
        pass

    def handle_PRN(self, pc):
        '''Print numeric value stored in the given register.'''
        #Print to the console the decimal integer value that is stored in the given register.
        operand_a = self.get_operands(pc, 1)
        print(self.reg[operand_a])

    def handle_PUSH(self, pc):
        '''Push the value in the given register on the stack'''
        #Decrement the SP
        self.reg[SP] -= 1
        #Grab the value stored at the register argument
        reg_num = self.get_operands(pc, 1)
        val = self.reg[reg_num]
        #Copy the value in the given register to the address pointed to by SP
        self.ram_write(self.reg[SP], val)

    def handle_RET(self, pc):
        '''Return from subroutine.'''
        #Pop the value from the top of the stack and store it in the PC.
        self.pc = self.ram_read(self.reg[SP])

        #increment the SP
        self.reg[SP] += 1

    def handle_SHL(self, pc):
        '''Shift the value in registerA left by the number of bits specified in registerB, filling the low bits with 0.'''
        operand_a, operand_b = self.get_operands(pc)
        #ALU
        self.alu('SHL', operand_a, operand_b)

    def handle_SHR(self, pc):
        '''Shift the value in registerA right by the number of bits specified in registerB, filling the high bits with 0.'''
        operand_a, operand_b = self.get_operands(pc)
        #ALU
        self.alu('SHR', operand_a, operand_b)

    def handle_ST(self, pc):
        '''Store value in registerB in the address stored in registerA.'''
        #This opcode writes to memory.
        pass

    def handle_SUB(self, pc):
        '''Subtract the value in the second register from the first, storing the result in registerA.'''
        operand_a, operand_b = self.get_operands(pc)
        #ALU instruction
        self.alu('SUB', operand_a, operand_b)

    def handle_XOR(self, pc):
        '''Perform a bitwise-XOR between the values in registerA and registerB, storing the result in registerA.'''
        operand_a, operand_b = self.get_operands(pc)
        #ALU
        self.alu('XOR', operand_a, operand_b)

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
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'AND':
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == 'CMP':
            '''Compare the values in two registers'''
            #If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
            #If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
            #If they are equal, set the Equal E flag to 1, otherwise set it to 0.
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
        elif op == 'DEC':
            self.reg[reg_a] -= 1
        elif op == 'DIV':
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == 'INC':
            self.reg[reg_a] += 1
        elif op == 'MOD':
            self.reg[reg_a] %= self.reg[reg_b]
        elif op == 'NOT':
            #HELP
            pass
        elif op == 'OR':
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == 'SHL':
            self.reg[reg_a] <<= self.reg[reg_b]
        elif op == 'SHR':
            self.reg[reg_a] >>= self.reg[reg_b]
        elif op == 'XOR':
            self.reg[reg_a] ^= self.reg[reg_b]
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
            #Instruction Register
            ir = self.ram_read(self.pc)
            #bitwise shift to grab the first 2 digits of the instruction
            num_operands = ir >> 6
            #access the branchtable to handle the instruction (function call)
            self.branchtable[ir](self.pc)
            #if pc set directly, dont increment the pc(grab the 4th digit of the instruction):
            if (ir & 0b00010000) >> 4 == 0:
                #increment the pc
                self.pc += num_operands + 1