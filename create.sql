drop database bookstore
create database bookstore
use bookstore

CREATE TABLE BSUSER
(
    Username VARCHAR(15) NOT NULL,
    Password VARCHAR(15) NOT NULL,
    Email VARCHAR(20) NOT NULL,
    PRIMARY KEY(Username)
);

CREATE TABLE AUTHOR
(
    AuthorID VARCHAR(15) NOT NULL,
    Authorname VARCHAR(15) NOT NULL,
    PRIMARY KEY(AuthorID)
);

CREATE TABLE BOOK
(
    ISBN CHAR(14) NOT NULL,
    Edition VARCHAR(15),
    Title VARCHAR(50) NOT NULL,
    AuthorID VARCHAR(15) NOT NULL,
    PRIMARY KEY(ISBN),
    FOREIGN KEY(AuthorID) references AUTHOR(AuthorID)
);

CREATE TABLE LISTING
(
    Seller VARCHAR(15) NOT NULL,
    Book CHAR(14) NOT NULL,
    Price DECIMAL(4,2) NOT NULL,
    Quantity INT,
    CHECK 		  (Quantity > 0),
    PRIMARY KEY(Seller, Book),
    FOREIGN KEY(Book) references BOOK(ISBN),
    FOREIGN KEY(Seller) references BSUSER(Username)
);

CREATE TABLE USER_REVIEW
(
    Reviewer VARCHAR(15) NOT NULL,
    Reviewee VARCHAR(15) NOT NULL,
    Rating INT NOT NULL,
    Review TEXT,
    CHECK 		  (Rating >= 1 AND Rating <= 5),
    PRIMARY KEY(Reviewer, Reviewee),
    FOREIGN KEY(Reviewer) references BSUSER(Username),
    FOREIGN KEY(Reviewee) references BSUSER(Username)
);

CREATE TABLE BOOK_REVIEW
(
    Reviewer VARCHAR(15) NOT NULL,
    Book CHAR(14) NOT NULL,
    Review TEXT,
    Rating INT NOT NULL,
    CHECK 		  (Rating >= 1 OR Rating <= 5),
    PRIMARY KEY(Reviewer, Book),
    FOREIGN KEY(Reviewer) references BSUSER(Username),
    FOREIGN KEY(Book) references BOOK(ISBN)
);

CREATE TABLE TRANSACT
(
    BuyerUN VARCHAR(15) NOT NULL,
    SellerUN VARCHAR(15) NOT NULL,
    BookID CHAR(14) NOT NULL,
    DateTime CHAR(23) NOT NULL,
    PRIMARY KEY(BuyerUN, SellerUN, BookID, DateTime),
    FOREIGN KEY(BuyerUN) references BSUSER(Username),
    FOREIGN KEY(SellerUN,BookID) references LISTING (Seller, Book)
);

go
create trigger t_user_reivew on USER_REVIEW for insert as
if (select count(*)
    from TRANSACT t, inserted i
    where t.BuyerUN=i.Reviewer and t.SellerUN=i.Reviewee)=0
BEGIN
rollback TRANSACTION
end

go
create trigger t_book_reivew on BOOK_REVIEW for insert as
if (select count(*)
    from TRANSACT t, inserted i
    where t.BuyerUN=i.Reviewer and t.SellerUN=i.Book)=0
begin
rollback TRANSACTION
end