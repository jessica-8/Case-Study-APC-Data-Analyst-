
CREATE TABLE IF NOT EXISTS season (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    season_id INTEGER UNIQUE,
    season TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS club (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    club_id INTEGER UNIQUE,
    club_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS competition (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competition_id INTEGER UNIQUE,
    competition_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS player (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER UNIQUE,
    full_name TEXT NOT NULL,
    date_of_birth TEXT,
    nationality TEXT,
    position_main TEXT,
    position_other TEXT,
    height_cm TEXT,
    foot TEXT
);

CREATE TABLE IF NOT EXISTS standings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    club_id INTEGER UNIQUE,
    club_name TEXT NOT NULL,
    competition_id TEXT,
    league TEXT,
    league_position TEXT,
    season TEXT,
    season_id TEXT,
    FOREIGN KEY (season_id) REFERENCES season (season_id) ON DELETE SET NULL,
    FOREIGN KEY (club_id) REFERENCES club (club_id) ON DELETE SET NULL,
    FOREIGN KEY (competition_id) REFERENCES competition (competition_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS transfers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transfer_id INTEGER UNIQUE,
    transfer_date TEXT,
    transfer_type TEXT,
    season_id INTEGER,
    player_id INTEGER,
    player_age_at_transfer INTEGER,
    transfer_fee_euro INTEGER,
    transfer_fee_million INTEGER, 
    market_value_euro INTEGER,
    market_value_million INTEGER,
    from_club_id INTEGER,
    to_club_id INTEGER,
    from_competition_id INTEGER,
    to_competition_id INTEGER,
    FOREIGN KEY (player_id) REFERENCES player (player_id) ON DELETE CASCADE,
    FOREIGN KEY (season_id) REFERENCES season (season_id) ON DELETE SET NULL,
    FOREIGN KEY (from_club_id) REFERENCES club (club_id) ON DELETE SET NULL,
    FOREIGN KEY (to_club_id) REFERENCES club (club_id) ON DELETE SET NULL,
    FOREIGN KEY (from_competition_id) REFERENCES competition (competition_id) ON DELETE SET NULL,
    FOREIGN KEY (to_competition_id) REFERENCES competition (competition_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS playerStats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    season_id INTEGER,
    club_id INTEGER,
    competition_id TEXT,
    FOREIGN KEY (player_id) REFERENCES player (player_id) ON DELETE CASCADE,
    FOREIGN KEY (season_id) REFERENCES season (season_id) ON DELETE SET NULL,
    FOREIGN KEY (club_id) REFERENCES club (club_id) ON DELETE SET NULL,
    FOREIGN KEY (competition_id) REFERENCES competition (competition_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS teamStats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    season_id INTEGER,
    club_id INTEGER,
    club_name TEXT, 
    League_Position INTEGER,
    FOREIGN KEY (player_id) REFERENCES player (player_id) ON DELETE CASCADE,
    FOREIGN KEY (season_id) REFERENCES season (season_id) ON DELETE SET NULL,
    FOREIGN KEY (club_id) REFERENCES club (club_id) ON DELETE SET NULL
);
