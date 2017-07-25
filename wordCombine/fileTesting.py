#import sys
#print sys
#print(sys.path)
#from Geometry.GroundTruthPolygon import GroundTruthPolygon
#import Geometry
from Evaluation.GeoReader import load_json_file,get_ground_truth_list
from Geometry.DataModel import dataModel
from sklearn.naive_bayes import MultinomialNB
import sys


def getTrainingData(gt_list):
    data = []
    data_x=[]
    data_y=[]

    for i in range(len(gt_list)):
        for j in range(i + 1, len(gt_list)):
            newModel = dataModel(gt_list[i],gt_list[j])
            data.append(newModel)
            arr=[newModel.capital,newModel.txtRatio,newModel.distance,newModel.angle,newModel.sameWord]
            data_x.append(arr)
            data_y.append(newModel.samePhrase)

    return data,data_x,data_y





if __name__ == '__main__':
    groundTruthFile = '../USGS.geojson'

    result_obj = load_json_file(groundTruthFile)
    gt_list = get_ground_truth_list(result_obj)
    data, x_training, y_training = getTrainingData(gt_list)
    print "data mode len: %d x len: %d y len: %d" %(len(data),len(x_training),len(y_training))
    print  "data is loaded"
    clf = MultinomialNB().fit(x_training, y_training)



















