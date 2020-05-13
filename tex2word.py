import json
import re
import random

environments = ["abstract", "aligned", "myLemm", "myTheo", "myDef",
                "myCoro", "tabular","pkl"]
commands = ["\\begin{", "\\end{", "\\section{", "\\end{",
            "\\subsection{", "\\subsubsection{",
            "\\indent ", "\\hfill", "\\textbf{", "\\_", "\\caption{",
            "\\item ","\\em ","\\sf ","\\Paragraph{","\\newcommand{"]
syscoms=[r"\\vspace\{(.*?)\}",r"\\vspace\*\{(.*)\}",r"\\newcommand\{(.*?)\}"]

fInput = "in.txt"
fOutput = "out.txt"

repMap = {}

f = open(fInput, "r")
text = f.read()
f.close()


"""
Remove the captions
"""
ret = re.search(r"\\section\{(.*?)\}", text)
while ret != None:
    text = re.sub(r"\\section\{(.*?)\}", "", text)
    ret = re.search(r"\\section\{(.*?)\}", text)
ret = re.search(r"\\subsection\{(.*?)\}", text)
while ret != None:
    text = re.sub(r"\\subsection\{(.*?)\}", "", text)
    ret = re.search(r"\\subsection\{(.*?)\}", text)

"""
replace \par
"""
text=text.replace("\par"," ")


"""
Remove Comments and syscoms
"""
ret = re.search(r"(?<=[^\\])%(.*?)\n", text)
while ret != None:
    text = re.sub(r"(?<=[^\\])%(.*?)\n", "", text)
    ret = re.search(r"(?<=[^\\])%(.*?)\n", text)

for syscom in syscoms:
    text=re.sub(syscom,"",text)
"""
remove \n for short lines
"""
text = re.sub(r"(.{50,})\n", r"\1 ", text)
text = re.sub(r"\n(?=\$)", " ", text)
"""
Replace all the equations
"""
ret = re.search(r"\$\$([\s\S]*?)\$\$", text)
while ret != None:
    text = text.replace(ret.group(), "FooBar")
    ret = re.search(r"\$\$([\s\S]*?)\$\$", text)

ret = re.search(r"\$([\s\S]{1,5}?)\$", text)
if ret != None:
    text=re.sub(r"\$([\s\S]{1,5}?)\$",r"\1",text)

ret = re.search(r"\$([\s\S]*?)\$", text)
while ret != None:
    text = text.replace(ret.group(), "FooBar")
    ret = re.search(r"\$([\s\S]*?)\$", text)

"""
Protect labels, cites and refs
"""
ret = re.search(r"\\label\{(.*?)\}", text)
while ret != None:
    text = text.replace(ret.group(), "")
    ret = re.search(r"\\label\{(.*?)\}", text)

ret = re.search(r" \\cite\{(.*?)\}", text)
while ret != None:
    text = text.replace(ret.group(), "")
    ret = re.search(r"\\cite\{(.*?)\}", text)

ret = re.search(r"\\cite\{(.*?)\} ", text)
while ret != None:
    text = text.replace(ret.group(), "")
    ret = re.search(r"\\cite\{(.*?)\}", text)

ret = re.search(r"\\ref\{(.*?)\}", text)
while ret != None:
    text = text.replace(ret.group(), "1")
    ret = re.search(r"\\ref\{(.*?)\}", text)

"""replace fracs"""
text = text.replace(r"\\frac\{(.*?)\}\{(.*?)\}", "1")
"""
Deal with all figures,tables and algorithms
"""
ret = re.search(r"\\begin\{figure\}([\s\S]*?)\\end\{figure\}", text)
while ret != None:
    text = text.replace(ret.group(), "")
    ret = re.search(r"\\begin\{figure\}([\s\S]*?)\\end\{figure\}",text)

ret = re.search(r"\\begin\{table\}([\s\S]*?)\\end\{table\}", text)
while ret != None:
    text = text.replace(ret.group(), "")
    ret = re.search(r"\\begin\{table\}([\s\S]*?)\\end\{table\}",
                    text)

ret = re.search(r"\\begin\{algorithm\}([\s\S]*?)\\end\{algorithm\}",
                text)
while ret != None:
    text = text.replace(ret.group(), "")
    ret = re.search(
        r"\\begin\{algorithm\}([\s\S]*?)\\end\{algorithm\}", text)

"""
Handle the environments and commands
"""
for env in environments:
    text = text.replace("\\begin{" + env, "")
    text = text.replace("\\end{" + env, "")

for com in commands:
    text = text.replace(com, "")


"""
Handle the bracelets
"""
text = text.replace("{", "")

text = text.replace("}", "")

"""
Handle backslash
"""
text = text.replace("\\", "")
while text.find("  ")>0:
    text = text.replace("  ", " ")

text = text.replace(" .", ".")
text = text.replace(" ,", ",")


f = open(fOutput, "w", encoding='UTF-8')
f.write(text)
f.close()


