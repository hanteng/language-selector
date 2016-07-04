# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
from string import Template
import os.path, os, glob
import shutil
import codecs

import requests
import json
locale_select = requests.get("https://raw.githubusercontent.com/unicode-cldr/cldr-core/master/availableLocales.json").json()['availableLocales']['full']

# Partial Selected Construction
#locale_select = ['en-GB','my', 'zh-Hant'] # Can be extended in the future  'zh-Hant-HK', 'zh-Hant-MO', 'zh-Hans', 'zh-Hans-SG'

## Outpuing Lists

path_data = u'../data'
path_demo = u'../demo'
path_demo_template = u'../demo/_template'

json_src_template= u'http://raw.githubusercontent.com/hanteng/country-selector/master/data/{locale}/territories.json'

######## MSG for future locale translation ############
MSG=dict()
MSG['Country Selector']     ="Country Selector: Unicode CLDR resource application"
MSG['Country Selector_Q']   ="Select a country"
MSG['Country Selector_Q_AJAX']="Select a country (using AJAX)"

                   #COUNTRY_SEL, COUNTRY_SEL_Q, COUNTRY_SEL_Q_AJAX, PLACEHOLDER, DATALIST
output_DEMO_HTML=\
'''<!DOCTYPE html>  
<html>  
  <head>
  <meta charset="UTF-8">
    <title>COUNTRY_SEL</title>
    <link rel="stylesheet" href="css/style.css">
  </head>
  <body>
    <div id="page-wrapper">
      <h1>COUNTRY_SEL</h1>
      <label for="default">COUNTRY_SEL_Q</label>
      <input type="text" id="default" list="countries" placeholder="$PLACEHOLDER"> 
      $DATALIST
      <label for="ajax">COUNTRY_SEL_Q_AJAX</label>
      <input type="text" id="ajax" list="json-datalist" placeholder="$PLACEHOLDER">
      <datalist id="json-datalist"></datalist>
    </div>
    <script src="js/index.js"></script>
  </body>
</html>  
'''
########################################################


for l in locale_select:
    inputfn_HTML = os.path.join(path_data, l, "territories_snippet.htm")
    outputfn_HTML = os.path.join(path_demo, l, "index.htm")

    for directory in ['css', 'js']:
        d = os.path.join(path_demo, l, directory)
        if not os.path.exists(d):
            os.makedirs(d)
        if directory == 'css':
            shutil.copy2(os.path.join(path_demo_template, directory,"style.css"),
                         os.path.join(path_demo, l, directory,"style.css"))

    with codecs.open(os.path.join(path_demo_template, directory,"index.js"), "r", "utf-8") as file:
        text = file.read()
 
    text = Template(text).safe_substitute(JSON_SRC = json_src_template.format(locale = l) , \
                                          PLACEHOLDER = "e.g. HK",\
                                          )    

    with codecs.open(os.path.join(path_demo, l, directory,"index.js"), "w", "utf-8") as file:
        file.write(text)


    with codecs.open(inputfn_HTML, "r", "utf-8") as file:
        snippet = file.read()

    output=Template(output_DEMO_HTML).safe_substitute(COUNTRY_SEL = MSG['Country Selector'] , \
                                                      COUNTRY_SEL_Q = MSG['Country Selector_Q'] , \
                                                      COUNTRY_SEL_Q_AJAX = MSG['Country Selector_Q_AJAX'],\
                                                      PLACEHOLDER = "e.g. HK", \
                                                      DATALIST = snippet)    

    with codecs.open(outputfn_HTML, "w", "utf-8") as file:
        file.write(output)









