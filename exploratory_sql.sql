show databases;
create database tommy;

use tommy;

create table student(name varchar(20), college varchar(20));

insert into student values ('thomas', 'humber');
insert into student values ('veronika', 'ocad');
insert into student values ('terran', 'waterloo');
insert into student values ('elizabeth', 'guelph');
insert into student values ('cindy', 'toronto');

create table grades(science varchar(20), arts varchar(20));

insert into grades values ('B-', 'B');
insert into grades values ('C', 'A+');
insert into grades values ('B', 'A-');
insert into grades values ('A+', 'A-');
insert into grades values ('A+', 'B+');


