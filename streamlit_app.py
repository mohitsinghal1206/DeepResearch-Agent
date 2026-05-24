# import streamlit as st
# import os
# import time
# from dotenv import load_dotenv

# # Page configuration
# st.set_page_config(
#     page_title="Multi-Agent AI Research System",
#     page_icon="🔍",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for premium styling
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 2.8rem;
#         font-weight: 700;
#         background: linear-gradient(135deg, #FF4B4B, #FF8F8F);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 0.5rem;
#     }
#     .sub-header {
#         font-size: 1.2rem;
#         color: #555;
#         margin-bottom: 2rem;
#     }
#     .agent-card {
#         border-radius: 10px;
#         padding: 1.2rem;
#         background-color: #F8F9FA;
#         border-left: 5px solid #FF4B4B;
#         margin-bottom: 1rem;
#     }
#     .score-badge {
#         font-size: 1.5rem;
#         font-weight: 700;
#         color: #FF4B4B;
#         background-color: #FFEBEB;
#         padding: 0.3rem 0.8rem;
#         border-radius: 20px;
#         display: inline-block;
#         margin-bottom: 1rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Load environment variables
# load_dotenv()

# # Initialize session state for research results
# if 'research_state' not in st.session_state:
#     st.session_state.research_state = {
#         'topic': '',
#         'search_results': '',
#         'scraped_content': '',
#         'report': '',
#         'feedback': '',
#         'completed': False
#     }

# # Sidebar configuration
# st.sidebar.title("🛠️ Control Panel")
# st.sidebar.markdown("Configure your AI Research Assistant settings below.")

# # API Keys Input (collapsible, fallback to environment variables)
# with st.sidebar.expander("🔑 API Credentials", expanded=False):
#     tavily_key = st.text_input(
#         "Tavily API Key",
#         value=os.getenv("TAVILY_API_KEY", ""),
#         type="password",
#         help="Required for web search. Get one at tavily.com"
#     )
#     google_key = st.text_input(
#         "Google API Key",
#         value=os.getenv("GOOGLE_API_KEY", ""),
#         type="password",
#         help="Required for Gemini. Get one at Google AI Studio"
#     )

# # Save keys in environment variables if entered
# if tavily_key:
#     os.environ["TAVILY_API_KEY"] = tavily_key
# if google_key:
#     os.environ["GOOGLE_API_KEY"] = google_key

# # Sidebar Architecture details
# st.sidebar.markdown("---")
# st.sidebar.markdown("### 🤖 Agent Team Roles")
# st.sidebar.markdown("""
# - **🔍 Web Search Agent**: Queries Tavily to locate the top 5 articles/resources.
# - **📖 Deep Reader Agent**: Scrapes and parses clean text content from the most relevant resource URL using BeautifulSoup.
# - **✍️ Research Writer**: Compiles findings and drafts a structured Markdown report.
# - **⚖️ Quality Critic**: Reviews the draft report and evaluates it, providing a rating and critical feedback.
# """)

# # Main UI layout
# st.markdown("<div class='main-header'>DeepResearch AI Analyst</div>", unsafe_allow_html=True)
# st.markdown("<div class='sub-header'>A collaborative multi-agent pipeline that searches, reads, drafts, and reviews reports.</div>", unsafe_allow_html=True)

# # Define Tabs
# tab1, tab2, tab3 = st.tabs(["🚀 Research Studio", "📄 Generated Report", "📊 Agent Architecture"])

# with tab1:
#     st.markdown("### 🎯 Define Your Research Topic")
    
#     col1, col2 = st.columns([4, 1])
#     with col1:
#         topic_input = st.text_input(
#             "What topic would you like to research today?",
#             placeholder="e.g., Impact of Quantum Computing on Cryptography, History of LLMs, etc.",
#             label_visibility="collapsed"
#         )
#     with col2:
#         run_button = st.button("Start Research", type="primary", use_container_width=True)

#     # Execution flow
#     if run_button:
#         if not topic_input.strip():
#             st.error("Please enter a valid research topic.")
#         elif not os.getenv("TAVILY_API_KEY") or not os.getenv("GOOGLE_API_KEY"):
#             st.error("Missing API Keys! Please configure them in the sidebar 'API Credentials' expander or set them in your `.env` file.")
#         else:
#             # We import agents here so API keys are already in place
#             try:
#                 from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
                
#                 # Clear previous state
#                 st.session_state.research_state = {
#                     'topic': topic_input,
#                     'search_results': '',
#                     'scraped_content': '',
#                     'report': '',
#                     'feedback': '',
#                     'completed': False
#                 }
                
#                 # Step 1: Web Search Agent
#                 with st.status("🔍 Step 1: Web Search Agent is working...", expanded=True) as status:
#                     st.write(f"Searching Tavily for: *'{topic_input}'*...")
#                     search_agent = build_search_agent()
#                     search_result = search_agent.invoke({
#                         "messages": [('user', f"Find recent, reliable and detailed information about: {topic_input}")]
#                     })
#                     search_content = search_result['messages'][-1].content
#                     st.session_state.research_state['search_results'] = search_content
                    
#                     st.write("**Search Results Found:**")
#                     st.code(search_content[:500] + "\n... [truncated]", language="markdown")
#                     status.update(label="✅ Step 1: Web Search Completed!", state="complete", expanded=False)

#                 # Step 2: Reader Agent
#                 with st.status("📖 Step 2: Reader Agent is scraping top resources...", expanded=True) as status:
#                     st.write("Picking the most relevant URL and scraping content...")
#                     reader_agent = build_reader_agent()
#                     reader_result = reader_agent.invoke({
#                         'messages': [("user",
#                             f"Based on the following search results about '{topic_input}', "
#                             f"pick the most relevant URL and scrape it for deeper content.\n\n"
#                             f"Search Results:\n{search_content[:800]}"
#                         )]
#                     })
#                     scraped = reader_result['messages'][-1].content
#                     st.session_state.research_state['scraped_content'] = scraped
                    
#                     st.write("**Scraped Article Snippet:**")
#                     st.code(scraped[:500] + "\n... [truncated]", language="text")
#                     status.update(label="✅ Step 2: Scraped successfully!", state="complete", expanded=False)

#                 # Step 3: Writer Chain
#                 with st.status("✍️ Step 3: Research Writer is drafting the report...", expanded=True) as status:
#                     st.write("Writing structured Markdown report...")
#                     research_combined = (
#                         f"SEARCH RESULT:\n {search_content}\n\n"
#                         f"DETAILED SCRAPED CONTENT: \n {scraped}"
#                     )
#                     report = writer_chain.invoke({
#                         'topic': topic_input,
#                         'research': research_combined
#                     })
#                     st.session_state.research_state['report'] = report
                    
#                     st.write("**Report Drafted!**")
#                     status.update(label="✅ Step 3: Report drafted successfully!", state="complete", expanded=False)

#                 # Step 4: Critic Chain
#                 with st.status("⚖️ Step 4: Quality Critic is reviewing the report...", expanded=True) as status:
#                     st.write("Reviewing draft report, score computation, and identifying feedback areas...")
#                     feedback = critic_chain.invoke({
#                         'report': report
#                     })
#                     st.session_state.research_state['feedback'] = feedback
#                     st.session_state.research_state['completed'] = True
                    
#                     st.write("**Review Finished!**")
#                     status.update(label="✅ Step 4: Critique Completed!", state="complete", expanded=False)

#                 st.success("🎉 Research Pipeline Completed! Head over to the **Generated Report** tab to view your final report.")
#                 st.balloons()
                
#             except Exception as e:
#                 st.error(f"An error occurred while running the pipeline: {str(e)}")
#                 st.info("Check your API keys and internet connection.")

#     # Show inline summary of results if completed
#     if st.session_state.research_state['completed']:
#         st.markdown("---")
#         st.markdown("### 📋 Quick Pipeline Summary")
#         col_left, col_right = st.columns(2)
        
#         with col_left:
#             st.info(f"**Research Topic:** {st.session_state.research_state['topic']}")
#             st.markdown(f"**Web Search Results:** Length ~{len(st.session_state.research_state['search_results'])} chars")
#             st.markdown(f"**Scraped Content Snippet:** Length ~{len(st.session_state.research_state['scraped_content'])} chars")
            
#         with col_right:
#             st.markdown("#### Critic's Verdict")
#             feedback_text = st.session_state.research_state['feedback']
#             # Try to extract the score if present in the feedback text
#             if "Score:" in feedback_text:
#                 score_line = [line for line in feedback_text.split('\n') if "Score:" in line]
#                 if score_line:
#                     st.markdown(f"<div class='score-badge'>{score_line[0]}</div>", unsafe_allow_html=True)
#             st.text(feedback_text)
#     else:
#         st.info("Enter a topic and click **Start Research** to begin.")

# with tab2:
#     if st.session_state.research_state['completed']:
#         st.markdown("### 📄 Final Research Report")
        
#         # Download button
#         report_data = st.session_state.research_state['report']
#         st.download_button(
#             label="💾 Download Report as Markdown",
#             data=report_data,
#             file_name=f"research_report_{st.session_state.research_state['topic'].replace(' ', '_').lower()}.md",
#             mime="text/markdown",
#             use_container_width=True
#         )
        
#         st.markdown("---")
#         st.markdown(report_data)
#     else:
#         st.warning("⚠️ No report generated yet. Run a research task under the **Research Studio** tab first.")

# with tab3:
#     st.markdown("### 🏗️ Agent Architecture Overview")
#     st.markdown("Here is how the system is designed, which is great for explaining to recruiters and technical interviewers:")
    
#     # Visual architecture
#     st.markdown("""
#     ```mermaid
#     graph TD
#         User([User Topic Input]) --> SearchAgent[🔍 Search Agent]
#         SearchAgent -- Tavily Web Search API --> WebResults[Top Web Sources]
#         WebResults --> ReaderAgent[📖 Reader Agent]
#         ReaderAgent -- BeautifulSoup Web Scraper --> DeepContent[Scraped Text Content]
#         DeepContent --> WriterChain[✍️ Writer Chain]
#         WebResults --> WriterChain
#         WriterChain -- Gemini LLM & Prompt Template --> DraftReport[Structured Markdown Report]
#         DraftReport --> CriticChain[⚖️ Critic Chain]
#         CriticChain -- Analytical Critique Prompt --> CritiqueOutput[Score, Strengths, Improvements & Verdict]
#         CritiqueOutput --> User
#     ```
#     """)
    
#     st.markdown("""
#     ---
#     ### 💡 Key Design Patterns to Discuss in Interviews

#     1. **Decoupled Search vs. Extraction**:
#        - Instead of having a single agent do all the searching and reading, we split them. The **Search Agent** quickly identifies sources, while the **Reader Agent** focuses solely on extracting the core article body. This keeps token usage minimal and avoids hitting context window limits with irrelevant HTML boilerplate.
    
#     2. **Structured Chain Prompts**:
#        - The writer uses LangChain's pipeline expression style (`writer_prompt | llm | StrOutputParser()`), which separates structured writing logic from agentic search loops.
    
#     3. **Automated Quality Critique (Self-Reflection Pattern)**:
#        - This mirrors the **Self-Refine / Critic** design pattern in multi-agent systems. Rather than serving the first raw output, we route it through a dedicated critic chain to grade and suggest concrete adjustments.
    
#     4. **Streamlit Component State**:
#        - Using `st.status` container updates allows the user to see the exact progression of the asynchronous agents. Session State (`st.session_state`) ensures data persistence across UI tabs without re-triggering the LLM pipeline.
#     """)










import streamlit as st
import time
from pipeline import run_research_pipeline

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* Root tokens */
:root {
    --bg:        #0a0a0f;
    --surface:   #111118;
    --border:    #1e1e2e;
    --accent:    #6ee7b7;
    --accent2:   #818cf8;
    --accent3:   #f472b6;
    --text:      #e2e8f0;
    --muted:     #64748b;
    --warn:      #fbbf24;
}

/* Global reset */
html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Main container */
.block-container {
    max-width: 1100px !important;
    padding: 2.5rem 2rem !important;
}

/* ── Hero headline ── */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.6rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 55%, var(--accent3) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem;
}
.hero-sub {
    font-size: 0.85rem;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

/* ── Input area ── */
.stTextInput > div > div > input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(110,231,183,0.12) !important;
}

/* ── Primary button ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 2rem !important;
    transition: opacity 0.2s, transform 0.15s !important;
    width: 100% !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Pipeline step cards ── */
.step-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.step-card.active  { border-color: var(--accent2); }
.step-card.done    { border-color: var(--accent);  }
.step-card.idle    { border-color: var(--border);  }
.step-card.error   { border-color: var(--accent3); }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.92rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.step-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
}
.dot-idle   { background: var(--muted);   }
.dot-active { background: var(--accent2); box-shadow: 0 0 8px var(--accent2); animation: pulse 1.2s infinite; }
.dot-done   { background: var(--accent);  }
.dot-error  { background: var(--accent3); }

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(1.35); }
}

.step-label {
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 0.25rem;
    padding-left: 1.7rem;
}

/* ── Result expanders ── */
.stExpander {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    margin-bottom: 0.8rem !important;
}
.stExpander > div > div > div > div {
    background: var(--surface) !important;
    color: var(--text) !important;
}
summary {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
}

/* ── Report box ── */
.report-box {
    background: var(--surface);
    border: 1px solid var(--accent);
    border-radius: 12px;
    padding: 1.6rem 1.8rem;
    font-size: 0.9rem;
    line-height: 1.8;
    white-space: pre-wrap;
    word-break: break-word;
}
.report-box h1, .report-box h2, .report-box h3 {
    font-family: 'Syne', sans-serif;
    color: var(--accent);
}

/* ── Critic box ── */
.critic-box {
    background: var(--surface);
    border: 1px solid var(--accent2);
    border-radius: 12px;
    padding: 1.6rem 1.8rem;
    font-size: 0.9rem;
    line-height: 1.8;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Divider ── */
hr {
    border-color: var(--border) !important;
    margin: 1.8rem 0 !important;
}

/* ── Tag badge ── */
.badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-left: 0.5rem;
    vertical-align: middle;
}
.badge-green  { background: rgba(110,231,183,0.15); color: var(--accent);  border: 1px solid rgba(110,231,183,0.3); }
.badge-purple { background: rgba(129,140,248,0.15); color: var(--accent2); border: 1px solid rgba(129,140,248,0.3); }
.badge-pink   { background: rgba(244,114,182,0.15); color: var(--accent3); border: 1px solid rgba(244,114,182,0.3); }
.badge-yellow { background: rgba(251,191,36,0.15);  color: var(--warn);    border: 1px solid rgba(251,191,36,0.3);  }

/* ── Scrollbar ── */
::-webkit-scrollbar       { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Session state defaults ─────────────────────────────────────────────────────
for key in ("results", "running", "error", "topic_done"):
    if key not in st.session_state:
        st.session_state[key] = None if key in ("results", "error", "topic_done") else False


# ── Helper: step status card ───────────────────────────────────────────────────
def step_card(number: int, title: str, description: str, status: str):
    """status: 'idle' | 'active' | 'done' | 'error'"""
    icons = {"idle": "○", "active": "◉", "done": "✓", "error": "✕"}
    st.markdown(f"""
    <div class="step-card {status}">
        <div class="step-header">
            <span class="step-dot dot-{status}"></span>
            {icons[status]}&nbsp; Step {number} — {title}
        </div>
        <div class="step-label">{description}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Research<br>Intelligence System</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Powered by a four-stage multi-agent pipeline</div>', unsafe_allow_html=True)

# ── Input row ──────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1.2])
with col_input:
    topic = st.text_input(
        label="topic",
        label_visibility="collapsed",
        placeholder="Enter a research topic  e.g. 'Quantum computing breakthroughs 2025'",
        key="topic_input",
    )
with col_btn:
    st.write("")          # vertical nudge
    run_clicked = st.button("▶  Run", use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Two-column layout: pipeline status (left) + results (right) ───────────────
left, right = st.columns([1, 2], gap="large")

with left:
    st.markdown("#### Pipeline")
    step1 = st.empty()
    step2 = st.empty()
    step3 = st.empty()
    step4 = st.empty()

    def render_steps(active: int, done_up_to: int, error_at: int = -1):
        steps = [
            ("Search Agent",   "Gathering recent information from the web"),
            ("Reader Agent",   "Scraping top URLs for deep content"),
            ("Writer Chain",   "Drafting the structured research report"),
            ("Critic Chain",   "Reviewing and scoring the report"),
        ]
        placeholders = [step1, step2, step3, step4]
        for i, (ph, (title, desc)) in enumerate(zip(placeholders, steps), start=1):
            if i == error_at:
                status = "error"
            elif i < active or i <= done_up_to:
                status = "done"
            elif i == active:
                status = "active"
            else:
                status = "idle"
            with ph:
                step_card(i, title, desc, status)

    render_steps(active=0, done_up_to=0)   # initial idle state

with right:
    result_area = st.empty()

# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_clicked:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.running = True
        st.session_state.results = None
        st.session_state.error   = None

        with result_area.container():
            status_msg = st.info("🔄 Pipeline starting…")

        try:
            # Step 1
            render_steps(active=1, done_up_to=0)
            with result_area.container():
                st.info("🔍 Search Agent is fetching information…")

            from agents import build_search_agent
            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent,reliable and detailed information about: {topic}")]
            })
            search_content = search_result["messages"][-1].content

            # Step 2
            render_steps(active=2, done_up_to=1)
            with result_area.container():
                st.info("📄 Reader Agent is scraping top resources…")

            from agents import build_reader_agent
            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{search_content[:800]}"
                )]
            })
            scraped_content = reader_result["messages"][-1].content

            # Step 3
            render_steps(active=3, done_up_to=2)
            with result_area.container():
                st.info("✍️ Writer Chain is drafting the report…")

            from agents import writer_chain
            research_combined = (
                f"SEARCH RESULT:\n {search_content}\n\n"
                f"DETAILED SCRAPED CONTENT: \n {scraped_content}"
            )
            report = writer_chain.invoke({"topic": topic, "research": research_combined})

            # Step 4
            render_steps(active=4, done_up_to=3)
            with result_area.container():
                st.info("🔎 Critic Chain is reviewing the report…")

            from agents import critic_chain
            feedback = critic_chain.invoke({"report": report})

            # All done
            render_steps(active=5, done_up_to=4)
            st.session_state.results = {
                "search_results":  search_content,
                "scraped_content": scraped_content,
                "report":          report,
                "feedback":        feedback,
            }
            st.session_state.topic_done = topic

        except Exception as e:
            st.session_state.error = str(e)
            render_steps(active=0, done_up_to=0, error_at=1)

        st.session_state.running = False
        st.rerun()


# ── Display results ───────────────────────────────────────────────────────────
if st.session_state.results:
    r = st.session_state.results
    with result_area.container():
        st.markdown(
            f"### Results&nbsp;"
            f'<span class="badge badge-green">Done</span>'
            f'<span class="badge badge-purple">{st.session_state.topic_done}</span>',
            unsafe_allow_html=True,
        )

        # ── Final report (prominent) ──
        st.markdown(
            f'<span style="font-family:Syne,sans-serif;font-weight:700;font-size:1rem;'
            f'text-transform:uppercase;letter-spacing:.06em;color:var(--accent);">'
            f'📋 Final Report</span>',
            unsafe_allow_html=True,
        )
        st.markdown(f'<div class="report-box">{r["report"]}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Critic feedback ──
        st.markdown(
            f'<span style="font-family:Syne,sans-serif;font-weight:700;font-size:1rem;'
            f'text-transform:uppercase;letter-spacing:.06em;color:var(--accent2);">'
            f'🧠 Critic Feedback</span>',
            unsafe_allow_html=True,
        )
        st.markdown(f'<div class="critic-box">{r["feedback"]}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Raw intermediate data (collapsed) ──
        with st.expander("🔍 Search Agent Output"):
            st.text(r["search_results"])

        with st.expander("📄 Reader Agent Scraped Content"):
            st.text(r["scraped_content"])

elif st.session_state.error:
    with result_area.container():
        st.markdown(
            f'<span class="badge badge-pink">Error</span>',
            unsafe_allow_html=True,
        )
        st.error(f"Pipeline failed: {st.session_state.error}")

elif not st.session_state.running:
    with result_area.container():
        st.markdown("""
        <div style="
            border: 1px dashed #1e1e2e;
            border-radius: 12px;
            padding: 3rem 2rem;
            text-align: center;
            color: #64748b;
            font-size: 0.88rem;
            line-height: 2;
        ">
            <div style="font-size:2.5rem;margin-bottom:0.8rem;">🔬</div>
            Enter a topic above and hit <strong style="color:#e2e8f0;">Run</strong> to kick off the pipeline.<br>
            Results will appear here — search output, scraped content,<br>the final report, and critic feedback.
        </div>
        """, unsafe_allow_html=True)
