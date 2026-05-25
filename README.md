
# ⚔️ Insults & Cutlasses

Fight your way through to the Swordmaster of Melee Island, armed with your witty insults and sharp comebacks!

---

## 🏴 Introduction

Free-form chatting with NPCs has always been a dream. When large language models (LLMs) became widely available, we got closer to that vision, but most solutions depend on remote servers, which breaks immersion, adds latency, and removes offline play.

For a truly complete experience, the model must run locally.

That introduces constraints: small memory footprint, CPU/GPU efficiency, and compatibility with low-end devices such as laptops, embedded systems, or even smartphones.

Several small models exist, but many struggle with:

- Strict instruction following
- Structured outputs
- Consistent roleplay behavior
- Maintaining personality across turns

Large models perform better, but are too resource-heavy for local-first gaming.

Then came **Gemma 4 E2B**, a model small enough to run locally, even without a GPU, while still maintaining strong instruction-following ability.

However, out of the box, it still lacked consistent *roleplay structure* and *game-like dialogue discipline*. It could break character or ignore formatting rules.

To solve this, I trained a **LoRA adapter** to enforce a structured duel system:

- Insult generation
- Reply generation
- Reply evaluation (judging quality)

This makes the model behave like a true *Monkey Island style insult sword fighting system*.

---

## 🧠 Training

A custom dataset (`MonkeyIslandStylePirateDuelDataset.jsonl`) was created to teach the model a strict interaction loop:

```

Insult → Reply → Judge

```

The model learns to:

- Generate creative pirate insults
- Respond with witty comebacks
- Evaluate whether a comeback is strong or weak

Training was performed using:

- 💻 AMD Ryzen 5 PRO 4650G CPU
- 🧠 32GB RAM
- 🏋️ Fully CPU-based fine-tuning

The full training pipeline is available in:

```

InsultsAndCutlasses.ipynb

```

The result is a **LoRA adapter** that can be applied to the base model or compatible GGUF quantizations.

---

## 🎮 The Game

*Insults & Cutlasses* is a terminal-based insult sword fighting game inspired by *The Secret of Monkey Island*.

### Gameplay Loop

- The game begins with the iconic line:

```

My name is Guybrush Threepwood. Prepare to die!

```

- The player types insults at a prompt:

```

Guybrush> _

```

- The opponent responds with AI-generated insults.

- The player must reply with witty comebacks.

- A judge evaluates each reply:
- 🟢 Good comeback → opponent gets a point
- 🔴 Weak comeback → player gets a point

- First to **3 points wins the duel**

---

## ⚙️ Installation

### 1. Install requirements

```bash
pip install -r requirements.txt

```

Required dependencies include:

-   `llama-cpp-python`

-   `colorama`

* * * * *

### 2\. Download the model

Download the quantized model:

```
https://huggingface.co/unsloth/gemma-4-E2B-it-GGUF/resolve/main/gemma-4-E2B-it-Q4_K_M.gguf

```

Put the file in your project directory.

* * * * *

🚀 Running the Game
-------------------

```
python InsultsAndCutlasses.py

```

* * * * *


💡 Philosophy
-------------

This project explores what happens when:

> **local LLMs meet structured gameplay systems**

Instead of free-form chatbot interaction, the model is constrained into a *game loop*, where creativity is guided by rules, scoring, and competition.

The goal is not just conversation, but **playable intelligence**.

* * * * *

⚖️ License
----------

MIT License

* * * * *

🤝 Credits
----------

-   Inspired by *The Secret of Monkey Island* insult sword fighting

-   Built with `llama.cpp`, `Gemma 4 E2B`, and LoRA fine-tuning techniques

-   Special thanks to the open-source AI community and contributors who make local LLM development possible

-   Huge thanks to the **Dev.to community** for fostering experimentation and creativity in AI game development

This project was developed as part of the **Gemma 4 Challenge** hosted on Dev.to:

[Dev.to Gemma 4 Challenge](https://dev.to/devteam/join-the-gemma-4-challenge-3000-prize-pool-for-ten-winners-23in?utm_source=chatgpt.com)
