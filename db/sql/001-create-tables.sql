---- drop ----
drop table if exists test_table;

---- create ----
create table if not exists test_table (
    id int(20) auto_increment,
    name varchar(20) not null,
    created_at datetime default null,
    updated_at datetime default null,
    primary key (id)
) default charset = utf8 collate = utf8_bin;