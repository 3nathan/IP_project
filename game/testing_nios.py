
import subprocess
import time
import select

n_terminal = subprocess.Popen(['nios2-terminal'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)

for i in range(4):
    output = n_terminal.stdout.readline().strip()
    print(output)

def send(text):
    n_terminal.stdin.write(text + '\n')
    n_terminal.stdin.flush()

# This function needs to be used in conjuction with the values being sent from the terminal constantly.
def get_last():
    last_line = ''
    while True:
        ready, _, _ = select.select([n_terminal.stdout], [], [], 0.1)
        if ready:    
            line = n_terminal.stdout.readline().strip()
            # print(line)
            if line:
                last_line = line
        else:
            break
    return last_line

def receive_tilt():
    send("s") # Tilt will be xtilt_ytilt
    tilt = n_terminal.stdout.readline().strip()
    tilt.split('_') # This should be a list made of both tilts
    return tilt

def send_score(score):
    score_string = str(score)
    char_score = (6 - len(score_string)) * '0' + score_string
    send('Update_score:\ ' + char_score)

# start = time.time()
# send('s')


send('a')
output = n_terminal.stdout.readline()
print(output.strip())

send('g')
send('l')
time.sleep(1)
print(get_last())
time.sleep(0.1)

send('s')
# end = time.time()
for i in range(50):
    print(get_last())
    time.sleep(0.05)


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

