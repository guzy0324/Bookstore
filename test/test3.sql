use bookstore
drop trigger t_transact
go
create trigger t_transact on TRANSACT for insert as
if (select quantity from book, inserted where ISBN=inserted.BookID) <= 0
begin
rollback transaction
end
waitfor delay '00:00:10'
update book set quantity=quantity-1 where ISBN=(select BookID from inserted)
update bookmark_book set Owned=1 where BookID=(select BookID from inserted)
and Owner=(select Buyer from inserted)
go

update book set quantity=1 where ISBN='bookIDbookIDbo'
begin tran
set transaction isolation level read committed
select quantity from book where ISBN='bookIDbookIDbo'
insert into TRANSACT
values('DateTime1','un','bookIDbookIDbo')
commit tran