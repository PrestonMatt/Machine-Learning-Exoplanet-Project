from get_and_format_data import get, getall
import csv
from sklearn.svm import LinearSVC
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix
from collections import Counter
import time
from imblearn.over_sampling import SMOTE
import numpy as np

#opens CSV file and just inputs it for the
#~5000 training data points, each with ~4000 points themselves
# each feature is a light reading with evenly spaced timestamps
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

#opens CSV file and just inputs it for the
#~500 testing data points, each with ~4000 points themselves
def getTestData():
    test_stars = []
    with open('exoTest.csv', newline='') as csvfile:
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

            test_stars.append(data)

    X = test_stars
    Y = []
    for i in range(len(test_stars)):
        star2 = test_stars[i]
        if(star2[0]==2.0):
            Y.append(1)
        elif(star2[0]==1.0):
            Y.append(-1)
        test_stars[i] = star2[1:]

    return (X,Y)

#given a dataset of X (Y not needed), n (granulation constant)
#returns subdataset granulated such that
#every nth data point is removed
def granulate_data(X,n):
    new_X = []
    discarded = []
    for indexNum in range(len(X)):
        if(indexNum % n == 0):
            discarded.append(X[indexNum])
        else:
            new_X.append(X[indexNum])
    return (new_X,discarded)

def granulate_specifically(X):
    X = granulate_data(X,5)[1] #[1] ==> every discarded, i.e. 50th point

    #for each point in the training, make it less finely grained data, taking every other item:
    for i in range(len(X)):
        X[i] = granulate_data(X[i],2)[0]

    return X

def print_arr(X):
    for x in X:
        print(str(x))

def SMOTE_data(X_train,Y_train):
    sm = SMOTE(random_state = 42)
    X_res,Y_res = sm.fit_resample(X_train,Y_train)
    return (X_res,Y_res)

def main_func():
    try:
        X_train,Y_train = getTrainData()
        X_test,Y_test = getTestData()
        #X_test,Y_test = getall()

        print("Data reaped. Starting granulation.")

        #X_train = granulate_specifically(X_train)
        #X_test = granulate_specifically(X_test)
        print("Number of training samples: " + str(len(X_train)))
        print("Number of testing samples: " + str(len(X_test)))
        print("Number of points per sample in training data: " + str(len(X_train[0])))
        print("Number of points per sample in testing data: " + str(len(X_test[0])))

        #Y_train = granulate_data(Y_train,5)[1]
        #Y_test = granulate_data(Y_test,5)[1]
        print("Number of training answers: " + str(len(Y_train)))
        print("Number of testing answers: " + str(len(Y_test)))

        print("Starting Fourier transform.")
        for i in range(len(X_train)):
            list = X_train[i]
            new_list = np.abs(np.fft.fft(list)).tolist()
#            scaling = StandardScaler()
#            new_list = scaling.fit_transform(new_list)
            X_train[i] = new_list
        for i in range(len(X_test)):
            list = X_test[i]
            new_list = np.abs(np.fft.fft(list)).tolist()
#            scaling = StandardScaler()
#            new_list = scaling.fit_transform(new_list)
            X_test[i] = new_list
        
        print("FFT finished. Starting scaling")
        #for speed:
        #scaling1 = MinMaxScaler(feature_range=(-1,1)).fit(X_train)
        scaling = StandardScaler()
        X_train = scaling.fit_transform(X_train)
        X_test = scaling.transform(X_test)
        print("Scaling done. Starting SMOTE")

        X_train,Y_train = SMOTE_data(X_train,Y_train)
        print("SMOTE done. Starting testing")

        clf = LinearSVC()
        clf.fit(X_train,Y_train)

        print("\n")
        #print(X_test)
        #print("printed")
        #print(Y_test)
        #print(X_train)
        #print(Y_train)
        #print("Accuracy: " + str(clf.score(X_test,Y_test)))
        Y_predict = clf.predict(X_test)
        print("Accuracy: " + str(accuracy_score(Y_test, Y_predict)))
        print("Confusion matrix: " + str(confusion_matrix(Y_test, Y_predict)))

    except KeyboardInterrupt:
        print("Program stopped by keyboard")
        #print(timer.cancel())
        return

time1 = time.gmtime()
main_func()
time2 = time.gmtime()

time_hr1 = (int(time1.tm_hour)*3600)
time_hr2 = (int(time2.tm_hour)*3600)

time_min1 = (int(time1.tm_min)*60)
time_min2 = (int(time2.tm_min)*60)

time_sec1 = (int(time1.tm_sec))
time_sec2 = (int(time2.tm_sec))

time_total_1 = time_hr1 + time_min1 + time_sec1
time_total_2 = time_hr2 + time_min2 + time_sec2

total_time = str(time_total_2 - time_total_1)
             
print("Runtime of program: " + total_time + " sec.")
