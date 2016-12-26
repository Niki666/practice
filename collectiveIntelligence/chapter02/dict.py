# encoding: utf-8
# names=['Alice','Beth','Cecil','Dee-Dee','Earl']
# numbers=['2341','9102','3158','0142','5551']
# print numbers[names.index('Cecil')]
# phonebook={'Alice':'2341','Beth':'9102','Cecil':'3258'}

# items=[('name','Gumby'),('age',42)]
# d = dict(items)
# print d['name']
# print len(d)
# print x
#简单数据库
#使用人名作为键的字典。每个人用另一个字典表示(嵌套字典)
people={'Alice':{'phone':'2341','addr':'Foo drive 23'},
        'Beth':{'phone':'9102','addr':'Bar street 42'},
        'Cecil':{'phone':'3158','addr':'Baz avenue 90'}}
#针对电话号码和地址使用的描述性标签，会在打印输出的时候用到
labels={'phone':'phone number','addr':'address'}
name=raw_input('Name:')
#查找电话号码还是地址，使用正确的键：
request=raw_input('phone number(p) or address(a)?')
#使用正确的键
key=''
if request=='p':
    key='phone'
if request=='a':
    key='addr'
#如果名字是字典中的有效键才打印的信息
if name in people:
    print "%s's %s is %s." %(name,labels[key],people[name][key])

# template='''<html>
# <head><title>%(title)s</title></head>
# <body>
# <h1>%(title)s</h1>
# <p>%(text)s</p>
# </body>'''
# data={'title':'My Home Page','text':'hau daieh d'}
# print template%data


