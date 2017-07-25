

from Geometry.GroundTruthPolygon import GroundTruthPolygon



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

class dataModel():

    def __init__(self,gt1,gt2):
        self.gt1 = gt1
        self.gt2 = gt2
        self.capital = gt1.same_captial(gt2)
        self.txtRatio = min(gt1.get_area_per_letter()/gt2.get_area_per_letter(),gt2.get_area_per_letter()/gt1.get_area_per_letter())
        self.distance = gt1.calculate_polygon_distabce(gt2)
        self.angle = min(abs(gt1.find_orientation(gt2) - 180), gt1.find_orientation(gt2))
        self.sameWord = (gt1.word == gt2.word)
        self.samePhrase = same_phrase(gt1,gt2)



    def get_word1(self):
        return self.gt1

    def get_word2(self):
        return self.gt2