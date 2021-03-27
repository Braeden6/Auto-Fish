import os
from PIL import Image
import numpy as np
from sklearn.neural_network import MLPClassifier
from joblib import dump, load

TOP_LEFT_X = 0.05078125
TOP_LEFT_Y = 0.76182
TOP_RIGHT_X = 0.058
TOP_RIGHT_Y = 0.7746

def prepImages():
    for filename in os.listdir("imagesForModel"):
        image = Image.open(os.getcwd() + "/imagesForModel/" + filename).convert("L")
        img = image.load()
        TOP_LEFT_X1 = int(TOP_LEFT_X*image.size[0])
        TOP_RIGHT_X1 = int(TOP_RIGHT_X*image.size[0])
        TOP_LEFT_Y1 = int(TOP_LEFT_Y*image.size[1])
        TOP_RIGHT_Y1 = int(TOP_RIGHT_Y*image.size[1])
        imgNew = Image.new("L", (TOP_RIGHT_X1-TOP_LEFT_X1,TOP_RIGHT_Y1-TOP_LEFT_Y1))
        imageNew = imgNew.load()
        for x in range(0, TOP_RIGHT_X1 - TOP_LEFT_X1):
            for y in range(0, TOP_RIGHT_Y1 - TOP_LEFT_Y1):
                imageNew[x,y] = img[(x + TOP_LEFT_X1), (y + TOP_LEFT_Y1)]
        imgNew = imgNew.resize((width,height), Image.ANTIALIAS)
        number = int(filename[:-4].split("_")[1])
        imgNew.save(os.getcwd() + "/TestingExample/" + str(NUMBER) + "_" + str(number) +".png")
        NUMBER += 1


if __name__ == '__main__':
    X = []
    y = []
    for filename in os.listdir(os.path.dirname(os.getcwd()) + "/TestingExample"):
        img = Image.open(os.path.dirname(os.getcwd()) + "/TestingExample/" + filename)
        img = np.asarray(img)
        X.append(img.flatten())
        ones = np.zeros(8)
        num = int(filename[:-4].split("_")[1])
        ones[num-1] = 1
        y.append(ones)
    X = np.array(X)/255
    Xtest = X[300:393]
    X = X[0:300]
    y = np.array(y)
    ytest = y[300:393]
    y = y[0:300]
    clf = MLPClassifier(solver='lbfgs', hidden_layer_sizes=(100,20,8), max_iter=1000)
    for i in range(20):
        clf.fit(X,y)
        y_pred = clf.predict_proba(Xtest)
        correct = 0
        for i in range(y_pred.shape[0]):
            if np.argmax(y_pred[i]) == np.argmax(ytest[i]):
                correct += 1
        if (correct/y_pred.shape[0] == 1):
            dump(clf,os.path.dirname(os.getcwd()) + "/model.joblib")
            print("saved model, ", correct/y_pred.shape[0])
            break

    #dump(clf,os.path.dirname(os.getcwd()) + "/model.joblib")
    # clf = load('model.joblib')
