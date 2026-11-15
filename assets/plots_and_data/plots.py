"""LinkedIn games: two interactive charts from linkedin_games.csv.
Run:  python linkedin_games_plots.py linkedin_games.csv
Makes linkedin_games.html next to the CSV. Open it in any browser (works offline).
Needs: pip install plotly pandas
"""
import sys,html
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
ME,AVG="#E85A4A","#009490"  # coral = me, teal = average (checked for colour-blind separation and contrast)
INK,MUTED,GRID="#1f1f1f","#6b6b6b","#ececec"
# One colour per game, picked to suggest each game and checked so neighbouring games stay distinguishable (incl. colour-blind).
# LinkedIn doesn't publish official game colours; to use your own, change the hex codes here.
GAME_COL={"crossclimb":"#2a78d6","patches":"#e87ba4","queens":"#6250d6","sudoku":"#008300","tango":"#eda100","wend":"#1baf7a","zip":"#eb6834"}
EXTRA=["#e34948","#8a6d3b","#5f6b7a"]  # for any new game not listed above
WEEK=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
ABBR={"Monday":"Mon","Tuesday":"Tue","Wednesday":"Wed","Thursday":"Thu","Friday":"Fri","Saturday":"Sat","Sunday":"Sun"}
def mmss(s):return f"{int(s)//60}:{int(s)%60:02d}"
def load(path):
    df=pd.read_csv(path,skipinitialspace=True)
    df.columns=[c.strip() for c in df.columns]
    df["Game"]=df["Game"].str.strip().str.lower().replace({"mini sudoku":"sudoku"})  # same game, two spellings in the log
    df["Hint"]=pd.to_numeric(df["Hint"],errors="coerce")  # blank hint -> not recorded
    # One "session" per day played. Uses a Date column if you add one; otherwise counts each change of day name in row order.
    if "Date" in df.columns:
        d=df["Date"].astype(str).str.strip()  # day/month/year, with a 2- or 4-digit year
        df["Date"]=pd.to_datetime(d,format="%d/%m/%y",errors="coerce").fillna(pd.to_datetime(d,format="%d/%m/%Y",errors="coerce"))
        df["Session"]=df["Date"].rank(method="dense").astype(int)
        df["Label"]=df["Date"].dt.strftime("%a %d %b")
    else:
        df["Session"]=(df["Day"]!=df["Day"].shift()).cumsum()
        df["Label"]=df["Day"].map(ABBR).fillna(df["Day"])+" "+df["Session"].astype(str)
    df["Score"]=df["Average Time"]/df["My Time"]  # 2.0 = twice as fast as average, 0.5 = twice as slow
    df["Pct"]=(df["Average Time"]-df["My Time"])/df["Average Time"]*100  # +40 = took 40% less time than average, -40 = 40% more
    df["HintTxt"]=df["Hint"].apply(lambda h:"not recorded" if pd.isna(h) else str(int(h)))
    return df
def style(fig,title,sub):
    fig.update_layout(template="plotly_white",font=dict(family="Inter, system-ui, sans-serif",color=INK,size=13),
        title=dict(text=f"<b>{title}</b><br><span style='font-size:13px;color:{MUTED}'>{sub}</span>",x=0,xanchor="left"),
        margin=dict(l=60,r=30,t=90,b=60),hoverlabel=dict(bgcolor="white",font_size=13,bordercolor="#d0d0d0"),plot_bgcolor="white")
    return fig
def scatter(df):
    games=sorted(df["Game"].unique());col={g:GAME_COL.get(g,EXTRA[i%len(EXTRA)]) for i,g in enumerate(games)}
    df=df.copy();df["DayIdx"]=df["Day"].str.strip().str.capitalize().map(WEEK.index)
    off={g:(i-(len(games)-1)/2)*0.1 for i,g in enumerate(games)}  # each game gets its own slot within a day, so dots don't sit on top of each other
    df["X"]=df["DayIdx"]+df["Game"].map(off)
    df["Size"]=(df["Score"].clip(0.25,4)**0.5)*15
    fig=go.Figure()
    for g in games:
        d=df[df["Game"]==g]
        cd=pd.DataFrame({"g":d["Game"],"l":d["Label"],"m":d["My Time"].map(mmss),"a":d["Average Time"].map(mmss),
            "s":d["Score"].map(lambda v:f"{v:.2f}×"),"p":d["Pct"].map(lambda p:f"{abs(p):.0f}% {'less' if p>=0 else 'more'} time"),"h":d["HintTxt"]})
        fig.add_trace(go.Scatter(x=d["X"],y=d["My Time"],mode="markers",name=g,legendgroup=g,
            marker=dict(size=d["Size"],sizemin=6,color=col[g],opacity=0.9,line=dict(color="white",width=1.5)),customdata=cd,
            hovertemplate="<b>%{customdata[0]}</b> · %{customdata[1]}<br>Me: <b>%{customdata[2]}</b> vs average %{customdata[3]}<br>Score %{customdata[4]} (%{customdata[5]})<br>Hints: %{customdata[6]}<extra></extra>"))
    # Weekly trend: median time per weekday across all games (and all weeks)
    med=df.groupby("DayIdx")[["Average Time","My Time"]].median().reset_index()
    fig.add_trace(go.Scatter(x=med["DayIdx"],y=med["Average Time"],mode="lines",name="Average player, median",legendgroup="trend",legendgrouptitle_text="Weekly trend",
        line=dict(color="#9a9a9a",width=2,dash="dash"),hovertemplate="Median average-player time: %{y:.0f}s<extra></extra>"))
    fig.add_trace(go.Scatter(x=med["DayIdx"],y=med["My Time"],mode="lines",name="Me, median",legendgroup="trend",
        line=dict(color="#3a3a3a",width=2),hovertemplate="My median time: %{y:.0f}s<extra></extra>"))
    # Size key (legend only): dot size = how many times faster than the average player
    for r,lab in((0.5,"0.5× (twice as slow)"),(1,"1× (same as average)"),(2,"2× (twice as fast)")):
        fig.add_trace(go.Scatter(x=[None],y=[None],mode="markers",name=lab,legendgroup="key",legendgrouptitle_text="Dot size vs average",
            marker=dict(size=(r**0.5)*15,color="#8a8a8a",line=dict(color="white",width=1.5))))
    top=max(df["My Time"].max(),df["Average Time"].max());step=30 if top<=300 else 60 if top<=600 else 120
    ticks=list(range(0,int(top)+step,step))
    fig.update_yaxes(title="Time (m:ss)",rangemode="tozero",gridcolor=GRID,zeroline=False,tickvals=ticks,ticktext=[mmss(t) for t in ticks])
    fig.update_xaxes(title=None,tickvals=list(range(7)),ticktext=WEEK,range=[-0.6,6.6],showgrid=False,zeroline=False)
    for i in range(1,7):fig.add_vline(x=i-0.5,line=dict(color=GRID,width=1))
    fig.update_layout(height=600,legend=dict(groupclick="togglegroup",tracegroupgap=14,title_text="Games"))
    return style(fig,"My times by day of the week","Each dot is one of my games: colour = game, size = how many times faster than the average player I was. Lower is faster. Click a game in the legend to hide or show it.")
def heatmap(df):
    games=sorted(df["Game"].unique());sess=df.drop_duplicates("Session")[["Session","Label"]]
    z,txt,hov=[],[],[]
    for g in games:
        zr,tr,hr=[],[],[]
        for s,l in sess.itertuples(index=False):
            r=df[(df["Game"]==g)&(df["Session"]==s)]
            if r.empty:zr.append(None);tr.append("");hr.append(f"<b>{g}</b> · {l}<br>Not played");continue
            r=r.iloc[0];p=max(-100,min(100,r["Pct"]))
            zr.append(p);h=r["Hint"]
            tr.append(f"{r['Pct']:+.0f}%"+(f"<br>{int(h)} hint{'s' if h!=1 else ''}" if pd.notna(h) and h>0 else ""))
            hr.append(f"<b>{g}</b> · {l}<br>Me {mmss(r['My Time'])} vs average {mmss(r['Average Time'])}<br><b>{abs(r['Pct']):.0f}% {'less' if r['Pct']>=0 else 'more'} time</b> than average<br>Hints: {r['HintTxt']}")
        z.append(zr);txt.append(tr);hov.append(hr)
    # Diverging: teal = slower than average, light grey = level, coral = faster
    scale=[[0,AVG],[0.25,"#8fcfcb"],[0.5,"#f1f1f1"],[0.75,"#f4ab9f"],[1,ME]]
    fig=go.Figure(go.Heatmap(z=z,x=sess["Session"],y=games,text=txt,texttemplate="%{text}",textfont=dict(size=12,color=INK),
        customdata=hov,hovertemplate="%{customdata}<extra></extra>",colorscale=scale,zmid=0,zmin=-100,zmax=100,xgap=3,ygap=3,
        colorbar=dict(title=dict(text="vs average",side="top"),tickvals=[-100,-50,0,50,100],ticktext=["2× slower","50% more","level","50% less","instant"],len=0.8,thickness=12)))
    fig.update_yaxes(autorange="reversed",showgrid=False,title=None)
    short=df.drop_duplicates("Session")["Day"].str.strip().str[:3].str.capitalize()
    fig.update_xaxes(showgrid=False,side="top",title=None,tickvals=sess["Session"],ticktext=list(short))
    fig.update_layout(height=120+60*len(games))
    return style(fig,"Where I beat the average","Each square is one game on one day. The number is how much less (+) or more (−) time I took than the average player. Coral = faster, teal = slower.")
def main(csv):
    csv=Path(csv);df=load(csv)
    a,b=scatter(df),heatmap(df)
    played=len(df);beat=(df["Pct"]>0).sum()
    table=df[["Label","Game","My Time","Average Time","Hint"]].assign(**{"Less time than avg":df["Pct"].map(lambda p:f"{p:+.0f}%")}).to_html(index=False,border=0,classes="t",na_rep="—")
    page=f"""<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>LinkedIn games</title>
<style>body{{font-family:Inter,system-ui,sans-serif;background:#fff;color:{INK};max-width:1100px;margin:0 auto;padding:24px 16px}}h1{{font-size:1.6rem;margin:0 0 4px}}.sub{{color:{MUTED};margin:0 0 20px}}
.chart{{border:1px solid #e6e6e6;border-radius:10px;padding:8px;margin-bottom:24px}}details{{margin-top:8px}}summary{{cursor:pointer;color:{MUTED}}}table.t{{border-collapse:collapse;font-size:.9rem;margin-top:10px}}.t th,.t td{{padding:6px 10px;border-bottom:1px solid #eee;text-align:left}}</style></head><body>
<h1>LinkedIn games</h1><p class="sub">{df['Session'].nunique()} days · {played} games · beat the average in {beat} of {played}</p>
<div class="chart" id="by-day">{a.to_html(full_html=False,include_plotlyjs="cdn",config={"displaylogo":False})}</div>
<div class="chart" id="heatmap">{b.to_html(full_html=False,include_plotlyjs=False,config={"displaylogo":False})}</div>
<details><summary>Show the data as a table</summary>{table}</details></body></html>"""
    out=csv.with_name("linkedin_games.html");out.write_text(page,encoding="utf-8");print("Saved",out)
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else "linkedin_games.csv")
