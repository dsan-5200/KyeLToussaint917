"""
Generate all figures for the DC Displacement project.
- 2 static (matplotlib/seaborn)
- 2 interactive (plotly → HTML)
- 1 linked view (plotly subplot)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json, os

# ── Paths ──────────────────────────────────────────────────────────────────────
DATA = "/home/claude/displacement-project/data/dc_displacement.csv"
OUT  = "/home/claude/displacement-project/figures"
os.makedirs(OUT, exist_ok=True)

df = pd.read_csv(DATA)

# ── Palette / theme ────────────────────────────────────────────────────────────
ACCENT   = "#E8401C"   # burnt orange
BLUE     = "#1A3A5C"   # deep navy
GOLD     = "#F5A623"   # amber
LIGHT    = "#F4F0E8"   # warm off-white
MID      = "#8FA8C8"   # muted blue
DARK_BG  = "#0F1923"   # near-black

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.facecolor": LIGHT,
    "figure.facecolor": LIGHT,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#CCCCCC",
    "text.color": BLUE,
    "axes.labelcolor": BLUE,
    "xtick.color": BLUE,
    "ytick.color": BLUE,
    "grid.color": "#DDDDDD",
    "grid.linewidth": 0.6,
})


fig, ax = plt.subplots(figsize=(11, 7))
fig.patch.set_facecolor(LIGHT)

d23 = df[df.year == 2023].sort_values("rent_burden_pct", ascending=True)
colors = [ACCENT if b >= 30 else BLUE for b in d23.rent_burden_pct]

bars = ax.barh(d23.neighborhood, d23.rent_burden_pct, color=colors,
               edgecolor="white", linewidth=0.6, height=0.7)

ax.axvline(30, color=GOLD, linewidth=1.8, linestyle="--", zorder=5)
ax.text(30.5, len(d23) - 0.6, "Severe burden\nthreshold (30%)",
        color=GOLD, fontsize=8.5, fontweight="bold", va="top")

for bar, val in zip(bars, d23.rent_burden_pct):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%", va="center", fontsize=8.5,
            color=ACCENT if val >= 30 else BLUE, fontweight="bold")

ax.set_xlabel("Share of income spent on rent (%)", fontsize=11, labelpad=8)
ax.set_title("Who's Rent-Burdened in D.C.?", fontsize=16, fontweight="bold",
             pad=16, color=BLUE)
ax.text(0.0, 1.01, "Neighborhoods where residents spend ≥30% of income on rent, 2023",
        transform=ax.transAxes, fontsize=10, color="#555555")

legend_handles = [
    mpatches.Patch(color=ACCENT, label="Severely rent-burdened (≥30%)"),
    mpatches.Patch(color=BLUE,   label="Below threshold"),
]
ax.legend(handles=legend_handles, loc="lower right", framealpha=0.7,
          edgecolor="#CCCCCC", fontsize=9)
ax.set_xlim(0, 55)
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%g%%'))
plt.tight_layout()
plt.savefig(f"{OUT}/static1_rent_burden.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ static1_rent_burden.png")


#Black population share decline: small multiples

high_gentrify = df[df.gentrify_score >= 0.75]["zip"].unique()
sub = df[df.zip.isin(high_gentrify)]
neighborhoods = sub[["zip", "neighborhood"]].drop_duplicates().set_index("zip")["neighborhood"].to_dict()

fig, axes = plt.subplots(2, 4, figsize=(14, 7), sharey=False)
fig.patch.set_facecolor(LIGHT)
axes_flat = axes.flatten()

for i, z in enumerate(high_gentrify[:8]):
    ax = axes_flat[i]
    zdf = sub[sub.zip == z].sort_values("year")
    ax.fill_between(zdf.year, zdf.black_pct, alpha=0.25, color=BLUE)
    ax.plot(zdf.year, zdf.black_pct, color=BLUE, linewidth=2)
    ax.plot(zdf.year.iloc[0],  zdf.black_pct.iloc[0],  "o", color=GOLD,   zorder=5, ms=6)
    ax.plot(zdf.year.iloc[-1], zdf.black_pct.iloc[-1], "o", color=ACCENT, zorder=5, ms=6)
    ax.set_title(neighborhoods[z], fontsize=9, fontweight="bold", color=BLUE, pad=5)
    ax.set_ylabel("Black pop. %", fontsize=8)
    ax.set_xticks([2010, 2016, 2023])
    ax.tick_params(labelsize=7.5)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%g%%'))
    pct_change = zdf.black_pct.iloc[-1] - zdf.black_pct.iloc[0]
    ax.text(0.97, 0.08, f"{pct_change:+.1f}pp", transform=ax.transAxes,
            fontsize=9, color=ACCENT, ha="right", fontweight="bold")

fig.suptitle("Black Residents Disappearing from Gentrifying D.C. Neighborhoods",
             fontsize=15, fontweight="bold", color=BLUE, y=1.01)
fig.text(0.5, 0.98, "% Black population, 2010–2023  |  Orange dot = 2010, Red dot = 2023",
         ha="center", fontsize=9.5, color="#555555")
plt.tight_layout()
plt.savefig(f"{OUT}/static2_black_pop_decline.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ static2_black_pop_decline.png")

# Rent trend over time, filterable by ZIP
# 
fig = go.Figure()

zip_names = df[["zip","neighborhood"]].drop_duplicates().set_values = \
    dict(zip(df.zip.unique(), df.groupby("zip")["neighborhood"].first()))

color_seq = px.colors.qualitative.Dark24

for i, (z, grp) in enumerate(df.groupby("zip")):
    name = grp["neighborhood"].iloc[0]
    grp_s = grp.sort_values("year")
    visible = True if grp["gentrify_score"].iloc[0] > 0.7 else "legendonly"
    fig.add_trace(go.Scatter(
        x=grp_s.year, y=grp_s.median_rent,
        mode="lines+markers",
        name=name,
        visible=visible,
        line=dict(width=2.5, color=color_seq[i % len(color_seq)]),
        marker=dict(size=5),
        hovertemplate=(
            f"<b>{name}</b><br>"
            "Year: %{x}<br>"
            "Median Rent: $%{y:,.0f}<extra></extra>"
        )
    ))

fig.update_layout(
    title=dict(text="Median Rent by D.C. Neighborhood (2010–2023)",
               font=dict(size=20, color=BLUE), x=0.01),
    xaxis=dict(title="Year", tickmode="linear", dtick=2,
               gridcolor="#E0E0E0", linecolor="#CCCCCC"),
    yaxis=dict(title="Median Monthly Rent ($)", tickprefix="$",
               gridcolor="#E0E0E0", linecolor="#CCCCCC"),
    plot_bgcolor=LIGHT,
    paper_bgcolor=LIGHT,
    font=dict(family="Georgia, serif", color=BLUE),
    legend=dict(title="Neighborhood", bgcolor="rgba(244,240,232,0.9)",
                bordercolor="#CCCCCC", borderwidth=1),
    hovermode="x unified",
    height=520,
)
fig.write_html(f"{OUT}/interactive1_rent_trend.html",
               include_plotlyjs="cdn", full_html=False)
print("✓ interactive1_rent_trend.html")


#Scatter: rent increase vs Black pop decline (2010→2023)

pivot = df[df.year.isin([2010, 2023])].copy()
p10 = pivot[pivot.year==2010][["zip","neighborhood","median_rent","black_pct","eviction_rate","gentrify_score"]].rename(
    columns={"median_rent":"rent_2010","black_pct":"black_2010","eviction_rate":"evict_2010"})
p23 = pivot[pivot.year==2023][["zip","median_rent","black_pct","eviction_rate"]].rename(
    columns={"median_rent":"rent_2023","black_pct":"black_2023","eviction_rate":"evict_2023"})
scatter_df = p10.merge(p23, on="zip")
scatter_df["rent_change_pct"] = ((scatter_df.rent_2023 - scatter_df.rent_2010) / scatter_df.rent_2010) * 100
scatter_df["black_change"]    = scatter_df.black_2023 - scatter_df.black_2010

fig2 = px.scatter(
    scatter_df,
    x="rent_change_pct",
    y="black_change",
    size="evict_2023",
    color="gentrify_score",
    color_continuous_scale=["#1A3A5C", "#E8401C"],
    hover_name="neighborhood",
    hover_data={
        "rent_change_pct": ":.1f",
        "black_change":    ":.1f",
        "evict_2023":      ":.1f",
        "gentrify_score":  False,
    },
    labels={
        "rent_change_pct": "Rent Increase 2010–2023 (%)",
        "black_change":    "Change in Black Population Share (pp)",
        "evict_2023":      "Eviction Rate 2023 (%)",
        "gentrify_score":  "Gentrification Score",
    },
    title="The Displacement Equation: Rising Rent, Declining Black Residents",
    size_max=30,
)
fig2.add_hline(y=0, line_dash="dash", line_color="#999999", line_width=1)
fig2.add_annotation(x=scatter_df.rent_change_pct.max() * 0.95,
                    y=1.5, text="Population stable",
                    showarrow=False, font=dict(size=9, color="#888888"))
fig2.add_annotation(x=scatter_df.rent_change_pct.max() * 0.95,
                    y=-1.5, text="Population declining",
                    showarrow=False, font=dict(size=9, color=ACCENT))
fig2.update_layout(
    plot_bgcolor=LIGHT, paper_bgcolor=LIGHT,
    font=dict(family="Georgia, serif", color=BLUE),
    height=520,
    coloraxis_colorbar=dict(title="Gentrify<br>Score"),
)
fig2.write_html(f"{OUT}/interactive2_scatter.html",
                include_plotlyjs="cdn", full_html=False)
print("✓ interactive2_scatter.html")


#Rent burden over time + eviction rate (side by side, shared x)

linked = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Rent Burden Over Time (%)", "Eviction Rate Over Time (%)"),
    shared_xaxes=False,
)

top5 = df[df.year==2023].nlargest(5, "rent_burden_pct")["zip"].tolist()
colors5 = [ACCENT, BLUE, GOLD, "#4CAF50", "#9C27B0"]

for idx, (z, c) in enumerate(zip(top5, colors5)):
    zdf = df[df.zip==z].sort_values("year")
    name = zdf["neighborhood"].iloc[0]
    linked.add_trace(go.Scatter(
        x=zdf.year, y=zdf.rent_burden_pct, name=name,
        line=dict(color=c, width=2.2), mode="lines+markers",
        legendgroup=name,
        hovertemplate=f"<b>{name}</b><br>Year: %{{x}}<br>Burden: %{{y:.1f}}%<extra></extra>",
    ), row=1, col=1)
    linked.add_trace(go.Scatter(
        x=zdf.year, y=zdf.eviction_rate, name=name,
        line=dict(color=c, width=2.2), mode="lines+markers",
        legendgroup=name, showlegend=False,
        hovertemplate=f"<b>{name}</b><br>Year: %{{x}}<br>Eviction: %{{y:.1f}}%<extra></extra>",
    ), row=1, col=2)

linked.update_layout(
    title=dict(text="Rent Burden & Evictions Move Together in D.C.'s Hardest-Hit Neighborhoods",
               font=dict(size=17, color=BLUE), x=0.02),
    plot_bgcolor=LIGHT, paper_bgcolor=LIGHT,
    font=dict(family="Georgia, serif", color=BLUE),
    height=460,
    legend=dict(bgcolor="rgba(244,240,232,0.9)", bordercolor="#CCCCCC", borderwidth=1),
    hovermode="x",
)
linked.update_xaxes(gridcolor="#E0E0E0", tickmode="linear", dtick=2)
linked.update_yaxes(gridcolor="#E0E0E0")
linked.write_html(f"{OUT}/linked_view.html",
                  include_plotlyjs="cdn", full_html=False)
print("✓ linked_view.html")

