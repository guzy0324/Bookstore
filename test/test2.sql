use bookstore
select quantity from book where ISBN='bookIDbookIDbo'
insert into TRANSACT
values('DateTime','un','bookIDbookIDbo')
go

insert into bookmark values('bmtitle','descript')
insert into BOOKMARK_BOOK
values('bmtitle','un','bookIDbookIDbo',0)

update book set Quantity=2 where ISBN='bookIDbookIDbo'
insert into TRANSACT
values('DateTime','un','bookIDbookIDbo')
select quantity from book where ISBN='bookIDbookIDbo'
select owned from BOOKMARK_BOOK
where Title='bmtitle' and BookID='bookIDbookIDbo'