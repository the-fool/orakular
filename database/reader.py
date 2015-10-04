import sys, os
with open('dummy_data.sql') as f:
  out = open('dummy.txt', 'w')
  buf = f.readline()
  for x in range(10):
    t = ''
    buf = f.readline()
    l = buf.split(' ')
    t = ' '.join(l[4:])
    out.write(str(t))
