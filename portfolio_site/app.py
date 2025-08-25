import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Akhilesh Singh - Portfolio", page_icon="📊", layout="wide")

# --- Header ---
st.title("👋 Hi, I'm Akhilesh Singh")
st.subheader("ITS Specialist | AI & Data Enthusiast | DevOps Learner")

st.write(
    """
    🚦 I specialize in **Tolling, Traffic Management, ITS Systems**  
    🔹 Currently exploring **AI, ML, DevOps, and Cloud**  
    🔹 Passionate about building smart solutions for real-world problems  
    """
)

# --- Profile Pic ---
st.image("assets/profile.jpg", width=200)

# --- Resume Download ---
with open("assets/resume.pdf", "rb") as file:
    st.download_button("📄 Download Resume", file, "Akhilesh_Singh_Resume.pdf")

# --- Skills ---
st.header("⚡ Skills")
st.write(
    """
    - **Programming:** Python, Java, SQL, Linux Bash  
    - **Data Tools:** Pandas, NumPy, Power BI, Streamlit  
    - **DevOps Tools:** GitHub, Jenkins, Docker, AWS  
    - **ITS Domain Expertise:** Tolling, Traffic Systems, EV Charging  
    """
)

# --- Projects ---
st.header("🚀 Projects")
st.markdown("""
- 📊 **Traffic Data Dashboard** – Power BI analytics on 200k+ rows of tolling data  
- 🤖 **Algo Trading Bot** – Zerodha API, risk-reward, alerts, cloud-deployed  
- 🧠 **AI Health App** – Diagnosis + Firebase + Stripe integration  
- 🎮 **Snake Scrum Battle** – Multiplayer Streamlit game for fun team bonding  
""")

# --- Contact ---
st.header("📬 Contact Me")
st.write("📧 akhi.singh1989@gmail.com") 
st.write("[🌐 LinkedIn](https://www.linkedin.com) | [💻 GitHub](https://github.com)")
