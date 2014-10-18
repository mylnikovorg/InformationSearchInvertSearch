import pickle
from functools import reduce
import sys
import re

import pymorphy2


morph = pymorphy2.MorphAnalyzer()

__author__ = 'Alex Mylnikov'
maxOutPutResult = 3
with open(sys.argv[1], 'rb') as f:
    termList = pickle.load(f)
    print("Index loaded...\nWe are ready for your query\nHint: For exit type 'exit'")


def get_documents_by_term(term):
    if morph.parse(term)[0].normal_form in termList:
        return termList[morph.parse(term)[0].normal_form]
    else:
        return dict()


def print_all_docs(docs):
    if len(docs) > 0:
        outStr = "found in "
        tmpSetLen = len(docs)
        if tmpSetLen > maxOutPutResult:
            count = 1
            for ii in docs:
                if count > maxOutPutResult:
                    break
                outStr += ii + " "
                count += 1
            outStr += "and " + str(tmpSetLen - maxOutPutResult) + " more"

        else:
            for ii in docs:
                outStr += ii + " "
        print(outStr)
    else:
        print("no documents found")


for i in sys.stdin:
    if i.strip() == 'exit':
        exit(0)
    # много /1 это /1 лучше
    inQuery = i.strip()
    if "/" in inQuery:

        for line in inQuery.split("/"):

            if len(line.strip().split()) > 1:
                word = line.strip().split()
                docs = get_documents_by_term(word[1])
                rast = word[0]
                temp_dict = dict()
                docs_that_can_be_usefull = middle_result.keys() & docs.keys()
                for this_doc in middle_result.keys() & docs.keys():
                    # print(this_doc + " - " + rast)
                    array_first = sorted(list(middle_result[this_doc]))
                    array_second = sorted(list(docs[this_doc]))
                    # print(array_first)
                    # print(array_second)

                    if "+" in word[0]:
                        temp_list = set(
                            [second for second in array_second for first in array_first if
                             abs(second - first) >= int(word[0][1])])
                        if len(temp_list) > 0:
                            temp_dict[this_doc] = temp_list
                    elif "-" in word[0]:

                        temp_list = set(
                            [second for second in array_second for first in array_first if
                             abs(second - first) <= int(word[0][1])])
                        if len(temp_list) > 0:
                            temp_dict[this_doc] = temp_list
                    else:
                        temp_list = set(
                            [second for second in array_second for first in array_first if
                             abs(second - first) == int(word[0])])
                        if len(temp_list) > 0:
                            temp_dict[this_doc] = temp_list

                middle_result = temp_dict;
            # if int(second) - int(first) == int(rast)
            else:
                middle_result = get_documents_by_term(line.strip())

        print_all_docs(middle_result.keys())
    else:

        if ("OR" in inQuery) or ("AND" in inQuery):
            if ("OR" in inQuery) and ("AND" in inQuery):
                print("incorrect query")
            else:
                if "OR" in inQuery:
                    inQuery = inQuery.replace("OR", "")
                    inQuery = re.sub(r'\s+', ' ', inQuery)
                    print_all_docs(reduce(lambda x, y: x | y,
                                          [get_documents_by_term(morph.parse(word)[0].normal_form).keys() for word in
                                           inQuery.split(" ")]))

                if "AND" in inQuery:
                    inQuery = inQuery.replace("AND", "")
                    inQuery = re.sub(r'\s+', ' ', inQuery)
                    print_all_docs(reduce(lambda x, y: x & y,
                                          [get_documents_by_term(morph.parse(word)[0].normal_form).keys() for word in
                                           inQuery.split(" ")]))




        else:
            print_all_docs(get_documents_by_term(morph.parse(inQuery)[0].normal_form))

