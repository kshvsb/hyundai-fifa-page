#!/usr/bin/env python3
"""Patch 5: Major overhaul — logo, bottom bar, predictions, country drill-down, remove Drive to Final, etc."""

import json, re

with open('/Users/keshav/Documents/Claude/hyundai-fifa-page/index.html', 'r') as f:
    html = f.read()

# Read the H logo base64
with open('/tmp/hlogo_b64.txt', 'r') as f:
    h_logo_b64 = f.read().strip()

# ─── 1. BOTTOM NAV: Make it fixed/sticky, always on screen ───
html = html.replace(
    """  .bottom-nav{
    position:absolute;bottom:0;left:0;right:0;
    background:rgba(255,255,255,.95);backdrop-filter:blur(20px);
    border-top:1px solid var(--line);
    display:flex;justify-content:space-around;padding:10px 0 20px;
  }""",
    """  .bottom-nav{
    position:sticky;bottom:0;left:0;right:0;
    background:rgba(255,255,255,.97);backdrop-filter:blur(20px);
    border-top:1px solid var(--line);
    display:flex;justify-content:space-around;padding:10px 0 20px;
    flex-shrink:0;z-index:50;
  }"""
)

# ─── 2. REMOVE "Drive to the Final" promo ───
# Find and replace the promo-interstitial-1 rendering
old_drive = """  // --- INTERSTITIAL 1: Drive to the Final ---
  $('#promo-interstitial-1').innerHTML = `<div style="
    border-radius:16px;overflow:hidden;position:relative;margin-top:16px;
    background:linear-gradient(135deg,#002c5f 0%,#003d82 40%,#00aad2 100%);
    padding:20px 18px;
    box-shadow:0 6px 20px rgba(0,44,95,.2);
  ">
    <div style="position:absolute;right:-30px;top:-30px;width:160px;height:160px;border-radius:50%;background:rgba(255,255,255,.06);"></div>
    <div style="position:absolute;right:30px;bottom:-40px;width:120px;height:120px;border-radius:50%;background:rgba(0,170,210,.15);"></div>
    <div style="display:flex;align-items:center;gap:6px;margin-bottom:10px;">
      <svg viewBox="0 0 60 36" style="height:18px;width:auto;flex-shrink:0;">
        <ellipse cx="30" cy="18" rx="27" ry="14" fill="none" stroke="#fff" stroke-width="2.5"/>
        <path d="M 20 11 L 24 11 L 24 16.5 L 36 16.5 L 36 11 L 40 11 L 40 25 L 36 25 L 36 19.5 L 24 19.5 L 24 25 L 20 25 Z" fill="#fff" transform="skewX(-12) translate(6 0)"/>
      </svg>
      <span style="font-size:9px;font-weight:800;color:rgba(255,255,255,.7);letter-spacing:1.5px;text-transform:uppercase;">Official FIFA Partner</span>
    </div>
    <div style="font-size:18px;font-weight:900;color:#fff;line-height:1.2;margin-bottom:4px;">Drive to the Final</div>
    <div style="font-size:12px;color:rgba(255,255,255,.8);line-height:1.4;margin-bottom:12px;">Test drive a Hyundai across 40+ countries. Win a 4-day trip to the World Cup with match tickets.</div>
    <div style="display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,.18);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,.3);border-radius:20px;padding:7px 14px;font-size:11px;font-weight:700;color:#fff;">
      Enter now ⟶
    </div>
    <div style="position:absolute;right:16px;bottom:16px;font-size:28px;">🏆</div>
  </div>`;"""

new_drive = """  // --- INTERSTITIAL 1: Winning Predictions (SportRadar) ---
  $('#promo-interstitial-1').innerHTML = `<div style="
    border-radius:16px;overflow:hidden;position:relative;margin-top:16px;
    background:var(--card);border:1px solid var(--line);
    padding:16px 16px 10px;
  ">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
      <div style="font-size:14px;font-weight:800;color:var(--text);">Title favourites</div>
      <div style="font-size:9px;color:var(--muted);font-weight:500;">SportRadar</div>
    </div>
    <div style="display:flex;flex-direction:column;gap:8px;">
      ${[
        {name:'Spain',flag:'🇪🇸',pct:15},
        {name:'France',flag:'🇫🇷',pct:14},
        {name:'England',flag:'🏴\\u200D☠️',pct:12},
        {name:'Brazil',flag:'🇧🇷',pct:9},
        {name:'Argentina',flag:'🇦🇷',pct:9},
        {name:'Portugal',flag:'🇵🇹',pct:7},
        {name:'Germany',flag:'🇩🇪',pct:5}
      ].map(t => '<div style="display:flex;align-items:center;gap:10px;"><span style="font-size:18px;">' + t.flag + '</span><span style="flex:1;font-size:12px;font-weight:600;color:var(--text);">' + t.name + '</span><div style="width:100px;height:6px;background:var(--line);border-radius:3px;overflow:hidden;"><div style=\\"width:' + (t.pct / 15 * 100) + '%;height:100%;background:linear-gradient(90deg,#002c5f,#00aad2);border-radius:3px;\\"></div></div><span style="font-size:11px;font-weight:700;color:var(--text);min-width:28px;text-align:right;">' + t.pct + '%</span></div>').join('')}
    </div>
  </div>`;"""

html = html.replace(old_drive, new_drive)

# ─── 3. REMOVE "View group matches" from standings ───
html = html.replace(
    """    html += `</div>
    <div style="text-align:center;padding:8px 0;">
      <span style="font-size:11px;color:var(--hyundai-accent);font-weight:600;cursor:pointer;" onclick="showGroupMatches('${g.id}')">View group matches ›</span>
    </div>`;""",
    """    html += `</div>`;"""
)

# ─── 4. FIX STANDINGS ALIGNMENT — head vs row padding mismatch ───
# Head has padding:10px 12px, row has padding:11px 14px — make them match
html = html.replace(
    """  .standings-head{
    display:grid;grid-template-columns:24px 1fr 24px 24px 24px 24px 28px 32px;
    padding:10px 12px;font-size:10px;font-weight:700;color:var(--muted);
    background:#f8fafe;text-transform:uppercase;letter-spacing:.5px;
    border-bottom:1px solid var(--line);
  }
  .standings-row{
    display:grid;grid-template-columns:24px 1fr 24px 24px 24px 24px 28px 32px;
    padding:11px 14px;font-size:12px;align-items:center;
    border-bottom:1px solid var(--line);font-weight:600;
  }""",
    """  .standings-head{
    display:grid;grid-template-columns:24px 1fr 24px 24px 24px 24px 28px 32px;
    padding:10px 14px;font-size:10px;font-weight:700;color:var(--muted);
    background:#f8fafe;text-transform:uppercase;letter-spacing:.5px;
    border-bottom:1px solid var(--line);gap:0;
  }
  .standings-row{
    display:grid;grid-template-columns:24px 1fr 24px 24px 24px 24px 28px 32px;
    padding:11px 14px;font-size:12px;align-items:center;
    border-bottom:1px solid var(--line);font-weight:600;gap:0;
  }"""
)

# ─── 5. RENAME TABS — more like Google/FIFA ───
html = html.replace(
    """    <div class="tab active" data-tab="overview">Overview</div>
    <div class="tab" data-tab="matches">Matches</div>
    <div class="tab" data-tab="standings">Table</div>
    <div class="tab" data-tab="knockout">Knockout</div>
    <div class="tab" data-tab="scorers">Players</div>""",
    """    <div class="tab active" data-tab="overview">Home</div>
    <div class="tab" data-tab="matches">Matches</div>
    <div class="tab" data-tab="standings">Groups</div>
    <div class="tab" data-tab="knockout">Bracket</div>
    <div class="tab" data-tab="scorers">Squads</div>"""
)

# ─── 6. FIX "See all" BUTTON — switch to Matches tab ───
html = html.replace(
    """<div class="section-title"><h2>Up Next</h2><a href="#">See all</a></div>""",
    """<div class="section-title"><h2>Up Next</h2><a href="#" onclick="event.preventDefault();document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));document.querySelector('.tab[data-tab=matches]').classList.add('active');document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));document.getElementById('panel-matches').classList.add('active');document.querySelector('.content').scrollTop=0;">See all</a></div>"""
)

# ─── 7. ADD COUNTRY CLICK → TEAM MATCHES OVERLAY ───
# Add CSS for team-matches overlay
team_overlay_css = """
  /* Team matches overlay */
  .team-overlay{
    position:absolute;inset:0;background:var(--bg);z-index:90;
    transform:translateX(100%);transition:transform .3s ease;
    overflow-y:auto;-webkit-overflow-scrolling:touch;
    display:flex;flex-direction:column;
  }
  .team-overlay.open{transform:translateX(0);}
  .team-overlay-header{
    display:flex;justify-content:space-between;align-items:center;
    padding:14px 18px;background:linear-gradient(135deg,var(--fifa-navy),var(--fifa-blue));
    color:#fff;font-size:13px;font-weight:700;position:sticky;top:0;z-index:10;flex-shrink:0;
  }
  .team-overlay-body{flex:1;overflow-y:auto;padding:16px 18px 100px;}
"""
html = html.replace(
    "  /* Match Detail Overlay */",
    team_overlay_css + "\n  /* Match Detail Overlay */"
)

# Add team overlay HTML before the match overlay
html = html.replace(
    """  <!-- Match Detail Overlay -->""",
    """  <!-- Team Matches Overlay -->
  <div class="team-overlay" id="team-overlay">
    <div class="team-overlay-header">
      <span class="overlay-back" onclick="document.getElementById('team-overlay').classList.remove('open')">← Back</span>
      <span id="team-overlay-title"></span>
      <span></span>
    </div>
    <div class="team-overlay-body" id="team-overlay-content"></div>
  </div>

  <!-- Match Detail Overlay -->"""
)

# Add the openTeamMatches function before openMatchDetail
team_matches_fn = r"""
function openTeamMatches(teamId) {
  const t = team(teamId);
  if (!t || !t.name) return;
  const overlay = document.getElementById('team-overlay');
  const title = document.getElementById('team-overlay-title');
  const content = document.getElementById('team-overlay-content');

  title.textContent = t.flag + ' ' + t.name;

  // Find all matches for this team
  const matches = DB.matches.filter(m => m.home_team_id === teamId || m.away_team_id === teamId);
  matches.sort((a, b) => (a.match_date + a.match_time_utc).localeCompare(b.match_date + b.match_time_utc));

  let html = '';

  // Group stage info
  const standing = DB.standings.find(s => s.team_id === teamId);
  if (standing) {
    const grp = DB.groups.find(g => g.id === standing.group);
    html += `<div style="background:var(--card);border-radius:14px;border:1px solid var(--line);padding:14px 16px;margin-bottom:16px;">
      <div style="font-size:13px;font-weight:700;color:var(--text);margin-bottom:8px;">${grp ? grp.name : 'Group'}</div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;text-align:center;">
        <div><div style="font-size:18px;font-weight:800;color:var(--text);">${standing.played}</div><div style="font-size:9px;color:var(--muted);font-weight:600;">Played</div></div>
        <div><div style="font-size:18px;font-weight:800;color:var(--green);">${standing.won}</div><div style="font-size:9px;color:var(--muted);font-weight:600;">Won</div></div>
        <div><div style="font-size:18px;font-weight:800;color:var(--muted);">${standing.drawn || 0}</div><div style="font-size:9px;color:var(--muted);font-weight:600;">Drawn</div></div>
        <div><div style="font-size:18px;font-weight:800;color:#e53e3e;">${standing.lost || 0}</div><div style="font-size:9px;color:var(--muted);font-weight:600;">Lost</div></div>
      </div>
    </div>`;
  }

  html += `<div style="font-size:14px;font-weight:700;color:var(--text);margin-bottom:12px;">Matches</div>`;

  matches.forEach(m => {
    const h = team(m.home_team_id);
    const a = team(m.away_team_id);
    const homeName = h.name || m.home_placeholder || 'TBD';
    const awayName = a.name || m.away_placeholder || 'TBD';
    const homeCode = h.short_code || m.home_placeholder || 'TBD';
    const awayCode = a.short_code || m.away_placeholder || 'TBD';
    const homeFlag = h.flag || '';
    const awayFlag = a.flag || '';
    const isPlayed = m.status === 'finished';
    const dt = new Date(m.match_date + 'T00:00:00');
    const dateStr = dt.toLocaleDateString('en-US', {weekday:'short', day:'numeric', month:'short'});
    const v = venue(m.venue_id);
    const stageLabel = m.group ? 'Group ' + m.group : m.stage;

    html += `<div style="background:var(--card);border-radius:12px;border:1px solid var(--line);padding:14px;margin-bottom:8px;cursor:pointer;" onclick="document.getElementById('team-overlay').classList.remove('open');setTimeout(()=>openMatchDetail(${m.id}),350);">
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

  // Star players for this team
  const stars = DB.players.filter(p => p.team_id === teamId && p.is_star);
  if (stars.length) {
    html += `<div style="font-size:14px;font-weight:700;color:var(--text);margin:16px 0 12px;">Key Players</div>`;
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

  content.innerHTML = html;
  overlay.classList.add('open');
  content.scrollTop = 0;
}
"""

html = html.replace(
    "function openMatchDetail(matchId) {",
    team_matches_fn + "\nfunction openMatchDetail(matchId) {"
)

# ─── 8. MAKE TEAM NAMES CLICKABLE in standings ───
# Replace the standings row team-cell to be clickable
html = html.replace(
    """        <span class="team-cell"><span class="mini-flag">${t.flag}</span>${t.name}</span>""",
    """        <span class="team-cell" style="cursor:pointer;" onclick="openTeamMatches(${s.team_id})"><span class="mini-flag">${t.flag}</span>${t.name}</span>"""
)

# ─── 9. REPLACE H LOGO in header ───
# The header currently has a large Hyundai logo. Replace with the H logo file
# Find the existing logo-chip img tag and replace the src
# The logo-chip img has class="hyundai-logo"
# We need to find the base64 data for the current logo and replace it
# Actually, let's just find the logo-chip and replace its content

# Find the current hyundai-logo img src (it's a huge base64 string)
import re
# Replace the logo-chip content with the new H logo
logo_pattern = r'<div class="logo-chip"><img class="hyundai-logo" src="data:image/png;base64,[^"]*"'
logo_replacement = f'<div class="logo-chip"><img class="hyundai-logo" src="data:image/png;base64,{h_logo_b64}"'
html = re.sub(logo_pattern, logo_replacement, html)

# Also adjust the logo-chip CSS to work better with the H logo
html = html.replace(
    """  .logo-chip{
    background:rgba(255,255,255,.12);border-radius:10px;padding:6px 8px;display:flex;align-items:center;
  }
  .hyundai-logo{height:18px;width:auto;filter:brightness(0) invert(1);}""",
    """  .logo-chip{
    background:rgba(255,255,255,.12);border-radius:10px;padding:4px 8px;display:flex;align-items:center;
  }
  .hyundai-logo{height:22px;width:auto;object-fit:contain;}"""
)

# ─── 10. KNOCKOUT ROUND SLIDING ANIMATION ───
# Replace the hidden/visible toggle with a sliding transition
html = html.replace(
    """  .ko-round-container{transition:opacity .3s,transform .3s;}
  .ko-round-container.hidden{display:none;opacity:0;transform:translateX(20px);}
  .ko-round-container.visible{display:block;opacity:1;transform:none;}""",
    """  .ko-round-container{
    transition:transform .4s cubic-bezier(.25,.46,.45,.94),opacity .4s ease;
    position:absolute;inset:0;opacity:0;pointer-events:none;
    transform:translateX(60px);
  }
  .ko-round-container.visible{
    position:relative;opacity:1;pointer-events:auto;
    transform:translateX(0);
  }
  .ko-round-container.slide-left{
    transform:translateX(-60px);opacity:0;pointer-events:none;
  }"""
)

# Add a wrapper for knockout round containers to handle positioning
html = html.replace(
    """      <div id="knockout-bracket"></div>""",
    """      <div id="knockout-bracket" style="position:relative;overflow:hidden;"></div>"""
)

# Update the filter button click handler for sliding animation
old_filter_handler = """  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const roundKey = btn.dataset.round;
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      btn.scrollIntoView({behavior:'smooth', block:'nearest', inline:'center'});
      roundContainers.forEach(rc => {
        if (rc.dataset.round === roundKey) {
          rc.classList.remove('hidden');
          rc.classList.add('visible');
        } else {
          rc.classList.remove('visible');
          rc.classList.add('hidden');
        }
      });
    });
  });"""

new_filter_handler = """  let currentRoundIdx = 0;
  filterBtns.forEach((btn, btnIdx) => {
    btn.addEventListener('click', () => {
      const roundKey = btn.dataset.round;
      const newIdx = btnIdx;
      const goingRight = newIdx > currentRoundIdx;

      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      btn.scrollIntoView({behavior:'smooth', block:'nearest', inline:'center'});

      roundContainers.forEach(rc => {
        if (rc.classList.contains('visible')) {
          // Slide the current one out
          rc.classList.remove('visible');
          rc.classList.add(goingRight ? 'slide-left' : 'hidden');
          setTimeout(() => {
            rc.classList.remove('slide-left');
            rc.classList.add('hidden');
          }, 400);
        }
      });

      // Slide the new one in
      const target = Array.from(roundContainers).find(rc => rc.dataset.round === roundKey);
      if (target) {
        target.classList.remove('hidden', 'slide-left');
        target.style.transform = goingRight ? 'translateX(60px)' : 'translateX(-60px)';
        target.style.opacity = '0';
        void target.offsetHeight;
        target.classList.add('visible');
        target.style.transform = '';
        target.style.opacity = '';
      }

      currentRoundIdx = newIdx;
    });
  });"""

html = html.replace(old_filter_handler, new_filter_handler)

# ─── 11. REDUCE content bottom padding (bottom bar is now sticky) ───
html = html.replace(
    ".content{padding:14px 18px 110px;flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch;}",
    ".content{padding:14px 18px 20px;flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch;}"
)

with open('/Users/keshav/Documents/Claude/hyundai-fifa-page/index.html', 'w') as f:
    f.write(html)

print("✅ Patch 5 applied:")
print("  1. Bottom nav: sticky, always visible")
print("  2. Drive to the Final: replaced with Sportradar predictions")
print("  3. View group matches: removed from standings")
print("  4. Standings alignment: fixed head/row padding")
print("  5. Tabs renamed: Home, Matches, Groups, Bracket, Squads")
print("  6. See all button: now switches to Matches tab")
print("  7. Team click overlay: click country name → see all matches + stats + players")
print("  8. H logo: updated from file")
print("  9. Knockout animation: slide left/right on round switch")
print(" 10. Content padding: reduced (sticky bottom bar)")
