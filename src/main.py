import streamlit as st
from few_shot_prompting import FewShotPrompting
from post_generator import generate_post

st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="✍️",
    layout="centered"
)

length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish", "Bengali"]


def apply_theme(is_dark):
    if is_dark:
        st.markdown(
            """
            <style>
            :root {
                --bg-gradient: linear-gradient(135deg, #0f172a, #020617);
                --card-bg: #1e293b;
                --text-color: #f8fafc;
                --muted-text: #94a3b8;
                --border-color: #334155;
                --accent-gradient: linear-gradient(135deg, #6366f1, #8b5cf6);
                --selectbox-bg: #1e293b;
                --selectbox-text: #f8fafc;
            }
            .stApp {
                background: var(--bg-gradient);
                color: var(--text-color);
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            :root {
                --bg-gradient: linear-gradient(135deg, #f8fafc, #f1f5f9);
                --card-bg: #ffffff;
                --text-color: #0f172a;
                --muted-text: #475569;
                --border-color: #e2e8f0;
                --accent-gradient: linear-gradient(135deg, #2563eb, #3b82f6);
                --selectbox-bg: #ffffff;
                --selectbox-text: #0f172a;
            }
            .stApp {
                background: var(--bg-gradient);
                color: var(--text-color);
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            background-color: var(--card-bg) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 16px !important;
            padding: 24px !important;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05) !important;
        }

        div[data-baseweb="select"] > div {
            background-color: var(--selectbox-bg) !important;
            color: var(--selectbox-text) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 10px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        textarea {
            background-color: var(--selectbox-bg) !important;
            color: var(--selectbox-text) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 10px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            line-height: 1.6 !important;
        }

        div.stButton > button {
            background: var(--accent-gradient) !important;
            color: white !important;
            border: none !important;
            padding: 12px 24px !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2) !important;
            width: 100% !important;
        }

        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3) !important;
            opacity: 0.95;
        }

        div.stButton > button:active {
            transform: translateY(1px) !important;
        }

        div.stDownloadButton > button {
            background: transparent !important;
            color: var(--text-color) !important;
            border: 1px solid var(--border-color) !important;
            padding: 12px 24px !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100% !important;
        }

        div.stDownloadButton > button:hover {
            background: var(--border-color) !important;
            transform: translateY(-2px) !important;
        }

        .linkedin-card {
            background-color: var(--card-bg);
            color: var(--text-color);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.05);
            margin-top: 15px;
            margin-bottom: 25px;
        }

        .linkedin-header {
            display: flex;
            align-items: center;
            margin-bottom: 18px;
        }

        .linkedin-avatar {
            font-size: 24px;
            background: var(--accent-gradient);
            width: 48px;
            height: 48px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 14px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .linkedin-user-info {
            display: flex;
            flex-direction: column;
        }

        .linkedin-user-info strong {
            font-size: 15px;
            color: var(--text-color);
        }

        .linkedin-subtext {
            font-size: 12px;
            color: var(--muted-text);
        }

        .linkedin-content {
            font-size: 15px;
            line-height: 1.6;
            white-space: pre-wrap;
            color: var(--text-color);
            margin-top: 8px;
        }

        .gradient-title {
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            font-weight: 800;
            font-size: 2.6rem;
            margin-bottom: 8px;
        }

        .subtitle {
            text-align: center;
            color: var(--muted-text);
            font-size: 1.1rem;
            margin-bottom: 30px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def main():
    import os
    if not os.getenv("GROQ_CLOUD_API_KEY"):
        st.error("🔑 **Groq API Key is missing!**\n\nPlease configure your `GROQ_CLOUD_API_KEY` to start generating posts.")
        st.markdown(
            """
            ### How to fix:
            * **On Streamlit Cloud:**
              1. Click **Manage app** in the bottom-right corner of your app screen.
              2. Open the app settings / secrets menu (three dots icon).
              3. Paste the following line:
                 ```toml
                 GROQ_CLOUD_API_KEY = "your-actual-groq-key"
                 ```
              4. Save and the app will redeploy automatically.
            
            * **On Localhost:**
              Make sure you have a `.env` file in the root folder containing:
              ```env
              GROQ_CLOUD_API_KEY="your-actual-groq-key"
              ```
            """
        )
        return

    if "theme" not in st.session_state:
        st.session_state.theme = True

    col_title, col_toggle = st.columns([5, 1.2])

    with col_toggle:
        toggle = st.toggle("🌙 Dark Mode", value=st.session_state.theme)

    st.session_state.theme = toggle
    apply_theme(st.session_state.theme)

    st.markdown(
        """
        <h1 class="gradient-title">✍️ LinkedIn Post Generator</h1>
        <p class="subtitle">Craft engaging professional updates in seconds using AI and few-shot examples</p>
        """,
        unsafe_allow_html=True
    )

    file_system = FewShotPrompting()
    tags = file_system.get_tags()

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            selected_tag = st.selectbox("📌 Topic / Theme", options=tags, key="topic")

        with col2:
            selected_length = st.selectbox("📏 Desired Length", options=length_options, key="length")

        with col3:
            selected_language = st.selectbox("🌐 Output Language", options=language_options, key="language")

        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        generate_clicked = st.button("🚀 Generate Post", use_container_width=True)

    if generate_clicked:
        st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
        with st.spinner("✨ Generating your perfect LinkedIn post..."):
            post = generate_post(selected_length, selected_language, selected_tag)

        with st.container(border=True):
            st.markdown("### 📝 Output Preview")

            tab_preview, tab_raw = st.tabs(["✨ Formatted Preview", "📋 Copy & Edit"])

            with tab_preview:
                st.markdown(
                    f"""
                    <div class="linkedin-card">
                        <div class="linkedin-header">
                            <span class="linkedin-avatar">✍️</span>
                            <div class="linkedin-user-info">
                                <strong>LinkedIn Post Generator</strong>
                                <span class="linkedin-subtext">AI Content Creator • Just now</span>
                            </div>
                        </div>
                        <div class="linkedin-content">{post}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with tab_raw:
                st.code(post, language="text")
                st.text_area("Interactive Editor", value=post, height=250, key="interactive_output")

            st.download_button(
                label="📥 Download Post as Text File",
                data=post,
                file_name=f"linkedin_post_{selected_tag.lower().replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )


if __name__ == "__main__":
    main()