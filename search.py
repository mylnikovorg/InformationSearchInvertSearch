import pickle
from sys import stdin

import pymorphy2


morph = pymorphy2.MorphAnalyzer()

__author__ = 'root'
maxOutPutResult = 2
with open("index.inv", 'rb') as f:
    my_list = pickle.load(f)

termList, docLists = [], []
for i in my_list:
    termList.append(i[0])
    docLists.append(i[1])
print("Index loaded...\nWe are ready for your query\nHint: For exit type 'exit'")

for i in stdin:
    if i.strip() == 'exit':
        exit(0)

    inQuery = i.strip()
    if ("OR" in inQuery) or ("AND" in inQuery):
        if ("OR" in inQuery) and ("AND" in inQuery):
            print("incorrect query")
        else:
            if "OR" in inQuery:
                inQuery = inQuery.replace("OR", "")
                tmpset = set()
                for iii in inQuery.split(" "):
                    iii = morph.parse(iii)[0].normal_form
                    if iii in termList:
                        tmpset = tmpset | docLists[termList.index(iii)]
                # print(a)
                if len(tmpset) > 0:
                    outStr = "found "
                    tmpSetLen = len(tmpset)
                    if tmpSetLen > maxOutPutResult:
                        count = 1
                        for ii in tmpset:
                            if count > maxOutPutResult:
                                break
                            outStr += ii + " "
                            count += 1
                        outStr += "and " + str(tmpSetLen - maxOutPutResult) + " more"

                    else:
                        for ii in tmpset:
                            outStr += ii + " "
                    print(outStr)
                else:
                    print("no documents found")

            if "AND" in inQuery:
                inQuery = inQuery.replace("AND", "")
                tmpset = set()
                flag = 1
                for iii in inQuery.split(" "):
                    iii = morph.parse(iii)[0].normal_form
                    if iii in termList:
                        if flag == 1:
                            tmpset = tmpset | docLists[termList.index(iii)]
                        else:
                            tmpset = tmpset & docLists[termList.index(iii)]
                    else:
                        tmpset = tmpset & set()
                # print(a)
                if len(tmpset) > 0:
                    outStr = "found "
                    tmpSetLen = len(tmpset)
                    if tmpSetLen > maxOutPutResult:
                        count = 1
                        for ii in tmpset:
                            if count > maxOutPutResult:
                                break
                            outStr += ii + " "
                            count += 1
                        outStr += "and " + str(tmpSetLen - maxOutPutResult) + " more"

                    else:
                        for ii in tmpset:
                            outStr += ii + " "
                    print(outStr)
                else:
                    print("no documents found")


    else:
        inQuery = morph.parse(inQuery)[0].normal_form
        if inQuery in termList:
            tmpset = docLists[termList.index(inQuery)]
            outStr = "found "
            tmpSetLen = len(tmpset)
            if tmpSetLen > maxOutPutResult:
                count = 1
                for ii in tmpset:
                    if count > maxOutPutResult:
                        break
                    outStr += ii + " "
                    count += 1
                outStr += "and " + str(tmpSetLen - maxOutPutResult) + " more"

            else:
                for ii in tmpset:
                    outStr += ii + " "
            print(outStr)
        else:
            print("no documents found")

