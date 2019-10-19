---- drop ----
drop table if exists t_user;

drop table if exists t_effector;

---- create ----
create table if not exists t_user (
    private_id int(20) auto_increment,
    public_id varchar(20) not null,
    password varchar(20) not null,
    created_at datetime default current_timestamp,
    latest_updated_at datetime on update current_timestamp,
    primary key(private_id)
) default charset = utf8 collate utf8_bin;

create table if not exists t_effector (
    id int(20) auto_increment,
    creator_id (20) not null,
    code text not null,
    created_at datetime default current_timestamp,
    latest_updated_at datetime on update current_timestamp,
    primary key(id)
) default charset = utf8 collate utf8_bin;