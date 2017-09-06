# -*- coding: utf-8 -*-
import MeCab
import sys
import os
import csv
from HTMLParser import HTMLParser

class TestParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = False

    def handle_starttag(self, tag, attrs):
        if tag == "span" or tag == "a" or tag == "td" or tag == "br":
            self.flag = True

    def handle_data(self, data):
        if self.flag:
            arrStr.append(data)
            self.flag = False

def getWords(node):
    words = []
    while node:
        word = node.surface.decode('utf-8')
        words.append(word)
        node = node.next
    return words

def getNouns(node):
    nouns = []
    while node:
        noun = node.feature.split(",")[0].decode('utf-8')
        nouns.append(noun)
        node = node.next
    return nouns

def findFiles(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)

def checkTxtStr(str):
    checkFlg = False
    if len(str) > 0 and '%%' not in str:
        checkFlg = True
    return str, checkFlg

def makeSingleWord(ustr, w, filename):
    mt = MeCab.Tagger('mecabrc')
    encoded_text = ustr.encode('utf-8')
    node = mt.parseToNode(encoded_text)
    words, nouns = getWords(node), getNouns(node)

    for (word, noun) in zip(words, nouns):
        if "記号" not in noun and word != "\"":
            if noun != "BOS/EOS":
                print(u"{0} : {1}".format(word, noun))
                w.write(u"{0}\t{1}".format(word, noun).encode('utf_8') + '\t' + filename + '\n')


if __name__ == '__main__':
    tgPath = sys.argv[1]
    w = open(sys.argv[2], 'w')
    header = 'word\tnoun\tfile\n'
    w.write(header)
    ampFlg = False
    arrStr = []

    for file in findFiles(tgPath):
        if str(file).find("html") > 0:
            f = open(file, 'r').read()
            parser = TestParser()
            parser.feed(f)
            parser.close()
            filename = os.path.basename(file)
            for word in arrStr:
                if '%%' not in word:
                    makeSingleWord(word, w, filename)
            arrStr = []
        elif str(file).find("txt") > 0:
            f = open(file, 'r')
            for line in f:
                check = True
                if '%%[' in line:
                    ampFlg = True
                if ']%%' in line:
                    ampFlg = False
                if ampFlg:
                    check = False
                else:
                    line, check = checkTxtStr(line)
                if check:
                    filename = os.path.basename(file)
                    makeSingleWord(line, w, filename)
            f.close()
        elif str(file).find("csv") > 0:
            reader = csv.reader(open(file,"rU"))
            for line in reader:
                filename = os.path.basename(file)
                makeSingleWord(line[0], w, filename)
    w.close()