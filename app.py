import streamlit as st
import urllib.request, json
st.set_page_config(page_title="Ajira AI — Pata Kazi Kenya", page_icon="💼", layout="centered")
st.markdown("""<style>.stApp{background:#0a0c10;color:#e8edf5}
.j-card{background:#0d1117;border:1px solid #21262d;border-radius:10px;padding:14px 18px;margin:8px 0}
.stButton>button{background:#1f6feb;color:#fff;border:none;border-radius:8px;padding:10px 24px;font-weight:700;width:100%}
</style>""", unsafe_allow_html=True)
API_KEY = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY","")

# ── Public-facing service availability check ──────────────────────────────────
if not API_KEY:
    st.warning(
        "⚠️ **Huduma hii haipo tayari katika toleo hili la majaribio.**\n\n"
        "Tunaendelea kuboresha. Rudi baadaye au wasiliana na msimamizi.\n\n"
        "_This service is not yet available in this demo version. "
        "We are working on it — please check back soon._"
    )
    st.stop()

SYS = "Wewe ni mshauri wa kazi Kenya. Jibu kwa Kiswahili. Toa ushauri wa vitendo kuhusu: kutafuta kazi, CV, mahojiano, gig economy, na ujasiriamali kwa vijana."
def ask(q):
    if not API_KEY: return "❌ API key not configured."
    url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    body={"contents":[{"role":"user","parts":[{"text":q}]}],"systemInstruction":{"parts":[{"text":SYS}]},"generationConfig":{"temperature":0.3,"maxOutputTokens":700}}
    try:
        req=urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r: return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e: return f"❌ {e}"
st.markdown("# 💼 Ajira AI"); st.markdown("**Pata Kazi Kenya — Mwongozo wa Vijana**")
tab1,tab2,tab3,tab4=st.tabs(["🔍 Tafuta Kazi","📄 Tengeneza CV","🎤 Maandalizi ya Mahojiano","💻 Gig Economy"])
with tab1:
    field=st.selectbox("Uwanja wako:",["IT/Teknolojia","Afya","Elimu","Fedha/Benki","Kilimo","Ujenzi","Usafirishaji","Sanaa/Media","Serikali"])
    exp=st.radio("Uzoefu:",["Shahada mpya","Mwaka 1-3","Miaka 3-5","Miaka 5+"],horizontal=True)
    county=st.selectbox("Kaunti:",["Nairobi","Mombasa","Kisumu","Nakuru","Eldoret","Thika"])
    if st.button("🔍 Tafuta Nafasi",key="j1"):
        with st.spinner("..."): r=ask(f"Fursa za kazi za {field} kwa mtu mwenye uzoefu wa {exp} katika {county} Kenya. Toa: Majina ya kampuni, jinsi ya kuomba, mishahara ya makadirio, na maombi ya mtandaoni (Fuzu, BrighterMonday, LinkedIn).")
        st.markdown(f'<div class="j-card">{r.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
with tab2:
    name=st.text_input("Jina lako:"); edu=st.selectbox("Elimu:",["Cheti","Diploma","Shahada","Masters"]); skills=st.text_input("Ujuzi wako mkuu:")
    if st.button("📄 Tengeneza CV",key="j2") and name and skills:
        with st.spinner("..."): r=ask(f"Tengeneza muundo wa CV kwa {name}, elimu ya {edu}, ujuzi: {skills}. CV ya Kenya — muundo wa kisasa, Kiingereza rasmi.")
        st.markdown(f'<div class="j-card">{r.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
with tab3:
    role=st.text_input("Nafasi unayoomba:",placeholder="Mfano: Software Developer at Safaricom")
    if st.button("🎤 Maswali ya Mahojiano",key="j3") and role:
        with st.spinner("..."): r=ask(f"Maswali 8 ya mahojiano ya kawaida kwa nafasi ya {role} Kenya na majibu bora. Jumuisha: swali la behavioral, technical, na salary negotiation.")
        st.markdown(f'<div class="j-card">{r.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
with tab4:
    if st.button("💻 Fursa za Gig Economy Kenya",key="j4"):
        with st.spinner("..."): r=ask("Fursa bora za gig economy kwa vijana Kenya 2024: Upwork, Fiverr, Uber, Bolt, Glovo, online tutoring. Jinsi ya kuanza kila moja, mapato ya makadirio, na vidokezo.")
        st.markdown(f'<div class="j-card">{r.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
st.markdown("---"); st.caption("💼 Ajira AI v1.0 | Fuzu: fuzu.com | BrighterMonday: brightermonday.co.ke | CC BY-NC-ND 4.0")
