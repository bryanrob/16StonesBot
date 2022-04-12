create table if not exists main (
    id int,
    guild int,
    wins int default '0',
    losses int default '0',
    w_l_ratio double default '0',
    moyai int default '0'
);