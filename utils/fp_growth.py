from itertools import combinations

class treeNode:
    def __init__(self,nameValue,numOccur,parentNode):
        self.name = nameValue #值
        self.count = numOccur #计数
        self.nodeLink = None #横向链
        self.parent = parentNode #父亲节点
        self.children = {}   #儿子节点
    def inc(self,numOccur):
        self.count += numOccur
    def disp(self,ind = 1):   #输出显示
        print(' ' * ind,self.name,' ',self.count)
        for child in self.children.values():
            child.disp(ind + 1)


from collections import OrderedDict
def loadSimpDat():
    simpDat=[['r','z','h','j','p'],
             ['z','y','x','w','v','u','t','s'],
             ['z'],
             ['r','x','n','o','s'],
             ['y','r','x','z','q','t','p'],
             ['y','z','x','e','q','s','t','m']]
    return simpDat

def createInitSet(dataSet):
    retDict=OrderedDict()
    for trans in dataSet:
        retDict[frozenset(trans)]=1
    return retDict


#创建FP树代码
def createTree(dataSet,minSup=1):
    headerTable={}#用来存储每项元素及其出现次数
    for trans in dataSet:#遍历每条记录
        for item in trans:#遍历每条记录的每项元素
            headerTable[item]=headerTable.get(item,0)+dataSet[trans]#计算每项元素的出现次数
    num = len(dataSet)
    for k in list(headerTable.keys()):
        if headerTable[k]/float(num)<minSup:
            del(headerTable[k])#如果某项元素的支持度小于最小支持度，从headerTable中删掉该元素
    freqItemSet=set(headerTable.keys())#freqItemSet中的每一项元素的支持度均大于或等于最小支持度
    if len(freqItemSet)==0:
        return None,None
    for k in headerTable:
        headerTable[k]=[headerTable[k],None]
    retTree=treeNode('Null Set',1,None)#创建根节点
    for tranSet,count in dataSet.items():#遍历每一条事务数据
        localD={}
        for item in tranSet:#遍历这条数据中的每个元素
            if item in freqItemSet:#过滤每条记录中支持度小于最小支持度的元素
                localD[item]=headerTable[item][0]#把headerTable中记录的该元素的出现次数赋值给localD中的对应键
        if len(localD)>0:#如果该条记录有符合条件的元素
            orderedItems=[v[0] for v in sorted(localD.items(),key=lambda p:p[1],reverse=True)]#元素按照支持度排序，支持度越大，排位越靠前
            updateTree(orderedItems,retTree,headerTable,count)
    return retTree,headerTable


def updateTree(items,inTree,headerTable,count):
    if items[0] in inTree.children:#如果inTree的子节点中已经存在该元素
        inTree.children[items[0]].inc(count)#树中该元素增加值，增加的值为该元素所在记录的出现次数
    else:
        inTree.children[items[0]]=treeNode(items[0],count,inTree)#如果树中不存在该元素，重新创建一个节点
        if headerTable[items[0]][1]==None:#如果在相似元素的字典headerTable中，该元素键对应的列表值中，起始元素为None
            headerTable[items[0]][1]=inTree.children[items[0]]#把新创建的这个节点赋值给起始元素
        else:
            updateHeader(headerTable[items[0]][1],inTree.children[items[0]])#如果在相似元素字典headerTable中，该元素键对应的值列表中已经有了起始元素，那么把这个新建的节点放到值列表的最后
    if len(items)>1:#如果在这条记录中，符合条件的元素个数大于1
        updateTree(items[1::],inTree.children[items[0]],headerTable,count)#从第二个元素开始，递归调用updateTree函数。
def updateHeader(nodeToTest,targetNode):#该函数实现把targetNode放到链接的末端
    while (nodeToTest.nodeLink!=None):
        nodeToTest=nodeToTest.nodeLink
    nodeToTest.nodeLink=targetNode




def ascendTree(leafNode,prefixPath):#该函数找出元素节点leafNode的所有前缀路径，并把包括该leafNode及其前缀路径的各个节点的名称保存在prefixPath中
    if leafNode.parent!=None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent,prefixPath)

#寻找条件基代码
def findPrefixPath(basePat,treeNode):
    condPats={}
    while treeNode!=None:
        prefixPath=[]
        ascendTree(treeNode,prefixPath)
        if len(prefixPath)>1:
            condPats[frozenset(prefixPath[1:])]=treeNode.count#某个元素的前缀路径不包括该元素本身
        treeNode=treeNode.nodeLink#下一个相似元素
    return condPats#condPats存储的是元素节点treeNode及其所有相似元素节点的前缀路径和它的计数

#构建条件FP树代码
def mineTree(inTree,headerTable,minSup,preFix,freqItemList):
    bigL=[v[0] for v in sorted(headerTable.items(),key=lambda p:p[1][0])]#排序，从频率低到频率高排列树中的元素
    for basePat in bigL:#遍历inTree中的所有元素
        newFreqSet=preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        conPattBases=findPrefixPath(basePat,headerTable[basePat][1])#寻找元素basePat及其相似元素的所有前缀路径，并以字典的形式存储它们
        myCondTree,myHead=createTree(conPattBases,minSup)
        if myHead!=None:#只要FP树中还有元素，递归调用mineTree函数
            mineTree(myCondTree,myHead,minSup,newFreqSet,freqItemList)


#关联评估代码
def comb(itemsList, data, iSup, iConf):  
    result = []
    for items in itemsList:
        if len(items) == 1:
            continue
        for i in range(len(items)-1):
            for item in combinations(items,i+1):
                _items2 = set(items) - set(item)
                _result = [item, _items2]
                sup = getsup(items, data)
                if sup < iSup:
                    continue
                _result.append(sup)
                conf = 0.5/getsup(item, data)
                if conf < iConf:
                    continue
                _result.append(conf)
                lift = conf/getsup(_items2, data)
                _result.append(lift)
                _result.append(conf/lift)
                result.append(_result)
    return result

def getsup(item, data): #获取支持度
    count = 0
    for d in data:
        if set(item).issubset(set(d)):
            count += 1
    return count/float(len(data))



if __name__ == '__main__':
    initSet=createInitSet(loadSimpDat())
    myFPtree,myHeaderTab=createTree(initSet,0.5)
    myFPtree.disp()
    # freqItemSet=set(myHeaderTab.keys())
    # for item in freqItemSet:
    #     condPats=findPrefixPath(item,myHeaderTab[item][1])
    #     print(item)
    #     print(condPats)
    freqItems=[]
    mineTree(myFPtree,myHeaderTab,0.5,set([]),freqItems)
    print(len(freqItems))
    # print(freqItems)
    print(comb(freqItems, initSet, 0.5, 0.5))

    