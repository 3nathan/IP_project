import subprocess

class Fpga():
    def __init__(self):
        self.pressedKeys = {
                'left': 0,
                'up': 0,
                'down': 0,
                'right':0,
                }

        self.n_terminal = subprocess.Popen(['nios2-terminal'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
        self.__cleanFpgaData()

    def __send(self):
        self.n_terminal.stdin.write(self.text + '\n')
        self.n_terminal.stdin.flush()

    def __cleanFpgaData(self):
        for i in range(4):
            print(self.n_terminal.stdout.readline().strip())

    def updateKeys(self):
        #get fpga list
        self.text = 's'
        self.__send()
        fpga = (self.n_terminal.stdout.readline().strip().split('<-->'))[1].strip().split('_')
        print(fpga)
        print('got message from fpga')
        fpga[0] = int(fpga[0])
        fpga[1] = int(fpga[1])
        if fpga[0] > 100 and fpga[1] < 30 and fpga[1] > -30:
            self.pressedKeys['left'] = 1
        elif fpga[1] < -100 and fpga[0] > -30 and fpga[0] > 30:
            self.pressedKeys['up'] = 1
        elif fpga[1] > 100 and fpga[0] < 30 and fpga[0] > -30:
            self.pressedKeys['down'] = 1
        elif fpga[0] < -100 and fpga[1] < 30 and fpga[1] > 30:
            self.pressedKeys['right'] = 1

    def resetKeys(self):
        self.pressedKeys = {
                'left': 0,
                'up': 0,
                'down': 0,
                'right':0,
                }

    def updateScore(self, score):
        score_string = str(score)
        char_score = (6 - len(score_string)) * '0' + score_string
        self.text = 'Update_score:_' + char_score
        self.__send()

    def exitNios(self):
        self.n_terminal.terminate()
        self.n_terminal.wait()
