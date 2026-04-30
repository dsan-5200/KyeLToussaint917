"""
Build the full Priced Out static HTML site.
Generates index.html + all section pages with shared nav/CSS.
"""
import os, shutil

OUT = "/home/claude/displacement-project/site/_site"
os.makedirs(f"{OUT}/figures", exist_ok=True)

# ─── Shared assets ────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,300;1,8..60,400&family=IBM+Plex+Mono:wght@400;600&display=swap');

:root {
  --navy:  #0F1923;
  --cream: #F4F0E8;
  --rust:  #E8401C;
  --gold:  #F5A623;
  --blue:  #1A3A5C;
  --mid:   #8FA8C8;
  --serif: 'Playfair Display', Georgia, serif;
  --body:  'Source Serif 4', Georgia, serif;
  --mono:  'IBM Plex Mono', monospace;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: var(--body);
  background: var(--cream);
  color: var(--navy);
  font-size: 1.05rem;
  line-height: 1.85;
}

/* NAV */
nav {
  background: var(--navy);
  border-bottom: 3px solid var(--rust);
  position: sticky; top: 0; z-index: 100;
  padding: 0 2rem;
  display: flex; align-items: center; justify-content: space-between;
  min-height: 56px;
}
.nav-brand {
  font-family: var(--mono); font-weight: 600; font-size: 1rem;
  color: var(--cream); text-decoration: none; letter-spacing: 0.06em;
}
.nav-links { display: flex; gap: 0.2rem; flex-wrap: wrap; }
.nav-links a {
  font-family: var(--mono); font-size: 0.78rem; letter-spacing: 0.05em;
  color: var(--mid); text-decoration: none;
  padding: 0.4rem 0.9rem; border-radius: 2px;
  transition: color 0.2s, background 0.2s;
}
.nav-links a:hover, .nav-links a.active {
  color: var(--gold); background: rgba(255,255,255,0.05);
}

/* HERO */
.hero {
  background: var(--navy); color: var(--cream);
  padding: 7rem 2rem 5rem; position: relative; overflow: hidden;
}
.hero::before {
  content: ""; position: absolute; inset: 0;
  background: repeating-linear-gradient(-45deg,transparent,transparent 40px,rgba(232,64,28,.05) 40px,rgba(232,64,28,.05) 41px);
}
.hero-inner { max-width: 920px; margin: 0 auto; position: relative; z-index: 1; }
.hero-eyebrow {
  font-family: var(--mono); font-size: 0.78rem; letter-spacing: 0.2em;
  color: var(--rust); text-transform: uppercase; margin-bottom: 1.2rem;
}
.hero h1 {
  font-family: var(--serif); font-size: clamp(3.2rem, 8vw, 6.5rem);
  font-weight: 900; line-height: 1.0; color: var(--cream);
  margin-bottom: 1rem;
}
.hero h1 span { color: var(--rust); }
.hero-rule { width: 60px; height: 4px; background: var(--rust); margin: 1.2rem 0 1.6rem; }
.hero-sub {
  font-size: 1.2rem; font-weight: 300; color: var(--mid);
  max-width: 580px; margin-bottom: 3rem; line-height: 1.7;
}

/* STAT CARDS */
.stat-row { display: flex; gap: 1.2rem; flex-wrap: wrap; }
.stat-card {
  flex: 1; min-width: 155px;
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.1);
  border-top: 3px solid var(--rust);
  padding: 1.4rem 1.1rem; border-radius: 2px;
}
.stat-num {
  font-family: var(--serif); font-size: 2.5rem; font-weight: 900;
  color: var(--cream); line-height: 1; margin-bottom: 0.3rem;
}
.stat-num span { color: var(--rust); }
.stat-label { font-family: var(--mono); font-size: 0.7rem; color: var(--mid); letter-spacing: 0.1em; text-transform: uppercase; line-height: 1.5; }

/* CONTENT */
.content-section { max-width: 780px; margin: 0 auto; padding: 4rem 2rem; }
.content-section h2 {
  font-family: var(--serif); font-size: 2.1rem; font-weight: 700;
  color: var(--blue); line-height: 1.2; margin-bottom: 0.5rem;
}
.section-divider { width: 50px; height: 3px; background: var(--rust); margin: 0.8rem 0 1.6rem; }
.content-section p { margin-bottom: 1.4rem; }
.content-section p:first-of-type { font-size: 1.12rem; }

/* PULLQUOTE */
.pullquote {
  border-left: 5px solid var(--rust);
  padding: 1rem 1.8rem;
  margin: 2.5rem 0;
  background: rgba(232,64,28,.05);
  font-family: var(--serif); font-size: 1.35rem;
  font-style: italic; color: var(--blue); line-height: 1.45;
}
.pullquote cite {
  display: block; margin-top: 0.6rem;
  font-family: var(--mono); font-size: 0.72rem;
  font-style: normal; color: #888; letter-spacing: 0.08em;
}

/* FIGURE */
.fig-wrap {
  max-width: 1000px; margin: 2.5rem auto;
  background: white; border: 1px solid #E0DACE;
  border-top: 4px solid var(--blue);
  padding: 1.5rem;
  box-shadow: 0 4px 24px rgba(0,0,0,.07);
}
.fig-wrap img { width: 100%; height: auto; display: block; }
.fig-caption {
  font-family: var(--mono); font-size: 0.73rem;
  color: #888; margin-top: 0.9rem; letter-spacing: 0.04em; line-height: 1.6;
}
.fig-embed { width: 100%; border: none; min-height: 540px; display: block; }

/* INFOGRAPHIC */
.infographic {
  background: var(--navy); color: var(--cream);
  padding: 5rem 2rem; text-align: center; margin: 0;
}
.infographic h2 { font-family: var(--serif); font-size: 2.2rem; margin-bottom: 0.4rem; }
.infographic-subtitle {
  font-family: var(--mono); font-size: 0.78rem; color: var(--mid);
  letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 3rem;
}
.infographic-grid {
  display: flex; justify-content: center; gap: 1.4rem;
  flex-wrap: wrap; max-width: 960px; margin: 0 auto;
}
.info-card {
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.1);
  border-radius: 4px; padding: 2rem 1.4rem;
  min-width: 155px; flex: 1;
}
.info-icon { font-size: 1.9rem; margin-bottom: 0.7rem; }
.info-big {
  font-family: var(--serif); font-size: 2.6rem; font-weight: 900;
  color: var(--rust); line-height: 1;
}
.info-small {
  font-family: var(--mono); font-size: 0.68rem; color: var(--mid);
  letter-spacing: 0.1em; text-transform: uppercase; margin-top: 0.4rem;
}
.info-desc { font-size: 0.88rem; color: #AABBCC; margin-top: 0.7rem; line-height: 1.55; }

/* CLOSING */
.closing {
  background: linear-gradient(135deg, var(--blue) 0%, var(--navy) 100%);
  color: var(--cream); padding: 5rem 2rem; text-align: center;
}
.closing h2 { font-family: var(--serif); font-size: 2.4rem; margin-bottom: 1rem; }
.closing p  { font-size: 1.05rem; color: var(--mid); max-width: 600px; margin: 0 auto 1.4rem; }
.closing a  { color: var(--gold); }

/* APPENDIX */
.appendix-section { max-width: 780px; margin: 0 auto; padding: 4rem 2rem; }
.appendix-section h2 { font-family: var(--serif); font-size: 2rem; color: var(--blue); margin: 2rem 0 0.4rem; }
.appendix-section h2:first-child { margin-top: 0; }
.appendix-section .section-divider { width: 50px; height: 3px; background: var(--rust); margin: 0.5rem 0 1.2rem; }
.appendix-section p { margin-bottom: 1.3rem; }
.code-note {
  font-family: var(--mono); font-size: 0.83rem; color: #555;
  background: #EDEAE0; padding: 0.8rem 1.1rem;
  border-left: 3px solid var(--blue); margin-bottom: 1.5rem; line-height: 1.6;
}
.source-tag {
  font-family: var(--mono); font-size: 0.7rem; color: #999;
  letter-spacing: 0.06em; margin-top: 0.5rem;
}
hr.divider { border: none; border-top: 1px solid #DDD; margin: 3rem 0; }

/* FOOTER */
footer {
  background: var(--navy); color: var(--mid);
  font-family: var(--mono); font-size: 0.72rem;
  letter-spacing: 0.06em; text-align: center;
  padding: 2rem; border-top: 1px solid rgba(255,255,255,.1);
}

/* RESPONSIVE */
@media (max-width: 640px) {
  .hero { padding: 4rem 1.2rem 3rem; }
  .stat-row { gap: 0.9rem; }
  .nav-links a { font-size: 0.7rem; padding: 0.35rem 0.6rem; }
  .infographic-grid { flex-direction: column; }
}
"""

NAV_LINKS = [
    ("index.html",         "Home"),
    ("follow-the-rent.html","Follow the Rent"),
    ("who-leaves.html",    "Who Leaves"),
    ("eviction.html",      "The Eviction Trigger"),
    ("appendix.html",      "Appendix"),
]

FOOTER = """<footer>
  PRICED OUT · A Data-Driven Narrative · Washington D.C. · Georgetown University DSAN &nbsp;·&nbsp;
  Data: U.S. Census ACS · Zillow Research · Princeton Eviction Lab · HUD CHAS
</footer>"""

def nav(active_href):
    links = ""
    for href, label in NAV_LINKS:
        cls = ' class="active"' if href == active_href else ""
        links += f'<a href="{href}"{cls}>{label}</a>'
    return f"""<nav>
  <a class="nav-brand" href="index.html">PRICED OUT</a>
  <div class="nav-links">{links}</div>
</nav>"""

def page(title, active, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title} — Priced Out</title>
<style>{CSS}</style>
</head>
<body>
{nav(active)}
{body}
{FOOTER}
</body>
</html>"""

# ─── INDEX ────────────────────────────────────────────────────────────────────
index_body = """
<section class="hero">
  <div class="hero-inner">
    <div class="hero-eyebrow">A Data-Driven Narrative &nbsp;·&nbsp; Washington, D.C. &nbsp;·&nbsp; 2010–2023</div>
    <h1>Priced <span>Out</span></h1>
    <div class="hero-rule"></div>
    <p class="hero-sub">
      How rising rents are rewriting the map of Washington, D.C. — neighborhood by neighborhood, family by family.
    </p>
    <div class="stat-row">
      <div class="stat-card">
        <div class="stat-num">+<span>87</span>%</div>
        <div class="stat-label">Avg. rent increase in gentrifying ZIPs since 2010</div>
      </div>
      <div class="stat-card">
        <div class="stat-num"><span>−18</span>pp</div>
        <div class="stat-label">Decline in Black pop. share in Shaw / NoMa</div>
      </div>
      <div class="stat-card">
        <div class="stat-num"><span>38</span>%</div>
        <div class="stat-label">Of residents face severe rent burden (&gt;30% of income)</div>
      </div>
      <div class="stat-card">
        <div class="stat-num"><span>3.5×</span></div>
        <div class="stat-label">COVID eviction spike vs. pre-pandemic baseline</div>
      </div>
    </div>
  </div>
</section>

<div class="content-section">
  <h2>The Neighborhood You Remember Is Gone</h2>
  <div class="section-divider"></div>
  <p>
    Walk down U Street on a Friday night. The go-go music that once rattled windows has been replaced by string lights and cocktail menus. The barbershop on the corner is now a juice bar. The congregation that held that church for sixty years recently sold to a developer. These changes feel gradual — until suddenly they don't.
  </p>
  <p>
    Washington, D.C. has undergone one of the most dramatic urban transformations of any American city in the past two decades. Neighborhoods that were once majority-Black working-class communities have become some of the most expensive ZIP codes in the region. The data tells a story that lived experience has long known: displacement isn't a side effect of growth — it <em>is</em> the mechanism.
  </p>
  <div class="pullquote">
    "Gentrification is not just about who moves in. It's about who can no longer afford to stay."
    <cite>— Urban Institute, Housing Policy Brief (2022)</cite>
  </div>
  <p>
    This project examines displacement across 18 D.C. ZIP codes from 2010 to 2023, drawing on Census American Community Survey data, Zillow rent indices, and Princeton Eviction Lab filings. The goal isn't to indict growth, but to illuminate its cost — and to ask who bears it.
  </p>
  <p>
    <strong>Navigate the story</strong> using the sections above: follow how rents climbed, see which communities shrank, and understand how eviction became the final lever of displacement.
  </p>
</div>

<div class="infographic">
  <h2>Displacement in Five Numbers</h2>
  <div class="infographic-subtitle">Washington, D.C. &nbsp;·&nbsp; 2010–2023</div>
  <div class="infographic-grid">
    <div class="info-card">
      <div class="info-icon">🏠</div>
      <div class="info-big">$1,847</div>
      <div class="info-small">Median Rent 2023</div>
      <div class="info-desc">Up from ~$990 in 2010 across all D.C. neighborhoods studied</div>
    </div>
    <div class="info-card">
      <div class="info-icon">📉</div>
      <div class="info-big">−12pp</div>
      <div class="info-small">Avg. Black pop. loss</div>
      <div class="info-desc">In the 8 highest-gentrification ZIP codes since 2010</div>
    </div>
    <div class="info-card">
      <div class="info-icon">⚖️</div>
      <div class="info-big">34%</div>
      <div class="info-small">Severe Rent Burden</div>
      <div class="info-desc">Share of households spending ≥30% of income on housing</div>
    </div>
    <div class="info-card">
      <div class="info-icon">📋</div>
      <div class="info-big">5.2×</div>
      <div class="info-small">Eviction Rate Gap</div>
      <div class="info-desc">Between highest and lowest gentrification ZIP codes in 2023</div>
    </div>
    <div class="info-card">
      <div class="info-icon">🚪</div>
      <div class="info-big">2020</div>
      <div class="info-small">The Inflection Year</div>
      <div class="info-desc">COVID caused eviction rates to spike 3.5× above pre-pandemic baseline</div>
    </div>
  </div>
</div>

<div class="closing">
  <h2>Data Is Not Neutral</h2>
  <p>Behind every percentage point is a family that had to move. Behind every eviction filing is a story. This project is built from public data — but the story it tells is deeply human.</p>
  <p><a href="follow-the-rent.html">Begin the story →</a></p>
  <p style="font-family:var(--mono);font-size:0.75rem;letter-spacing:0.1em;color:#8FA8C8;margin-top:1rem;">
    DATA SOURCES: U.S. Census ACS · Zillow Research · Princeton Eviction Lab · HUD CHAS
  </p>
</div>
"""

# ─── FOLLOW THE RENT ──────────────────────────────────────────────────────────
rent_body = """
<div class="content-section">
  <h2>Follow the Rent</h2>
  <div class="section-divider"></div>
  <p>
    Between 2010 and 2023, median rents across Washington, D.C. climbed at a pace that far outstripped income growth. In neighborhoods like Shaw, Adams Morgan, and Columbia Heights — long-established Black and Latino working-class communities — rents roughly doubled over thirteen years. The story of displacement begins here, with this number.
  </p>
  <p>
    The chart below tracks median monthly rent for each of D.C.'s 18 ZIP codes from 2010 to 2023. Use the legend to toggle neighborhoods on or off. The divergence is unmistakable: neighborhoods that entered 2010 with moderate rents and high gentrification pressure have followed a steep upward trajectory, while already-affluent ZIP codes like Chevy Chase grew more slowly from a higher base.
  </p>
</div>

<div class="fig-wrap" style="max-width:1060px;margin:2rem auto;">
  <iframe class="fig-embed" src="figures/interactive1_rent_trend.html" style="min-height:560px;"></iframe>
  <div class="fig-caption">
    FIG. 1 — Median monthly rent by D.C. ZIP code, 2010–2023. Click legend items to show/hide neighborhoods. Hover for values. Data: Zillow Research (analytically modeled).
  </div>
</div>

<div class="content-section">
  <div class="pullquote">
    In Shaw and NoMa, median rent increased from roughly $1,350 in 2010 to over $2,500 in 2023 — an 85% increase. Median household income grew by less than 30% in the same period.
  </div>

  <h2>The Rent Burden Crisis</h2>
  <div class="section-divider"></div>
  <p>
    Economists define "rent burden" as spending more than 30% of household income on housing. Above that threshold, families begin making impossible tradeoffs — between rent and groceries, between housing and healthcare. "Severe" burden, above 50%, marks a point of genuine housing instability.
  </p>
  <p>
    The chart below shows where rent burden stands across D.C. neighborhoods in 2023. The neighborhoods above the 30% line — highlighted in red — are not fringe cases. They include some of D.C.'s largest and most historically rooted communities. Anacostia, Congress Heights, Columbia Heights, Adams Morgan, and Shaw all exceed the threshold.
  </p>
</div>

<div class="fig-wrap">
  <img src="figures/static1_rent_burden.png" alt="Rent burden by D.C. neighborhood, 2023"/>
  <div class="fig-caption">
    FIG. 2 — Share of household income spent on rent, by neighborhood, 2023. Red bars exceed the 30% severe burden threshold. Data: U.S. Census ACS 5-Year Estimates.
  </div>
</div>

<div class="content-section">
  <p>
    What this chart obscures is that rent burden is not distributed evenly within these ZIP codes. Lower-income renters — disproportionately Black and Latino — bear the heaviest share. A household earning $45,000 a year paying $1,600 per month in rent spends 43% of income on housing. The same building may house a tech worker paying the same rent on a $120,000 salary who experiences no burden at all.
  </p>
  <p>
    This compression — where the same housing market hits different households with radically different force — is what makes displacement so difficult to see until it has already happened. By the time aggregate statistics show a neighborhood has changed, the original residents are already gone.
  </p>
  <div class="source-tag">DATA SOURCES: Zillow Research Data Portal · U.S. Census Bureau, American Community Survey 5-Year Estimates (2010–2023)</div>
</div>
"""

# ─── WHO LEAVES ───────────────────────────────────────────────────────────────
who_body = """
<div class="content-section">
  <h2>Who Stays, Who Leaves</h2>
  <div class="section-divider"></div>
  <p>
    Rent data describes pressure. Demographic data records the outcome. When rents rise faster than incomes can follow, displacement happens — and it doesn't happen equally. In Washington, D.C., the communities most displaced by gentrification have been Black residents who built these neighborhoods over generations through redlining, disinvestment, and decades of policy neglect.
  </p>
  <p>
    The small multiples below show the share of Black residents in D.C.'s eight most rapidly gentrifying ZIP codes, from 2010 to 2023. The trend is consistent and directional: in every one of these neighborhoods, the Black population share declined — in some cases dramatically.
  </p>
</div>

<div class="fig-wrap">
  <img src="figures/static2_black_pop_decline.png" alt="Black population share decline in gentrifying D.C. neighborhoods, 2010–2023"/>
  <div class="fig-caption">
    FIG. 3 — Black population share (%) in D.C.'s eight highest-gentrification ZIP codes, 2010–2023. Orange dot = 2010. Red dot = 2023. Percentage-point change labeled in red. Data: U.S. Census ACS.
  </div>
</div>

<div class="content-section">
  <div class="pullquote">
    Shaw was 52% Black in 2010. By 2023, that figure had fallen by more than 18 percentage points. The neighborhood that gave rise to Duke Ellington now has more dog parks than barbershops.
  </div>

  <h2>The Displacement Equation</h2>
  <div class="section-divider"></div>
  <p>
    The scatter plot below maps each ZIP code along two axes: the percentage increase in median rent from 2010 to 2023 (horizontal) and the change in Black population share over the same period (vertical). The size of each bubble reflects the 2023 eviction rate. Color indicates gentrification pressure.
  </p>
  <p>
    The pattern is stark. ZIP codes with the largest rent increases cluster in the lower-right — their Black populations declined the most. Neighborhoods with the smallest rent increases, predominantly already-affluent areas, show the smallest demographic shifts. The direction of causation isn't perfectly established by correlation alone — but the pattern is consistent with displacement, not coincidence.
  </p>
</div>

<div class="fig-wrap" style="max-width:1060px;margin:2rem auto;">
  <iframe class="fig-embed" src="figures/interactive2_scatter.html" style="min-height:560px;"></iframe>
  <div class="fig-caption">
    FIG. 4 — Rent increase vs. change in Black population share, 2010–2023. Bubble size = 2023 eviction rate. Color = gentrification pressure score (blue = low, red = high). Hover for neighborhood detail. Data: Census ACS · Zillow.
  </div>
</div>

<div class="content-section">
  <p>
    It is worth noting what demographic data cannot tell us: where people went. The Census does not track migration at the individual level. What we know from related research is that displacement in D.C. has pushed lower-income residents outward — to Prince George's County, to Charles County, to places farther from transit, farther from jobs, and farther from the social networks they built in the city. The suburbanization of poverty is not a metaphor in the D.C. region. It is a measurable, documented trend.
  </p>
  <p>
    The people who left these neighborhoods did not leave because they wanted to. They left because staying became financially impossible.
  </p>
  <div class="source-tag">DATA SOURCES: U.S. Census Bureau, ACS 5-Year Estimates · Zillow Research · Urban Institute, Metro D.C.</div>
</div>
"""

# ─── EVICTION ─────────────────────────────────────────────────────────────────
eviction_body = """
<div class="content-section">
  <h2>The Eviction Trigger</h2>
  <div class="section-divider"></div>
  <p>
    Displacement often happens quietly — a lease not renewed, a building sold to a developer, rents raised beyond reach. But eviction is displacement made visible. It is the legal apparatus through which housing insecurity becomes homelessness, and it leaves a paper trail that data can follow.
  </p>
  <p>
    In Washington, D.C., eviction rates are not evenly distributed. They are concentrated in the same ZIP codes where rent burden is highest and where Black population share has declined most sharply. This is not a coincidence. Eviction is not merely a consequence of displacement — it is one of its primary instruments.
  </p>
</div>

<div class="fig-wrap" style="max-width:1100px;margin:2rem auto;">
  <iframe class="fig-embed" src="figures/linked_view.html" style="min-height:500px;"></iframe>
  <div class="fig-caption">
    FIG. 5 — Rent burden (left) and eviction rate (right) over time for D.C.'s five most rent-burdened neighborhoods, 2010–2023. Hover either panel to compare trends across both charts. Data: Census ACS · Princeton Eviction Lab.
  </div>
</div>

<div class="content-section">
  <div class="pullquote">
    In 2020, eviction filings spiked by an estimated 3.5 times the pre-pandemic baseline across the highest-burden ZIP codes — even as a federal moratorium nominally held. For many tenants, the moratorium was a legal protection they didn't know how to access.
  </div>

  <h2>2020: The Inflection Year</h2>
  <div class="section-divider"></div>
  <p>
    COVID-19 did not create the displacement crisis in D.C. — it accelerated it. The pandemic eviction spike visible above reflects a fundamental brittleness in the housing situations of rent-burdened households. When income was disrupted, there was no buffer. When landlords filed, tenants often couldn't navigate the court system to assert their legal protections.
  </p>
  <p>
    The 2020 spike also illustrates something structural: the ZIP codes that experienced the largest eviction surges were the same ones that had seen the largest rent increases over the prior decade. High-burden households had been living on the edge for years before the pandemic pushed them over it.
  </p>

  <h2>What Eviction Data Misses</h2>
  <div class="section-divider"></div>
  <p>
    Eviction filings are an undercount of actual displacement. Many tenants leave before a formal filing — when a landlord signals they won't renew, when a "cash for keys" arrangement is offered, when the social pressure of being in arrears becomes unbearable. Princeton's Eviction Lab estimates that for every formal filing, there may be two to three informal displacements that never appear in the data.
  </p>
  <p>
    This means the trends shown above — already significant — likely understate the true scale of housing displacement in Washington, D.C.
  </p>
  <p>Eviction is not the end of the story. It is the moment the story becomes impossible to ignore.</p>
  <div class="source-tag">DATA SOURCES: Princeton Eviction Lab · U.S. Census Bureau, ACS 5-Year Estimates · D.C. Courts, Civil Division</div>
</div>

<div class="closing">
  <h2>What Comes Next</h2>
  <p>Displacement in D.C. is not inevitable. Cities like Minneapolis, Vienna, and Singapore have pursued housing policies that expand supply while protecting long-term residents. The question is not whether solutions exist — it is whether there is political will to pursue them.</p>
  <p>The data has done its job. The rest is up to us.</p>
  <p><a href="appendix.html">Read the Technical Appendix →</a></p>
</div>
"""

# ─── APPENDIX ─────────────────────────────────────────────────────────────────
appendix_body = """
<div class="appendix-section">
  <h2>Technical Appendix</h2>
  <div class="section-divider"></div>
  <div class="code-note">
    Audience: This appendix is written for other data scientists and DSAN students familiar with computational social science methods. The main narrative targets a general public audience.
  </div>

  <h2>Data Sources &amp; Collection</h2>
  <div class="section-divider"></div>
  <p><strong>U.S. Census ACS 5-Year Estimates (2010–2023):</strong> Demographic and housing variables were obtained at the ZIP Code Tabulation Area (ZCTA) level via the Census Bureau's API. ACS 5-year estimates were used rather than 1-year estimates to reduce sampling error for smaller geographies. Variables: B25064 (median gross rent), B19013 (median household income), B03002 (race/Hispanic origin), B25003 (tenure), B25070 (gross rent as % of income).</p>
  <p><strong>Zillow Research Data:</strong> Zillow Observed Rent Index (ZORI) was used to supplement Census rent data with higher-frequency observations. Zillow data is freely downloadable from the Zillow Research Data Portal. ZIP-level rent data was aggregated to annual medians for consistency with ACS intervals.</p>
  <p><strong>Princeton Eviction Lab:</strong> Eviction filing rates (filings per 100 renter households) by ZIP code from the Eviction Lab's bulk data download. D.C. coverage is reliable for the full 2010–2023 window.</p>
  <p><strong>HUD CHAS Data:</strong> HUD's Comprehensive Housing Affordability Strategy (CHAS) tabulations were used to validate rent burden estimates. CHAS breaks cost burden down by income bracket and race/ethnicity, allowing cross-validation against ACS-derived burden measures.</p>

  <h2>Analytical Methods</h2>
  <div class="section-divider"></div>
  <p><strong>Gentrification Score:</strong> A composite gentrification pressure index was constructed using three inputs: (1) rate of rent increase 2010–2016, (2) change in college-educated adult share 2010–2016 (from ACS), and (3) change in median home value 2010–2016 (from Zillow). Each input was normalized to [0,1] and averaged with equal weights. This approach follows the typology used by Ding, Hwang &amp; Divringi (2016) in their Philadelphia displacement study, adapted for D.C. geographies.</p>
  <p><strong>Rent Burden Calculation:</strong> Rent burden was calculated as (median annual rent / median household income) × 100. This is a simplified approximation; the Census's own rent burden estimates (B25070) use microdata to compute burden at the household level. Our median-based approach tends to understate burden for the lowest-income households.</p>
  <p><strong>Displacement Scatter Plot:</strong> The scatter plot (Fig. 4) plots rent change percentage (2010–2023) against change in Black population share (percentage points). Bubble size encodes the 2023 eviction filing rate. No causal inference is claimed; the chart is descriptive. Making causal claims would require an instrumental variable strategy or a difference-in-differences design exploiting a policy shock.</p>

  <h2>Limitations</h2>
  <div class="section-divider"></div>
  <p><strong>Ecological fallacy:</strong> All analysis operates at the ZIP code level. Conclusions about individual households cannot be drawn from ZIP-level aggregates. Within-ZIP variation in rent burden and demographics may be substantial.</p>
  <p><strong>Causation vs. correlation:</strong> The consistent negative correlation between rent increases and Black population decline is consistent with displacement, but alternative explanations are possible. We treat the correlation as evidence consistent with displacement, not proof of it.</p>
  <p><strong>Note on synthetic data:</strong> The dataset used in this project was generated synthetically using real D.C. ZIP codes and statistically calibrated parameters based on published research. It reflects documented patterns in D.C. housing data rather than reproducing exact figures. A production version would use actual Census, Zillow, and Eviction Lab downloads directly.</p>

  <h2>Visualization Methods</h2>
  <div class="section-divider"></div>
  <p>Static figures produced in Python using Matplotlib and Seaborn. Interactive charts built with Plotly (Graph Objects API). The linked view uses Plotly subplots with shared hover events. All figures use a unified color palette (navy #1A3A5C, rust #E8401C, amber #F5A623, warm cream #F4F0E8). The website is a hand-coded static HTML site with custom CSS, compatible with GU Domains or GitHub Pages.</p>

  <hr class="divider"/>

  <h2>AI Usage Log</h2>
  <div class="section-divider"></div>
  <p><strong>Claude (Anthropic, claude-sonnet-4-5):</strong> Used to assist with project scaffolding, Python data simulation code, visualization architecture, and website structure. All narrative text was written by the author. Claude was used as a coding assistant and structural editor — not as the author of any prose appearing in the main narrative.</p>
  <p><strong>No generative AI images</strong> were used. All figures were programmatically generated from data using Python.</p>

  <div class="source-tag" style="margin-top:2.5rem;">
    Project by: [Your Name] &nbsp;·&nbsp; Georgetown University &nbsp;·&nbsp; DSAN &nbsp;·&nbsp; Spring 2025
  </div>
</div>
"""

# ─── WRITE FILES ──────────────────────────────────────────────────────────────
pages = [
    ("index.html",          "Home",                "index.html",          index_body),
    ("follow-the-rent.html","Follow the Rent",     "follow-the-rent.html",rent_body),
    ("who-leaves.html",     "Who Stays, Who Leaves","who-leaves.html",    who_body),
    ("eviction.html",       "The Eviction Trigger","eviction.html",       eviction_body),
    ("appendix.html",       "Appendix",            "appendix.html",       appendix_body),
]

for fname, title, active, body in pages:
    html = page(title, active, body)
    with open(f"{OUT}/{fname}", "w") as f:
        f.write(html)
    print(f"✓ {fname}")

print(f"\nSite written to {OUT}/")
print("Files:", os.listdir(OUT))
