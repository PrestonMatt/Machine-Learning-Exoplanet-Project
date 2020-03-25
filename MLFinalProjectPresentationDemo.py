#mostly copying code from the OG files, and showing a test:
import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from imblearn.over_sampling import SMOTE
#from get_and_format_data import get, getall
#import csv
#from sklearn.metrics import accuracy_score, confusion_matrix

########################################################################################

#pulled straight out of the model:
def getTrainData():
    train_stars = []
    with open('exoTrain.csv', newline='') as csvfile:
        exoplanetreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        cnt = 1
        for star in exoplanetreader:
            #skip row 1
            if(cnt == 1):
                cnt += 1
                continue
            
            planetDataStr = star[0]
            data = planetDataStr.split(',')
            for x in range(len(data)):
                point = float(data[x])
                data[x] = point
            train_stars.append(data)

    X = train_stars
    Y = []
    for i in range(len(train_stars)):
        star2 = train_stars[i]
        if(star2[0]==2.0): # exoplanet
            Y.append(1)
        elif(star2[0]==1.0): # no exoplanet
            Y.append(-1)
        train_stars[i] = star2[1:]

    return (X,Y)

def SMOTE_data(X_train,Y_train):
    sm = SMOTE(random_state = 42)
    X_res,Y_res = sm.fit_resample(X_train,Y_train)
    return (X_res,Y_res)

########################################################################################

X_train,Y_train = getTrainData()
X_test = []
Y_test = []

print("Data reaped.")

fig, ax = plt.subplots(6)

z = 0
removal_indeces = []
for n in range(len(X_train)):
    if(Y_train[n] == 1 and z < 3):
        print("Graph #" + str(z) + " is classified as " + str(Y_train[n]) + " confirmed exoplanet.")
        greenline = ax[z].plot(X_train[n],'go',label="Confirmed Exoplanet")
        X_test.append(X_train[n])
        #X_train.remove(X_train[n])
        Y_test.append(Y_train[n])
        #Y_train.remove(Y_train[n])
        removal_indeces.append(n)
        z += 1
    elif(Y_train[n] == -1 and z >= 3):
        print("Graph #" + str(z) + " is classified as " + str(Y_train[n]) + " no exoplanet.")
        redline = ax[z].plot(X_train[n],'ro',label="No Exoplanet")
        X_test.append(X_train[n])
        #X_train.remove(X_train[n])
        Y_test.append(Y_train[n])
        #Y_train.remove(Y_train[n])
        removal_indeces.append(n)
        z += 1

    if(z == 6):
        break
#fig.legend(labels=["Confirmed Exoplanet","No Exoplanet"])
#ax[0].legend("Confirmed Exoplanet")
ax[3].set_ylabel("flux value")
#ax[5].legend("No Exoplanet")
ax[5].set_xlabel("Time: incriments of 30 min")
#for q in range(len(ax)):
    #ax[q].set_title("Sample Star #" + str(q))
    #ax[q].set_xlabel('flux value')
    #ax[q].set_ylabel('Time (in incriments of 30 min)')
fig.suptitle("Plots of Stars\' flux value over time")
#fig.legend(greenline[0],redline[0],["Confirmed Exoplanet","No Exoplanet"],title="Class")
fig.align_labels()
#fig.add_axes("Time (in incriments of 30 min)","flux value")
fig.show()

#remove the test data I took from the training data set
for star_index in removal_indeces:
    #print("Removing star at index " + str(star_index))
    X_train.remove(X_train[star_index])
    Y_train.remove(Y_train[star_index])

print("Graph done.")


########################################################################################

#pulled straight out of the model:
try:
    print("Starting Fourier transform.")
    for i in range(len(X_train)):
        list = X_train[i]
        new_list = np.abs(np.fft.fft(list)).tolist()
#       scaling = StandardScaler()
#       new_list = scaling.fit_transform(new_list)
        X_train[i] = new_list
    for i in range(len(X_test)):
        list = X_test[i]
        new_list = np.abs(np.fft.fft(list)).tolist()
#       scaling = StandardScaler()
#       new_list = scaling.fit_transform(new_list)
        X_test[i] = new_list
        
    print("FFT finished. Starting scaling")
    scaling = StandardScaler()
    X_train = scaling.fit_transform(X_train)
    X_test = scaling.transform(X_test)
    print("Scaling done. Starting SMOTE")

    X_train,Y_train = SMOTE_data(X_train,Y_train)
    print("SMOTE done. Starting testing")

    clf = LinearSVC()
    clf.fit(X_train,Y_train)
    
    Y_predict = clf.predict(X_test)
    m = 0
    for prediction in Y_predict:
        print("The model thinks that graph #" + str(m) + " is " + str(prediction))
        m += 1
    #print("Accuracy: " + str(clf.accuracy_score(Y_test, Y_predict)))
    #print("Confusion matrix: " + str(confusion_matrix(Y_test, Y_predict)))

except KeyboardInterrupt:
    print("Program stopped by keyboard")

