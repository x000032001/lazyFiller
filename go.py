#!/usr/bin/python

import json
import codecs
from pprint import pprint

IN_DIR = 'origin/'
OUT_DIR = 'html/'

with codecs.open(IN_DIR + 'data.json','r','utf-8') as data_file:
    data = json.load(data_file)

with open(IN_DIR + 'menu.json','r') as menu_file:
    menu = json.load(menu_file)

with open(IN_DIR + 'template.html','r') as TL:
    tl = TL.read()
    tl = tl.decode('utf-8','ignore')

menu_code = ""
for ele in data:
    tl_copy = tl
    for key in ele:
        val = ele[key]
        target = "<!-- @" + key + "@ -->"

        # block special key
        # prefix dash for output file name
        if key[0] != '_':
            # if is html then just write it to output
            if '.html' in val:
                with open(IN_DIR + val,'r') as inc_file:
                    inc = inc_file.read()
                    tl = tl.replace(target,"<!-- ##"+val+"-->\n"+inc+"<!-- ##"+val+"-->\n")
            elif key == "menu":
                if ele['menu']['id'] != "":
                    menu_code += menu['item'] % (ele['menu']['id'] ,ele['_out_'] ,ele['menu']['text'])
            else:
                tl = tl.replace(target,val)
    #print type(tl)
    with open(OUT_DIR + ele['_out_'],'w') as out:
        out.write(tl.encode('utf-8'))
        out.close()
    tl = tl_copy

menu_out = ""
for line in menu['header']:
    menu_out += line
menu_out += menu_code + menu['footer']

for ele in data:
    with open(OUT_DIR + ele['_out_'],'r') as in_file:
        text = in_file.read()
        in_file.close()
    #print type(text)
    #print type(menu_out)
    text = text.decode('utf-8')
    text = text.replace("<!-- @menu@ -->",menu_out)
    with open(OUT_DIR + ele['_out_'],'w') as out_file:
        out_file.write(text.encode('utf-8'))
        out_file.close()

print "DONE!"
