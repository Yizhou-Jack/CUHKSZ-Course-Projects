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


# Create initial list
import copy
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


# Calculate all of the conditional probability
Yilist = []
for i in range(len(no1list)):
    for j in range(1,len(no2list)+1):
        for l in range(1,len(no2list[j-1])+1):
            countYi = 0
            countAiYi = 0
            for instance in train_data:
                if instance[0] == i+1:
                    countYi += 1
                    if instance[j] == l:
                        countAiYi += 1
            no1list[i][j-1][l-1] = countAiYi/countYi
    Yilist.append(countYi/len(train_data))


# Predict train data set's label and test data set's label
pred_train_label_list = []
pred_test_label_list = []
for instance in train_data:
    pred_train_label = predict_label(instance,no1list,Yilist)
    pred_train_label_list.append(pred_train_label)
for instance in test_data:
    pred_test_label = predict_label(instance,no1list,Yilist)
    pred_test_label_list.append(pred_test_label)


# Compare the true label with pred label and then produce the confusion matrix
confu_matrix = []
for i in range(len(no1list)):
    confu_matrix.append([0] * len(no1list))
for i in range(len(test_data)):
    confu_matrix[test_data[i][0] - 1][pred_test_label_list[i] - 1] += 1
print('Test Dataset Confusion Matrix:')
for i in confu_matrix:
    for j in i:
        print(j, end='\t')
    print('\n')
#confu_matrix = []
#for i in range(len(no1list)):
#    confu_matrix.append([0]*len(no1list))
#for i in range(len(train_data)):
#    confu_matrix[train_data[i][0]-1][pred_train_label_list[i]-1] += 1
#print('Train Dataset Confusion Matrix:')
#for i in confu_matrix:
#    for j in i:
#        print(j,end='\t')
#    print('\n')