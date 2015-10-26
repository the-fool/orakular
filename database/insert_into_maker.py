import sys, os

header = ['into students (sid, sname, major, s_level, age)',
          'into department (did, dname)',
          'into faculty (fid, fname, deptid)',
          'into courses (cid, cname, meets_at, room, fid, limit)',
          'into staff (sid, sname, deptid)'
         ]
           
with open('dummy.txt') as i:
  with open('data.sql', 'w') as o:
    index = 0
    while True:
      ln = i.readline()
      if ln.rstrip() == 'BEGIN':
        while True:
          ln = i.readline()
          if ln.rstrip() == 'END': 
            break
          o.write('insert  ' + header[index] + '\n') 
          o.write('     values ' + ln + '/') 
        index = index + 1
      else: 
        break

    o.close()
