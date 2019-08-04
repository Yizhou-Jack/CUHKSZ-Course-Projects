# Functions
# Use to predict label
def predict_label(instance,condi_prob_list,yilist):
    prob_list = []
    for i in range(len(condi_prob_list)):
        prob = 1
        for j in range(1,len(instance)):
            prob = prob*condi_prob_list[i][j-1][instance[j]-1]
        prob = prob*yilist[i]
        prob_list.append(prob)
    loc = prob_list.index(max(prob_list))
    return loc+1


# Pass parameters in command line
import os
import sys
nowcwd = os.getcwd()
train_data_name = sys.argv[1]
test_data_name = sys.argv[2]
train_data_path = nowcwd+'\\'+train_data_name
test_data_path = nowcwd+'\\'+test_data_name


# Create the train data set and test data set
train_data = []
test_data = []
with open(train_data_path) as f:
    for line in f.readlines():
        sub = line[:-1].split(' ')
        data = list(map(lambda x: int(x[len(x)-1]), sub))
        train_data.append(data)
with open(test_data_path) as f:
    for line in f.readlines():
        sub = line[:-1].split(' ')
        data = list(map(lambda x: int(x[len(x) - 1]), sub))
        test_data.append(data)


# The model's setting
t = 3


# Initialize weight list, big list and a list
import copy
weight_list = [1/len(train_data)]*len(train_data)
a_list = []
all_classifier_conditional_list = []
all_classifier_Yi_list = []

no2list = []
for j in range(1,len(train_data[0])):
    elementset = set()
    for instance in train_data:
        elementset.add(instance[j])
    no2list.append([0]*len(elementset))
no1list = []
no1elementset = set()
for instance in train_data:
    no1elementset.add(instance[0])
for i in range(len(no1elementset)):
    no1list.append(copy.deepcopy(no2list))


# Adaboost function
import math
def adaboost(t,no1list,weight_list,train_data,test_data):
    weightlist = weight_list
    classifier_result_list_train = []
    classifier_result_list_test = []
    a_list = []
    for number in range(t):
        # Calculate the conditional probability and Yi probability
        Yilist = []
        no1list_1 = copy.deepcopy(no1list)
        for i in range(len(no1list)):
            for j in range(1, len(no2list) + 1):
                for l in range(1, len(no2list[j - 1]) + 1):
                    countYi = 0
                    countAiYi = 0
                    for m in range(len(train_data)):
                        if train_data[m][0] == i + 1:
                            countYi += weightlist[m]
                            if train_data[m][j] == l:
                                countAiYi += weightlist[m]
                    no1list_1[i][j - 1][l - 1] = countAiYi / countYi
            Yilist.append(countYi)
        # Predict the label and store it into list
        pred_train_label_list = []
        pred_test_label_list = []
        for instance in train_data:
            pred_train_label = predict_label(instance, no1list_1, Yilist)
            pred_train_label_list.append(pred_train_label)
        for instance in test_data:
            pred_test_label = predict_label(instance, no1list_1, Yilist)
            pred_test_label_list.append(pred_test_label)
        classifier_result_list_train.append(pred_train_label_list)
        classifier_result_list_test.append(pred_test_label_list)
        # Calcualte the error
        e = 0
        for i in range(len(train_data)):
            if train_data[i][0] != pred_train_label_list[i]:
                e += weightlist[i]
        # Append a into a_list
        a = 0.5*math.log((1-e)/e)
        a_list.append(a)
        # Get the adapt weight
        for i in range(len(weightlist)):
            if train_data[i][0] != pred_train_label_list[i]:
                weightlist[i] *= math.exp(a)
            if train_data[i][0] == pred_train_label_list[i]:
                weightlist[i] *= math.exp(-1 * a)
        sum_weight = sum(weightlist)
        weightlist = list(map(lambda x: x / sum_weight, weightlist))
    return classifier_result_list_train, classifier_result_list_test, a_list


# Get the result of adaboost
crltrain, crltest, al = adaboost(t,no1list,weight_list,train_data,test_data)


# Combine the weak classifier to strong classifier
bigset_train = []
bigset_test = []
for i in range(len(train_data)):
    lendata = len(train_data[0])
    bigset_train.append([0]*lendata)
    bigset_test.append([0]*lendata)
for i in range(len(crltrain)):
    for j in range(len(crltrain[i])):
        bigset_train[j][crltrain[i][j]-1] += al[i]
for i in range(len(crltest)):
    for j in range(len(crltest[i])):
        bigset_test[j][crltest[i][j]-1] += al[i]
final_result_train = []
final_result_test = []
for prob in bigset_train:
    loc = prob.index(max(prob))
    final_result_train.append(loc+1)
for prob in bigset_test:
    loc = prob.index(max(prob))
    final_result_test.append(loc+1)


# Construct the confusion matrix
# Test
confu_matrix = []
for i in range(len(no1list)):
    confu_matrix.append([0]*len(no1list))
for i in range(len(test_data)):
    confu_matrix[test_data[i][0]-1][final_result_test[i]-1] += 1
print('Test Dataset Confusion Matrix:')
for i in confu_matrix:
    for j in i:
        print(j,end='\t')
    print('\n')
# Train
#confu_matrix = []
#for i in range(len(no1list)):
#    confu_matrix.append([0]*len(no1list))
#for i in range(len(train_data)):
#    confu_matrix[train_data[i][0]-1][final_result_train[i]-1] += 1
#print('Train Dataset Confusion Matrix:')
#for i in confu_matrix:
#    for j in i:
#        print(j,end='\t')
#    print('\n')