import streamlit as st
import streamlit.components.v1 as components
import numpy as np

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(page_title="🎯 GuessVerse", page_icon="🎯", layout="centered")

# ==============================================================================
# DIFFICULTY CONFIG  (mirrors the original easy() / medium() / hard() functions)
# ==============================================================================
DIFFICULTIES = {
    "EASY":   {"low": 1,  "high": 30,  "max_attempts": 8, "hint_attempt": 6, "check5": False, "code": "01"},
    "MEDIUM": {"low": 1,  "high": 70,  "max_attempts": 6, "hint_attempt": 5, "check5": True,  "code": "02"},
    "HARD":   {"low": 1,  "high": 100, "max_attempts": 5, "hint_attempt": 5, "check5": True,  "code": "03"},
}


def build_hint(num: int, difficulty: str) -> str:
    """Reproduces the exact hint text/logic from the original script."""
    lines = []
    lines.append("Divisible by 2" if num % 2 == 0 else "Not divisible by 2")

    if difficulty == "EASY":
        lines.append("Divisible by 3." if num % 3 == 0 else "Not divisible by 3.")
        if 1 <= num <= 10:
            band = "1 - 10"
        elif 11 <= num <= 20:
            band = "11 - 20"
        else:
            band = "21 - 30"
        return f"{lines[0]} & {lines[1]}\nThe number is between {band}"

    else:
        lines.append("Divisible by 3" if num % 3 == 0 else "Not divisible by 3")
        lines.append("Divisible by 5." if num % 5 == 0 else "Not divisible by 5.")
        if difficulty == "MEDIUM":
            if 1 <= num <= 25:
                band = "1 - 25"
            elif 26 <= num <= 50:
                band = "26 - 50"
            else:
                band = "51 - 70"
        else:  # HARD
            if 1 <= num <= 25:
                band = "1 - 25"
            elif 26 <= num <= 50:
                band = "26 - 50"
            elif 51 <= num <= 75:
                band = "51 - 75"
            else:
                band = "76 - 100"
        return f"{lines[0]}, {lines[1]} & {lines[2]}\nThe number is between {band}"


# ==============================================================================
# THEMES & FONTS — user-selectable palette / typography
# ==============================================================================
THEMES = {
    "Neon Vault":    {"cyan": "#00f0ff", "magenta": "#ff2ee6", "amber": "#ffcc00", "green": "#39ff8f", "red": "#ff3b5c", "bg": "#080615", "ink": "#eae8ff", "dim": "#8b85b8", "swatch": ["#00f0ff", "#ff2ee6", "#080615"]},
    "Sunset Arcade": {"cyan": "#ff9d5c", "magenta": "#ff4d8d", "amber": "#ffd166", "green": "#ff7b54", "red": "#e63946", "bg": "#170b1f", "ink": "#fff1e6", "dim": "#c98fa0", "swatch": ["#ff9d5c", "#ff4d8d", "#170b1f"]},
    "Matrix Terminal": {"cyan": "#39ff14", "magenta": "#00ff9c", "amber": "#c6ff00", "green": "#39ff14", "red": "#ff2b2b", "bg": "#020a05", "ink": "#d8ffe0", "dim": "#5f9f6f", "swatch": ["#39ff14", "#00ff9c", "#020a05"]},
    "Cyber Purple":  {"cyan": "#8a5cff", "magenta": "#c74bff", "amber": "#ffb84d", "green": "#5cffb8", "red": "#ff4f9a", "bg": "#0c0620", "ink": "#efe6ff", "dim": "#9a89c9", "swatch": ["#8a5cff", "#c74bff", "#0c0620"]},
    "Ocean Depths":  {"cyan": "#4fd6e8", "magenta": "#4f7bff", "amber": "#ffd76a", "green": "#48e0b0", "red": "#ff6b6b", "bg": "#040f1a", "ink": "#e2f6ff", "dim": "#7ba0b8", "swatch": ["#4fd6e8", "#4f7bff", "#040f1a"]},
    "Rose Gold":     {"cyan": "#ffb6c1", "magenta": "#e07a9e", "amber": "#f6c453", "green": "#c9a86a", "red": "#d1495b", "bg": "#1c0f14", "ink": "#fff0f3", "dim": "#c99aa8", "swatch": ["#ffb6c1", "#f6c453", "#1c0f14"]},
}

FONTS = {
    "Arcade":       {"display": "'Press Start 2P', monospace", "body": "'Space Grotesk', sans-serif", "mono": "'Share Tech Mono', monospace",
                      "import": "Press+Start+2P&family=Space+Grotesk:wght@400;500;600;700&family=Share+Tech+Mono"},
    "Futuristic":   {"display": "'Orbitron', sans-serif", "body": "'Rajdhani', sans-serif", "mono": "'Share Tech Mono', monospace",
                      "import": "Orbitron:wght@600;800;900&family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono"},
    "Elegant":      {"display": "'Playfair Display', serif", "body": "'Lato', sans-serif", "mono": "'Space Mono', monospace",
                      "import": "Playfair+Display:wght@700;900&family=Lato:wght@400;600;700&family=Space+Mono"},
    "Playful":      {"display": "'Fredoka', sans-serif", "body": "'Nunito', sans-serif", "mono": "'Space Mono', monospace",
                      "import": "Fredoka:wght@500;600;700&family=Nunito:wght@400;600;700&family=Space+Mono"},
    "Classic Mono": {"display": "'IBM Plex Mono', monospace", "body": "'IBM Plex Sans', sans-serif", "mono": "'IBM Plex Mono', monospace",
                      "import": "IBM+Plex+Mono:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700"},
}

REACTION_PACKS = {
    "Classic": {"low": "📈", "high": "📉", "win_first": "🎉", "win": "🏆", "lose": "😔", "hint": "💡"},
    "Animals": {"low": "🐒", "high": "🦉", "win_first": "🐯", "win": "🦄", "lose": "🐢", "hint": "🦊"},
    "Faces":   {"low": "😅", "high": "😬", "win_first": "🤩", "win": "😎", "lose": "😭", "hint": "🤔"},
    "Space":   {"low": "🚀", "high": "🛰️", "win_first": "🌟", "win": "🪐", "lose": "☄️", "hint": "👽"},
    "Foodie":  {"low": "🍋", "high": "🌶️", "win_first": "🍰", "win": "🍾", "lose": "🥺", "hint": "🍿"},
}

if "theme_name" not in st.session_state:
    st.session_state.theme_name = "Neon Vault"
if "font_name" not in st.session_state:
    st.session_state.font_name = "Arcade"
if "reaction_name" not in st.session_state:
    st.session_state.reaction_name = "Classic"


def generate_css(theme: dict, font: dict) -> str:
    from string import Template
    css = Template("""
<style>
@import url('https://fonts.googleapis.com/css2?family=$FONT_IMPORT&display=swap');

:root{
    --bg-deep:$BG;
    --cyan:$CYAN;
    --magenta:$MAGENTA;
    --amber:$AMBER;
    --green:$GREEN;
    --red:$RED;
    --ink:$INK;
    --dim:$DIM;
    --font-display:$FONT_DISPLAY;
    --font-body:$FONT_BODY;
    --font-mono:$FONT_MONO;
}

html, body, [class*="css"]{
    font-family:var(--font-body);
}

.stApp{
    background:
        radial-gradient(ellipse at 50% -10%, rgba(255,46,230,0.18) 0%, transparent 55%),
        radial-gradient(ellipse at 50% 110%, rgba(0,240,255,0.14) 0%, transparent 55%),
        var(--bg-deep);
    overflow-x:hidden;
}

/* Animated retro grid horizon */
.grid-floor{
    position:fixed;
    left:0; right:0; bottom:0;
    height:46vh;
    background-image:
        linear-gradient(rgba(0,240,255,0.35) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,240,255,0.35) 1px, transparent 1px);
    background-size:56px 56px;
    transform:perspective(280px) rotateX(58deg) scale(2.1);
    transform-origin:bottom;
    mask-image:linear-gradient(to top, rgba(0,0,0,0.9), transparent 85%);
    -webkit-mask-image:linear-gradient(to top, rgba(0,0,0,0.9), transparent 85%);
    animation:gridScroll 3.2s linear infinite;
    z-index:0;
    pointer-events:none;
    opacity:0.55;
}
@keyframes gridScroll{ from{background-position-y:0;} to{background-position-y:56px;} }

.scanlines{
    position:fixed; inset:0; z-index:1; pointer-events:none;
    background:repeating-linear-gradient(to bottom, rgba(255,255,255,0.025) 0px, rgba(255,255,255,0.025) 1px, transparent 2px, transparent 3px);
    mix-blend-mode:overlay;
}

.main .block-container{ max-width:760px; padding-top:1.6rem; position:relative; z-index:2;}

/* ------------ THEME TOGGLE ICON ------------- */
div[data-testid="stPopover"] button{
    border-radius:50% !important;
    width:44px !important; height:44px !important;
    font-size:1.15rem !important;
    padding:0 !important;
    display:flex; align-items:center; justify-content:center;
}

/* ------------ HEADER ------------- */
.vault-header{ text-align:center; margin-bottom:1.6rem; }
.vault-header .eyebrow{
    font-family:var(--font-mono);
    letter-spacing:0.35em;
    font-size:0.72rem;
    color:var(--cyan);
    text-shadow:0 0 8px rgba(0,240,255,0.9);
    margin-bottom:0.6rem;
}
.vault-header h1{
    font-family:var(--font-display);
    font-size:1.85rem;
    color:var(--ink);
    text-shadow:
        0 0 6px var(--magenta),
        0 0 18px rgba(255,46,230,0.65),
        0 0 40px rgba(0,240,255,0.35);
    margin:0;
    animation:flicker 5s infinite;
}
@keyframes flicker{
    0%,97%,100%{opacity:1;}
    98%{opacity:0.72;}
    99%{opacity:0.92;}
}
.vault-header .sub{
    color:var(--dim); font-size:0.92rem; margin-top:0.55rem; font-family:var(--font-mono);
}

/* ------------ PANEL ------------- */
.panel{
    background:linear-gradient(160deg, rgba(20,16,46,0.92), rgba(10,8,28,0.92));
    border:1px solid rgba(0,240,255,0.28);
    border-radius:14px;
    padding:1.7rem 1.8rem;
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.02) inset,
        0 18px 40px rgba(0,0,0,0.55),
        0 0 30px rgba(0,240,255,0.06);
    margin-bottom:1.3rem;
    position:relative;
}
.panel::before{
    content:'';
    position:absolute; top:0; left:18px; right:18px; height:1px;
    background:linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity:0.7;
}
.panel-label{
    font-family:var(--font-mono);
    color:var(--magenta);
    font-size:0.72rem;
    letter-spacing:0.22em;
    margin-bottom:0.9rem;
    text-shadow:0 0 8px rgba(255,46,230,0.6);
}

/* ------------ DIFFICULTY CARDS ------------- */
.diff-card{
    border-radius:12px;
    padding:1.1rem 1.1rem 1.3rem;
    text-align:center;
    border:1px solid rgba(255,255,255,0.08);
    background:rgba(255,255,255,0.02);
    height:100%;
}
.diff-code{
    font-family:var(--font-mono);
    font-size:0.7rem;
    color:var(--dim);
    letter-spacing:0.2em;
}
.diff-card h3{
    font-family:var(--font-display);
    font-size:0.95rem;
    margin:0.5rem 0 0.7rem;
}
.diff-easy h3{ color:var(--green); text-shadow:0 0 12px rgba(57,255,143,0.6);}
.diff-med h3{ color:var(--amber); text-shadow:0 0 12px rgba(255,204,0,0.6);}
.diff-hard h3{ color:var(--red); text-shadow:0 0 12px rgba(255,59,92,0.6);}
.diff-card p{ color:var(--ink); font-size:0.82rem; margin:0.15rem 0; font-family:var(--font-mono);}

/* ------------ LED ATTEMPT ROW ------------- */
.led-row{ display:flex; gap:8px; justify-content:center; margin:0.6rem 0 1rem; flex-wrap:wrap;}
.led{
    width:22px; height:22px; border-radius:50%;
    background:radial-gradient(circle at 35% 30%, #3a3560, #14102b);
    border:1px solid rgba(255,255,255,0.12);
}
.led.on{
    background:radial-gradient(circle at 35% 30%, #baffde, var(--green));
    box-shadow:0 0 10px var(--green), 0 0 22px rgba(57,255,143,0.55);
}
.led.used{
    background:radial-gradient(circle at 35% 30%, #ffd3dd, var(--red));
    box-shadow:0 0 10px var(--red), 0 0 22px rgba(255,59,92,0.4);
}

/* ------------ DIGITAL READOUT ------------- */
.readout{
    font-family:var(--font-mono);
    text-align:center;
    border:1px solid rgba(0,240,255,0.25);
    border-radius:10px;
    padding:0.85rem;
    margin:0.9rem 0;
    background:rgba(0,0,0,0.35);
}
.readout.low{ color:var(--cyan); text-shadow:0 0 10px rgba(0,240,255,0.7);}
.readout.high{ color:var(--amber); text-shadow:0 0 10px rgba(255,204,0,0.7);}
.readout.invalid{ color:var(--red); border-color:var(--red); text-shadow:0 0 10px rgba(255,59,92,0.6);}
.readout .arrow{ font-size:1.3rem; }

.hint-panel{
    border:1px dashed var(--magenta);
    border-radius:10px;
    padding:0.9rem 1rem;
    color:var(--ink);
    font-family:var(--font-mono);
    background:rgba(255,46,230,0.05);
    white-space:pre-line;
    margin-top:0.7rem;
}

/* ------------ WIN / LOSE BANNERS ------------- */
.result-win{
    text-align:center; padding:1.6rem 1rem; border-radius:14px;
    background:linear-gradient(160deg, rgba(57,255,143,0.12), rgba(0,240,255,0.08));
    border:1px solid rgba(57,255,143,0.5);
    box-shadow:0 0 40px rgba(57,255,143,0.25);
}
.result-win h2{
    font-family:var(--font-display); color:var(--green); font-size:1.35rem;
    text-shadow:0 0 16px rgba(57,255,143,0.8);
    margin-bottom:0.5rem;
}
.result-lose{
    text-align:center; padding:1.6rem 1rem; border-radius:14px;
    background:linear-gradient(160deg, rgba(255,59,92,0.14), rgba(20,16,46,0.4));
    border:1px solid rgba(255,59,92,0.5);
    box-shadow:0 0 40px rgba(255,59,92,0.2);
    animation:glitch 0.4s steps(2) 3;
}
.result-lose h2{
    font-family:var(--font-display); color:var(--red); font-size:1.35rem;
    text-shadow:0 0 16px rgba(255,59,92,0.85);
    margin-bottom:0.5rem;
}
@keyframes glitch{
    0%{ transform:translate(0,0); }
    25%{ transform:translate(-2px,1px); }
    50%{ transform:translate(2px,-1px); }
    75%{ transform:translate(-1px,-1px); }
    100%{ transform:translate(0,0); }
}

/* ------------ INPUTS / BUTTONS ------------- */
.stTextInput input, .stNumberInput input{
    background:rgba(0,0,0,0.35) !important;
    color:var(--ink) !important;
    border:1px solid rgba(0,240,255,0.35) !important;
    border-radius:8px !important;
    font-family:var(--font-mono) !important;
}
div.stButton > button{
    font-family:var(--font-display) !important;
    font-size:0.68rem !important;
    letter-spacing:0.03em;
    border-radius:8px !important;
    border:1px solid rgba(0,240,255,0.5) !important;
    background:linear-gradient(160deg, rgba(0,240,255,0.14), rgba(255,46,230,0.10)) !important;
    color:var(--ink) !important;
    padding:0.65rem 1rem !important;
    box-shadow:0 0 18px rgba(0,240,255,0.15);
    transition:all 0.15s ease;
}
div.stButton > button:hover{
    border-color:var(--magenta) !important;
    box-shadow:0 0 24px rgba(255,46,230,0.4) !important;
    transform:translateY(-1px);
}

/* ------------ THEME PICKER SWATCHES ------------- */
.swatch-row{ display:flex; gap:6px; margin-top:4px; }
.swatch-dot{ width:16px; height:16px; border-radius:50%; border:1px solid rgba(255,255,255,0.25); }

/* ------------ EMOJI REACTIONS ------------- */
.reaction-emoji{
    display:inline-block;
    font-size:2.2rem;
    line-height:1;
    animation:popIn 0.45s cubic-bezier(.34,1.56,.64,1);
    vertical-align:middle;
    margin-right:0.4rem;
}
@keyframes popIn{
    0%{ transform:scale(0) rotate(-15deg); opacity:0; }
    60%{ transform:scale(1.25) rotate(6deg); opacity:1; }
    100%{ transform:scale(1) rotate(0deg); opacity:1; }
}
.reaction-big{
    font-size:3.4rem;
    display:block;
    margin-bottom:0.3rem;
    animation:popIn 0.55s cubic-bezier(.34,1.56,.64,1);
}
</style>

<div class="grid-floor"></div>
<div class="scanlines"></div>
""")
    return css.substitute(
        BG=theme["bg"], CYAN=theme["cyan"], MAGENTA=theme["magenta"], AMBER=theme["amber"],
        GREEN=theme["green"], RED=theme["red"], INK=theme["ink"], DIM=theme["dim"],
        FONT_IMPORT=font["import"], FONT_DISPLAY=font["display"], FONT_BODY=font["body"], FONT_MONO=font["mono"],
    )


current_theme = THEMES[st.session_state.theme_name]
current_font = FONTS[st.session_state.font_name]
st.markdown(generate_css(current_theme, current_font), unsafe_allow_html=True)


# ==============================================================================
# THEME PICKER — floating icon with palette + font selection
# ==============================================================================
_picker_col = st.columns([6, 1])[1]
with _picker_col:
    if hasattr(st, "popover"):
        with st.popover("🎨"):
            st.markdown("**Color theme**")
            new_theme = st.selectbox(
                "Palette", list(THEMES.keys()),
                index=list(THEMES.keys()).index(st.session_state.theme_name),
                label_visibility="collapsed", key="theme_select",
            )
            swatches = "".join(f'<div class="swatch-dot" style="background:{c}"></div>' for c in THEMES[new_theme]["swatch"])
            st.markdown(f'<div class="swatch-row">{swatches}</div>', unsafe_allow_html=True)

            st.markdown("**Font style**")
            new_font = st.selectbox(
                "Font", list(FONTS.keys()),
                index=list(FONTS.keys()).index(st.session_state.font_name),
                label_visibility="collapsed", key="font_select",
            )

            st.markdown("**Emoji reactions**")
            new_reaction = st.selectbox(
                "Reactions", list(REACTION_PACKS.keys()),
                index=list(REACTION_PACKS.keys()).index(st.session_state.reaction_name),
                label_visibility="collapsed", key="reaction_select",
            )
            rp = REACTION_PACKS[new_reaction]
            st.markdown(
                f'<div style="font-size:1.3rem;">{rp["low"]} {rp["high"]} {rp["win_first"]} {rp["win"]} {rp["lose"]} {rp["hint"]}</div>',
                unsafe_allow_html=True,
            )

            if (new_theme != st.session_state.theme_name
                    or new_font != st.session_state.font_name
                    or new_reaction != st.session_state.reaction_name):
                st.session_state.theme_name = new_theme
                st.session_state.font_name = new_font
                st.session_state.reaction_name = new_reaction
                st.rerun()
    else:
        with st.expander("🎨 Theme"):
            new_theme = st.selectbox("Palette", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.theme_name))
            new_font = st.selectbox("Font", list(FONTS.keys()), index=list(FONTS.keys()).index(st.session_state.font_name))
            new_reaction = st.selectbox("Reactions", list(REACTION_PACKS.keys()), index=list(REACTION_PACKS.keys()).index(st.session_state.reaction_name))
            if (new_theme != st.session_state.theme_name
                    or new_font != st.session_state.font_name
                    or new_reaction != st.session_state.reaction_name):
                st.session_state.theme_name = new_theme
                st.session_state.font_name = new_font
                st.session_state.reaction_name = new_reaction
                st.rerun()



# ==============================================================================
# CONFETTI BURST (canvas, plays once on win)
# ==============================================================================
def confetti_burst():
    components.html(
        """
        <canvas id="c" style="position:fixed;inset:0;pointer-events:none;z-index:9999;"></canvas>
        <script>
        const canvas = document.getElementById('c');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const colors = ['#00f0ff','#ff2ee6','#ffcc00','#39ff8f'];
        let pieces = [];
        for(let i=0;i<160;i++){
            pieces.push({
                x: Math.random()*canvas.width,
                y: -20 - Math.random()*canvas.height*0.4,
                r: 4+Math.random()*5,
                c: colors[Math.floor(Math.random()*colors.length)],
                vy: 2+Math.random()*4,
                vx: -2+Math.random()*4,
                rot: Math.random()*360,
                vr: -6+Math.random()*12
            });
        }
        let frame=0;
        function draw(){
            ctx.clearRect(0,0,canvas.width,canvas.height);
            pieces.forEach(p=>{
                p.x+=p.vx; p.y+=p.vy; p.rot+=p.vr;
                ctx.save();
                ctx.translate(p.x,p.y);
                ctx.rotate(p.rot*Math.PI/180);
                ctx.fillStyle=p.c;
                ctx.fillRect(-p.r/2,-p.r/2,p.r,p.r*1.6);
                ctx.restore();
            });
            frame++;
            if(frame<160){ requestAnimationFrame(draw); }
            else { ctx.clearRect(0,0,canvas.width,canvas.height); }
        }
        draw();
        </script>
        """,
        height=0,
        width=0,
    )


# ==============================================================================
# EMOJI RAIN — full-screen emoji popup burst (difficulty picks, tension, win, lose)
# ==============================================================================
def emoji_rain(emojis, count=70, life=170):
    glyphs_js = ",".join(f'"{g}"' for g in emojis)
    components.html(
        f"""
        <canvas id="er" style="position:fixed;inset:0;pointer-events:none;z-index:9999;"></canvas>
        <script>
        const canvas = document.getElementById('er');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const glyphs = [{glyphs_js}];
        let pieces = [];
        for(let i=0;i<{count};i++){{
            pieces.push({{
                x: Math.random()*canvas.width,
                y: -40 - Math.random()*canvas.height*0.6,
                s: 22+Math.random()*26,
                g: glyphs[Math.floor(Math.random()*glyphs.length)],
                vy: 2+Math.random()*3.6,
                vx: -1.6+Math.random()*3.2,
                rot: Math.random()*360,
                vr: -5+Math.random()*10
            }});
        }}
        let frame=0;
        function draw(){{
            ctx.clearRect(0,0,canvas.width,canvas.height);
            pieces.forEach(p=>{{
                p.x+=p.vx; p.y+=p.vy; p.rot+=p.vr;
                ctx.save();
                ctx.translate(p.x,p.y);
                ctx.rotate(p.rot*Math.PI/180);
                ctx.font = p.s+"px sans-serif";
                ctx.textAlign="center"; ctx.textBaseline="middle";
                ctx.fillText(p.g, 0, 0);
                ctx.restore();
            }});
            frame++;
            if(frame<{life}){{ requestAnimationFrame(draw); }}
            else {{ ctx.clearRect(0,0,canvas.width,canvas.height); }}
        }}
        draw();
        </script>
        """,
        height=0,
        width=0,
    )


EASY_POPUP = ["🙂", "⭐", "✨", "🎯", "👍"]
MEDIUM_POPUP = ["🔥", "💥", "⚡", "🌪️"]
HARD_POPUP = ["😈", "🔥", "💀", "⚡"]
TENSION_POPUP = ["😰", "😭", "⏳", "💦", "😱"]
WIN_POPUP = ["🎉", "🎊", "🥳", "✨", "🏆"]
LOSE_POPUP = ["😭", "💔", "😢"]
def init_state():
    defaults = dict(
        stage="name", name="", difficulty=None, number=None,
        attempt=1, max_attempts=0, message="", message_type="",
        hint_used=False, hint_text="", won=False, celebrated=False,
        pending_effect=None, tension_shown=False, lose_shown=False,
    )
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


init_state()


def start_game(difficulty: str):
    cfg = DIFFICULTIES[difficulty]
    st.session_state.difficulty = difficulty
    st.session_state.number = int(np.random.randint(cfg["low"], cfg["high"] + 1))
    st.session_state.attempt = 1
    st.session_state.max_attempts = cfg["max_attempts"]
    st.session_state.message = ""
    st.session_state.message_type = ""
    st.session_state.hint_used = False
    st.session_state.hint_text = ""
    st.session_state.won = False
    st.session_state.celebrated = False
    st.session_state.pending_effect = difficulty
    st.session_state.tension_shown = False
    st.session_state.lose_shown = False
    st.session_state.stage = "playing"


def reset_all():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    init_state()


# ==============================================================================
# HEADER
# ==============================================================================
st.markdown(
    """
    <div class="vault-header">
        <div class="eyebrow">SECURE TERMINAL // ACCESS MODULE</div>
        <h1>🎯 GuessVerse</h1>
        <div class="sub">Enter the World of Smart Guessing.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# STAGE: NAME
# ==============================================================================
if st.session_state.stage == "name":
    st.markdown('<div class="panel"><div class="panel-label">// IDENTIFY YOURSELF</div>', unsafe_allow_html=True)
    name = st.text_input("Operator name", placeholder="Enter your name...", label_visibility="collapsed")
    if st.button("▶ AUTHENTICATE"):
        if name.strip():
            st.session_state.name = name.strip().title()
            st.session_state.stage = "difficulty"
            st.rerun()
        else:
            st.warning("Operator name required.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# STAGE: DIFFICULTY
# ==============================================================================
elif st.session_state.stage == "difficulty":
    st.markdown(
        f'<div class="panel"><div class="panel-label">// WELCOME, {st.session_state.name.upper()} — SELECT CLEARANCE LEVEL</div>',
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            '<div class="diff-card diff-easy"><div class="diff-code">CODE 01</div>'
            '<h3>EASY</h3><p>RANGE 1-30</p><p>8 ATTEMPTS</p></div>',
            unsafe_allow_html=True,
        )
        if st.button("ENGAGE", key="easy_btn"):
            start_game("EASY")
            st.rerun()

    with c2:
        st.markdown(
            '<div class="diff-card diff-med"><div class="diff-code">CODE 02</div>'
            '<h3>MEDIUM</h3><p>RANGE 1-70</p><p>6 ATTEMPTS</p></div>',
            unsafe_allow_html=True,
        )
        if st.button("ENGAGE", key="med_btn"):
            start_game("MEDIUM")
            st.rerun()

    with c3:
        st.markdown(
            '<div class="diff-card diff-hard"><div class="diff-code">CODE 03</div>'
            '<h3>HARD</h3><p>RANGE 1-100</p><p>5 ATTEMPTS</p></div>',
            unsafe_allow_html=True,
        )
        if st.button("ENGAGE", key="hard_btn"):
            start_game("HARD")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# STAGE: PLAYING
# ==============================================================================
elif st.session_state.stage == "playing":
    cfg = DIFFICULTIES[st.session_state.difficulty]
    attempt = st.session_state.attempt
    max_attempts = st.session_state.max_attempts
    attempts_left = max_attempts - attempt + 1
    rp = REACTION_PACKS[st.session_state.reaction_name]

    if st.session_state.pending_effect:
        _pack = {"EASY": EASY_POPUP, "MEDIUM": MEDIUM_POPUP, "HARD": HARD_POPUP}[st.session_state.pending_effect]
        emoji_rain(_pack, count=80 if st.session_state.pending_effect == "HARD" else 65)
        st.session_state.pending_effect = None

    if attempts_left == 1 and not st.session_state.tension_shown:
        emoji_rain(TENSION_POPUP, count=60)
        st.session_state.tension_shown = True

    st.markdown(
        f'<div class="panel"><div class="panel-label">// LOCK STATUS — {st.session_state.difficulty} '
        f'({cfg["low"]}-{cfg["high"]})</div>',
        unsafe_allow_html=True,
    )

    leds = ""
    for i in range(max_attempts):
        if i < attempt - 1:
            leds += '<div class="led used"></div>'
        elif i == attempt - 1:
            leds += '<div class="led on"></div>'
        else:
            leds += '<div class="led"></div>'
    st.markdown(f'<div class="led-row">{leds}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<p style="text-align:center;color:var(--dim);font-family:var(--font-mono);font-size:0.8rem;">'
        f'ATTEMPT {attempt} / {max_attempts} &nbsp;•&nbsp; {attempts_left} REMAINING</p>',
        unsafe_allow_html=True,
    )

    if st.session_state.message_type == "low":
        st.markdown(
            f'<div class="readout low" key="{attempt}">'
            f'<span class="reaction-emoji">{rp["low"]}</span> {st.session_state.message}</div>',
            unsafe_allow_html=True,
        )
    elif st.session_state.message_type == "high":
        st.markdown(
            f'<div class="readout high" key="{attempt}">'
            f'<span class="reaction-emoji">{rp["high"]}</span> {st.session_state.message}</div>',
            unsafe_allow_html=True,
        )
    elif st.session_state.message_type == "invalid":
        st.markdown(
            f'<div class="readout invalid">'
            f'<span class="reaction-emoji">⚠️</span> {st.session_state.message}</div>',
            unsafe_allow_html=True,
        )

    gcol, bcol = st.columns([3, 1])
    with gcol:
        guess = st.number_input(
            f"Enter a number ({cfg['low']}-{cfg['high']})", step=1,
            value=cfg["low"], key=f"guess_input_{attempt}", label_visibility="collapsed",
        )
    with bcol:
        submit = st.button("🔓 CRACK")

    if submit:
        guess = int(guess)
        if guess < cfg["low"] or guess > cfg["high"]:
            st.session_state.message = f"⚠ Invalid range! Please choose between {cfg['low']}-{cfg['high']}."
            st.session_state.message_type = "invalid"
            st.rerun()
        else:
            num = st.session_state.number
            if guess == num:
                st.session_state.won = True
                st.session_state.stage = "done"
                st.rerun()
            elif guess < num:
                st.session_state.message = "Too low. Raise the value."
                st.session_state.message_type = "low"
                st.session_state.attempt += 1
            else:
                st.session_state.message = "Too high. Lower the value."
                st.session_state.message_type = "high"
                st.session_state.attempt += 1

            if st.session_state.attempt > max_attempts:
                st.session_state.stage = "done"
            st.rerun()

    # Hint trigger — matches original: offered exactly when attempt hits the threshold
    if st.session_state.attempt == cfg["hint_attempt"] and not st.session_state.hint_used:
        st.write("")
        st.markdown(
            '<p style="color:var(--magenta);font-family:var(--font-mono);font-size:0.85rem;">'
            '⚠ LOW ATTEMPTS REMAINING — DECRYPT HINT?</p>',
            unsafe_allow_html=True,
        )
        hc1, hc2 = st.columns(2)
        with hc1:
            if st.button(f"{rp['hint']} YES, DECRYPT"):
                st.session_state.hint_text = build_hint(st.session_state.number, st.session_state.difficulty)
                st.session_state.hint_used = True
                st.rerun()
        with hc2:
            if st.button("✕ NO, PROCEED BLIND"):
                st.session_state.hint_used = True
                st.session_state.hint_text = ""
                st.rerun()

    if st.session_state.hint_used and st.session_state.hint_text:
        st.markdown(f'<div class="hint-panel">{rp["hint"]} {st.session_state.hint_text}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("↺ ABORT / RESTART"):
        reset_all()
        st.rerun()

# ==============================================================================
# STAGE: DONE
# ==============================================================================
elif st.session_state.stage == "done":
    rp = REACTION_PACKS[st.session_state.reaction_name]
    if st.session_state.won:
        tries = st.session_state.attempt
        if not st.session_state.celebrated:
            confetti_burst()
            emoji_rain(WIN_POPUP, count=90)
            st.session_state.celebrated = True
        if tries == 1:
            line = "You cracked it on your first try!"
            big_emoji = rp["win_first"]
        else:
            line = f"Vault cracked in {tries} attempts."
            big_emoji = rp["win"]
        st.markdown(
            f"""
            <div class="result-win">
                <span class="reaction-big">{big_emoji}</span>
                <div style="font-family:var(--font-mono);color:var(--dim);letter-spacing:0.2em;font-size:0.75rem;">ACCESS GRANTED</div>
                <h2>🔓 UNLOCKED</h2>
                <p style="color:var(--ink);font-family:var(--font-mono);">{st.session_state.name}, {line}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        if not st.session_state.lose_shown:
            emoji_rain(LOSE_POPUP, count=70)
            st.session_state.lose_shown = True
        st.markdown(
            f"""
            <div class="result-lose">
                <span class="reaction-big">{rp["lose"]}</span>
                <div style="font-family:var(--font-mono);color:var(--dim);letter-spacing:0.2em;font-size:0.75rem;">ACCESS DENIED</div>
                <h2>🔒 VAULT LOCKED</h2>
                <p style="color:var(--ink);font-family:var(--font-mono);">
                    {st.session_state.name}, the code was <b>{st.session_state.number}</b>.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("↻ RETRY LEVEL"):
            st.session_state.stage = "difficulty"
            st.rerun()
    with c2:
        if st.button("⟲ FULL RESET"):
            reset_all()
            st.rerun()