create table if not exists main (
    id bigint unsigned,
    guild bigint unsigned,
    wins int default '0',
    losses int default '0',
    w_l_ratio double default '0.0',
    moyai int default '0'
);