# encoding: utf-8
critics={'Lisa Rose':{'Lady in the Water':2.5,'Snakes on a Plane':3.5,
                      'Just My Luck':3.0,'Superman Returns':3.5,
                      'You,Me and Dupree':2.5,'The Night Listener':3.0},
         'Gene Seymour':{'Lady in the Water':3.0,'Snakes on a Plane':3.5,
                         'Just My Luck':1.5,'Superman Returns':5.0,
                         'You,Me and Dupree':3.5,'The Night Listener':3.0},
         'Michael Phillips':{'Lady in the Water':2.5,'Snakes on a Plane':3.0,
                             'Superman Returns':3.5,'The Night Listener':4.0},
         'Claudia Puig':{'Snakes on a Plane':3.5,'Just My Luck':3.0,
                         'Superman Returns':4.0,'You,Me and Dupree':2.5,
                         'The Night Listener':4.5},
         'Mick LaSalle':{'Lady in the Water':3.0,'Snakes on a Plane':4.0,
                         'Just My Luck':2.0,'Superman Returns':3.0,
                         'You,Me and Dupree':2.0,'The Night Listener':3.0},
         'Jack Matthews':{'Lady in the Water':3.0,'Snakes on a Plane':4.0,
                          'Superman Returns':5.0,'You,Me and Dupree':3.5,
                          'The Night Listener':3.0},
         'Toby':{'Snakes on a Plane':4.5,'Superman Returns':4.0,'You,Me and Dupree':1.0}}

#计算recommendation的相似度
from math import sqrt
#但会一个有关person1与person2的基于距离的相似度评价
def sim_distance(prefs, person1,person2):
    #得到shared_item的列表
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    #如果两者之间没有共同之处，则返回0
    if len(si)==0:return 0
    #计算所有差值的平方和
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
                        for item in prefs[person1]if item in prefs[person2]])
    return 1/(1+sqrt(sum_of_squares))

#皮尔逊相关系数法
def sim_person(prefs,p1,p2):
    #得到双方都评价过的物品列表
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]:si[item]=1
    #得到列表元素的个数
    n=len(si)

    if n==0: return 1
    #对所有偏好求和
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])
    #求平方和
    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
    #求乘积之和
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
    #计算皮尔逊评价值
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0: return 0
    r = num/den

    return r

#为评论者打分
#从反映偏好的字典返回最为匹配者
#返回结果的个数和相思参数均为可选参数
def topMatches(prefs,person,n=5,similarity=sim_person):
    scores=[(similarity(prefs,person,other),other)
            for other in prefs if other!=person]
    #对列表进行排序，评价最高者排在前面
    scores.sort()
    scores.reverse()
    return scores[0:n]

#加权page15
#利用所有他人评价值的加权平均，为某人提供建议
def getRecommendations(prefs,person,similarity=sim_person):
    totals={}
    simSums={}
    for other in prefs:
        #不要和自己作比较
        if other==person: continue
        sim=similarity(prefs,person,other)

        #忽略评价值为零或小于零的情况
        if sim<=0: continue
        for item in prefs[other]:

            #只对自己还未看过的影片评价
            if item not in prefs[person] or prefs[person][item]==0:
                #相似度*评价值
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                #相似度之和
                simSums.setdefault(item,0)
                simSums[item]+=sim

    #建立一个归一化的列表
    rankings=[(total/simSums[item],item) for item,total in totals.items()]

    #返回经过排序的列表
    rankings.sort()
    rankings.reverse()
    return rankings

#0612
#数据格式转换
def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            #将物品与人员对调
            result[item][person]=prefs[person][item]
    return result

def calculateSimilarItems(prefs,n=10):
    #建立字典，以给出与浙西额物品最为详尽的所有其他物品
    result={}
    #以物品为中心对偏好矩阵实施倒置处理
    itemPrefs=transformPrefs(prefs)
    c=0
    for item in itemPrefs:
        #force on the update big data
        c+=1
        if c%100==0:
            print "%d / %d" % (c,len(itemPrefs))
        scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
        result[item]=scores
    return result

#0613
def getRecommendedItems(prefs,itemMatch,user):
    userRatings=prefs[user]
    scores={}
    totalSim={}

    #loop through user ratings
    for (item,rating) in userRatings.items():
        #loop through the similar item
        for (similarity,item2)in itemMatch[item]:

            #if this user has rated this item ,ignore
            if item2 in userRatings:
                continue

            #weighting ratings and similarity
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating

            #全部相似度之和
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity
        #将每个合计值除以加权和，求出平均值
        rankings=[(score/totalSim[item],item) for item,score in scores.items()]
        #按最高值到最低值的顺序，返回评分结果
        rankings.sort()
        rankings.reverse()
        return rankings

def loadMovieLens():
    #获取影片标题
    movies={}
    for line in open('./ml-100k/u.item'):
        (id,title)=line.split('|')[0:2]
        movies[id]=title

    #加载数据
    prefs={}
    for line in open('./ml-100k/u.data'):
        (user, movieid, rating, ts)=line.split('\t')
        prefs.setdefault(user,{})
        prefs[user][movies[movieid]]=float(rating)
    return prefs