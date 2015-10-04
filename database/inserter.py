import sys, os

header = ['into students (sid, sname, major, s_level, age)',
  'into department (did, dname)']
           
with open('dummy.txt') as i:
  with open('data.sql', 'w') as o:
    o.write('insert all\n')
    while True:
      ln = i.readline()
      if (ln.rstrip() == 'END'): 
        print "breaking"
        break

      o.write('into students (sid, sname, major, s_level, age)\n') 
      o.write('values ' + ln)
    while True:
      ln = i.readline()
      if (ln.rstrip() == 'END\n') or (not ln): 
        print "broke 2"
        break
      o.write('into department\n')
      o.write('values' + ln)
