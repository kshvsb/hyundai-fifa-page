#!/usr/bin/env python3
"""Patch 6: Revert header logo, fix partner footer logo, add Your Team picker, clean nav."""

import re

with open('/Users/keshav/Documents/Claude/hyundai-fifa-page/index.html', 'r') as f:
    html = f.read()

# Read H logo base64 for the footer
with open('/tmp/hlogo_b64.txt', 'r') as f:
    h_logo_b64 = f.read().strip()

# ─── 1. REVERT HEADER LOGO — get original from index_old.html ───
with open('/Users/keshav/Documents/Claude/hyundai-fifa-page/index_old.html', 'r') as f:
    old_html = f.read()

# Extract original Hyundai logo base64 from old file
old_logo_match = re.search(r'hyundai-logo" src="data:image/png;base64,([^"]+)"', old_html)
if old_logo_match:
    original_logo_b64 = old_logo_match.group(1)
    # Replace current H logo with original full logo in header
    html = re.sub(
        r'(hyundai-logo" src="data:image/png;base64,)[^"]+(")',
        r'\g<1>' + original_logo_b64 + r'\2',
        html
    )
    print("  ✓ Header logo reverted to original HYUNDAI text logo")
else:
    print("  ✗ Could not find original logo in index_old.html")

# Revert logo-chip CSS to original
html = html.replace(
    """  .logo-chip{
    background:rgba(255,255,255,.12);border-radius:10px;padding:4px 8px;display:flex;align-items:center;
  }
  .hyundai-logo{height:22px;width:auto;object-fit:contain;}""",
    """  .logo-chip{
    background:rgba(255,255,255,.12);border-radius:10px;padding:6px 8px;display:flex;align-items:center;
  }
  .hyundai-logo{height:16px;width:auto;display:block;filter:brightness(0) invert(1);}"""
)

# ─── 2. REPLACE SVG in "Since 1999" footer with H logo image ───
old_svg_icon = """<div style="flex-shrink:0;width:40px;height:40px;border-radius:10px;background:rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;">
      <svg viewBox="0 0 60 36" style="height:18px;width:auto;">
        <ellipse cx="30" cy="18" rx="27" ry="14" fill="none" stroke="#fff" stroke-width="2.5"/>
        <path d="M 20 11 L 24 11 L 24 16.5 L 36 16.5 L 36 11 L 40 11 L 40 25 L 36 25 L 36 19.5 L 24 19.5 L 24 25 L 20 25 Z" fill="#fff" transform="skewX(-12) translate(6 0)"/>
      </svg>
    </div>"""

new_img_icon = f"""<div style="flex-shrink:0;width:40px;height:40px;border-radius:10px;background:rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;">
      <img src="data:image/png;base64,{h_logo_b64}" style="height:24px;width:auto;object-fit:contain;">
    </div>"""

html = html.replace(old_svg_icon, new_img_icon)

# ─── 3. CLEAN UP BOTTOM NAV — rename sections ───
html = html.replace(
    """  <div class="bottom-nav">
    <div class="nav-item active"><div class="nav-icon">⚽</div>Matches</div>
    <div class="nav-item"><div class="nav-icon">📊</div>Stats</div>
    <div class="nav-item"><div class="nav-icon">🏆</div>Teams</div>
  </div>""",
    """  <div class="bottom-nav">
    <div class="nav-item active" data-bnav="home"><div class="nav-icon">⚽</div>Home</div>
    <div class="nav-item" data-bnav="your-team"><div class="nav-icon">⭐</div>Your Team</div>
    <div class="nav-item" data-bnav="explore"><div class="nav-icon">🔍</div>Explore</div>
  </div>"""
)

# ─── 4. ADD "Your Team" OVERLAY with team picker ───
# Add CSS
your_team_css = """
  /* Your Team overlay */
  .your-team-overlay{
    position:absolute;inset:0;background:var(--bg);z-index:80;
    display:none;flex-direction:column;
  }
  .your-team-overlay.open{display:flex;}
  .your-team-header{
    display:flex;justify-content:space-between;align-items:center;
    padding:14px 18px;background:linear-gradient(135deg,var(--fifa-navy),var(--fifa-blue));
    color:#fff;font-size:14px;font-weight:700;flex-shrink:0;
  }
  .your-team-body{flex:1;min-height:0;overflow-y:auto;padding:16px 18px 20px;}
  .team-pick-card{
    display:flex;align-items:center;gap:12px;padding:14px;
    background:var(--card);border-radius:12px;border:1px solid var(--line);
    margin-bottom:8px;cursor:pointer;transition:all .15s;
  }
  .team-pick-card:active{transform:scale(.98);background:#f0f4ff;}
  .team-pick-flag{font-size:28px;}
  .team-pick-name{font-size:14px;font-weight:600;color:var(--text);}
  .team-pick-group{font-size:11px;color:var(--muted);}
"""

html = html.replace("  /* Match Detail Overlay */", your_team_css + "\n  /* Match Detail Overlay */")

# Add Your Team overlay HTML
your_team_html = """  <!-- Your Team Overlay -->
  <div class="your-team-overlay" id="your-team-overlay">
    <div class="your-team-header">
      <span>Your Team</span>
      <span style="cursor:pointer;padding:4px 8px;" onclick="document.getElementById('your-team-overlay').classList.remove('open')">✕</span>
    </div>
    <div class="your-team-body" id="your-team-body"></div>
  </div>

  """

html = html.replace("  <!-- Team Matches Overlay -->", your_team_html + "<!-- Team Matches Overlay -->")

# ─── 5. ADD YOUR TEAM JS LOGIC ───
your_team_js = r"""
// ─── YOUR TEAM FEATURE ───
const YOUR_TEAM_KEY = 'fifa2026_your_team';

function getYourTeam() {
  const id = localStorage.getItem(YOUR_TEAM_KEY);
  return id ? parseInt(id) : null;
}

function setYourTeam(teamId) {
  localStorage.setItem(YOUR_TEAM_KEY, teamId);
  renderYourTeam();
}

function clearYourTeam() {
  localStorage.removeItem(YOUR_TEAM_KEY);
  showTeamPicker();
}

function showTeamPicker() {
  const overlay = document.getElementById('your-team-overlay');
  const body = document.getElementById('your-team-body');

  // Group teams by group
  let html = '<div style="font-size:15px;font-weight:700;color:var(--text);margin-bottom:4px;">Choose your team</div>';
  html += '<div style="font-size:12px;color:var(--muted);margin-bottom:16px;">Pick a team to track throughout the tournament</div>';

  const groups = {};
  DB.standings.forEach(s => {
    if (!groups[s.group]) groups[s.group] = [];
    groups[s.group].push(s);
  });

  Object.keys(groups).sort().forEach(gId => {
    const grp = DB.groups.find(g => g.id === gId);
    html += `<div style="font-size:12px;font-weight:700;color:var(--muted);margin:12px 0 6px;text-transform:uppercase;letter-spacing:.5px;">${grp ? grp.name : gId}</div>`;
    groups[gId].forEach(s => {
      const t = team(s.team_id);
      html += `<div class="team-pick-card" onclick="setYourTeam(${s.team_id});document.getElementById('your-team-overlay').classList.remove('open');">
        <span class="team-pick-flag">${t.flag}</span>
        <div>
          <div class="team-pick-name">${t.name}</div>
          <div class="team-pick-group">${grp ? grp.name : ''}</div>
        </div>
      </div>`;
    });
  });

  body.innerHTML = html;
  overlay.classList.add('open');
}

function renderYourTeam() {
  const teamId = getYourTeam();
  const overlay = document.getElementById('your-team-overlay');
  const body = document.getElementById('your-team-body');

  if (!teamId) {
    showTeamPicker();
    return;
  }

  const t = team(teamId);
  if (!t || !t.name) { showTeamPicker(); return; }

  // Build team dashboard
  let html = '';

  // Team header
  html += `<div style="text-align:center;padding:20px 0 16px;">
    <div style="font-size:48px;margin-bottom:8px;">${t.flag}</div>
    <div style="font-size:20px;font-weight:800;color:var(--text);">${t.name}</div>
    <div style="font-size:12px;color:var(--muted);margin-top:4px;">${t.short_code || ''}</div>
  </div>`;

  // Group stats
  const standing = DB.standings.find(s => s.team_id === teamId);
  if (standing) {
    const grp = DB.groups.find(g => g.id === standing.group);
    html += `<div style="background:var(--card);border-radius:14px;border:1px solid var(--line);padding:14px 16px;margin-bottom:16px;">
      <div style="font-size:13px;font-weight:700;color:var(--text);margin-bottom:10px;">${grp ? grp.name : 'Group'} Standings</div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;text-align:center;">
        <div><div style="font-size:20px;font-weight:800;color:var(--text);">${standing.played}</div><div style="font-size:9px;color:var(--muted);font-weight:600;">Played</div></div>
        <div><div style="font-size:20px;font-weight:800;color:var(--green);">${standing.won}</div><div style="font-size:9px;color:var(--muted);font-weight:600;">Won</div></div>
        <div><div style="font-size:20px;font-weight:800;color:var(--muted);">${standing.drawn || 0}</div><div style="font-size:9px;color:var(--muted);font-weight:600;">Drawn</div></div>
        <div><div style="font-size:20px;font-weight:800;color:#e53e3e;">${standing.lost || 0}</div><div style="font-size:9px;color:var(--muted);font-weight:600;">Lost</div></div>
      </div>
      <div style="text-align:center;margin-top:10px;">
        <span style="font-size:22px;font-weight:900;color:var(--fifa-navy);">${standing.points}</span>
        <span style="font-size:11px;color:var(--muted);font-weight:600;"> pts</span>
      </div>
    </div>`;
  }

  // Matches
  const matches = DB.matches.filter(m => m.home_team_id === teamId || m.away_team_id === teamId);
  matches.sort((a, b) => (a.match_date + (a.match_time_utc||'')).localeCompare(b.match_date + (b.match_time_utc||'')));

  if (matches.length) {
    html += `<div style="font-size:14px;font-weight:700;color:var(--text);margin-bottom:10px;">Fixtures & Results</div>`;
    matches.forEach(m => {
      const h = team(m.home_team_id);
      const a = team(m.away_team_id);
      const homeCode = h.short_code || m.home_placeholder || 'TBD';
      const awayCode = a.short_code || m.away_placeholder || 'TBD';
      const homeFlag = h.flag || '';
      const awayFlag = a.flag || '';
      const isPlayed = m.status === 'finished';
      const dt = new Date(m.match_date + 'T00:00:00');
      const dateStr = dt.toLocaleDateString('en-US', {weekday:'short', day:'numeric', month:'short'});
      const v = venue(m.venue_id);
      const stageLabel = m.group ? 'Group ' + m.group : m.stage;

      html += `<div style="background:var(--card);border-radius:12px;border:1px solid var(--line);padding:14px;margin-bottom:8px;cursor:pointer;" onclick="document.getElementById('your-team-overlay').classList.remove('open');setTimeout(()=>openMatchDetail(${m.id}),100);">
        <div style="font-size:10px;color:var(--muted);font-weight:600;margin-bottom:8px;">${stageLabel} · ${dateStr}</div>
        <div style="display:flex;align-items:center;justify-content:center;gap:0;">
          <div style="flex:1;display:flex;align-items:center;justify-content:flex-end;gap:8px;">
            <span style="font-size:13px;font-weight:${m.home_team_id===teamId?'700':'500'};color:var(--text);">${homeCode}</span>
            <span style="font-size:22px;">${homeFlag}</span>
          </div>
          <div style="min-width:70px;text-align:center;">
            ${isPlayed
              ? '<span style="font-size:18px;font-weight:800;color:var(--text);">' + m.home_score + ' - ' + m.away_score + '</span>'
              : '<span style="font-size:13px;font-weight:600;color:var(--muted);">' + (m.match_time_utc || 'TBD') + '</span>'}
          </div>
          <div style="flex:1;display:flex;align-items:center;gap:8px;">
            <span style="font-size:22px;">${awayFlag}</span>
            <span style="font-size:13px;font-weight:${m.away_team_id===teamId?'700':'500'};color:var(--text);">${awayCode}</span>
          </div>
        </div>
        <div style="font-size:10px;color:var(--muted);text-align:center;margin-top:6px;">${v.name || ''}</div>
      </div>`;
    });
  }

  // Key players
  const stars = DB.players.filter(p => p.team_id === teamId && p.is_star);
  if (stars.length) {
    html += `<div style="font-size:14px;font-weight:700;color:var(--text);margin:16px 0 10px;">Key Players</div>`;
    stars.forEach(p => {
      html += `<div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid var(--line);">
        <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#e2e8f0,#cbd5e1);display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:800;color:var(--fifa-navy);">${p.jersey_number || '?'}</div>
        <div style="flex:1;">
          <div style="font-size:13px;font-weight:600;color:var(--text);">${p.name}</div>
          <div style="font-size:10px;color:var(--muted);">${p.position} · ${p.club || ''}</div>
        </div>
      </div>`;
    });
  }

  // Change team button
  html += `<div style="text-align:center;margin-top:20px;">
    <button onclick="clearYourTeam()" style="background:none;border:1px solid var(--line);border-radius:20px;padding:10px 20px;font-size:12px;font-weight:600;color:var(--muted);cursor:pointer;">Change Team</button>
  </div>`;

  body.innerHTML = html;
  overlay.classList.add('open');
}

// Wire up bottom nav
document.querySelectorAll('.bottom-nav .nav-item').forEach(item => {
  item.addEventListener('click', () => {
    const action = item.dataset.bnav;
    document.querySelectorAll('.bottom-nav .nav-item').forEach(i => i.classList.remove('active'));
    item.classList.add('active');

    if (action === 'home') {
      document.getElementById('your-team-overlay').classList.remove('open');
      // Switch to home tab
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelector('.tab[data-tab="overview"]').classList.add('active');
      document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
      document.getElementById('panel-overview').classList.add('active');
      document.querySelector('.content').scrollTop = 0;
    } else if (action === 'your-team') {
      renderYourTeam();
    } else if (action === 'explore') {
      document.getElementById('your-team-overlay').classList.remove('open');
      // Switch to matches tab
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelector('.tab[data-tab="matches"]').classList.add('active');
      document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
      document.getElementById('panel-matches').classList.add('active');
      document.querySelector('.content').scrollTop = 0;
    }
  });
});
"""

# Insert the Your Team JS before the closing </script> tag at the very end
# Find the last </script> and insert before it
last_script_idx = html.rfind('</script>')
if last_script_idx != -1:
    html = html[:last_script_idx] + your_team_js + '\n' + html[last_script_idx:]

# ─── 6. FIX BRACKET SCROLL — limit bracket container height ───
# The knockout bracket overflow should be limited to its content
html = html.replace(
    '      <div id="knockout-bracket" style="position:relative;overflow:hidden;"></div>',
    '      <div id="knockout-bracket" style="position:relative;"></div>'
)

with open('/Users/keshav/Documents/Claude/hyundai-fifa-page/index.html', 'w') as f:
    f.write(html)

print("✅ Patch 6 applied:")
print("  1. Header logo: reverted to original HYUNDAI text logo")
print("  2. Since 1999 footer: now uses H logo image")
print("  3. Bottom nav: Home | Your Team | Explore")
print("  4. Your Team feature: pick a team, track stats/matches/players, change team")
print("  5. Bracket overflow: removed overflow:hidden")
