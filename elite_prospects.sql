
select version();
create database chl_players;
show databases;

use chl_players;

select * from meta_data;
delete from meta_data;

select * from yearly_player_stats;
delete from yearly_player_stats;

select * 
from yearly_player_stats
where ep_id = 9223;