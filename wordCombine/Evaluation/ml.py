
from GeoReader import load_json_file,get_ground_truth_list
from Geometry.DataModel import dataModel
from MinimumBoundingBox.MinimumBoundingBox import minimum_bounding_box
import pickle
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import svm
import matplotlib.pyplot as plt
import numpy as np




def same_phrase(gt1,gt2):
    if gt1.word == gt1.phrase:
        return 0
    if gt2.word == gt2.phrase:
        return 0
    if gt1.word == gt2.word :
        return 0
    if gt1.phrase == gt2.phrase:
        return 1

    return 0

def getTrainingData(gt_list):
    data = []
    data_x=[]
    data_y=[]
    total_link = 0
    for i in range(len(gt_list)):
        for j in range(i + 1, len(gt_list)):
            if same_phrase(gt_list[i],gt_list[j]):
                total_link+=1
            newModel = dataModel(gt_list[i],gt_list[j])
            data.append(newModel)
            arr=[newModel.capital,newModel.txtRatio,newModel.distance,newModel.sameWord]
            data_x.append(arr)
            data_y.append(newModel.samePhrase)

    return data,data_x,data_y,total_link

def write_to_file(filename,text):
    f = open(filename, 'a+')
    #for item in text:
    f.write(str(text))
        #f.write(" ")
    f.write("\n")
    f.close()




def create_model():

    groundTruthFile = '../usgs15_pa.geojson'

    result_obj = load_json_file(groundTruthFile)
    gt_list = get_ground_truth_list(result_obj)
    data, x_training, y_training,total = getTrainingData(gt_list)
    print "data mode len: %d x len: %d y len: %d" %(len(data),len(x_training),len(y_training))
    print  "data is loaded"


    # for i in range(0,30000):
    #     print "word1: %s word2: %s" % (data[i].gt1.word, data[i].gt2.word)
    #     print "phrase1: %s phrase2: %s" % (data[i].gt1.phrase, data[i].gt2.phrase)
    #     print x_training[i]
    #     write_to_file("usgs15_train.txt",x_training[i])
    #     print y_training[i]
    clf = svm.SVC(gamma=0.001, C=100.)
    clf.fit(x_training,y_training)
    print "create model"
    filename = 'finalized_model.sav'
    pickle.dump(clf, open(filename, 'wb'))
    print "save model"

def random_forest():
    groundTruthFile = '../usgs15_pa.geojson'
    attribute = ['captial','txtRatio','distance','sameWord']



    result_obj = load_json_file(groundTruthFile)
    gt_list = get_ground_truth_list(result_obj)
    data, x_training, y_training, total = getTrainingData(gt_list)
    print "data mode len: %d x len: %d y len: %d" %(len(data),len(x_training),len(y_training))
    print  "data is loaded"


    x_shape = len(x_training[0])

    #clf = svm.SVC(gamma=0.001, C=100.)

    clf =ExtraTreesClassifier(n_estimators=250,
                                  random_state=0)

    clf.fit(x_training, y_training)
    print "create model"
    filename = 'forest.sav'
    pickle.dump(clf, open(filename, 'wb'))
    print "save model"

    importances = clf.feature_importances_

    std = np.std([tree.feature_importances_ for tree in clf.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print("Feature ranking:")

    for f in range(len(x_training[0])):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

    # Plot the feature importances of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(x_shape), importances[indices],
            color="r", yerr=std[indices], align="center")
    plt.xticks(range(x_shape), indices)
    plt.xlim([-1, x_shape])
    plt.show()


def test_new_map(groundTruthName,resultFileName):
    print "test new map"
    #name  = "finalized_model.sav"
    name = "forest.sav"
    with open(name, 'rb') as f:
        clf = pickle.load(f)
    groundTruthFile = groundTruthName


    result_obj = load_json_file(groundTruthFile)
    gt_list = get_ground_truth_list(result_obj)
    data, x_training, y_training,total = getTrainingData(gt_list)

    predicted =clf.predict(x_training)
    #writefile = "USGS_for.txt"
    writefile =resultFileName



    print "predicted value is"
    print predicted

    f = open(writefile, 'w')
    for item in predicted:
        f.write(str(item)+"\t")
    f.close()
    print "save ans"


def get_evaluation(groundTruthName,resultFileName):

    print "begin evaluation"
    correct_link = 0
    detect_link = 0
    #total_link = 0

    result_obj = load_json_file(groundTruthName)
    gt_list = get_ground_truth_list(result_obj)
    data, x_training, y_training,total_link = getTrainingData(gt_list)

    with open(resultFileName, 'r') as f:
        arr = f.read().split("\t")
    for count, num in enumerate(arr):
        if num == '1':
            detect_link += 1
            print "word1: %s word2: %s" % (data[count].gt1.word, data[count].gt2.word)
            print "phrase1: %s phrase2: %s" % (data[count].gt1.phrase, data[count].gt2.phrase)
            if data[count].gt1.phrase == data[count].gt2.phrase:
                correct_link += 1
            else:
                print "!!!"

    print "correct: %d detect: %d total: %d" %(correct_link,detect_link,total_link)
    print "precision is: %f" % (float(correct_link) / detect_link)
    print "recall is: %f" % (float(correct_link) / total_link)


def get_value(filename):



    groundTruthFile = '../USGS.geojson'

    result_obj = load_json_file(groundTruthFile)
    gt_list = get_ground_truth_list(result_obj)
    data, x_training, y_training = getTrainingData(gt_list)

    with open(filename, 'r') as f:
        arr = f.read().split("\t")
        #print arr

    for count, num in enumerate(arr):
        if num == '1':
            print count
            print "word1: %s word2: %s" % (data[count].gt1.word, data[count].gt2.word)
            print "phrase1: %s phrase2: %s" % (data[count].gt1.phrase, data[count].gt2.phrase)



if __name__ == '__main__':
    points = ((1, 2), (5, 4), (-1, -3))
    bounding_box = minimum_bounding_box(points)  # returns namedtuple

    print bounding_box.area  # 16
    print bounding_box.rectangle_center  # (1.3411764705882352, 1.0647058823529414)
    print bounding_box.corner_points
    # groundTruthName = '../usgs-60-amboy-1943.geojson'
    # resultFileName = 'usgs-60-amboy-1943.txt'
    # create_model()
    #
    #
    # #random_forest()
    # test_new_map(groundTruthName,resultFileName)
    # get_evaluation(groundTruthName,resultFileName)



    #test_new_map()
    #filename = "ml.txt"

    # with open(filename, 'r') as myfile:
    #     ans=myfile.read().split("\t")
    #     #print ans






    # for i in range(0,100):
    #     print "word1: %s word2: %s" % (data[i].gt1.word, data[i].gt2.word)
    #     print "phrase1: %s phrase2: %s" % (data[i].gt1.phrase, data[i].gt2.phrase)
    #     print x_training[i]
    #     print y_training[i]

    # for i in range(0,len(d_1)):
    #     #print d_1[i]
    #     print "word1: %s word2: %s" % (d_1[i].gt1.word, d_1[i].gt2.word)
    #     print "phrase1: %s phrase2: %s" %(d_1[i].gt1.phrase, d_1[i].gt2.phrase)
    #     print ans[i]
        # if (d_1[i].gt1.phrase ==d_1[i].gt2.phrase and ans[i]==1):
        #     print "correct"
        # elif (d_1[i].gt1.phrase !=d_1[i].gt2.phrase and ans[i]==0):
        #     print "correct"
        # else:
        #     print "wrong"























