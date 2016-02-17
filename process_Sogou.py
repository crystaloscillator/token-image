# -*- coding: utf-8 -*-

import os
import time
import jieba
from bs4 import BeautifulSoup as bs

from progressbar import ProgressBar

import codecs


Dir = "./sogou/SogouCAS"

sport_url = set()
finance_url = set()
ent_url = set()
auto_url = set()
tech_url  = set()

Dic = {'Ａ':'A','Ｂ':'B','Ｃ':'C','Ｄ':'D','Ｅ':'E','Ｆ':'F','Ｇ':'G','Ｈ':'H','Ｉ':'I','Ｊ':'J','Ｋ':'K','Ｌ':'L','Ｍ':'M','Ｎ':'N','Ｏ':'O','Ｐ':'P','Ｑ':'Q',\
'Ｒ':'R','Ｓ':'S','Ｔ':'T','Ｕ':'U','Ｖ':'V','Ｗ':'W','Ｘ':'X','Ｙ':'Y','Ｚ':'Z','ａ':'a','ｂ':'b','ｃ':'c','ｄ':'d','ｅ':'e','ｆ':'f','ｇ':'g','ｈ':'h','ｉ':'i','ｊ':'j',\
'ｋ':'k','ｌ':'l','ｍ':'m','ｎ':'n','ｏ':'o','ｐ':'p','ｑ':'q','ｒ':'r','ｓ':'s','ｔ':'t','ｕ':'u','ｖ':'v','ｗ':'w','ｘ':'x','ｙ':'y','ｚ':'z','１':'1','２':'2','３':'3',\
'４':'4','５':'5','６':'6','７':'7','８':'8','９':'9','０':'0','．':'.'}

dot = {'。','（','）','！','「','」','，','、','；','：','”','“','～',\
        '＜','＞','．','é','︶','『','』','﹗','ī','ō','／',"〔", '〕','｜',\
        "？","＠","｛","｝","￥","《","》",'…','【','】','︿','＃','＄','％','＆','＊','＋','⊙','［','］',\
       "［","］","—","·","－"}

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

def seg(content):

    content = j.text.encode('utf-8')
    content = replace_all(content,Dic)

    Cut=jieba.cut(''.join(content.split())) #斷詞
    li = []
    for u in Cut:
        if u.encode('utf-8') not in dot:  #清洗全形符號
            li.append(u) #沒在dot裡的就寫進陣列

    content = (' '.join(li)).encode('utf-8') #將陣列用空白格開, 傳回字串

    return content, len(li)


totfiles = len(os.listdir(Dir))
pbar = ProgressBar(maxval=totfiles).start()


cnt = 0
with open(Dir+'_Combine.txt',"w") as fid:

    for t, name in enumerate(os.listdir(Dir)): 
        time.sleep(0.01)
        pbar.update(t + 1)
        From = Dir + '/' + name
        with codecs.open(From, encoding='gbk', errors='ignore') as f:
            soup = bs(f.read(),"html.parser")
            for i, j in zip(soup.select('url'), soup.select('content')): 

                url_mention = i.text
                content = j.text

                if content == '' or url_mention == '':
                    continue

                if "http://sports." in url_mention and url_mention not in sport_url:
                    sport_url.add(url_mention)

                    content, seqlen = seg(content)

                    if seqlen > 30:
                        cnt += 1
                        fid.write("1" + "\t" + content.strip()+'\n')

                elif "http://ent." in url_mention and url_mention not in ent_url:
                    ent_url.add(url_mention)

                    content, seqlen = seg(content)

                    if seqlen > 30:
                        cnt += 1
                        fid.write("2" + "\t" + content.strip()+'\n')

                elif "http://auto." in url_mention and url_mention not in auto_url:
                    auto_url.add(url_mention)

                    content, seqlen = seg(content)

                    if seqlen > 30:
                        cnt += 1
                        fid.write("3" + "\t" + content.strip()+'\n')

                elif "http://finance." in url_mention and url_mention not in finance_url:
                    finance_url.add(url_mention)

                    content, seqlen = seg(content)

                    if seqlen > 30:
                        cnt += 1
                        fid.write("4" + "\t" + content.strip()+'\n')

                elif "http://tech." in url_mention and url_mention not in tech_url:
                    tech_url.add(url_mention)

                    content, seqlen = seg(content)
                    if seqlen > 30:
                        cnt += 1
                        fid.write("5" + "\t" + content.strip()+'\n')

pbar.finish()

print '\n---------------'
print 'Multiple_File_Combine_Ori-Len',"\t",cnt
print 'Final_Combine_File_Len',len([line for line in open(Dir+'_Combine.txt')])
print '---------------\n'

