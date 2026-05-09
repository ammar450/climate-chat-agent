# 🌍 Climate Chat Agent

**Version 2.3.0** - E-OBS Knowledge Graph Integration (1950-2024)

An intelligent question-answering system for European climate data using Retrieval-Augmented Generation (RAG). Combines Large Language Models with Knowledge Graphs to provide accurate, grounded answers about climate observations.

> **Key Innovation:** The LLM NEVER invents numbers. All climate data comes directly from the E-OBS Knowledge Graph via validated SPARQL queries.

---

## 🚀 Quick Links

- **[📦 Setup & Installation](SETUP.md)** - Get started in 5 minutes
- **[🎯 Features](FEATURES.md)** - Complete feature list and capabilities
- **[🏗️ Architecture](ARCHITECTURE.md)** - RAG flow and system design
- **[📊 Dataset Information](DATASET.md)** - E-OBS specifications and coverage
- **[💻 Usage & Examples](USAGE.md)** - Query examples by category
- **[🔌 API Reference](API.md)** - REST API documentation
- **[👨‍💻 Development Guide](DEVELOPMENT.md)** - For contributors and developers

---

## ✨ Key Features

- 🤖 **Multi-LLM Support** - Works with Ollama (local) or OpenAI/SAIA (cloud)
- 🧠 **Knowledge-Graph RAG** - Grounded responses from SPARQL queries
- 💬 **Multi-Session Chat** - ChatGPT-like interface with session management
- 🔧 **Smart Typo Correction** - Auto-fixes climate term errors ("temprature" → "temperature")
- 📅 **Advanced Date Validation** - Strict format validation, nearest date fallback (1950-2024)
- 🌍 **Location Filtering** - 50+ European countries, coordinate parsing
- 🚀 **Fast Pattern Matching** - Instant responses for common queries
- 🔒 **Security First** - Query validation, rate limiting, read-only SPARQL
- 📦 **Smart Caching** - Common queries cached for sub-second responses
- 📊 **18 Query Templates** - Covering statistics, time-series, location-based queries

[**→ See all features**](FEATURES.md)

---

## 📊 Dataset

**E-OBS Knowledge Graph** - European Climate Observations

- **328 million observations** across Europe (1950-2024)
- **5 climate variables:** Temperature (daily/min/max), Precipitation, Sea level pressure
- **0.1° × 0.1° spatial resolution** (~11km grid)
- **Daily temporal resolution**
- **Coverage:** 25°N-75°N, 25°W-45°E

[**→ Dataset details**](DATASET.md)

---

## 🏗️ Architecture

```
User Question
    ↓
LLM Planner (Ollama/OpenAI)
    ├─ Selects SPARQL query template
    └─ Extracts parameters (location, time, variable)
        ↓
SPARQL Query Execution
    ├─ Security validation (SELECT only)
    └─ Query E-OBS Knowledge Graph
        ↓
Knowledge Graph Results
    └─ Returns: observations, statistics, metadata
        ↓
LLM Explainer (Ollama/OpenAI)
    ├─ Input: question + KG context
    └─ Output: grounded answer (no hallucinations)
        ↓
User Interface
```

**Key Principle:** The LLM never invents climate data. All numbers come from the knowledge graph.

[**→ Architecture details**](ARCHITECTURE.md)

---

## ⚡ Quick Start

### Prerequisites

- Python 3.9+
- LLM backend: Ollama (local) or OpenAI API key

### Installation

```bash
# 1. Clone repository
git clone <repository-url>
cd climate-chat-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your LLM provider settings

# 4. Run the application
python main.py
```

Access the chat interface at `http://localhost:8000`

[**→ Complete setup guide**](SETUP.md)

---

## 💻 Usage Examples

### Basic Queries

```
"What variables are available?"
→ Lists: Temperature, Precipitation, Sea level pressure

"What was the temperature in Berlin on 2020-06-15?"
→ Returns temperature observation with coordinates

"Average precipitation in July 2019"
→ Computes monthly average from daily data
```

### Time-Based Queries

```
"Highest temperature in 2020"
"Precipitation last week"
"Compare January 2020 vs January 2010"
```

### Location-Based Queries

```
"Temperature in Paris yesterday"
"Average temperature in Germany in 2019"
"Precipitation at 52.5°N 13.4°E"
```

### Statistical Queries

```
"Standard deviation of temperature in 2020"
"How many observations are there?"
"Temperature variability in Berlin"
```

[**→ More examples**](USAGE.md) | [**→ API reference**](API.md)

---

## 🧪 Testing & Evaluation

The project includes a comprehensive evaluation framework with 30 test questions:

```bash
# Run full evaluation
python evaluation/evaluate_agent.py --report

# Run specific test
python evaluation/evaluate_agent.py --question-id 5

# Windows users - interactive menu
evaluation\run_evaluation.bat
```

**Current Performance:**
- ✅ **86.67% success rate** (26/30 tests passing)
- ✅ **46.67% template match rate** (14/30 exact template matches)
- ✅ All 18 query templates validated
- ✅ Coverage across 11 categories and 3 difficulty levels

[**→ Evaluation documentation**](evaluation/README.md)

---

## 🔒 Security Features

- ✅ **Query Validation** - Only SELECT queries allowed
- ✅ **Rate Limiting** - 100 requests/minute per IP
- ✅ **Backend-Only SPARQL** - No direct endpoint exposure
- ✅ **Query Timeouts** - 30-second maximum execution
- ✅ **Result Limits** - Maximum 500 results per query
- ✅ **Input Sanitization** - All inputs validated and sanitized

---

## 📁 Project Structure

```
climate-chat-agent/
├── main.py                    # FastAPI application
├── requirements.txt           # Python dependencies
├── .env.example              # Configuration template
├── README.md                 # This file
├── SETUP.md                  # Installation guide
├── FEATURES.md               # Complete feature list
├── ARCHITECTURE.md           # System design
├── DATASET.md                # E-OBS dataset info
├── USAGE.md                  # Query examples
├── API.md                    # API documentation
├── DEVELOPMENT.md            # Development guide
├── src/                      # Source code
│   ├── agent/               # LangGraph agent
│   ├── formatting/          # Response formatters
│   ├── llm/                 # LLM providers
│   ├── parsers/             # Query parsers
│   ├── query/               # SPARQL client
│   └── utils/               # Utilities
├── static/                   # Web interface
├── tests/                    # Unit tests
├── evaluation/               # Evaluation framework
└── docs/                     # Additional documentation
```

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add tests if applicable
5. Submit a Pull Request

**Areas for contribution:**
- Additional SPARQL query templates
- Support for more climate variables
- Enhanced NLP understanding
- Improved visualization
- Documentation improvements

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed guidelines.

---

## 📜 License

MIT License - see LICENSE file for details.

---

## 📞 Support & Documentation

- **Setup Issues?** See [SETUP.md](SETUP.md)
- **Usage Questions?** See [USAGE.md](USAGE.md)
- **API Integration?** See [API.md](API.md)
- **Want to Contribute?** See [DEVELOPMENT.md](DEVELOPMENT.md)
- **Architecture Details?** See [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🎯 Version History

### v2.3.0 (Current)
- E-OBS full dataset integration (1950-2024)
- 328 million observations
- 18 validated query templates

### v2.2.0
- Smart typo correction
- Advanced date validation
- Location-based filtering
- Dual response formats

### v2.1.0
- Multi-session chat interface
- Enhanced caching
- Rate limiting

### v2.0.0
- LangGraph agent integration
- RAG implementation
- SPARQL security hardening

**For detailed version history and changelog, see [docs/UPDATES.md](docs/UPDATES.md)**

---

**Built with:** Python • FastAPI • LangGraph • SPARQL • Virtuoso • Ollama/OpenAI

