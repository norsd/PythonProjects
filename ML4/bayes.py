#coding:utf-8
__author__ = 'y'

from numpy import *

#返回2个数组
#1个含有6个子数组
#1个含有6个0或者1的长度为6的int[]
#其中0表示正常词汇
#其中1表示侮辱性词汇
def loadDataSet():
    postingList = [
        ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
        ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
        ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
        ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
        ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
        ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
        ]
    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec

#返回一维词汇表
#将string[][]中重复的过滤后转化为一个string[]
def createVocabList(arg_dataSet):
    vocabSet = set([])
    for document in arg_dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)


#返回int[],长度和vocabList一致,
#[i] = 0 表示 inputSet中没有vocabList[i]这个词汇没有出现过
#[i] = 1 表示 inputSet中没有vocabList[i]这个词汇出现过
def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print "the word: %s is not in my Vocabulary!" % word
    return returnVec


def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    p0Num = zeros(numWords)
    p1Num = zeros(numWords)
    p0Denom = 0.0
    p1Denom = 0.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = p1Num / p1Denom
    p0Vect = p0Num / p0Denom
    return p0Vect, p1Vect, pAbusive
