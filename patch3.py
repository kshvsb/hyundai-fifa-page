#!/usr/bin/env python3
"""Patch 3: Fix match card proportions, update 48 teams to official FIFA groups, improve standings."""
import re, json

with open('/Users/keshav/Documents/Claude/hyundai-fifa-page/index.html', 'r') as f:
    html = f.read()

# ─── 1. FIX MATCH CARD — time too big, everything bold ───
old_sched_css = """  .schedule-card{
    background:var(--card);border-radius:14px;padding:18px 16px 14px;border:1px solid var(--line);
    margin-bottom:8px;text-align:center;
  }
  .sched-matchup{
    display:flex;align-items:center;justify-content:center;gap:0;margin-bottom:8px;
  }
  .sched-team{
    display:flex;align-items:center;gap:8px;min-width:0;flex:1;
  }
  .sched-team.home{justify-content:flex-end;}
  .sched-team.away{justify-content:flex-start;}
  .sched-team .team-code{font-size:14px;font-weight:700;color:var(--text);}
  .sched-team .team-flag{font-size:26px;line-height:1;}
  .sched-center{
    min-width:80px;text-align:center;padding:0 8px;
  }
  .sched-center .sched-time{
    font-size:22px;font-weight:800;color:var(--text);
    letter-spacing:-0.5px;
  }
  .sched-center .sched-score{
    font-size:26px;font-weight:900;color:var(--text);
    letter-spacing:2px;
  }
  .sched-info{
    font-size:11px;color:var(--muted);line-height:1.5;
  }
  .sched-info .sched-stage{font-weight:600;color:var(--hyundai-accent);}
  .sched-info .sched-venue{font-weight:400;}"""

new_sched_css = """  .schedule-card{
    background:var(--card);border-radius:14px;padding:16px;border:1px solid var(--line);
    margin-bottom:8px;
  }
  .sched-matchup{
    display:flex;align-items:center;justify-content:center;gap:0;margin-bottom:10px;
  }
  .sched-team{
    display:flex;align-items:center;gap:10px;min-width:0;flex:1;
  }
  .sched-team.home{justify-content:flex-end;}
  .sched-team.away{justify-content:flex-start;flex-direction:row;}
  .sched-team .team-code{font-size:15px;font-weight:600;color:var(--text);}
  .sched-team .team-flag{font-size:28px;line-height:1;}
  .sched-center{
    min-width:76px;text-align:center;padding:0 6px;
  }
  .sched-center .sched-time{
    font-size:16px;font-weight:700;color:var(--text);
    letter-spacing:0px;
  }
  .sched-center .sched-score{
    font-size:22px;font-weight:800;color:var(--text);
    letter-spacing:1px;
  }
  .sched-info{
    font-size:11px;color:var(--muted);line-height:1.5;text-align:center;
  }
  .sched-info .sched-stage{font-weight:600;color:var(--hyundai-accent);}
  .sched-info .sched-venue{font-weight:400;}"""

html = html.replace(old_sched_css, new_sched_css)

# ─── 2. UPDATE ALL 48 TEAMS — Official FIFA 2026 World Cup Draw ───
m = re.search(r'window\.__FIFA_DATA\s*=\s*({.*?});', html, re.DOTALL)
data = json.loads(m.group(1))

# Official FIFA 2026 group compositions from fifa.com
official_groups = {
    'A': [('Mexico','MEX','🇲🇽'), ('South Africa','RSA','🇿🇦'), ('South Korea','KOR','🇰🇷'), ('Czechia','CZE','🇨🇿')],
    'B': [('Canada','CAN','🇨🇦'), ('Bosnia and Herzegovina','BIH','🇧🇦'), ('Qatar','QAT','🇶🇦'), ('Switzerland','SUI','🇨🇭')],
    'C': [('Brazil','BRA','🇧🇷'), ('Morocco','MAR','🇲🇦'), ('Haiti','HAI','🇭🇹'), ('Scotland','SCO','🏴󠁧󠁢󠁳󠁣󠁴󠁿')],
    'D': [('USA','USA','🇺🇸'), ('Paraguay','PAR','🇵🇾'), ('Australia','AUS','🇦🇺'), ('Türkiye','TUR','🇹🇷')],
    'E': [('Germany','GER','🇩🇪'), ('Curaçao','CUW','🇨🇼'), ("Côte d'Ivoire",'CIV','🇨🇮'), ('Ecuador','ECU','🇪🇨')],
    'F': [('Netherlands','NED','🇳🇱'), ('Japan','JPN','🇯🇵'), ('Sweden','SWE','🇸🇪'), ('Tunisia','TUN','🇹🇳')],
    'G': [('Belgium','BEL','🇧🇪'), ('Egypt','EGY','🇪🇬'), ('IR Iran','IRN','🇮🇷'), ('New Zealand','NZL','🇳🇿')],
    'H': [('Spain','ESP','🇪🇸'), ('Cabo Verde','CPV','🇨🇻'), ('Saudi Arabia','KSA','🇸🇦'), ('Uruguay','URU','🇺🇾')],
    'I': [('France','FRA','🇫🇷'), ('Senegal','SEN','🇸🇳'), ('Iraq','IRQ','🇮🇶'), ('Norway','NOR','🇳🇴')],
    'J': [('Argentina','ARG','🇦🇷'), ('Algeria','ALG','🇩🇿'), ('Austria','AUT','🇦🇹'), ('Jordan','JOR','🇯🇴')],
    'K': [('Portugal','POR','🇵🇹'), ('Congo DR','COD','🇨🇩'), ('Uzbekistan','UZB','🇺🇿'), ('Colombia','COL','🇨🇴')],
    'L': [('England','ENG','🏴󠁧󠁢󠁥󠁮󠁧󠁿'), ('Croatia','CRO','🇭🇷'), ('Ghana','GHA','🇬🇭'), ('Panama','PAN','🇵🇦')],
}

# Build fresh teams list
new_teams = []
team_id = 1
group_team_map = {}  # group -> [team_ids]
for group_letter in 'ABCDEFGHIJKL':
    group_team_map[group_letter] = []
    for name, code, flag in official_groups[group_letter]:
        new_teams.append({
            'id': team_id,
            'name': name,
            'short_code': code,
            'flag': flag,
            'group': group_letter,
            'confederation': '',
        })
        group_team_map[group_letter].append(team_id)
        team_id += 1

data['teams'] = new_teams

# Update groups
data['groups'] = [{'id': g, 'name': f'Group {g}'} for g in 'ABCDEFGHIJKL']

# Update standings
new_standings = []
for group_letter in 'ABCDEFGHIJKL':
    for tid in group_team_map[group_letter]:
        new_standings.append({
            'team_id': tid,
            'group': group_letter,
            'played': 0, 'won': 0, 'drawn': 0, 'lost': 0,
            'goals_for': 0, 'goals_against': 0,
            'goal_difference': 0, 'points': 0
        })
data['standings'] = new_standings

# Update group matches — 3 match days per group (6 matches per group = 72 total)
# Keep knockout matches, replace group matches
ko_matches = [x for x in data['matches'] if 'Group' not in x.get('stage', 'Group')]
new_group_matches = []
match_id = 1
match_num = 1

# Venues for group stage
venues_by_group = {
    'A': [1, 2], 'B': [4, 14], 'C': [9, 3], 'D': [13, 8],
    'E': [7, 15], 'F': [6, 10], 'G': [11, 16], 'H': [12, 5],
    'I': [8, 1], 'J': [6, 7], 'K': [13, 9], 'L': [14, 11],
}

# Schedule: MD1 (Jun 11-14), MD2 (Jun 16-19), MD3 (Jun 21-24)
md_dates = {
    'A': ['2026-06-11','2026-06-16','2026-06-21'],
    'B': ['2026-06-12','2026-06-17','2026-06-22'],
    'C': ['2026-06-12','2026-06-17','2026-06-22'],
    'D': ['2026-06-13','2026-06-18','2026-06-23'],
    'E': ['2026-06-13','2026-06-18','2026-06-23'],
    'F': ['2026-06-14','2026-06-19','2026-06-24'],
    'G': ['2026-06-14','2026-06-19','2026-06-24'],
    'H': ['2026-06-15','2026-06-20','2026-06-25'],
    'I': ['2026-06-15','2026-06-20','2026-06-25'],
    'J': ['2026-06-16','2026-06-21','2026-06-26'],
    'K': ['2026-06-16','2026-06-21','2026-06-26'],
    'L': ['2026-06-17','2026-06-22','2026-06-27'],
}

md_times = ['01:00','07:00','13:00','19:00']  # UTC times spread across the day

for group_letter in 'ABCDEFGHIJKL':
    tids = group_team_map[group_letter]
    vids = venues_by_group[group_letter]
    dates = md_dates[group_letter]

    # MD1: 1v3, 2v4
    matchups = [
        (tids[0], tids[2], dates[0], md_times[(match_num-1) % 4], vids[0]),
        (tids[1], tids[3], dates[0], md_times[(match_num) % 4], vids[1]),
        # MD2: 1v4, 2v3
        (tids[0], tids[3], dates[1], md_times[(match_num+1) % 4], vids[1]),
        (tids[1], tids[2], dates[1], md_times[(match_num+2) % 4], vids[0]),
        # MD3: 1v2, 3v4
        (tids[0], tids[1], dates[2], md_times[0], vids[0]),
        (tids[2], tids[3], dates[2], md_times[0], vids[1]),
    ]

    for home, away, date, time, vid in matchups:
        new_group_matches.append({
            'id': match_id,
            'match_number': match_num,
            'stage': 'Group Stage',
            'group': group_letter,
            'home_team_id': home,
            'away_team_id': away,
            'home_placeholder': None,
            'away_placeholder': None,
            'venue_id': vid,
            'match_date': date,
            'match_time_utc': time,
            'home_score': None,
            'away_score': None,
            'status': 'scheduled',
            'minute': None,
        })
        match_id += 1
        match_num += 1

# Renumber knockout matches to continue from group matches
for i, km in enumerate(ko_matches):
    km['id'] = match_id + i

data['matches'] = new_group_matches + ko_matches

# Update players to reference correct team IDs
# Map old team names to new team IDs
name_to_new_id = {}
for t in new_teams:
    name_to_new_id[t['name']] = t['id']
    name_to_new_id[t['short_code']] = t['id']

# Simple name mappings for common variants
name_to_new_id['Czech Republic'] = name_to_new_id.get('Czechia', 4)
name_to_new_id['Italy'] = None  # Italy not in tournament
name_to_new_id['Bosnia'] = name_to_new_id.get('Bosnia and Herzegovina')

# Keep only players whose teams are in the tournament
# For now, clear players and we'll re-add key stars
star_players = [
    # Group A
    {'name':'Raúl Jiménez','position':'Forward','team_id':1,'is_star':1},
    {'name':'Santiago Giménez','position':'Forward','team_id':1,'is_star':1},
    {'name':'Edson Álvarez','position':'Midfielder','team_id':1,'is_star':1},
    {'name':'Percy Tau','position':'Forward','team_id':2,'is_star':1},
    {'name':'Son Heung-min','position':'Forward','team_id':3,'is_star':1},
    {'name':'Kim Min-jae','position':'Defender','team_id':3,'is_star':1},
    {'name':'Patrik Schick','position':'Forward','team_id':4,'is_star':1},
    # Group B
    {'name':'Alphonso Davies','position':'Defender','team_id':5,'is_star':1},
    {'name':'Jonathan David','position':'Forward','team_id':5,'is_star':1},
    {'name':'Edin Džeko','position':'Forward','team_id':6,'is_star':1},
    {'name':'Akram Afif','position':'Forward','team_id':7,'is_star':1},
    {'name':'Granit Xhaka','position':'Midfielder','team_id':8,'is_star':1},
    # Group C
    {'name':'Vinícius Jr','position':'Forward','team_id':9,'is_star':1},
    {'name':'Rodrygo','position':'Forward','team_id':9,'is_star':1},
    {'name':'Endrick','position':'Forward','team_id':9,'is_star':1},
    {'name':'Achraf Hakimi','position':'Defender','team_id':10,'is_star':1},
    {'name':'Hakim Ziyech','position':'Midfielder','team_id':10,'is_star':1},
    {'name':'Scott McTominay','position':'Midfielder','team_id':12,'is_star':1},
    # Group D
    {'name':'Christian Pulisic','position':'Forward','team_id':13,'is_star':1},
    {'name':'Weston McKennie','position':'Midfielder','team_id':13,'is_star':1},
    {'name':'Miguel Almirón','position':'Forward','team_id':14,'is_star':1},
    # Group E
    {'name':'Florian Wirtz','position':'Midfielder','team_id':17,'is_star':1},
    {'name':'Jamal Musiala','position':'Midfielder','team_id':17,'is_star':1},
    {'name':'Kai Havertz','position':'Forward','team_id':17,'is_star':1},
    {'name':'Moisés Caicedo','position':'Midfielder','team_id':20,'is_star':1},
    # Group F
    {'name':'Cody Gakpo','position':'Forward','team_id':21,'is_star':1},
    {'name':'Virgil van Dijk','position':'Defender','team_id':21,'is_star':1},
    {'name':'Takefusa Kubo','position':'Forward','team_id':22,'is_star':1},
    {'name':'Wataru Endo','position':'Midfielder','team_id':22,'is_star':1},
    {'name':'Alexander Isak','position':'Forward','team_id':23,'is_star':1},
    # Group G
    {'name':'Kevin De Bruyne','position':'Midfielder','team_id':25,'is_star':1},
    {'name':'Jérémy Doku','position':'Forward','team_id':25,'is_star':1},
    {'name':'Mohamed Salah','position':'Forward','team_id':26,'is_star':1},
    # Group H
    {'name':'Lamine Yamal','position':'Forward','team_id':29,'is_star':1},
    {'name':'Pedri','position':'Midfielder','team_id':29,'is_star':1},
    {'name':'Rodri','position':'Midfielder','team_id':29,'is_star':1},
    {'name':'Darwin Núñez','position':'Forward','team_id':32,'is_star':1},
    {'name':'Federico Valverde','position':'Midfielder','team_id':32,'is_star':1},
    # Group I
    {'name':'Kylian Mbappé','position':'Forward','team_id':33,'is_star':1},
    {'name':'Antoine Griezmann','position':'Forward','team_id':33,'is_star':1},
    {'name':'Aurélien Tchouaméni','position':'Midfielder','team_id':33,'is_star':1},
    {'name':'Sadio Mané','position':'Forward','team_id':34,'is_star':1},
    {'name':'Erling Haaland','position':'Forward','team_id':36,'is_star':1},
    {'name':'Martin Ødegaard','position':'Midfielder','team_id':36,'is_star':1},
    # Group J
    {'name':'Lionel Messi','position':'Forward','team_id':37,'is_star':1},
    {'name':'Julián Álvarez','position':'Forward','team_id':37,'is_star':1},
    {'name':'Enzo Fernández','position':'Midfielder','team_id':37,'is_star':1},
    {'name':'David Alaba','position':'Defender','team_id':39,'is_star':1},
    # Group K
    {'name':'Cristiano Ronaldo','position':'Forward','team_id':41,'is_star':1},
    {'name':'Bruno Fernandes','position':'Midfielder','team_id':41,'is_star':1},
    {'name':'Rafael Leão','position':'Forward','team_id':41,'is_star':1},
    {'name':'Luis Díaz','position':'Forward','team_id':44,'is_star':1},
    {'name':'James Rodríguez','position':'Midfielder','team_id':44,'is_star':1},
    # Group L
    {'name':'Jude Bellingham','position':'Midfielder','team_id':45,'is_star':1},
    {'name':'Bukayo Saka','position':'Forward','team_id':45,'is_star':1},
    {'name':'Harry Kane','position':'Forward','team_id':45,'is_star':1},
    {'name':'Luka Modrić','position':'Midfielder','team_id':46,'is_star':1},
    {'name':'Mohammed Kudus','position':'Forward','team_id':47,'is_star':1},
]

# Add IDs
for i, p in enumerate(star_players):
    p['id'] = i + 1

data['players'] = star_players

# ─── 3. UPDATE STANDINGS — add D, L columns and "Show full group" in renderStandings ───
# We'll update the renderStandings function to include D and L columns

# Re-inject data
new_data_str = 'window.__FIFA_DATA = ' + json.dumps(data, separators=(',', ':'), ensure_ascii=False) + ';'
pat = re.compile(r'window\.__FIFA_DATA\s*=\s*\{.*?\};', re.DOTALL)
match_obj = pat.search(html)
if match_obj:
    html = html[:match_obj.start()] + new_data_str + html[match_obj.end():]

# ─── 4. UPDATE STANDINGS CSS — add D and L columns ───
old_standings_head_css = """  .standings-head{
    display:grid;grid-template-columns:24px 1fr 28px 28px 28px 36px;
    padding:10px 14px;font-size:10px;font-weight:700;color:var(--muted);
    background:#f8fafe;text-transform:uppercase;letter-spacing:.5px;
    border-bottom:1px solid var(--line);
  }"""

new_standings_head_css = """  .standings-head{
    display:grid;grid-template-columns:24px 1fr 24px 24px 24px 24px 28px 32px;
    padding:10px 12px;font-size:10px;font-weight:700;color:var(--muted);
    background:#f8fafe;text-transform:uppercase;letter-spacing:.5px;
    border-bottom:1px solid var(--line);
  }"""

html = html.replace(old_standings_head_css, new_standings_head_css)

# Update standings-row grid
old_standings_row = """  .standings-row{
    display:grid;grid-template-columns:24px 1fr 28px 28px 28px 36px;"""
new_standings_row = """  .standings-row{
    display:grid;grid-template-columns:24px 1fr 24px 24px 24px 24px 28px 32px;"""
html = html.replace(old_standings_row, new_standings_row)

# ─── 5. UPDATE renderStandings — add D, L columns + "View group" link ───
old_renderStandings = r"""function renderStandings() {
  const el = $('#group-standings');
  let html = '';
  DB.groups.forEach(g => {
    const groupTeams = DB.standings.filter(s => s.group === g.id);
    html += `<div class="section-title"><h2>${g.name}</h2></div>
    <div class="standings">
      <div class="standings-head"><span>#</span><span>Team</span><span>P</span><span>W</span><span>GD</span><span>PTS</span></div>`;
    groupTeams.forEach((s, i) => {
      const t = team(s.team_id);
      const cls = i < 2 ? ' qualified' : '';
      html += `<div class="standings-row">
        <span class="pos${cls}">${i + 1}</span>
        <span class="team-cell"><span class="mini-flag">${t.flag}</span>${t.name}</span>
        <span class="num">${s.played}</span><span class="num">${s.won}</span>
        <span class="num">${s.goal_difference >= 0 ? '+' : ''}${s.goal_difference}</span>
        <span class="pts">${s.points}</span>
      </div>`;
    });
    html += '</div>';"""

new_renderStandings = r"""function renderStandings() {
  const el = $('#group-standings');
  let html = '';
  DB.groups.forEach(g => {
    const groupTeams = DB.standings.filter(s => s.group === g.id);
    html += `<div class="section-title"><h2>${g.name}</h2></div>
    <div class="standings">
      <div class="standings-head"><span>#</span><span>Team</span><span>P</span><span>W</span><span>D</span><span>L</span><span>GD</span><span>Pts</span></div>`;
    groupTeams.forEach((s, i) => {
      const t = team(s.team_id);
      const cls = i < 2 ? ' qualified' : '';
      html += `<div class="standings-row">
        <span class="pos${cls}">${i + 1}</span>
        <span class="team-cell"><span class="mini-flag">${t.flag}</span>${t.name}</span>
        <span class="num">${s.played}</span><span class="num">${s.won}</span>
        <span class="num">${s.drawn || 0}</span><span class="num">${s.lost || 0}</span>
        <span class="num">${s.goal_difference >= 0 ? '+' : ''}${s.goal_difference}</span>
        <span class="pts">${s.points}</span>
      </div>`;
    });
    html += `</div>
    <div style="text-align:center;padding:8px 0;">
      <span style="font-size:11px;color:var(--hyundai-accent);font-weight:600;cursor:pointer;" onclick="showGroupMatches('${g.id}')">View group matches ›</span>
    </div>`;"""

html = html.replace(old_renderStandings, new_renderStandings)

# ─── 6. FIX the stage label in matchCard — 'Group Stage' not 'First Stage' for group matches ───
# Actually the user's FIFA screenshot says "First Stage" which IS correct for FIFA 2026
# But let's keep it as is

# ─── 7. Add showGroupMatches function ───
# Insert before the closing of init()
old_init_end = "  renderMatches();"
new_init_end = """  renderMatches();

  // Show group matches helper
  window.showGroupMatches = function(groupId) {
    // Switch to Matches tab and scroll to that group's matches
    $$('.tab').forEach(t => t.classList.remove('active'));
    $$('.panel').forEach(p => p.classList.remove('active'));
    $('[data-tab="matches"]').classList.add('active');
    $('#panel-matches').classList.add('active');
    // Find first match of this group and scroll to it
    setTimeout(() => {
      const cards = $$('.schedule-card');
      for (const card of cards) {
        const info = card.querySelector('.sched-stage');
        if (info && info.textContent.includes('Group ' + groupId)) {
          card.scrollIntoView({behavior:'smooth', block:'center'});
          card.style.boxShadow = '0 0 0 2px var(--hyundai-accent)';
          setTimeout(() => card.style.boxShadow = '', 2000);
          break;
        }
      }
    }, 100);
  };"""

html = html.replace(old_init_end, new_init_end, 1)

# ─── 8. Fix day-label to not be too bold ───
old_day = """  .day-group{margin-bottom:18px;}
  .day-label{
    font-size:14px;font-weight:800;color:var(--text);
    margin-bottom:10px;padding-left:2px;
    display:flex;justify-content:space-between;align-items:center;
  }"""

new_day = """  .day-group{margin-bottom:16px;}
  .day-label{
    font-size:13px;font-weight:700;color:var(--text);
    margin-bottom:8px;padding:6px 0 6px 2px;
    border-bottom:1px solid var(--line);
  }"""

html = html.replace(old_day, new_day)

with open('/Users/keshav/Documents/Claude/hyundai-fifa-page/index.html', 'w') as f:
    f.write(html)

print("✅ Patch 3 applied:")
print(f"  - Match cards: reduced time to 16px, team codes to 15px semi-bold, flags 28px")
print(f"  - 48 teams updated to official FIFA 2026 draw (Groups A-L)")
print(f"  - {len(star_players)} star players seeded across all groups")
print(f"  - {len(new_group_matches)} group matches generated (6 per group)")
print(f"  - Standings: added D (draws) and L (losses) columns")
print(f"  - Added 'View group matches' link under each group table")
print(f"  - Day labels refined: lighter weight, with bottom border")
