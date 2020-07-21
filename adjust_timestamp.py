import re
import numpy as np

def add_time(t, OFFSET):

    # Convert to ints
    t = [int(i) for i in t] 

    # Add milliseconds if present
    ms = OFFSET % 1
    ms *= 1000
    ms = int(np.round(ms))

    if ms > 0:
        t[3] += ms
        if t[3] >= 1000:
            t[2] += 1
            t[3] -= 1000

    # Add seconds
    s = int(np.floor(OFFSET))

    if s > 0:
        t[2] += s
        if t[2] >= 60:
            # Add to minutes
            t[1] += t[2] // 60
            t[2] = t[2] % 60

            # Add to hours
            if t[1] >= 60:
                t[0] += t[1] // 60
                t[1] = t[1] % 60

    string = '{0:02d}:{1:02d}:{2:02d}.{3:03d}'.format(t[0], t[1], t[2], t[3])

    # print(string)
    return string

def sub_time(t, OFFSET):

    # Convert to ints
    t = [int(i) for i in t] 

    # Add milliseconds if present
    ms = OFFSET % -1
    ms *= 1000
    ms = int(np.round(ms))

    if ms < 0:
        t[3] += ms
        if t[3] < 0:
            t[2] -= 1
            t[3] += 1000

    # Add seconds
    s = int(np.ceil(OFFSET))

    if s < 0:
        t[2] += s
        if t[2] < 0:
            # Add to minutes
            t[1] += t[2] // 60
            t[2] = (t[2] % 60)

            # Add to hours
            if t[1] < 0:
                t[0] += t[1] // 60
                t[1] = (t[1] % 60)

    string = '{0:02d}:{1:02d}:{2:02d}.{3:03d}'.format(t[0], t[1], t[2], t[3])

    # print(string)
    return string



def adjust_time(line, f, n, OFFSET): 
    pattern = '[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}'
    pattern_number = '[0-9]{2,3}'
    result = re.match(pattern, line)


    if result:
        times = re.findall(pattern_number, line)

        if OFFSET > 0:
            t1 = add_time(times[0:4], OFFSET)
            t2 = add_time(times[4:], OFFSET)
        else:
            t1 = sub_time(times[0:4], OFFSET)
            t2 = sub_time(times[4:], OFFSET)

        append = '{} --> {}\n'.format(t1, t2)
    else:
        append = line
    
    n.write(append)





# Specify the target of comversion
target = "./IR2/IR2_intro.vtt"

# Specify offset in seconds
OFFSET = -4.7


f = open(target)

save_target = target[0:-4] + '_new.vtt'
n = open(save_target, "x")

for line in f:
    adjust_time(line, f, n, OFFSET)

f.close()
n.close

# print(f.readline())

