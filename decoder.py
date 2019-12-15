
import json
import re
import random


def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring


def strB2Q(ustring):
    """半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:  # 半角空格直接转化
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:  # 半角字符（除空格）根据关系转化
            inside_code += 65248
        rstring += chr(inside_code)
    return rstring


signal1="<[\s\S]*?herf=\""
signal2="\">[\s\S]*?<[\s\S]*?>"


fTranlate="translated.txt"
fDecode="result.txt"
fReplace="replace.json"

repMap=json.load(open(fReplace,"r"))
text=open(fTranlate,"r",encoding='UTF-8').read()
text=strQ2B(text)

text=re.sub("<font[\s\S]*?>","",text)
text=re.sub("</font>","",text)
text=re.sub("<html[\s\S]*?>","",text)
text=re.sub("</html>","",text)
text=re.sub("<body[\s\S]*?>","",text)
text=re.sub("</body>","",text)
text=re.sub("<div[\s\S]*?>","",text)
text=re.sub("</div>","",text)
ret=re.search(signal1+r"(.*?)"+signal2,text, re.IGNORECASE)
while ret!=None:
    key=ret.group(1)
    string=ret.group()
    print(key)
    if key in repMap:
        text=text.replace(string,repMap[key]["ori"])
    else:
        text=text.replace(string,"DECODE ERROR")
        print("ERROR")
    ret=re.search(signal1+r"(.*?)"+signal2,text, re.IGNORECASE)

text=text.replace("{ ","{")
text=text.replace(" }","}")
text=text.replace("\\ ","\\")

f=open(fDecode, "w",encoding='UTF-8')
f.write(text)
f.close()