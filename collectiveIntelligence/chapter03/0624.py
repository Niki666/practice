# encoding: utf-8
import clusters
reload(clusters)
blognames,words,data=clusters.readfile('blogdata.txt')
#
# coords=clusters.scaledown(data)
# clusters.draw2d(coords,blognames,jpeg='blogs2d.jpg')

# clust=clusters.hcluster(data)
# clusters.printclust(clust,labels=blognames)
# rdata=clusters.rotatematrix(data)
# wordclust=clusters.hcluster(data)
# clusters.drawdendrogram(wordclust,labels=words,jpeg='wordclust.jpg')
kclust=clusters.kcluster(data,k=10)
print [blognames[r] for r in kclust[9]]

# import urllib2
# from BeautifulSoup import BeautifulSoup
# c=urllib2.urlopen('http://kiwitobes.com/wiki/Programming_language.html')
# soup=BeautifulSoup(c.read())
# links=soup('a')
# print links[10]
# wants,people,data=clusters.readfile('zebo.txt')
# clust=clusters.hcluster(data,distance=clusters.tanimoto)
# clusters.drawdendrogram(clust,wants)