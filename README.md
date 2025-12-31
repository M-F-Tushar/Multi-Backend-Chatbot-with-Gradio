# 🤖 Universal AI Chatbot
 
A powerful, multi-backend chatbot with an enhanced Gradio interface that connects to 5 different AI providers with 100+ free models.
                                  
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black.svg)](https://github.com/M-F-Tushar/Multi-Backend-Chatbot-with-Gradio)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-5.0+-orange.svg)](https://gradio.app/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Models](https://img.shields.io/badge/Models-100+-brightgreen.svg)](#-available-models-december-2025)

> **⚠️ Important:** AI model availability changes frequently. Provider APIs may add, remove, or rename models at any time. The model lists in this README are current as of December 2025 but may not reflect real-time availability. 

---

## ✨ Features

### 🔌 **5 AI Providers Supported**
- **Ollama** - Run models locally (100% free, private, no API keys)
- **OpenRouter** - 26 validated free models with `:free` suffix
- **GitHub Models** - 21 validated models including GPT-5 series
- **Groq** - 11 models with ultra-fast inference
- **Gemini** - 13 Google AI models (1,500 free req/day)

### 🛠️ **Model Validation Tool**
- **Automated Audit** - `validate_models.py` included to check real-time availability
- **Error Detection** - Identifies auth errors, rate limits, 404s, and server overloads
- **JSON Reports** - Generates detailed validation reports with response times


### 🎨 **Enhanced Interface**
- Modern Gradio UI with custom theme
- Real-time API status indicators
- Model dropdown with 100+ options
- System prompt customization
- Temperature & max tokens controls
- Preset prompts (Code Expert, Writer, Analyst, Teacher)
- Export chat to Markdown
- Stop generation button
- Clear chat functionality

### 🚀 **Advanced Capabilities**
- Streaming responses for real-time interaction
- Conversation history support
- Empty choices safety checks (fixed streaming issues)
- Custom system prompts per conversation
- Temperature control for creativity adjustment
- Error handling with helpful suggestions

---

## 📋 Requirements

- **Python 3.8+**
- **Jupyter Notebook** or **VS Code** with Jupyter extension
- **Internet connection** (for cloud providers)
- **API Keys** (optional, depending on providers)

---

## 🚀 Quick Start

### 1️⃣ **Clone Repository**
```bash
git clone https://github.com/M-F-Tushar/Multi-Backend-Chatbot-with-Gradio.git
cd Multi-Backend-Chatbot-with-Gradio
```

### 2️⃣ **Install Dependencies**
```bash
pip install gradio openai python-dotenv google-generativeai
```

Or run the first code cell in the notebook:
```python
%pip install google-generativeai openai python-dotenv gradio -q
```

### 3️⃣ **Set Up API Keys**

Create a `.env` file in the project directory:

```bash
# Copy the example template
cp .env.example .env

# Edit .env with your favorite text editor
notepad .env  # Windows
nano .env     # Linux/Mac
```

Add your API keys (get them from the links below). Only add keys for providers you want to use:

```env
# OpenRouter (29 free models)
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# GitHub Models (23 free models)
GITHUB_TOKEN=ghp_your-token-here

# Groq (19 free models, ultra-fast)
GROQ_API_KEY=gsk_your-key-here

# Google Gemini (17 models)
GOOGLE_API_KEY=AIzaSy-your-key-here
```

**Note:** Ollama doesn't require an API key (local only).

### 4️⃣ **Run the Chatbot**

**Option D: Model Validation (CLI)**
```bash
python validate_models.py --quick-test
```

The interface will launch at `http://127.0.0.1:7860`


---

## 🔑 Getting API Keys

### 🆓 **Free Options (No Credit Card Required)**

#### 1. **Ollama** (Completely Free, Local)
```bash
# Install Ollama
# Windows/Mac: Download from https://ollama.ai
# Linux:
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3.2:1b

# Start Ollama (usually auto-starts)
ollama serve
```
**Models Available:** 14 models including Llama 3.3, Mistral, CodeLlama, Phi, Gemma 3, Qwen 2.5, DeepSeek R1


---

#### 2. **Groq** (Free Tier: 14,400 requests/day)
1. Visit [https://console.groq.com](https://console.groq.com)
2. Sign up with GitHub/Google
3. Go to "API Keys" → Create new key
4. Copy key to `.env` as `GROQ_API_KEY`

**Free Tier Limits:**
- 30 requests/minute
- 11 models including Llama 4 Maverick, Llama 3.3 70B, GPT-OSS 120B, Qwen


---

#### 3. **GitHub Models** (Free for Prototyping)
1. Generate a Personal Access Token:
   - Go to [https://github.com/settings/tokens](https://github.com/settings/tokens)
   - Click "Generate new token (classic)"
   - Select scopes: `read:user`, `read:org`
   - Generate and copy token
2. Add to `.env` as `GITHUB_TOKEN`

**Free Tier Limits:**
- 10-15 requests/minute (varies by model)
- 21 models including GPT-5 (nano/mini), o3-mini, o4-mini, Llama 3.2 90B, Phi-4


---

#### 4. **Google Gemini** (Free Tier: 1,500 requests/day)
1. Visit [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy key to `.env` as `GOOGLE_API_KEY`

**Free Tier Limits:**
- 15 requests/minute
- 13 models including Gemini 2.5, Gemini 3 Preview, Gemma 3, Robotics-ER


---

#### 5. **OpenRouter** (29 Free Models with `:free` suffix)
1. Visit [https://openrouter.ai](https://openrouter.ai)
2. Sign up (email/Google/GitHub)
3. Go to "Keys" → Create new key
4. Copy key to `.env` as `OPENROUTER_API_KEY`

**Free Tier Notes:**
- Must append `:free` to model IDs
- 26 models including Llama 3.3, Gemini 2.0 Flash, DeepSeek R1, Xiaomi MiMo-V2, NVIDIA Nemotron 3


---

## 📊 Available Models (December 2025)

> ⚠️ **Note:** Model availability changes frequently. The lists below reflect models available as of December 2025. Some models may be added, removed, or renamed by providers. Always check the dropdown in the interface for the most current list.

### **Ollama (14 Local Models)**
```
llama3.2:1b, llama3.2:3b, llama3.1:8b, llama3.1:70b, llama3.3:70b
mistral:7b, mixtral:8x7b, codellama:7b, codellama:34b
phi3:mini, phi3:medium, gemma2:9b, qwen2.5:7b, deepseek-r1:7b
```

### **OpenRouter (26 Validated Free Models)**
```
meta-llama/llama-3.3-70b-instruct:free
google/gemini-2.0-flash-exp:free
tngtech/deepseek-r1t2-chimera:free
xiaomi/mimo-v2-flash:free
nvidia/nemotron-3-nano-30b-a3b:free
... (21 more, see validate_models.py for full list)
```

### **GitHub Models (21 Validated Models)**
```
OpenAI: gpt-5 (nano/mini), o4-mini, o3-mini, gpt-4o
Meta Llama: Llama-3.3-70B, Llama-3.2-90B-Vision
Microsoft: Phi-4, Phi-4-reasoning, Phi-4-mini
Mistral: Codestral-2501
DeepSeek: DeepSeek-R1, DeepSeek-V3
```

### **Groq (11 Validated Models)**
```
llama-4-maverick, llama-4-scout
llama-3.3-70b-versatile, llama-3.1-8b-instant
openai/gpt-oss-120b, openai/gpt-oss-20b
moonshotai/kimi-k2, qwen/qwen3-32b
whisper-large-v3 (audio)
```

### **Gemini (13 Validated Models)**
```
gemini-3-pro-preview, gemini-3-pro-image-preview
gemini-2.5-pro, gemini-2.5-flash, gemini-2.5-flash-lite
gemini-2.0-flash-exp, gemini-robotics-er-1.5-preview
gemma-3-27b-it, gemma-3-12b-it, gemma-3-4b-it
```


---

## 🎛️ Usage Guide

### **Basic Usage**

1. **Launch the notebook** and run all cells
2. **Select Backend** from dropdown (Ollama/OpenRouter/GitHub/Groq/Gemini)
3. **Select Model** from auto-populated list
4. **Type your message** and press Enter or click Send

### **Advanced Settings**

Click "Advanced Settings" accordion to access:

- **System Prompt** - Customize AI behavior
  - Example: "You are a Python expert. Provide code with explanations."
  
- **Temperature** (0.0 - 2.0)
  - `0.0-0.5`: Focused, deterministic responses
  - `0.7`: Balanced (default)
  - `1.0-2.0`: Creative, varied responses

- **Max Tokens** (0 - 4096)
  - `0`: Unlimited (default)
  - `512`: Short responses
  - `2048`: Medium responses
  - `4096`: Long responses

### **Preset Prompts**

Quick-select specialized AI personas:

- **Code Expert** - For programming help
- **Creative Writer** - For storytelling and content
- **Data Analyst** - For data insights and analysis
- **Teacher** - For educational explanations

### **Export Chat**

1. Click "Export Chat" accordion
2. Click "Export to Markdown"
3. Copy the formatted conversation

---

## 🔧 Troubleshooting

### **GitHub Models: "list index out of range"**
✅ **FIXED** - Empty choices check added to streaming handler

### **Ollama: Connection Error**
```bash
# Make sure Ollama is running
ollama serve

# Check if models are installed
ollama list

# Pull a model if needed
ollama pull llama3.2:1b
```

### **API Key Errors**
1. Check `.env` file exists in project directory
2. Verify no extra spaces in API keys
3. Restart Jupyter kernel after editing `.env`
4. Run cell 2 again to reload environment

### **Model Not Found**
- **OpenRouter:** Add `:free` suffix to free models
- **GitHub:** Use exact model names (e.g., `Llama-3.3-70B-Instruct`)
- **Groq:** Use model IDs from the list above
- **Gemini:** Some models are preview/experimental

### **Rate Limit Exceeded**
- Free tiers have limits (see API Keys section)
- Wait a few minutes or switch to another provider
- Consider upgrading to paid tier for higher limits

---

## 📁 Project Structure

```
Multi-Backend-Chatbot-with-Gradio/
├── Chatbot.ipynb          # Main notebook with enhanced Gradio UI
├── README.md              # This documentation
├── .env.example           # Template for API keys (rename to .env and add your keys)
├── .env                   # Your API keys (DO NOT COMMIT - protected by .gitignore)
├── .gitignore             # Git configuration to protect sensitive files
└── LICENSE                # MIT License
```

## 🚀 Deployment Options

### **Local Development** (Recommended for Testing)
```bash
jupyter notebook Chatbot.ipynb
```

### **Cloud Deployment (Optional)**

#### **Hugging Face Spaces** (Free, Public)
1. Fork this repo to your GitHub account
2. Create new Hugging Face Space
3. Connect to your GitHub repo
4. Add API keys to Space secrets
5. Deploy!

#### **Streamlit Cloud** (Free)
Would require converting Gradio to Streamlit, but feasible.

#### **Docker Deployment**
Could containerize for cloud platforms (AWS, Azure, GCP, etc.)

---

## 🛠️ Technical Details

### **Architecture**
- **Frontend:** Gradio 5.0+ with custom CSS
- **Backend:** OpenAI-compatible API clients
- **Models:** 100+ free models across 5 providers
- **Streaming:** Real-time token-by-token responses

### **Key Improvements**
1. **GitHub o-series/GPT-5 fix** - Added `max_completion_tokens` support for advanced OpenAI models (Dec 21)
2. **Model Validation Tool** - Added `validate_models.py` for automated health checks
3. **Enhanced UI** - Modern theme, better layout, status indicators
4. **Dynamic model management** - Cleansed and refined model lists
5. **Safety features** - Empty streaming checks and provider connectivity status


### **Dependencies**
```
gradio>=5.0
openai>=1.0
python-dotenv>=1.0
google-generativeai>=0.3
```

---

## 🤝 Contributing

Found a bug? Want to add features? Here's how to contribute:

### **Fork & Clone**
```bash
git clone https://github.com/YOUR-USERNAME/Multi-Backend-Chatbot-with-Gradio.git
cd Multi-Backend-Chatbot-with-Gradio
```

### **Create a Branch**
```bash
git checkout -b feature/your-feature-name
```

### **Make Changes**
- Add new features, fix bugs, improve documentation
- Test thoroughly with different models
- Update README if adding new capabilities

### **Commit & Push**
```bash
git add .
git commit -m "Add your descriptive message"
git push origin feature/your-feature-name
```

### **Submit Pull Request**
- Go to [GitHub repo](https://github.com/M-F-Tushar/Multi-Backend-Chatbot-with-Gradio)
- Create Pull Request from your fork
- Describe your changes

---

## 🌟 Ideas for Contributions

- [ ] Add more AI providers (Anthropic Claude, Mistral API, etc.)
- [ ] Vision model support (image inputs)
- [ ] Voice input/output support
- [ ] Chat history persistence (SQLite/MongoDB)
- [ ] Multi-user authentication
- [ ] Custom model fine-tuning
- [ ] API usage statistics & cost tracking
- [ ] Docker containerization
- [ ] Streamlit version
- [ ] Web server deployment guide

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- **Gradio** - Beautiful web UI framework
- **OpenAI** - API standard that most providers follow
- **Meta, Google, Mistral, Microsoft** - Open-source models
- **OpenRouter, Groq, GitHub** - Free API access

---

## 📞 Support & Issues

### **Found a Bug?**
1. Check [existing issues](https://github.com/M-F-Tushar/Multi-Backend-Chatbot-with-Gradio/issues)
2. [Create a new issue](https://github.com/M-F-Tushar/Multi-Backend-Chatbot-with-Gradio/issues/new) with:
   - Python version
   - Which provider failed
   - Error message (full traceback)
   - Steps to reproduce

### **Troubleshooting**
1. Check the Troubleshooting section above
2. Verify your API keys in `.env`
3. Ensure all dependencies: `pip install --upgrade gradio openai python-dotenv google-generativeai`
4. Restart Jupyter kernel after editing `.env`
5. Check [GitHub Discussions](https://github.com/M-F-Tushar/Multi-Backend-Chatbot-with-Gradio/discussions) for community help

### **Feature Requests**
- Open a [GitHub Discussion](https://github.com/M-F-Tushar/Multi-Backend-Chatbot-with-Gradio/discussions)
- Or create an [Issue](https://github.com/M-F-Tushar/Multi-Backend-Chatbot-with-Gradio/issues) with `[FEATURE REQUEST]` label

---

## 🔮 Future Enhancements

- [ ] Vision model support (image inputs)
- [ ] Voice input/output
- [ ] Chat history persistence
- [ ] Multi-user support
- [ ] Custom model additions
- [ ] API usage statistics

---

**Happy Chatting! 🚀**

*Last Updated: December 21, 2025*

*Repository: [https://github.com/M-F-Tushar/Multi-Backend-Chatbot-with-Gradio](https://github.com/M-F-Tushar/Multi-Backend-Chatbot-with-Gradio)*
