import os
import textdist
from tokenize import tokenize
from io import BytesIO
from Components.CheckError import alignment


class checkError:
    def __init__(self):
        self.parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        self.dataSetFile = os.listdir(self.parentDir + "/Data/CodeDataset")
        self.keywordFile = os.listdir(self.parentDir + "/Data/Python_Words")
        self.text = ""
        self.line = 0

    def run(self,text,line):
        return self.parse(text,line)

    def parse(self, text,line):
        self.line = line
        errorLine = text[line].replace("\n", "")
        return self.kNN(errorLine)

    def kNN(self, errorLine):
        returnData = []
        for i in range(len(self.dataSetFile)):
            with open(self.parentDir + "/Data/CodeDataset/" + self.dataSetFile[i], "r",errors="ignore") as f:
                if i == 0:
                    data = f.readlines()
                else:
                    data += f.readlines()

        errorDataRAW = self.token(errorLine)
        errorData = self.is_user_string(errorDataRAW)
        OriginalStrings = list(set(errorDataRAW) - set(errorData))

        for replace_str in OriginalStrings:
            errorLine = errorLine.replace(replace_str, "_STR_")

        distance = []
        for i in data:
            distance.append(textdist.ratcliff_obershelp.distance(i, errorLine))
        _, data = zip(*sorted(zip(distance, data),reverse=False))

        knnList = []
        knnReturnList = []
        for i in range(5):
            try:
                nData = data[i].replace("\n", "").strip()
                knnReturnList.append(nData)
                tokens = self.token(nData)
                knnList.append(tokens)
            except:
                break

        returnData.append(knnReturnList.copy())
        valListDict = {}

        maxVal = -100
        selectedList = []
        errorList = []
        for i in knnList:
            aln = alignment.needle(errorData, i)
            identity = aln[0]
            score = aln[1]
            if score * identity > maxVal:  # maxVal:
                maxVal = score * identity
                selectedList = aln[3]
                errorList = aln[2]

            if len(aln[2]) not in valListDict.keys():
                valListDict[len(aln[2])] = [aln[2], [aln[3]], [score]]
            else:
                valListDict[len(aln[2])][1].append(aln[3])
                valListDict[len(aln[2])][2].append(score)

        token_ciktisi = self.is_user_defined(selectedList, errorList)
        token_ciktisi = ['{}' if i == '_STR_' else i for i in token_ciktisi]
        returnData.append(self.strTrueData(token_ciktisi).format(*OriginalStrings))
        return returnData

    def is_user_defined(self, alg, err):
        data = []
        nData = []
        for i in range(len(self.keywordFile)):
            with open(self.parentDir + "/Data/Python_Words/" + self.keywordFile[i], "r",
                      errors="ignore") as f:
                if i == 0:
                    data = f.read().splitlines()
                else:
                    data += f.read().splitlines()

        for i in range(len(alg)):
            if alg[i] not in data:
                nData.append(err[i])
            else:
                nData.append(alg[i])
        return nData

    def is_user_string(self, dataList):
        nData = []
        for i in range(len(self.keywordFile)):
            with open(self.parentDir + "/Data/Python_Words/" + self.keywordFile[i], "r",
                      errors="ignore") as f:
                if i == 0:
                    data = f.read().splitlines()
                else:
                    data += f.read().splitlines()
        for i in range(len(dataList)):
            if dataList[i] not in data:
                try:
                    if dataList[i - 1] == '"':
                        nData.append("_STR_")
                    elif dataList[i + 1] == '"':
                        nData.append("_STR_")
                    else:
                        nData.append(dataList[i])
                except:
                    nData.append(dataList[i])
            else:
                nData.append(dataList[i])
        return nData

    def checkBalance(self, expression):
        #hatalı satırdaki parantez sayısı dengeli değilse tokenizer çöküyor.
        #dengeli değilse dengeyi bulamayacağımız için bütün parantezleri sil.
        open_tup = tuple('({[')
        close_tup = tuple(')}]')
        paranthesis = ['(','[','{','}',']',')']
        map = dict(zip(open_tup, close_tup))
        queue = []
      
        for i in expression:
            if i in open_tup:
                queue.append(map[i])
            elif i in close_tup:
                if not queue or i != queue.pop():
                    for p in paranthesis:
                        expression=expression.replace(p,' ')
                    return expression
        if not queue:
            return expression
        else:
            for p in paranthesis:
                expression=expression.replace(p,' ')
            return expression

    def token(self, data):
        tokenarray = []
        data=self.checkBalance(data) # parantez sayısını kontrol et.
        g = tokenize(BytesIO(data.encode('utf-8')).readline)
        for token in g:
            if token.string != '' and token.string != "\n":
                if token.string[0] == '"' and token.string[-1] == '"' and len(token.string) > 2:
                    tokenarray.append('"')
                    tokenarray.append(token.string[1:-1])
                    tokenarray.append('"')
                else:
                    tokenarray.append(token.string)
        return tokenarray[1:]

    def strTrueData(self, errorData):
        trueData = ""
        for i in errorData:
            if i == "(" or i == ")":
                try:
                    if trueData[-1] != '"':
                        trueData = trueData[:-1] + i
                    else:
                        trueData += i
                except:
                    trueData += i
            elif i == "\t" or i == "\n":
                trueData += i
            elif i[-1] == "\n" or i[-1] == "\t":
                trueData += i
            elif i == "-":
                pass
            elif i[-1] == '"':
                if trueData[-1] == " ":
                    trueData = trueData[:-1] + i
                else:
                    trueData += i
            else:
                trueData += i + " "
        return trueData


a = checkError()
