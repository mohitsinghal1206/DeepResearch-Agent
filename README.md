# 🔬 DeepResearch Agent
### Autonomous Multi-Agent Research Pipeline powered by LangChain + Google Gemini

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-1.3+-green?style=flat-square)](https://langchain.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.57+-red?style=flat-square&logo=streamlit)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-orange?style=flat-square&logo=google)](https://deepmind.google/gemini)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

---

## 🧠 What is DeepResearch Agent?

DeepResearch Agent is a fully autonomous **multi-agent AI system** that researches any topic end-to-end — from searching the web to scraping sources, drafting a structured report, and critiquing it — all without human intervention.

Just enter a topic. The pipeline does the rest.

> Built to demonstrate real-world agentic AI design: tool use, multi-step reasoning, chain composition, and a production-ready Streamlit UI.

---

## ✨ Features

- 🔍 **Search Agent** — Queries the web via Tavily to find recent, reliable sources
- 📄 **Reader Agent** — Scrapes and extracts deep content from the most relevant URLs
- ✍️ **Writer Chain** — Drafts a structured research report with key findings and sources
- 🧠 **Critic Chain** — Reviews and scores the report with actionable feedback
- 🖥️ **Streamlit UI** — Clean, dark-themed interface with a live pipeline status tracker
- 🔁 **Fully Autonomous** — Zero human steps between input and final report

---

## 🏗️ System Architecture

```
User Input (Topic)
        │
        ▼
┌─────────────────┐
│  Search Agent   │  ← Tavily Search API + Gemini 2.5 Flash
│  (LangGraph)    │
└────────┬────────┘
         │ Search Results
         ▼
┌─────────────────┐
│  Reader Agent   │  ← BeautifulSoup Web Scraper + Gemini 2.5 Flash
│  (LangGraph)    │
└────────┬────────┘
         │ Scraped Content
         ▼
┌─────────────────┐
│  Writer Chain   │  ← LangChain LCEL + Gemini 2.5 Flash
│  (LangChain)    │
└────────┬────────┘
         │ Draft Report
         ▼
┌─────────────────┐
│  Critic Chain   │  ← LangChain LCEL + Gemini 2.5 Flash
│  (LangChain)    │
└────────┬────────┘
         │
         ▼
  Final Report + Score
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Google Gemini 2.5 Flash |
| Agent Framework | LangChain + LangGraph |
| Web Search | Tavily Search API |
| Web Scraping | BeautifulSoup4 + Requests |
| Chain Composition | LangChain LCEL (pipes) |
| UI | Streamlit |
| Deployment | Streamlit Community Cloud |

> The system is LLM-agnostic by design — swapping in OpenAI GPT or Mistral requires changing a single line.




## 🖥️ UI Preview

The Streamlit UI features:
- Live step-by-step pipeline tracker with animated status indicators
- Final report rendered in a clean formatted view
- Critic feedback with score and improvement suggestions
- Collapsible panels for raw search and scraped content

---

## 🔮 Roadmap

- [ ] Add memory across research sessions
- [ ] Support multiple LLM providers (OpenAI, Mistral)
- [ ] Export report as PDF or Word document
- [ ] Add citation verification agent
- [ ] Multi-topic batch research mode

---

> ⭐ If you found this useful, consider giving it a star — it helps others discover the project!