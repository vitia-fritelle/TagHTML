from requests import get
from requests.exceptions import Timeout
from requests.models import HTTPError
import os

#localizando o diretorio para salvar
md=os.path.dirname(__file__)
md2=md.replace('/','\\')


def checkStatus(response):
    try:
        response.raise_for_status()
    except HTTPError:
        print(f"O erro HTTP foi {response.raise_for_status()}")

def getCodigoFonte(site, tout=1):
    try:
        r=get(site, timeout=tout)
    except ConnectionError:
        print(f"Há um problema na rede.")
        return ''
    except Timeout:
        print(f"O site {site} não enviou nenhum byte em {tout}s.")
        return ''
    checkStatus(r)
    return r.text

def tagFind(text):
    try:
        t=text[:text.index('>')]
    except ValueError:
        return ''
    return t.replace('\\','')

def parser(html):
    tag=[tagFind(i) for i in html.split("</") if tagFind(i).find('<')==-1]
    tagDict=dict((name,tag.count(name)) for name in set(tag))
    return tagDict

def parserEmptyTag(html):
    emptyTags={'area','base','br','col','embed','hr',
           'img', 'input','keygen','link','meta',
           'param', 'source','track','wbr'}
    tagName={'<'+name for name in emptyTags}
    tagDict=dict((name[1:],html.count(name)) for name in tagName)
    return tagDict

def addDict(a,b):
    return dict(a,**b)

if __name__=="__main__":
    
    sites=("https://www.mercadolivre.com.br/",
    "https://www.magazineluiza.com.br/",
    "https://www.alibaba.com/",
    "https://global.jd.com/",
    "https://www.ebay.com/",
    "https://www.wayfair.com/",
    "https://www.chewy.com/",
    "https://www.coupang.com/",
    "https://www.wildberries.ru/",
    "https://www.farfetch.com/br/",
    "https://www.ozon.ru/"
    )

    #Processamento
    codFonte={getCodigoFonte(url,5) for url in sites}
    
    ##Criando conjunto de dicionários
    setDict=[addDict(parser(text),
                     parserEmptyTag(text)) for text in codFonte]
    
    ##Eu faço a atualização do dicionário em cima de todos os dicionários encontrados em 
    ##setDict. O que essa operação faz é como um append para dicionários, mas, como não tem 
    ##chave repetida em dicionário, só ocorre a tag única.
    dictFinal={}
    for dic in iter(setDict):
        dictFinal.update(dic)
    
    ##Contando quantas vezes a tag aparece
    for tagName in dictFinal.keys():
        dictFinal[tagName]=0
        for dic in iter(setDict):
            try:
                dictFinal[tagName]+=dic[tagName]
            except:
                pass

    print(dictFinal)
    exit()