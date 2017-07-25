# -*- coding: utf-8 -*-

# from Evaluation.database import connect_db

#from GroundTruthPolygon import GroundTruthPolygon
#import operator
#import itertools
#from operator import itemgetter
import json, math, sys
sys.path.append("/Users/haowenlin/PycharmProjects/wordCombine/Geometry/GeoPolygon.py")
from Geometry.GroundTruthPolygon import GroundTruthPolygon
import itertools
import numpy as np
#import sys
#from Operation.SpecialFormat import single_word


def load_json_file(filename):
    plain_text = open(filename).read()

    # Make the plain text can be recognized by the json module.
    plain_text = plain_text.replace(',}', '}')
    plain_text = plain_text.replace(',]', ']')
    plain_text = plain_text.replace('}]}]}', '}]}')
    plain_text = " ".join(plain_text.split("\n"))
    plain_text = plain_text.replace("\\", "")

    # print ("text " + plain_text)
    data = json.loads(plain_text)
    return data


def get_ground_truth_list(gt_obj):
    gt_list = []
    # txt = ""
    # loc = ""
    # phrase=""
    for count, feature in enumerate(gt_obj['features']):

            # new_gt_rect = GroundTruthPolygon(count, feature['properties']['txt_loc'],
            #                                  feature['properties']['txt'],
            #                                  feature['properties']['phrase'], feature['geometry']['coordinates'][0])



        new_gt_rect = GroundTruthPolygon(count, feature['properties']['txt_loc'],
                                             feature['properties']['txt'],
                                             feature['properties']['phrase'], feature['geometry']['coordinates'][0])

        gt_list.append(new_gt_rect)

    print "this file totaly has %d polygons\n" % (len(gt_list))

    return gt_list


# get all unique word phrases text in one shapfile
def get_all_phrases(gt_obj):
    word_list = set()

    for feature in gt_obj['features']:
        word_list.add(feature['properties']['Text'].lower())

    print len(word_list)
    file = open("phrases.txt", "w")

    for word in word_list:
        file.write(word)
        file.write("\n")

    file.close()


def process_letter_size(gt_list):
    gt_dictionary = {}

    for gt in gt_list:
        key = gt.phrase
        if key not in gt_dictionary:
            gt_dictionary[key] = []
        gt_dictionary[key].append(gt)

    max_word_pairs = []

    for key in gt_dictionary:
        gt_arr = gt_dictionary[key]
        print 'Key: {} Numer: "{}!"'.format(key, len(gt_arr))
        max_diff = 0.0
        max1 = gt_arr[0]
        max2 = gt_arr[0]

        for gt1, gt2 in itertools.combinations(gt_arr, 2):
            gt1_area = gt1.get_area_per_letter()
            gt2_area = gt2.get_area_per_letter()
            if max_diff < abs(gt1_area - gt2_area):
                max_diff = abs(gt1_area - gt2_area)
                max1 = gt1
                max2 = gt2
        cur_tuple = (max1, max2, max_diff)
        if max1 != max2:
            print max1.word + " " + max2.word + " " + str(max1.get_area_per_letter()) + " " + str(
                max2.get_area_per_letter()) + " " + str(max_diff)
        max_word_pairs.append(cur_tuple)



        # print 'Word1:{} Word2: {} Size: {} Diff:{}'.format(gt1.word, gt2.word, gt1.get_area_per_letter(), abs(gt1.get_area_per_letter() - gt2.get_area_per_letter()))
        # for pair in max_word_pairs:

        # print 'Word1:{} Word2: {} Size: {} Diff:{}'.format(pair[0].word, pair[1].word, pair[0].get_area_per_letter(), pair[3])


def filter_function(gt_list):
    filtered_list = []
    for gt in gt_list:
        # if "." in gt.word:
        # continue
        filtered_list.append(gt)
    return filtered_list


def get_gold_data_phrases(fname):
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    return content


def get_nearest_neighboar(gt_list):
    for i in range(0, len(gt_list), 1):
        for j in range(i + 1, len(gt_list), 1):
            num = gt_list[i].calculate_polygon_distabce(gt_list[j])
            tuple1 = (num, gt_list[j])
            tuple2 = (num, gt_list[i])
            gt_list[i].test.append(tuple1)
            gt_list[j].test.append(tuple2)

        gt_list[i].test.sort(key=lambda tup: tup[0])
    return gt_list







def get_associated_polygon(gt_list):
    for gt in gt_list:
        if gt.word == gt.phrase:
            continue
        if gt.degree == 0:
            continue
        potential_array = itertools.islice(gt.test, 2)  # 10
        for candidate in potential_array:
            letter_size = max(candidate[1].get_area_per_letter() / gt.get_area_per_letter(),
                              gt.get_area_per_letter() / candidate[1].get_area_per_letter())
            if letter_size < 1.5 and gt.word != candidate[1].word:  # 1.8
                if gt.same_captial(candidate[1]) and candidate[1].degree != 0:
                    if candidate[0] < min(gt.find_longest_line().length,
                                          candidate[1].find_longest_line().length) * 0.5:  # 5
                        if (gt.find_orientation(candidate[1]) < 20 or abs(
                                    gt.find_orientation(candidate[1]) - 180) < 20):
                            if gt.word != candidate[1].word:
                                gt.associated_polygon.append(candidate[1])

    return gt_list


def print_difference(list1, list2):
    for i in range(1, len(list1), 1):
        if len(list1[i].associated_polygon) == len(list2[i].associated_polygon):
            continue
        print "the word is:%s" % list1[i].word
        # print diff(list1[i].associated_polygon,list2[i].associated_polygon)
        print diff(list2[i].associated_polygon, list1[i].associated_polygon)


def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


def get_correct_position(word, text):
    if text.endswith(word) or text.startswith(word):
        return 1
    elif word == text:
        return 0
    else:
        return 2

    print "get_correct_position error %s:%s :%d" % (word, text, flag)

    return -10000


def check_nearby_word(gt_word, associated_word, text):
    arr = text.split()
    gt_index = 0
    associated_index = 0
    for count, content in enumerate(arr):
        if content == gt_word:
            gt_index = count
        if content == associated_word:
            associated_index = count
    # print gt_index,associated_index
    if abs(gt_index - associated_index) == 1:
        return True
    else:
        return False


def append_link_word():
    for gt in gt_list:
        # print "word: %s" % gt.word
        for wordPolygon in gt.associated_polygon:
            # print wordPolygon.word
            if gt in wordPolygon.associated_polygon and (gt not in wordPolygon.linkedWord):
                # print "1 "
                if not gt.finalized() and not wordPolygon.finalized():
                    # print "2"
                    gt.add_linked_word(wordPolygon)
                    wordPolygon.add_linked_word(gt)
    count = 0
    for gt in gt_list:
        print "word: %s phrase: %s" % (gt.word, gt.phrase)
        for polygon in gt.linkedWord:
            print polygon.word
            count += 1
            if polygon.word not in gt.phrase:
                print "!!!!"
    print "count is: %d" % (count)


def get_cost(gt_list, matrix):
    my_matrix =matrix
    for gt in gt_list:
        #print gt.id
        #associated_array = gt.test

        for count, candidate in enumerate(gt.test):
            my_matrix[gt.id][gt.id] += 1000
            if my_matrix[gt.id][candidate[1].id] == 0:
                letter_size = max(candidate[1].get_area_per_letter() / gt.get_area_per_letter(),
                                  gt.get_area_per_letter() / candidate[1].get_area_per_letter())
                angle = min(abs(gt.find_orientation(candidate[1]) - 180), gt.find_orientation(candidate[1]))
                my_matrix[gt.id][candidate[1].id] += letter_size * 5
                my_matrix[candidate[1].id][gt.id] += letter_size * 5

                my_matrix[gt.id][candidate[1].id] += angle
                my_matrix[candidate[1].id][gt.id] += angle

                if not gt.same_captial(candidate[1]):
                    my_matrix[gt.id][candidate[1].id] += 1000
                    my_matrix[candidate[1].id][gt.id] += 1000

                if gt.word == candidate[1].word:
                    my_matrix[gt.id][candidate[1].id] += 1000
                    my_matrix[candidate[1].id][gt.id] += 1000
            my_matrix[gt.id][candidate[1].id] += count
            #print my_matrix[gt.id][candidate[1].id]
            #print my_matrix[candidate[1].id][gt.id]
            #print "\n"

    print_matrix(my_matrix)

    return my_matrix


def print_matrix(matrix):
    # for i in range(len(matrix)):
    #     for j in range(5):
    #         print matrix[i][j]

    for i in range(0, len(matrix[0]), 1):
        print "word: %s  phrase: %s" % (gt_list[i].word, gt_list[i].phrase)

        ans =np.argsort(matrix[i])[:5]
        for word in ans:
            print "cost: %d word: %s" % (matrix[i][word], gt_list[word].word)
        print "\n"


def evaluation_result(gt_list):
    detected_polygon = 0
    correct_polygon = 0
    detected_correct = 0

    detected_polygon_linked = 0
    correct_polygon_linked = 0
    detected_correct_linked = 0
    wrong_ans = 0
    wrong_ans_linked = 0

    for gt in gt_list:
        print "the word is:%s   and the phrase is:  %s id is:%d" % (gt.word, gt.phrase, gt.id)
        if gt.word == gt.phrase:
            correct_polygon += 0
            correct_polygon_linked += 0
        else:
            correct_polygon += len(gt.phrase.split(" ")) - 1
            correct_polygon_linked += get_correct_position(gt.word, gt.phrase)
        # print correct_polygon_linked

        detected_polygon += len(gt.associated_polygon)
        detected_polygon_linked += len(gt.associated_polygon)
        # manual_check = 0
        for polygon in gt.associated_polygon:

            if polygon.phrase == gt.phrase:
                detected_correct += 1
                # manual_check+=1
                if check_nearby_word(gt.word, polygon.word, gt.phrase):
                    detected_correct_linked += 1
                    print polygon.word + "     cc"
                else:
                    print polygon.word + "     c"
                    wrong_ans_linked += 1

            else:
                print polygon.word
                wrong_ans += 1
                wrong_ans_linked += 1
        # if gt.word!= gt.phrase and manual_check !=len(gt.phrase.split(" "))-1:
        #    print "!!!"


        print "wrong ans: %d   wrong linked: %d correct %d" % (wrong_ans, wrong_ans_linked, detected_correct)
        #
        # print detected_correct, detected_polygon, correct_polygon
        print "\n"
    print "precision is: %f" % (float(detected_correct) / detected_polygon)
    print "recall is: %f" % (float(detected_correct) / correct_polygon)
    print detected_correct_linked, detected_polygon_linked, correct_polygon_linked
    print "wrong ans:%d wrong_link:%d correct %d" % (wrong_ans, wrong_ans_linked, detected_correct)
    print "precision_linked is: %f" % (float(detected_correct_linked) / detected_polygon_linked)
    print "recall_linked is: %f" % (float(detected_correct_linked) / correct_polygon_linked)


if __name__ == '__main__':
    # groundTruthFile = sys.argv[1]
    # groundTruthFile = '../USGS.geojson'
    groundTruthFile = '../USGS.geojson'

    result_obj = load_json_file(groundTruthFile)
    gt_list = get_ground_truth_list(result_obj)

    # myset = set()
    # f = open('testfile.txt', 'w')
    # for gt in gt_list:
    #
    #     if not filter_coordinates(gt.phrase):
    #         print filter_coordinates(gt.phrase)
    #         word = gt.phrase
    #
    #         myset.add(word)
    #     #f.write(word+'\n')
    #
    # for item in myset:
    #     #if not filter_coordinates(item):
    #     print item
    #     f.write(item + ' ')
    # f.close()


    gt_list = get_nearest_neighboar(gt_list)
    # list1= get_associated_polygon(gt_list)

    # evaluation_result(list1)
    # append_link_word()

    length = len(gt_list)
    w, h = length, length;
    matrix = [[0 for x in range(w)] for y in range(h)]
    matrix = get_cost(gt_list, matrix)
    #print_matrix(matrix)


    # count = 0
    # c2=0
    # for gt in gt_list:
    #     index = 0
    #     index2=0
    #     gt.test.sort(key=lambda tup: tup[0])
    #     print "The word:  %s  The phrase: %s" % (gt.word,gt.phrase)
    #
    #     top = itertools.islice(gt.test, 10)
    #     for tuple in top:
    #         #print tuple[1].word + " "
    #         if tuple[1].phrase == gt.phrase:
    #             index+=1
    #         letter_size = max(tuple[1].get_area_per_letter()/gt.get_area_per_letter(),gt.get_area_per_letter()/tuple[1].get_area_per_letter())
    #         #print "the letter size is : %s" %(letter_size)
    #         if letter_size < 1.8:
    #             if gt.same_captial(tuple[1]) and tuple[0]<gt.find_longest_line().length*2:
    #             #if (gt.find_orientation(tuple[1])<15 or abs(gt.find_orientation(tuple[1])-180)<15) :
    #             #print tuple[1].word + " "+str(gt.find_orientation(tuple[1]))+"? "+str(abs(gt.find_orientation(tuple[1])-180))+"    "
    #                 print tuple[1].word
    #                 if tuple[1].phrase == gt.phrase:
    #                     index2 += 1
    #
    #     if index != len(gt.phrase.split())-1 and (len(gt.word.split())==1):
    #         #print "index: %d  word len: %d" %(index,len(gt.phrase.split())-1)
    #         print "not matching: %s  %s" %(gt.word,gt.phrase)
    #         count+=1
    #
    #     if index == len(gt.phrase.split())-1 and index2 != len(gt.phrase.split())-1 and (len(gt.word.split())==1):
    #         #print "index: %d  word len: %d" %(index,len(gt.phrase.split())-1)
    #         #print "letter size: %s  %s" %(gt.word,gt.phrase)
    #         c2 += 1
    #
    #     print "\n"
    #
    # print count
    # print c2

    # sorted_gt_list  =sorted(gt_list, key=lambda gt:gt.get_center_location())

















    # phrase_set=set()
    # phrase_dic={}
    # for index,gt in enumerate(sorted_gt_list):
    #     print gt.word +": " +gt.phrase +":  "+str(gt.get_center_location())
    #     if gt.phrase not in phrase_set:
    #         phrase_dic[gt.phrase]=index
    #         #print gt.word+" " +str(index)
    #     phrase_set.add(gt.phrase)
    #
    # num=0
    # for element in phrase_set:
    #     count =0;
    #     loc = phrase_dic[element]
    #     if sorted_gt_list[loc].word == sorted_gt_list[loc].phrase:
    #         continue
    #     i= loc
    #     while i< loc+30:
    #         if i< len(sorted_gt_list) and sorted_gt_list[i].phrase == element :
    #             count+=1
    #             loc =i
    #         i+=1
    #     if count < len(element.split()):
    #         print element
    #         num+=1
    #
    # print num
    # get_all_phrases(result_obj)



# soda spring TWO soda spring
