
import streamlit as st
import streamlit.components.v1 as components
import time


# if 'enterprise_title' not in st.session_state:
#     st.session_state.enterprise_title=''

#st.set_page_config(page_title="SpeakQL for Enterprise", layout="wide", page_icon="🗣️")

# ---------- HEADER ----------
st.markdown(f"<h1 style='text-align: center;'>🗣️ SpeakQL for Enterprise</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Conversational SQL Interface for Enterprise Data Teams</h4>", unsafe_allow_html=True)
st.markdown("---")


#title_changes=['Teams', 'Organizations', 'Enterprise', 'You']


# ---------- VALUE PROP ----------
st.markdown("### 🚀 Why SpeakQL?")
st.markdown("""
SpeakQL transforms enterprise data interaction by enabling teams to query complex databases using natural language.  
Whether you're a business analyst, product manager, or executive — SpeakQL removes SQL barriers and delivers insights conversationally.
""")


# ---------- FEATURES ----------
st.empty()
st.markdown("### 🧩 Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ✅ Natural Language to SQL")
    st.markdown("Just ask questions — get precise SQL-powered answers.")

    st.markdown("#### 🎤 Voice-to-Text Input")
    st.markdown("Users can speak directly into the interface — SpeakQL automatically transcribes voice into actionable queries.")
    
    st.markdown("#### 🧱 ER Diagram Generation")
    st.markdown("Dynamically generate Entity-Relationship diagrams from your database schema, offering clear insights for analysts and engineers.")

    st.markdown("#### 🤖 SQL Agent Integration")
    st.markdown("SpeakQL leverages powerful SQL agents to manage multi-step reasoning, subqueries, and joins — making complex questions easy to answer.")

with col2:

    st.markdown("#### 🧠 LLM Integration")
    st.markdown("Uses advanced language models to generate optimized queries.")

    st.markdown("#### 📊 Multi-Database Support")
    st.markdown("Seamlessly connect to PostgreSQL, MySQL, Snowflake, Redshift, and more.")

    st.markdown("#### 🔄 Real-Time Feedback")
    st.markdown("Instant response and query history so your team can explore, refine, and collaborate.")
    
    st.markdown("#### 🔒 Run Locally & Private")
    st.markdown("SpeakQL runs entirely on your infrastructure. No data leaves your system — ensuring maximum compliance and privacy.")


# ---------- FUTURE ENHANCEMENTS ----------
st.empty()
st.markdown("### 🔮 Coming Soon...")

col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 🔍 Data Validation")
    st.markdown("Ensure output queries meet your compliance rules and logic. Custom validators can enforce formats, ranges, or relationships.")

    st.markdown("#### 👥 Human-in-the-Loop")
    st.markdown("Add human oversight where it matters — verify, approve, or correct generated queries before execution.")
  
with col4:
    st.markdown("#### 🔁 API & Plugin Ready")
    st.markdown("Integrate SpeakQL with dashboards, Slack, Jupyter, or BI tools using our developer-friendly APIs.")

    st.markdown("#### 🏢 Role-Based Access")
    st.markdown("Different users see different data — fully integrated with enterprise auth layers like OAuth, LDAP, or SSO.")


# ---------- TECH STACK USED ----------
st.divider()
st.markdown("#### 🛠️ Built with")

col1, col2, col3 = st.columns(3)

with col1:
    st.link_button("🐍 Python", "https://www.python.org", use_container_width=True)
    
with col2:
    st.link_button("🦜🔗 Langchain", "https://www.langchain.com", use_container_width=True)

with col3:
    st.link_button("🎈 Streamlit", "https://streamlit.io", use_container_width=True)
    



# ---------- CALL TO ACTION ----------
st.markdown("---")
st.markdown("## 👤 About Me")
st.markdown("""
I am a software engineer in Dallas and this is my first project using AI agents.  
Would love to get your opinion and feedback!
""")

email, linkedin, other = st.columns([0.15, 0.15, 0.7])
with email:
    st.markdown("""
    <div style='text-align: left;'>
        <a href="mailto:developwithyash@gmail.com">
            <button style='font-size:20px;padding:10px 30px;background-color:#eb8a0c;color:white;border:none;border-radius:8px;'>
                Email
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

with linkedin:
    st.markdown("""
    <div style='text-align: left;'>
        <a href="https://www.linkedin.com/in/yashnadkarni/">
            <button style='font-size:20px;padding:10px 30px;background-color:#0077B5;color:white;border:none;border-radius:8px;'>
                LinkedIn
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)


# ---------- FOOTER ----------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<center><small>&copy; 2025 SpeakQL</small></center>", unsafe_allow_html=True)

