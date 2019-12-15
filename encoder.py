
import json
import re
import random

signal1="<a herf=\""
signal2="\">lyp</a>"

environments=["abstract","aligned","myLemm","myTheo","myDef","myCoro","tabular"]
commands=["\\begin{","\\end{","\\section{","\\end{","\\subsection{","\\subsubsection{","\\par",
         "\\indent ","\\hfill","\\textbf{","\\_","\\caption{","\\item "]

def generate_random_str(randomlength=10):
    random_str = signal1
    base_str = '奥历史对此怕收到下求内粗'
    length = len(base_str) - 1
    key=""
    for i in range(randomlength):
        key+=base_str[random.randint(0, length)]
        
    random_str += key+ signal2
    return key,random_str


fInput= "paper.tex"
fOutput= "encoded.html"
fReplace= "replace.json"


repMap={}

f=open(fInput, "r",encoding='UTF-8')
text=f.read()
f.close()
text="<html><body>"+text+"</body></html>"
"""
Remove Comments
"""
ret=re.search(r"([^\\])%(.*?)\n",text)
while ret!=None:
    text=re.sub(r"([^\\])%(.*?)\n",r"\1",text)
    ret = re.search(r"([^\\])%(.*?)\n", text)


"""
Handle \par
"""
key, randstring=generate_random_str()
repMap[key]={"ori":r"\par"}
text=text.replace(r"\par",randstring)

"""
Replace all the equations
"""
ret=re.search(r"\$\$([\s\S]*?)\$\$",text)
while ret!=None:
    key, randstring=generate_random_str()
    repMap[key]={"ori":ret.group()}
    text=text.replace(ret.group(),randstring)
    ret = re.search(r"\$\$([\s\S]*?)\$\$", text)

ret=re.search(r"\$([\s\S]*?)\$",text)
while ret!=None:
    key, randstring=generate_random_str()
    repMap[key]={"ori":ret.group()}
    text=text.replace(ret.group(),randstring)
    ret = re.search(r"\$([\s\S]*?)\$", text)

"""
Protect labels, cites and refs
"""
ret=re.search(r"\\label\{(.*?)\}",text)
while ret!=None:
    key, randstring=generate_random_str()
    repMap[key]={"ori":ret.group()}
    text=text.replace(ret.group(),randstring)
    ret = re.search(r"\\label\{(.*?)\}", text)

ret=re.search(r"\\cite\{(.*?)\}",text)
while ret!=None:
    key, randstring=generate_random_str()
    repMap[key]={"ori":ret.group()}
    text=text.replace(ret.group(),randstring)
    ret = re.search(r"\\cite\{(.*?)\}", text)

ret=re.search(r"\\ref\{(.*?)\}",text)
while ret!=None:
    key, randstring=generate_random_str()
    repMap[key]={"ori":ret.group()}
    text=text.replace(ret.group(),randstring)
    ret = re.search(r"\\ref\{(.*?)\}", text)


"""
Deal with all figures and algorithms
"""
ret=re.search(r"\\begin\{figure\}([\s\S]*?)\\end\{figure\}",text)
while ret!=None:
    key, randstring=generate_random_str()
    repMap[key]={"ori":ret.group()}
    text=text.replace(ret.group(),randstring)
    ret=re.search(r"\\begin\{figure\}([\s\S]*?)\\end\{figure\}",text)

ret=re.search(r"\\begin\{algorithm\}([\s\S]*?)\\end\{algorithm\}",text)
while ret!=None:
    key, randstring=generate_random_str()
    repMap[key]={"ori":ret.group()}
    text=text.replace(ret.group(),randstring)
    ret=re.search(r"\\begin\{algorithm\}([\s\S]*?)\\end\{algorithm\}",text)


"""
Handle the environments and commands
"""
for env in environments:
    key,randstring = generate_random_str()
    repMap[key] = {"ori": "\\begin\{"+env}
    text = text.replace("\\begin\{"+env, randstring)
    key,randstring = generate_random_str()
    repMap[key] = {"ori": "\\end\{" + env}
    text = text.replace("\\end\{" + env, randstring)

for com in commands:
    key, randstring=generate_random_str()
    repMap[key]={"ori":com}
    text=text.replace(com,randstring)


"""
Handle the bracelets
"""
key, randstring=generate_random_str()
repMap[key]={"ori":"{"}
text=text.replace("{",randstring)

key, randstring=generate_random_str()
repMap[key]={"ori":"}"}
text=text.replace("}",randstring)

"""
Handle backslash
"""
key, randstring=generate_random_str()
repMap[key]={"ori":"\\"}
text=text.replace("\\",randstring)

f=open(fOutput, "w",encoding='UTF-8')
f.write(text)
f.close()

jsObj = json.dumps(repMap)

fileObject = open(fReplace, 'w',encoding='UTF-8')
fileObject.write(jsObj)
fileObject.close()



