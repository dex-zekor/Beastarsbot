
from unittest.util import strclass


# d2 = json.load(b)
# z = {}
# for chapter in d1 | d2:
#     for key, vaule in d1[chapter].items():
#         z[chapter] = {key:vaule}
#     for key, vaule in d2[chapter].items():
#         z[chapter][key] = vaule


def getpage(index_json: dict, args):
    chapter_number = args[0]
    page = args[1]
    lang_get = args[2]
    t_group_get = args[3]

    if  chapter_number in index_json:

        print("chapter found")
        chapter = index_json[chapter_number]
        if lang_get in chapter:
            groups = index_json[chapter_number][lang_get].keys()
            if t_group_get in groups:
                pass
            else:
                t_group_get = list(index_json[chapter_number][lang_get])[0]
        else:
            lang_get = list(index_json[chapter_number])[0]
            groups = index_json[chapter_number][lang_get].keys()
            if t_group_get in groups:
                pass
            else:
                t_group_get = list(index_json[chapter_number][lang_get])[0]
        if page in chapter[lang_get][t_group_get]:
            
            info= [chapter_number, page, lang_get, t_group_get]
            return info, chapter[lang_get][t_group_get][page]
    return ['','','',''],None
                
                


            
def getpagecount(index_json: dict, args):
    group = args[3]
    lang = args[2]
    pagecount = 0
    if args[0] in index_json:
        chapter_number =  args[0]
    return len(index_json[chapter_number][lang][group])
        


def getnextchapter(index_json: dict, args):
    chapter_number = args[0]
    page = args[1]
    lang_get = args[2]
    t_group_get = args[3]

    i = iter(index_json)
    for chapter in index_json:
        next(i)
        if chapter == chapter_number:
            break
    chapter_number = next(i,None)
    if chapter_number:
        info= [chapter_number, page, lang_get, t_group_get]
        return getfristpage(index_json,info)

def getprevchapter(index_json: dict, args):
    chapter_number = args[0]
    page = args[1]
    lang_get = args[2]
    t_group_get = args[3]
    prevchap = chapter_number
    i = iter(index_json)
    for chapter in index_json:
        next(i)

        if chapter == chapter_number:
            break
        prevchap = chapter
    if prevchap:
        info= [prevchap, page, lang_get, t_group_get]
        return getlastpage(index_json,info)

def getprevpage(index_json: dict, args):
    page = args[1]
    if int(page) >  1:
        page = str(int(page)-1)
        newargs = [args[0],page,args[2],args[3]]
        return getpage(index_json,newargs)
    else:
        return getprevchapter(index_json,args)


            
def getnextpage(index_json: dict, args):
    page = args[1]
    if int(page) <  getpagecount(index_json,args):
        page = str(int(page)+1)
        newargs = [args[0],page,args[2],args[3]]
        return getpage(index_json,newargs)
    else:
        return getnextchapter(index_json,args)

def getfristpage(index_json: dict, args):
    chapter_number = args[0]
    page = args[1]
    lang_get = args[2]
    t_group_get = args[3]
    if page != "1":
        page = "1"
        info= [chapter_number, page, lang_get, t_group_get]
        return getpage(index_json,info)
    else:
        return getprevchapter(index_json,args)

def getlastpage(index_json: dict, args):
    chapter_number = args[0]
    page = args[1]
    lang_get = args[2]
    t_group_get = args[3]
    last_page = str(getpagecount(index_json,args))
    if page != last_page:
        info= [chapter_number,last_page , lang_get, t_group_get]
        return getpage(index_json,info)
    else:
        return getnextchapter(index_json,args)

