import matplotlib.pyplot as plt
import csv

stars = []

with open('exoTest.csv', newline='') as csvfile:
    exoplanetreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    cnt = 1
    for row in exoplanetreader:
        #skip row 1
        if(cnt == 1):
            cnt += 1
            continue
        
        planetDataStr = row[0]
        data = planetDataStr.split(',')
        for x in range(len(data)):
            point = float(data[x])
            data[x] = point

        if(data[0] == 2 and cnt <= 4):
            #cut out the '2' value, i.e., the classifier saying its an exoplanet
            #data = data[1:]
            stars.append(data)
            cnt += 1
        elif(data[0] == 1 and cnt > 4):
            #data = data[1:]
            stars.append(data)
            cnt += 1

        #three stars of with and no planet            
        if(cnt == 8):
            break
        
fig, ax = plt.subplots(6)

n = 0
for star in stars:
    #test: print(star[0])
    if(star[0] == 2.0):
        ax[n].plot(star[1:],'go',label="Confirmed Exoplanet")
        n+=1
    else:
        ax[n].plot(star[1:],'ro',label="No Exoplanet")
        n+=1
    
fig.show()
