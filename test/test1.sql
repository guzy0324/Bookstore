use bookstore
insert into BSUSER values('un','pw','addr')
insert into AUTHOR values('aid','author')
insert into book
values('bookIDbookIDbo','bookTitle','aid',0)

select COUNT(*)
from transact t
where t.Buyer='a' and t.BookID='a'

insert into review
values('title','un','bookIDbookIDbo',1,'worst ever')