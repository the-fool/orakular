create table students
(sid integer primary key not null, sname varchar(50) not null, 
major varchar(30) default 'undeclared' not null, 
s_level varchar(15) not null, age integer);
/
create sequence student_id;
/
create trigger sid_increment
before insert on students
for each row
begin
  select student_id.NEXTVAL
  into :new.sid
  from dual;
end;
/
