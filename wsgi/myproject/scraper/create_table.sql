-- create table expert_advice (
	-- item_id integer	foreign key(item_id) on delete cascade on update cascade references item (item_id),
	-- s_id integer foreign key(s_id) on delete cascade on update cascade references b_structure (s_id),
	-- comments char (100)
-- );
-- PRAGMA foreign_keys = ON;

create table expert_advice (
	item_id integer	references item (item_id) on delete cascade on update cascade,
	s_id integer references bstructure (s_id) on delete cascade on update cascade,
	comments char (100)
);
create table users (
	user_id integer primary key autoincrement,
	user_name char (100)
);

create table forums (
	user_id integer	references users (user_id) on delete cascade on update cascade,
	comments char (100),
	vote     integer,
	item_id integer	references item (item_id) on delete cascade on update cascade
);

