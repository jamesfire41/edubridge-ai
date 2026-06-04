# 🎓 EduBridge AI

> **An autonomous AI agent platform connecting private tutors and students — powered by AMD ROCm**

[![ROCm](https://img.shields.io/badge/AMD-ROCm%206.x-ED1C24?logo=amd&logoColor=white)](https://rocm.docs.amd.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2.x-1C3C3C?logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🚀 What is EduBridge AI?

EduBridge AI is a **multi-agent AI system** that acts as a fully autonomous bridge between private tutors and their students. It handles scheduling, personalized learning delivery, payment management, and live session announcements — all through a familiar WhatsApp interface.

**Tutors don't need to be tech-savvy.** They simply input their teaching methods, subject material, and availability. EduBridge takes care of the rest.

```
Tutor → [Input: Subject + Method + Schedule] → EduBridge AI Agent → Student (via WhatsApp)
                                                      ↓
                                          Autonomous Learning Sessions
                                          Scheduling & Reminders
                                          Payment Processing
                                          Live Class Announcements
```

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🤖 **Autonomous Scheduling** | AI agent manages session booking, rescheduling, and reminders |
| 📚 **Personalized Learning** | Adapts content delivery based on student progress and tutor's method |
| 💬 **WhatsApp Native** | Communicates with both tutors and students via WhatsApp |
| 💳 **Payment Packages** | Manages tiered tutoring packages and payment confirmations |
| 📡 **Live Session Alerts** | Pushes announcements for upcoming online live classes |
| 🧠 **Local LLM via ROCm** | Runs open-source LLMs locally on AMD GPU — no OpenAI dependency |
| 🔌 **Plugin-ready** | Extensible agent tools for future integrations |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    EduBridge AI Core                    │
│                                                         │
│  ┌───────────┐   ┌───────────┐   ┌──────────────────┐  │
│  │ Scheduler │   │ Learning  │   │ Payment          │  │
│  │  Agent    │   │  Agent    │   │  Agent           │  │
│  └─────┬─────┘   └─────┬─────┘   └────────┬─────────┘  │
│        │               │                  │             │
│        └───────────────┼──────────────────┘             │
│                        │                                │
│              ┌─────────▼──────────┐                     │
│              │  Orchestrator      │                     │
│              │  (LangGraph)       │                     │
│              └─────────┬──────────┘                     │
│                        │                                │
│              ┌─────────▼──────────┐                     │
│              │  ROCm LLM Engine   │                     │
│              │  (Ollama + HF)     │                     │
│              └────────────────────┘                     │
└─────────────────────────────────────────────────────────┘
         │                              │
┌────────▼────────┐           ┌────────▼────────┐
│  Tutor Interface│           │ Student Interface│
│  (WhatsApp/Mock)│           │ (WhatsApp/Mock) │
└─────────────────┘           └─────────────────┘
```

### Agent Breakdown

- **Orchestrator** — LangGraph state machine that routes tasks between agents
- **Scheduler Agent** — Manages calendar, sends reminders, handles rescheduling requests
- **Learning Agent** — Generates session material based on tutor's curriculum input
- **Payment Agent** — Tracks packages, verifies payments, sends invoices
- **Notifier Agent** — Pushes live session alerts and announcements

---

## 🔧 Tech Stack

| Component | Technology |
|---|---|
| **AI Framework** | [LangGraph](https://langchain-ai.github.io/langgraph/) + [LangChain](https://langchain.com/) |
| **LLM Runtime** | [Ollama](https://ollama.com/) (ROCm backend) |
| **Recommended Models** | `mistral`, `llama3`, `phi3` via Ollama |
| **GPU Acceleration** | **AMD ROCm 6.x** |
| **WhatsApp Layer** | Mock (WA Business API ready) |
| **Scheduler** | APScheduler |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **Language** | Python 3.10+ |

---

## 📦 Installation

### Prerequisites

- AMD GPU with ROCm 6.x support ([ROCm compatibility list](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html))
- Python 3.10+
- Ollama with ROCm backend

### 1. Install ROCm & Ollama

```bash
# Install ROCm (Ubuntu 22.04)
sudo apt update
wget https://repo.radeon.com/amdgpu-install/6.1/ubuntu/jammy/amdgpu-install_6.1.60101-1_all.deb
sudo dpkg -i amdgpu-install_6.1.60101-1_all.deb
sudo amdgpu-install --usecase=rocm

# Install Ollama with ROCm
curl -fsSL https://ollama.com/install.sh | sh

# Pull a recommended model
ollama pull mistral
```

### 2. Clone & Setup EduBridge

```bash
git clone https://github.com/yourusername/edubridge-ai.git
cd edubridge-ai

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure

```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Run (Mock Mode)

```bash
python main.py --mode mock
```

---

## 🎮 Quick Demo

```bash
# Start the mock WhatsApp simulator
python main.py --mode mock

# In another terminal, simulate a tutor message
python scripts/simulate_tutor.py

# Simulate a student message
python scripts/simulate_student.py
```

**Sample interaction:**

```
[TUTOR → EduBridge]
"Tambahkan jadwal belajar matematika untuk Budi, Selasa & Kamis jam 4 sore.
Materi: Aljabar dasar, metode: soal latihan interaktif"

[EduBridge → STUDENT (Budi)]
"Halo Budi! 👋 Jadwal belajar Matematika kamu sudah dibuat:
📅 Selasa & Kamis, 16:00
📖 Materi: Aljabar Dasar
Ketik KONFIRMASI untuk menyetujui jadwal ini."

[STUDENT → EduBridge]
"KONFIRMASI"

[EduBridge → STUDENT]
"✅ Jadwal dikonfirmasi! Kamu akan dapat reminder 1 jam sebelumnya.
Paket belajarmu: Basic (4 sesi/bulan). Ketik PAKET untuk lihat opsi upgrade."
```

---

## 📁 Project Structure

```
edubridge-ai/
├── agents/
│   ├── orchestrator.py      # LangGraph main graph
│   ├── scheduler_agent.py   # Session scheduling logic
│   ├── learning_agent.py    # Curriculum & content delivery
│   ├── payment_agent.py     # Package & billing management
│   └── notifier_agent.py    # Alerts & announcements
├── core/
│   ├── llm_engine.py        # ROCm/Ollama LLM interface
│   ├── state.py             # Shared agent state schema
│   └── config.py            # App configuration
├── mock/
│   ├── whatsapp_mock.py     # Simulated WA interface
│   └── mock_data.py         # Sample tutors & students
├── tools/
│   ├── calendar_tool.py     # Scheduling tools
│   ├── payment_tool.py      # Payment verification tools
│   └── message_tool.py      # Messaging abstraction
├── tests/
│   └── test_agents.py
├── scripts/
│   ├── simulate_tutor.py
│   └── simulate_student.py
├── docs/
│   └── architecture.md
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🗺️ Roadmap

- [x] Core multi-agent architecture (LangGraph)
- [x] Mock WhatsApp interface
- [x] ROCm LLM engine integration
- [ ] Real WhatsApp Business API integration
- [ ] Web dashboard for tutors
- [ ] Payment gateway (Midtrans / Stripe)
- [ ] Multi-language support (Bahasa Indonesia + English)
- [ ] Student progress analytics
- [ ] Mobile app (React Native)

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) first.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [AMD ROCm](https://rocm.docs.amd.com/) for open-source GPU compute
- [LangGraph](https://langchain-ai.github.io/langgraph/) for agent orchestration
- [Ollama](https://ollama.com/) for local LLM serving
