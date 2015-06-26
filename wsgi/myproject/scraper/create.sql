create table item (item_id INTEGER NOT NULL primary key autoincrement,color varchar(30) NOT NULL,size char NOT NULL,typ varchar(35),fabric integer(2),styling varchar(30),brand varchar(35));

create table bstructure(item_id integer references item(item_id)on delete cascade on update cascade,s_id INTEGER primary key autoincrement,typ varchar(30) NOT NULL,fav_color varchar(100) NOT NULL);

 
