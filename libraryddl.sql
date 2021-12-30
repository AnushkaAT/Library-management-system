create table Book(
    book_code varchar(10) NOT NULL,
    name varchar(30),
    author varchar(20),
    publisher varchar(20),
    pages integer,
    keyword varchar(20),
    rack varchar(10),
    issued integer,
    primary key (book_code)
);

create table User(
    user_id varchar(10),
    role varchar(10),
    name varchar(30),
    dept varchar(20),
    phone varchar(10),
    primary key (user_id)
);

create table Issue(
    user_id varchar(10),
    book_code varchar(10),
    issued_on Date,
    return_date Date,
    primary key (user_id, book_code),
    foreign key (user_id) references User(user_id) on delete cascade,
    foreign key (book_code) references Book(book_code) on delete cascade
);

create table Login_details(
    user_id varchar(10),
    password varchar(10),
    login_time datetime,
    primary key (user_id, password),
    foreign key (user_id) references User(user_id) on delete cascade
);

create table Favorite(
    user_id varchar(10),
    book_code varchar(10),
    primary key (user_id, book_code),
    foreign key (user_id) references User(user_id) on delete cascade,
    foreign key (book_code) references Book(book_code) on delete cascade
)