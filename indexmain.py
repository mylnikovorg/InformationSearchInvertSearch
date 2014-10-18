import pickle
import sys

__author__ = 'root'
import re
import glob
import os
import pymorphy2
import string

print('Argument List:', str(sys.argv[1]))

morph = pymorphy2.MorphAnalyzer()
os.chdir(sys.argv[1])
termList = dict()
for file in glob.glob("*.txt"):
    counter = 0
    fileone = open(file, 'r')
    for line in fileone:

        line = re.sub(
            r"[" + """!"#$%&'()*+,./:;<=>?@[\]^_`{|}~©«""" + string.ascii_letters + string.digits + "„”\\\\\ufeff]",
            " ",
            line)
        print(line)
        for word in line.split():
            term = morph.parse(word)[0].normal_form
            if term in termList:
                if file in termList[term]:
                    termList[term][file].add(counter)
                else:
                    termList[term][file] = {counter, }



            else:
                termList[term] = {str(file): {counter, }, }
            counter += 1

os.chdir("../")
# f = open('index.inv','wb')
# f.write()
print(termList)

# l1 = list(zip(termList, docLists))
with open(sys.argv[2], 'wb') as f:
    pickle.dump(termList, f)

print("The index successfully saved to file '" + sys.argv[2] + "'")
# f.close() # you can omit
# for i in range(len(termList)):
# print(i,termList[i], docLists[i], type(docLists[i]))

# print (fileone.read())
# print(l1)

# print( morph.parse('автомобили')[0].normal_form)
