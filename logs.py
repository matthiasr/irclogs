from mod_python import apache
import re

content_type = "text/html; charset=UTF8"
head = """<html>
<body>"""
foot = """</body>
</html>"""

patterns = [
    (r"^(\d\d):(\d\d) (.*)$", r'<a href="#\1\2" name="\1\2">\1:\2</a> \3'),
    (r'^(.*)$',r'<p class="line">\1</p>'),
    # match URIs, whether in parentheses or not.
    # order is important
    # based on http://blog.dieweltistgarnichtso.net/constructing-a-regular-expression-that-matches-uris
    (r'''(?<!\()\b([A-Za-z][A-Za-z0-9\+\.\-]*:([A-Za-z0-9\.\-_~:/\?#\[\]@!\$&'\(\)\*\+,;=]|%[A-Fa-f0-9]{2})+)''',r'<a href="\1" target="_blank">\1</a>'),
    (r'''((?<=\()\b[A-Za-z][A-Za-z0-9\+\.\-]*:([A-Za-z0-9\.\-_~:/\?#\[\]@!\$&'\(\)\*\+,;=]|%[A-Fa-f0-9]{2})+(?=\)))''',r'<a href="\1" target="_blank">\1</a>'),
    ]

patterns_compiled = [(re.compile(p,re.U),s) for p,s in patterns]

def handler(req):
  req.content_type = content_type
  f = open(req.filename)
  req.write(head)
  for l in f:
    for p,s in patterns_compiled:
      l = p.sub(s,l)
    req.write(l)
  req.write(foot)
  f.close()
  return apache.OK
