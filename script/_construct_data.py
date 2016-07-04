# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
dir_outcome = "data"
## Outpuing Lists
outputfn_locales = "locales_available.json"
outputfn_src_lc = "territories.json"
outputfn_JSON = "languages.json"
outputfn_HTML = "languages_snippet.htm"

import os.path, glob
import json
import requests
import icu # pip install PyICU
import pandas as pd
import io

def url_request (url):
    r = requests.get(url)
    if r.status_code == 200:
        return r
    else:
        return None 


def load_json_list (lc_file, u):
    try:
        with open(lc_file, 'r', encoding="utf-8") as infile:
            _select = json.load (infile)
            print ("Loaded from local file.")
    except:
        results = url_request (url  = u)
        if results is not None:
            try:
                _select = results.json()['availableLocales']['full']
                with open(lc_file, 'w', encoding="utf-8") as outfile:
                    outfile.write("{}".format(_select).replace("'",'"'))
                print ("Loaded from designated url.")
            except:
                pass
    return _select

# Full Construction
URL_CLDR_JSON_AVAIL_LOCALES_LC = os.path.join ("..", dir_outcome, outputfn_locales)
URL_CLDR_JSON_AVAIL_LOCALES = "https://raw.githubusercontent.com/unicode-cldr/cldr-core/master/availableLocales.json"
locale_select = load_json_list (URL_CLDR_JSON_AVAIL_LOCALES_LC, URL_CLDR_JSON_AVAIL_LOCALES)

# Partial Selected Construction
#locale_select = ['en-GB','my', 'zh-Hant'] # Can be extended in the future  'zh-Hant-HK', 'zh-Hant-MO', 'zh-Hans', 'zh-Hans-SG'

## Retrive data directly from unicode-cldr project hosted at github
print ("Retrieve data now ...")
URL_CLDR_JSON_LANGUAGES = "https://raw.githubusercontent.com/hanteng/language-names/master/data/CLDR_language_name_{locale}.tsv"
locale_json={}
for l in locale_select: #[0:1] testing
    results = url_request (url  = URL_CLDR_JSON_LANGUAGES.format(locale=l))
    if results is not None:
        try:
            s = results.content
            locale_json [l] = pd.read_csv(io.StringIO(s.decode('utf-8')),
                                          header=0, delimiter="\t",
                                          names = ['code', 'name'],
                                          index_col = ['code'],
                                          keep_default_na=False, na_values=[])
            #results.json()['main'][l]['localeDisplayNames']['territories']
        except:
            pass

## Preprocessing and Generating lists
print ("Preprocessing data now ...")
ITEM_NAME_CODE = "{name}[{code}]"
ITEM_CODE_NAME = "{code}:{name}"
MISSING_LANG = "missing value of {langA} for {langB}"

outputlist_languages={}
for key, df in locale_json.items():

    ### Generate items for different group of lists
    n_c_full_data=[]
    n_c_data=[]
    c_n_data=[]

    c_n=dict()

    value = df.to_dict()['name']

    for k, v in value.items():
        if k==v:
            print (MISSING_LANG.format(langA=k, langB=key))
        else:
            c_n.update({k:v})
            
    for k,v in c_n.items():
        n_c_data.append(ITEM_NAME_CODE.format(name=v, code=k))
        c_n_data.append(ITEM_CODE_NAME.format(name=v, code=k))
   
    ### Sort by IBM's ICU library, which uses the full Unicode Collation Algorithm
    print ("Using IBM ICU for {}".format(key))
    collator = icu.Collator.createInstance(icu.Locale('{lc}.UTF-8'.format(lc=key)))
    n_c_data = sorted(n_c_data, key=collator.getSortKey )
    c_n_data = sorted(c_n_data, key=collator.getSortKey )

    outputlist_languages [key]  = n_c_data + c_n_data

## Outpuing Lists
for lc, outputlist in outputlist_languages.items():
    ### Create directory if not exists
    directory = os.path.join("..", dir_outcome, lc)
    if not os.path.exists(directory):
        os.makedirs(directory)
    outputfn_json = os.path.join (directory, outputfn_JSON)
    outputfn_html = os.path.join (directory, outputfn_HTML)
    
    with open(outputfn_json, 'w', encoding="utf-8") as outfile:
        outfile.write("{}".format(outputlist).replace("'",'"'))
        #json.dump("{}".format(outputlist), outfile)
    with open(outputfn_html, 'w', encoding="utf-8") as outfile:
        outputtxt = '''<datalist id="countries">'''+"".join(['''<option value="{v}">'''.format(v=x) for x in outputlist])+'''</datalist>'''
        outfile.write(outputtxt)

