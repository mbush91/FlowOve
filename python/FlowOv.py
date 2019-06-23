import json

PROFILES = '../html/profiles/profiles.json'

pf = open(PROFILES, 'r')

profiles = json.load(pf)

x = 1

def make_csv(fname, time, temp) :
    out = ""

    for i in range(len(time)) :
        out += "%s,%s\n"%(str(time[i]),str(temp[i]))    

    f = open(fname,'w')
    f.write(out)
    f.close()

def build_tempProfile(profile, frequency = 1) :
    times = profile['time']
    tempC = profile['tempC']

    num_points = len(times)
    idx = 0

    otime = []
    otemp = []

    while idx < (num_points-1) :
        y1 = tempC[idx]
        y2 = tempC[idx + 1]
        x1 = times[idx]
        x2 = times[idx + 1]

        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1

        t = x1 
        while t < x2 :
            otime.append(t)
            otemp.append(m*t+b)
            t += 1 / frequency
        idx += 1

    return otime, otemp


time,temp = build_tempProfile(profiles['Standard'],2)

make_csv('test.csv',time,temp)

pass