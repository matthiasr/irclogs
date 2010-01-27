from mod_python import apache

content_type = "text/html; charset=UTF8"

def handler(req):
  req.content_type = content_type
  f = open(req.filename)
  req.write("<html><body>")
  for l in f:
    req.write("<p>" + l + "</p>")
  req.write("</body></html>")
  f.close()
