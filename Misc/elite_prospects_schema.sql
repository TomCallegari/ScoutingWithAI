
-----------			DROP TABLES
DROP TABLE player_stats;
DROP TABLE meta_stats;
-----------


-----------			CREATE TABLES
CREATE TABLE meta_stats (
	id SERIAL PRIMARY KEY,
	ep_id INT,
	full_name VARCHAR,
	date_of_birth DATE,
	hometown VARCHAR,
	country VARCHAR,
	youth_team VARCHAR,
	position VARCHAR,
	height INT,
	weight INT,
	shoots VARCHAR(1)
);

CREATE TABLE player_stats (
	id SERIAL PRIMARY KEY,
	player_id INT NOT NULL,
	ep_id INT NOT NULL,
	season VARCHAR,
	team VARCHAR,
	league VARCHAR,
	games_played INT,
	goals INT,
	assists INT,
	penalty_min INT,
	plus_minus INT,
	FOREIGN KEY (player_id) REFERENCES meta_stats (id)
);
-----------


SELECT * FROM meta_stats;
SELECT * FROM player_stats;





