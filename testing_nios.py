
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

start = time.time()
for i in range(20):
    send('s')



for i in range(20):
    line = n_terminal.stdout.readline().strip()
end = time.time()
print(end - start)

send('Update_score:_696969')

#for i in range(20):
#    time.sleep(0.1)

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

