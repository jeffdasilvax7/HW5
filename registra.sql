drop database if exists db_registra;
create database db_registra;
use db_registra;

create table tbl_student (
	st_ID int unsigned auto_increment primary key,
	first_name varchar (50)not null,
	last_name varchar (50)not null,
	birthdate date not null,
    email text not null,
   
   check (birthdate <= '2015-01-01'),
   check (email regexp '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$')
); 

select *
from tbl_student;