
import subprocess
import time

n_terminal = subprocess.Popen(['nios2-terminal'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)

for i in range(4):
    output = n_terminal.stdout.readline().strip()
    print(output)

def send(text):
    n_terminal.stdin.write(text + '\n')
    n_terminal.stdin.flush()

def get_last():
    last_line = ''
    while True:
        line = n_terminal.stdout.readline().strip()
        print(line)
        if line:
            last_line = line
        else:
            break
    print(last_line)
    return last_line

def receive_tilt():
    tilt = send("send_tilt") # Tilt will be xtilt_ytilt
    tilt = tilt.split('_') # This should be a list made of both tilts
    return tilt

def send_score(score):
    score_string = str(score)
    print(score_string)
    char_score = (6 - len(score_string)) * '0' + score_string
    print(char_score)
    send('Upaate_score:\ ' + char_score)

# start = time.time()
for i in range(20):
    send('s')
    time.sleep(0.1)

for i in range(20):
    fpga = n_terminal.stdout.readline().strip()
#end = time.time()
#print(end - start)

send("Update_score:_696521")
time.sleep(0.101)

#output = []
#for i in range(20):
#    nostrip = n_terminal.stdout.readline()
#    output.append(nostrip.strip())
#    print(output[i])
#print(output)

#last_line = ''
#while True:
#    line = n_terminal.stdout.readline().strip()
#   print(line)
#    if line:
#        last_line = line
#    else:
#        break

# get_last()

n_terminal.terminate()
n_terminal.wait()

print("End")

