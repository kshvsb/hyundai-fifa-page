#!/bin/bash
# Export FIFA 2026 SQLite DB to data.json for the HTML frontend
cd "$(dirname "$0")"
DB="fifa2026.db"

sqlite3 -json "$DB" "
SELECT json_object(
  'id', t.id,
  'name', t.name,
  'short_code', t.short_code,
  'flag', t.flag_emoji,
  'group', t.group_id,
  'confederation', t.confederation,
  'is_host', t.is_host,
  'is_defending_champion', t.is_defending_champion
) as j FROM teams t ORDER BY t.group_id, t.id;
" | python3 -c "
import sys, json

rows = json.load(sys.stdin)
teams = [json.loads(r['j']) for r in rows]
teams_by_id = {t['id']: t for t in teams}
" 2>/dev/null

# Full export using python for proper JSON assembly
sqlite3 "$DB" << 'SQLEOF' > /dev/null
.mode json
.output /tmp/fifa_teams.json
SELECT id, name, short_code, flag_emoji as flag, group_id as 'group', confederation, is_host, is_defending_champion FROM teams ORDER BY group_id, id;
.output /tmp/fifa_venues.json
SELECT id, name, city, country, capacity, note FROM venues ORDER BY id;
.output /tmp/fifa_groups.json
SELECT id, name FROM groups_ ORDER BY id;
.output /tmp/fifa_matches.json
SELECT id, match_number, stage, group_id as 'group', home_team_id, away_team_id, home_placeholder, away_placeholder, venue_id, match_date, match_time_utc, home_score, away_score, status, minute FROM matches ORDER BY match_date, match_time_utc;
.output /tmp/fifa_standings.json
SELECT s.team_id, s.group_id as 'group', s.played, s.won, s.drawn, s.lost, s.goals_for, s.goals_against, s.goal_difference, s.points FROM standings s ORDER BY s.group_id, s.points DESC, s.goal_difference DESC;
.output /tmp/fifa_players.json
SELECT id, name, team_id, position, is_star FROM players ORDER BY team_id, is_star DESC;
.output /tmp/fifa_tournament.json
SELECT * FROM tournament;
SQLEOF

python3 << 'PYEOF'
import json

def load(path):
    with open(path) as f:
        return json.load(f)

data = {
    "tournament": load("/tmp/fifa_tournament.json")[0],
    "venues": load("/tmp/fifa_venues.json"),
    "groups": load("/tmp/fifa_groups.json"),
    "teams": load("/tmp/fifa_teams.json"),
    "matches": load("/tmp/fifa_matches.json"),
    "standings": load("/tmp/fifa_standings.json"),
    "players": load("/tmp/fifa_players.json"),
    "last_updated": "2026-05-25T18:00:00Z"
}

with open("data.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Exported data.json: {len(data['teams'])} teams, {len(data['matches'])} matches, {len(data['venues'])} venues, {len(data['players'])} players")
PYEOF
