# 🤖 AI-Powered Facebook BruteForce Tool

> Smart wordlist generator + brute force engine.  
> AI analyzes target info and generates contextual passwords automatically.

---

## ⚠️ Disclaimer

This tool is for **educational purposes and authorized penetration testing only**.  
**Do NOT use this tool on accounts you don't own or have explicit permission to test.**  
Unauthorized use is illegal and may result in criminal charges.  
The author is not responsible for any misuse of this tool.

---

## ✨ Features

- 🧠 **AI Wordlist Generation** — Claude AI generates smart, contextual passwords based on target info (name, birth year, nickname, hobby, etc.)
- 📄 **passwords.txt Support** — works with traditional wordlists too
- 🔀 **Combined Mode** — AI + wordlist merged for maximum coverage
- 🔑 **Your Own API Key** — each user brings their own Anthropic key (no shared costs)
- 💾 **Key Saved Locally** — enter once, reused automatically

---

## 🚀 Installation

```bash
git clone https://github.com/YOUR_USERNAME/fb-ai-bruteforce
cd fb-ai-bruteforce
pip install -r requirements.txt
```

---

## 🔑 API Key Setup

This tool uses **Anthropic Claude API** for AI wordlist generation.  
Get your free key: [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)

The key is stored at `~/.config/fb_ai_bf/config.json` (chmod 600 — only you can read it).

**Alternative:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python fb_ai_bruteforce.py
```

---

## 💻 Usage

```bash
python fb_ai_bruteforce.py
```

**3 modes available:**
```
1 → AI only         (generates passwords from target info)
2 → passwords.txt   (classic wordlist, original mode)
3 → AI + file       (combined, most powerful) ← recommended
```

---

## 📦 Requirements

```
requests
beautifulsoup4
anthropic
```

---

## 📁 Project Structure

```
fb-ai-bruteforce/
├── fb_ai_bruteforce.py   # Main tool
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 📜 License

MIT License — use responsibly.

