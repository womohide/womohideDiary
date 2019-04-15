import os
import shutil

#name of raw text must be "YYMMDD_title.txt"
#when daily,title is title of daily article
#when article review, title is title of article
#when book review, title is book title

def getcurrentlist():
    pypath=os.path.dirname(os.path.abspath(__file__))
    return pypath

def check_newfiles(rawd,listxt):
    newlist=[fina for fina in [filename for filename in os.listdir(rawd) if ".txt" in filename] if not fina.startswith('.')]
    with open(listxt) as f:
        noldlist = f.readlines()
    oldlist=[ffi.replace("\n","") for ffi in noldlist]
    newones=list(set(newlist)-set(oldlist))
    return newones

def replace_link(strl):
    for i in range(strl.count("](")):
        word=strl.split('](')[0].split('[')[-1]
        link=strl.split('](')[1].split(')')[0]
        newstrl='<a href="%s">[%s]</a>'%(link,word)
        strl=strl.replace("[%s](%s)"%(word,link),newstrl)
    while strl.count("***") != 0:
        strl=strl.replace('***','<em><strong>',1)
        strl=strl.replace('***','</strong></em>',1)
    while strl.count("**") != 0:
        strl=strl.replace('**','<strong>',1)
        strl=strl.replace('**','</strong>',1)
    while strl.count("*") != 0:
        strl=strl.replace('*','<em>',1)
        strl=strl.replace('*','</em>',1)
    return strl

def make_contents(rawtxtpath):
    txtname = os.path.splitext(rawtxtpath.split("/")[-1])[0]
    daten=txtname.split("_")[0]
    articlen=txtname.split("_")[1] 
    category=rawtxtpath.split("/")[-3]
    with open(rawtxtpath) as rawt:
        rt = rawt.readlines()
    rt_replace=[replace_link(li.replace("\n","<br>")) for li in rt]
    pcon = str(rt_replace[0])
    for lin in range(len(rt_replace)):
        if lin == 0:
            pass
        else:
            pcon+=str(rt_replace[lin])   
    txtname=rawtxtpath.split("/")[-1]
    return category,daten,articlen,pcon,txtname

def make_newhtml(category,date,title,pcon,pypath,txtn):
    ldate="20"+str(date)[0]+str(date)[1]+"/"+str(date)[2]+str(date)[3]+"/"+str(date)[4]+str(date)[5]
    if category == "article_review":
        basehtml = pypath+"/docs/article_review/basehtml/ar_base.html"
        listhtml = pypath+"/docs/article_review.html"
        listxtpath = pypath+"/docs/article_review/arlist.txt"
        newartipath = pypath+"/docs/article_review/ar_%s_%s.html"%(date,title)
        newarelpath = "article_review/ar_%s_%s.html"%(date,title)
        caten = "論文解説"
    elif category == 'book_review':
        basehtml = pypath+"/docs/book_review/basehtml/br_base.html"
        listhtml = pypath+"/docs/book_review.html"
        listxtpath = pypath+"/docs/book_review/brlist.txt"
        newartipath = pypath+"/docs/book_review/br_%s_%s.html"%(date,title)
        newarelpath = "book_review/br_%s_%s.html"%(date,title)
        caten = "書評"
    elif category == "list":
        basehtml = pypath+"/docs/list/basehtml/l_base.html"
        listhtml = pypath+"/docs/list.html"
        listxtpath = pypath+"/docs/list/llist.txt"
        newartipath = pypath+"/docs/list/dl_%s_%s.html"%(date,title)
        newarelpath = "list/dl_%s_%s.html"%(date,title)
        caten = "日報"
    else:
        pass
    ltitle = '[%s][%s]%s'%(date,caten,title)
    ltitle2 = '[%s]%s'%(caten,title)
    ltitle3 = '[%s]%s'%(date,title)
    with open(basehtml) as f:
        article = f.readlines()
    article_replace = [l.replace('titleinsertion', ltitle3) for l in [ll.replace("pcontents",pcon) for ll in article]]
    with open(newartipath, mode = 'w') as ff:
        ff.writelines(article_replace)
    with open(listxtpath, mode = "a") as fff:
        fff.write(txtn+"\n")
    with open(listhtml) as f4:
        listht = f4.readlines()
    listht.insert(27,'            <li><a href="%s">%s</a></li>\n'%(newarelpath,ltitle))
    with open(listhtml, mode = 'w') as f5:
        f5.writelines(listht)
    with open(pypath+"/docs/index.html") as f6:
        indexhtml = f6.readlines()
    if len(indexhtml) >= 44:
        del indexhtml[33:35]
    indexhtml.insert(29,"          <dt>%s</dt>\n"%(ldate))
    indexhtml.insert(30,'          <dd><a href="%s">%s</a></dd>\n'%(newarelpath,ltitle2))
    with open(pypath+"/docs/index.html", mode = 'w') as f7:
        f7.writelines(indexhtml)


pypath=getcurrentlist()

artrawd=pypath+("/docs/article_review/raw")
arlistp=pypath+("/docs/article_review/arlist.txt")
brtrawd=pypath+("/docs/book_review/raw")
brlistp=pypath+("/docs/book_review/brlist.txt")
ltrawd=pypath+("/docs/list/raw")
llistp=pypath+("/docs/list/llist.txt")
rawd=pypath+("/docs/rawtxt")

newone=check_newfiles(artrawd,arlistp)
count =0
if len(newone) !=0:
    for ne in newone:
        count += 1
        shutil.copy2(os.path.join(artrawd,ne),os.path.join(rawd,ne))
        category,daten,articlen,pcon,ttn = make_contents(os.path.join(artrawd,ne))
        make_newhtml(category,daten,articlen,pcon,pypath,ttn)
newone=check_newfiles(brtrawd,brlistp)
if len(newone) !=0:
    for ne in newone:
        count += 1
        shutil.copy2(os.path.join(brtrawd,ne),os.path.join(rawd,ne))
        category,daten,articlen,pcon,ttn = make_contents(os.path.join(brtrawd,ne))
        make_newhtml(category,daten,articlen,pcon,pypath,ttn)
newone=check_newfiles(ltrawd,llistp)
if len(newone) !=0:
    for ne in newone:
        count += 1
        shutil.copy2(os.path.join(ltrawd,ne),os.path.join(rawd,ne))
        category,daten,articlen,pcon,ttn = make_contents(os.path.join(ltrawd,ne))
        make_newhtml(category,daten,articlen,pcon,pypath,ttn)