import pickle

__author__ = 'root'
import re
import glob
import os

import pymorphy2


morph = pymorphy2.MorphAnalyzer()
os.chdir("./dir")
termList, docLists = [], []
for file in glob.glob("*.txt"):
    fileone = open(file, 'r')
    for line in fileone:
        line = re.sub(r"[-./,:;><–#?!=\[\]()\'\"\&\\„”»«]", "", line)
        for word in line.split():
            term = morph.parse(word)[0].normal_form
            if term in termList:
                indexOfTerm = termList.index(term)

                docLists[indexOfTerm].add(file)
            else:
                termList.append(term)
                docLists.append({file, })

os.chdir("../")
# f = open('index.inv','wb')
# f.write()
l1 = list(zip(termList, docLists))
with open('index.inv', 'wb') as f:
    pickle.dump(l1, f)

print("The index successfully saved")
# f.close() # you can omit
# for i in range(len(termList)):
# print(i,termList[i], docLists[i], type(docLists[i]))

# print (fileone.read())
# print(file)

# print( morph.parse('автомобили')[0].normal_form)
