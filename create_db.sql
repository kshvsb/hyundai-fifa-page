-- FIFA World Cup 2026 Database Schema & Seed Data
-- For Hyundai Bluelink FIFA Hub

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- ===== SCHEMA =====

CREATE TABLE IF NOT EXISTS tournament (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  year INTEGER NOT NULL,
  host_countries TEXT NOT NULL,
  start_date TEXT NOT NULL,
  end_date TEXT NOT NULL,
  total_teams INTEGER NOT NULL,
  total_matches INTEGER NOT NULL,
  format TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS venues (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  city TEXT NOT NULL,
  country TEXT NOT NULL,
  capacity INTEGER NOT NULL,
  note TEXT
);

CREATE TABLE IF NOT EXISTS groups_ (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS teams (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  short_code TEXT NOT NULL,
  flag_emoji TEXT NOT NULL,
  group_id TEXT REFERENCES groups_(id),
  confederation TEXT NOT NULL,
  is_host INTEGER DEFAULT 0,
  is_defending_champion INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS players (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  team_id INTEGER REFERENCES teams(id),
  position TEXT,
  is_star INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS matches (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  match_number INTEGER,
  stage TEXT NOT NULL,
  group_id TEXT REFERENCES groups_(id),
  home_team_id INTEGER REFERENCES teams(id),
  away_team_id INTEGER REFERENCES teams(id),
  home_placeholder TEXT,
  away_placeholder TEXT,
  venue_id INTEGER REFERENCES venues(id),
  match_date TEXT NOT NULL,
  match_time_utc TEXT,
  home_score INTEGER,
  away_score INTEGER,
  status TEXT DEFAULT 'scheduled',
  minute TEXT
);

CREATE TABLE IF NOT EXISTS match_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  match_id INTEGER REFERENCES matches(id),
  event_type TEXT NOT NULL,
  minute INTEGER,
  player_id INTEGER REFERENCES players(id),
  team_id INTEGER REFERENCES teams(id),
  detail TEXT
);

CREATE TABLE IF NOT EXISTS standings (
  team_id INTEGER REFERENCES teams(id),
  group_id TEXT REFERENCES groups_(id),
  played INTEGER DEFAULT 0,
  won INTEGER DEFAULT 0,
  drawn INTEGER DEFAULT 0,
  lost INTEGER DEFAULT 0,
  goals_for INTEGER DEFAULT 0,
  goals_against INTEGER DEFAULT 0,
  goal_difference INTEGER DEFAULT 0,
  points INTEGER DEFAULT 0,
  PRIMARY KEY (team_id, group_id)
);

CREATE TABLE IF NOT EXISTS top_scorers (
  player_id INTEGER REFERENCES players(id),
  goals INTEGER DEFAULT 0,
  assists INTEGER DEFAULT 0,
  PRIMARY KEY (player_id)
);

-- ===== SEED DATA =====

-- Tournament
INSERT INTO tournament VALUES (1, 'FIFA World Cup 26™', 2026, 'United States, Mexico, Canada', '2026-06-11', '2026-07-19', 48, 104, '12 groups of 4, top 2 + 8 best 3rd advance to R32, then knockout to Final');

-- Venues (16 stadiums)
INSERT INTO venues (id, name, city, country, capacity, note) VALUES
(1, 'Estadio Azteca', 'Mexico City', 'Mexico', 87523, 'Opening match; 3rd WC at this stadium'),
(2, 'Estadio Akron', 'Guadalajara (Zapopan)', 'Mexico', 49850, NULL),
(3, 'Estadio BBVA', 'Monterrey (Guadalupe)', 'Mexico', 53500, NULL),
(4, 'BMO Field', 'Toronto', 'Canada', 45736, 'Capacity expanded for WC'),
(5, 'BC Place', 'Vancouver', 'Canada', 54500, NULL),
(6, 'MetLife Stadium', 'East Rutherford (New York/NJ)', 'United States', 82500, 'Hosts the Final'),
(7, 'SoFi Stadium', 'Los Angeles', 'United States', 70240, 'Hosts semi-final'),
(8, 'AT&T Stadium', 'Arlington (Dallas)', 'United States', 80000, 'Hosts semi-final; most matches (9)'),
(9, 'Mercedes-Benz Stadium', 'Atlanta', 'United States', 71000, NULL),
(10, 'NRG Stadium', 'Houston', 'United States', 72220, NULL),
(11, 'Lincoln Financial Field', 'Philadelphia', 'United States', 69796, NULL),
(12, 'Hard Rock Stadium', 'Miami', 'United States', 64767, 'Hosts 3rd-place match'),
(13, 'Lumen Field', 'Seattle', 'United States', 69000, NULL),
(14, 'Levi''s Stadium', 'Santa Clara (San Francisco Bay)', 'United States', 68500, NULL),
(15, 'Arrowhead Stadium', 'Kansas City', 'United States', 76416, NULL),
(16, 'Gillette Stadium', 'Foxborough (Boston)', 'United States', 65878, NULL);

-- Groups (A-L)
INSERT INTO groups_ VALUES ('A', 'Group A'), ('B', 'Group B'), ('C', 'Group C'), ('D', 'Group D'),
('E', 'Group E'), ('F', 'Group F'), ('G', 'Group G'), ('H', 'Group H'),
('I', 'Group I'), ('J', 'Group J'), ('K', 'Group K'), ('L', 'Group L');

-- Teams (48)
-- Group A
INSERT INTO teams (id, name, short_code, flag_emoji, group_id, confederation, is_host) VALUES
(1, 'Mexico', 'MEX', '🇲🇽', 'A', 'CONCACAF', 1),
(2, 'South Africa', 'RSA', '🇿🇦', 'A', 'CAF', 0),
(3, 'South Korea', 'KOR', '🇰🇷', 'A', 'AFC', 0),
(4, 'Czech Republic', 'CZE', '🇨🇿', 'A', 'UEFA', 0);

-- Group B
INSERT INTO teams (id, name, short_code, flag_emoji, group_id, confederation, is_host) VALUES
(5, 'Canada', 'CAN', '🇨🇦', 'B', 'CONCACAF', 1),
(6, 'Italy', 'ITA', '🇮🇹', 'B', 'UEFA', 0),
(7, 'Qatar', 'QAT', '🇶🇦', 'B', 'AFC', 0),
(8, 'Switzerland', 'SUI', '🇨🇭', 'B', 'UEFA', 0);

-- Group C
INSERT INTO teams (id, name, short_code, flag_emoji, group_id, confederation, is_host) VALUES
(9, 'Brazil', 'BRA', '🇧🇷', 'C', 'CONMEBOL', 0),
(10, 'Morocco', 'MAR', '🇲🇦', 'C', 'CAF', 0),
(11, 'Haiti', 'HAI', '🇭🇹', 'C', 'CONCACAF', 0),
(12, 'Scotland', 'SCO', '🏴󠁧󠁢󠁳󠁣󠁴󠁿', 'C', 'UEFA', 0);

-- Group D
INSERT INTO teams (id, name, short_code, flag_emoji, group_id, confederation, is_host) VALUES
(13, 'United States', 'USA', '🇺🇸', 'D', 'CONCACAF', 1),
(14, 'Paraguay', 'PAR', '🇵🇾', 'D', 'CONMEBOL', 0),
(15, 'Australia', 'AUS', '🇦🇺', 'D', 'AFC', 0),
(16, 'Türkiye', 'TUR', '🇹🇷', 'D', 'UEFA', 0);

-- Group E
INSERT INTO teams (id, name, short_code, flag_emoji, group_id, confederation, is_host) VALUES
(17, 'Germany', 'GER', '🇩🇪', 'E', 'UEFA', 0),
(18, 'Curaçao', 'CUW', '🇨🇼', 'E', 'CONCACAF', 0),
(19, 'Ivory Coast', 'CIV', '🇨🇮', 'E', 'CAF', 0),
(20, 'Ecuador', 'ECU', '🇪🇨', 'E', 'CONMEBOL', 0);

-- Group F
INSERT INTO teams (id, name, short_code, flag_emoji, group_id, confederation, is_host) VALUES
(21, 'Netherlands', 'NED', '🇳🇱', 'F', 'UEFA', 0),
(22, 'Japan', 'JPN', '🇯🇵', 'F', 'AFC', 0),
(23, 'Poland', 'POL', '🇵🇱', 'F', 'UEFA', 0),
(24, 'Tunisia', 'TUN', '🇹🇳', 'F', 'CAF', 0);

-- Group G
INSERT INTO teams (id, name, short_code, flag_emoji, group_id, confederation, is_host) VALUES
(25, 'Belgium', 'BEL', '🇧🇪', 'G', 'UEFA', 0),
(26, 'Egypt', 'EGY', '🇪🇬', 'G', 'CAF', 0),
(27, 'Iran', 'IRN', '🇮🇷', 'G', 'AFC', 0),
(28, 'New Zealand', 'NZL', '🇳🇿', 'G', 'OFC', 0);

-- Group H
INSERT INTO teams (id, name, short_code, flag_emoji, group_id, confederation, is_host) VALUES
(29, 'Spain', 'ESP', '🇪🇸', 'H', 'UEFA', 0),
(30, 'Cape Verde', 'CPV', '🇨🇻', 'H', 'CAF', 0),
(31, 'Saudi Arabia', 'KSA', '🇸🇦', 'H', 'AFC', 0),
(32, 'Uruguay', 'URU', '🇺🇾', 'H', 'CONMEBOL', 0);

-- Group I
INSERT INTO teams (id, name, short_code, flag_emoji, group_id, confederation, is_host) VALUES
(33, 'France', 'FRA', '🇫🇷', 'I', 'UEFA', 0),
(34, 'Senegal', 'SEN', '🇸🇳', 'I', 'CAF', 0),
(35, 'Iraq', 'IRQ', '🇮🇶', 'I', 'AFC', 0),
(36, 'Norway', 'NOR', '🇳🇴', 'I', 'UEFA', 0);

-- Group J
INSERT INTO teams (id, name, short_code, flag_emoji, group_id, confederation, is_host) VALUES
(37, 'Argentina', 'ARG', '🇦🇷', 'J', 'CONMEBOL', 0),
(38, 'Algeria', 'ALG', '🇩🇿', 'J', 'CAF', 0),
(39, 'Austria', 'AUT', '🇦🇹', 'J', 'UEFA', 0),
(40, 'Jordan', 'JOR', '🇯🇴', 'J', 'AFC', 0);

-- Group K
INSERT INTO teams (id, name, short_code, flag_emoji, group_id, confederation, is_host) VALUES
(41, 'Portugal', 'POR', '🇵🇹', 'K', 'UEFA', 0),
(42, 'DR Congo', 'COD', '🇨🇩', 'K', 'CAF', 0),
(43, 'Uzbekistan', 'UZB', '🇺🇿', 'K', 'AFC', 0),
(44, 'Colombia', 'COL', '🇨🇴', 'K', 'CONMEBOL', 0);

-- Group L
INSERT INTO teams (id, name, short_code, flag_emoji, group_id, confederation, is_host) VALUES
(45, 'England', 'ENG', '🏴󠁧󠁢󠁥󠁮󠁧󠁿', 'L', 'UEFA', 0),
(46, 'Croatia', 'CRO', '🇭🇷', 'L', 'UEFA', 0),
(47, 'Ghana', 'GHA', '🇬🇭', 'L', 'CAF', 0),
(48, 'Panama', 'PAN', '🇵🇦', 'L', 'CONCACAF', 0);

-- Defending champion flag
UPDATE teams SET is_defending_champion = 1 WHERE id = 37;

-- Standings (initialize all teams at 0)
INSERT INTO standings (team_id, group_id) SELECT id, group_id FROM teams;

-- Matches — Group Stage Matchday 1 (June 11-14)
INSERT INTO matches (match_number, stage, group_id, home_team_id, away_team_id, venue_id, match_date, match_time_utc, status) VALUES
(1, 'Group Stage MD1', 'A', 1, 2, 1, '2026-06-11', '01:00', 'scheduled'),
(2, 'Group Stage MD1', 'A', 3, 4, 2, '2026-06-12', '08:00', 'scheduled'),
(3, 'Group Stage MD1', 'B', 5, 6, 4, '2026-06-12', '01:00', 'scheduled'),
(4, 'Group Stage MD1', 'D', 13, 14, 7, '2026-06-13', '07:00', 'scheduled'),
(5, 'Group Stage MD1', 'B', 7, 8, 14, '2026-06-13', '01:00', 'scheduled'),
(6, 'Group Stage MD1', 'C', 9, 10, 6, '2026-06-13', '04:00', 'scheduled'),
(7, 'Group Stage MD1', 'C', 11, 12, 16, '2026-06-14', '07:00', 'scheduled'),
(8, 'Group Stage MD1', 'D', 15, 16, 5, '2026-06-14', '10:00', 'scheduled'),
(9, 'Group Stage MD1', 'E', 17, 18, 10, '2026-06-14', '23:00', 'scheduled'),
(10, 'Group Stage MD1', 'F', 21, 22, 8, '2026-06-15', '02:00', 'scheduled');

-- Matches — Group Stage Matchday 1 cont'd (June 15-17)
INSERT INTO matches (match_number, stage, group_id, home_team_id, away_team_id, venue_id, match_date, match_time_utc, status) VALUES
(11, 'Group Stage MD1', 'E', 19, 20, 11, '2026-06-15', '05:00', 'scheduled'),
(12, 'Group Stage MD1', 'F', 23, 24, 3, '2026-06-15', '08:00', 'scheduled'),
(13, 'Group Stage MD1', 'H', 29, 30, 9, '2026-06-15', '22:00', 'scheduled'),
(14, 'Group Stage MD1', 'G', 25, 26, 13, '2026-06-16', '01:00', 'scheduled'),
(15, 'Group Stage MD1', 'H', 31, 32, 12, '2026-06-16', '04:00', 'scheduled'),
(16, 'Group Stage MD1', 'G', 27, 28, 7, '2026-06-16', '07:00', 'scheduled'),
(17, 'Group Stage MD1', 'I', 33, 34, 6, '2026-06-17', '01:00', 'scheduled'),
(18, 'Group Stage MD1', 'I', 35, 36, 16, '2026-06-17', '04:00', 'scheduled'),
(19, 'Group Stage MD1', 'J', 37, 38, 15, '2026-06-17', '07:00', 'scheduled'),
(20, 'Group Stage MD1', 'J', 39, 40, 14, '2026-06-17', '10:00', 'scheduled'),
(21, 'Group Stage MD1', 'K', 41, 42, 10, '2026-06-17', '23:00', 'scheduled'),
(22, 'Group Stage MD1', 'L', 45, 46, 8, '2026-06-18', '02:00', 'scheduled');

-- Matches — remaining MD1
INSERT INTO matches (match_number, stage, group_id, home_team_id, away_team_id, venue_id, match_date, match_time_utc, status) VALUES
(23, 'Group Stage MD1', 'K', 43, 44, 11, '2026-06-18', '05:00', 'scheduled'),
(24, 'Group Stage MD1', 'L', 47, 48, 9, '2026-06-18', '08:00', 'scheduled');

-- Knockout stage placeholder matches
INSERT INTO matches (match_number, stage, home_placeholder, away_placeholder, venue_id, match_date, status) VALUES
(89, 'Round of 32', '1A', '2B/3rd', 8, '2026-06-28', 'scheduled'),
(90, 'Round of 32', '1B', '2C/3rd', 6, '2026-06-28', 'scheduled'),
(97, 'Round of 16', 'W89', 'W90', 8, '2026-07-04', 'scheduled'),
(101, 'Quarter-final', 'W-QF1', 'W-QF2', 7, '2026-07-09', 'scheduled'),
(102, 'Quarter-final', 'W-QF3', 'W-QF4', 8, '2026-07-10', 'scheduled'),
(103, 'Semi-final', 'W-SF1', 'W-SF2', 8, '2026-07-14', 'scheduled'),
(104, 'Semi-final', 'W-SF3', 'W-SF4', 7, '2026-07-15', 'scheduled'),
(105, 'Third-place', 'L-SF1', 'L-SF2', 12, '2026-07-18', 'scheduled'),
(106, 'Final', 'W-SF1', 'W-SF2', 6, '2026-07-19', 'scheduled');

-- Key players
INSERT INTO players (name, team_id, position, is_star) VALUES
('Hirving Lozano', 1, 'Forward', 1), ('Edson Álvarez', 1, 'Midfielder', 1), ('Santiago Giménez', 1, 'Forward', 1),
('Son Heung-min', 3, 'Forward', 1), ('Lee Kang-in', 3, 'Midfielder', 1), ('Kim Min-jae', 3, 'Defender', 1),
('Gianluigi Donnarumma', 6, 'Goalkeeper', 1), ('Nicolò Barella', 6, 'Midfielder', 1), ('Federico Chiesa', 6, 'Forward', 1),
('Granit Xhaka', 8, 'Midfielder', 1),
('Vinícius Jr.', 9, 'Forward', 1), ('Rodrygo', 9, 'Forward', 1), ('Endrick', 9, 'Forward', 1),
('Achraf Hakimi', 10, 'Defender', 1), ('Hakim Ziyech', 10, 'Midfielder', 1),
('Christian Pulisic', 13, 'Forward', 1), ('Weston McKennie', 13, 'Midfielder', 1), ('Gio Reyna', 13, 'Midfielder', 1),
('Florian Wirtz', 17, 'Midfielder', 1), ('Jamal Musiala', 17, 'Midfielder', 1), ('Kai Havertz', 17, 'Forward', 1),
('Cody Gakpo', 21, 'Forward', 1), ('Xavi Simons', 21, 'Midfielder', 1), ('Virgil van Dijk', 21, 'Defender', 1),
('Takefusa Kubo', 22, 'Forward', 1), ('Kaoru Mitoma', 22, 'Forward', 1),
('Kevin De Bruyne', 25, 'Midfielder', 1), ('Jérémy Doku', 25, 'Forward', 1),
('Mohamed Salah', 26, 'Forward', 1),
('Lamine Yamal', 29, 'Forward', 1), ('Pedri', 29, 'Midfielder', 1), ('Rodri', 29, 'Midfielder', 1),
('Federico Valverde', 32, 'Midfielder', 1), ('Darwin Núñez', 32, 'Forward', 1),
('Kylian Mbappé', 33, 'Forward', 1), ('Antoine Griezmann', 33, 'Forward', 1), ('Aurélien Tchouaméni', 33, 'Midfielder', 1),
('Sadio Mané', 34, 'Forward', 1),
('Erling Haaland', 36, 'Forward', 1), ('Martin Ødegaard', 36, 'Midfielder', 1),
('Lionel Messi', 37, 'Forward', 1), ('Julián Álvarez', 37, 'Forward', 1), ('Enzo Fernández', 37, 'Midfielder', 1),
('Cristiano Ronaldo', 41, 'Forward', 1), ('Bruno Fernandes', 41, 'Midfielder', 1), ('Rafael Leão', 41, 'Forward', 1),
('Luis Díaz', 44, 'Forward', 1), ('Jhon Arias', 44, 'Forward', 1),
('Jude Bellingham', 45, 'Forward', 1), ('Bukayo Saka', 45, 'Forward', 1), ('Phil Foden', 45, 'Forward', 1),
('Luka Modrić', 46, 'Midfielder', 1), ('Joško Gvardiol', 46, 'Defender', 1),
('Victor Osimhen', 47, 'Forward', 0);
