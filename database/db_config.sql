drop trigger check_enrollment /
drop table students cascade constraints / 
drop table department cascade constraints / 
drop table faculty cascade constraints /
drop table courses cascade constraints / 
drop table enrolled / 
drop table staff /
drop sequence student_id / 
drop sequence faculty_id /
drop sequence staff_id / 
create table students 
	(sid integer primary key not null, 
	sname varchar(50) not null, 
	major varchar(30) default 'undeclared' not null, 
	s_level varchar2(15) not null, 
        age integer)
/
create table department
	(did integer primary key not null, 
	dname varchar(50))
/
create table faculty
	(fid integer primary key not null, 
	fname varchar(50), 
	deptid integer,
	foreign key(deptid) references department(did)
  	  on delete set null)
/
create table courses
	(cid varchar(16) primary key not null, 
	cname varchar(50) not null,
	meets_at char(30), 
	room varchar(15), 
	fid integer, 
	limit integer,
	actual_enrolled integer default 0,
	foreign key(fid) references faculty(fid) 
	  on delete set null)
/
create table enrolled
	(sid integer,
	cid varchar(16), 
	exam1 integer, 
	exam2 integer, 
	final integer,
  	primary key (sid, cid), 
  	foreign key(sid) references students(sid)
   	  on delete cascade
  	,
  	foreign key(cid) references courses(cid)
	  on delete cascade
	)
/
create table staff
	(sid integer primary key not null, 
	sname varchar(50), 
	deptid integer,
	foreign key(deptid) references department(did)
	  on delete set null)
/
create sequence student_id
/
create sequence faculty_id
/
create sequence staff_id
/
create trigger student_id_increment
before insert on students
for each row
begin
  select 5000 + MOD(student_id.NEXTVAL, 4000)
  into :new.sid
  from dual;
end;
/
create trigger fid_increment
before insert on faculty
for each row
begin
  select 4000 + MOD(faculty_id.NEXTVAL, 1000)
  into :new.fid
  from dual;
end;
/
create trigger staff_id_increment
before insert on staff
for each row
begin
  select 3000 + MOD(staff_id.NEXTVAL, 1000)
  into :new.sid
  from dual;
end;
/
create trigger check_enrollment
before insert or update on enrolled
for each row
declare 
	actual number; 
	maximum number;
begin
  select count(cid) 
  into actual
  from enrolled
  where enrolled.cid = :new.cid; 

  select limit
  into maximum
  from courses
  where courses.cid = :new.cid;

  if (maximum <= actual)
  then RAISE_APPLICATION_ERROR( -20001, 'Sorry, the class is full' );
  END IF;
END;
