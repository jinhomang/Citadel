drop table if exists user;
create table user (
	userid integer primary key autoincrement,
	username string not null,
	email string not null,
	pw_hash string not null
);


drop table if exists follower;
create table follower (
	who_id integer
	whom_id integer
);

drop table if exists message;
create table message (
	messageid integer primary key autoincrement,
	title string not null,
	text string not null
);

