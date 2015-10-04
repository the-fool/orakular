import sys, os
with open('dummy_data.sql') as f:
  out = open('dummy.sql', 'w')
  buf = f.readline()
  out.write(buf)
  for x in range(10):
    t = ''
    buf = f.readline()
    l = buf.split(' ')
    t = ' '.join(l[:4]) + ' (sid, sname, major, s_level, age) values ' + ' '.join(l[4:])
    out.write(str(t))
  buf = f.readline()
  out.write(buf) 
