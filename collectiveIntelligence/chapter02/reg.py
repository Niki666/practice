import re

rex = re.compile('Count="(.+?)"')

str = '<row Id="1" TagName=".net" Count="194395" ExcerptPostId="3624959" WikiPostId="3607476" />'
text = ''

print rex.findall(str)[0]
