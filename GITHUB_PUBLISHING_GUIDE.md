# 🚀 GitHub Publishing & SEO Strategy Guide

This guide documents the naming, search engine optimization (SEO), positioning, and step-by-step checklist for publishing this project to GitHub and public communities (Reddit, Product Hunt, Hacker News, YouTube).

---

## 📌 1. Final Brand & Identity

### Primary Recommendation: **Local AI Renamer**
* **Project Display Title**: `Local AI Renamer`
* **Alternative**: `Local AI Rename` (if a direct verb/action vibe is preferred)
* **GitHub Repository Name**: `local-ai-renamer` (or `local-ai-rename`)
* **Windows Executable Name**: `LocalAIRenamer.exe`
* **Windows Explorer Context Menu Entry**: `"Rename with Local AI"` (concise, professional)

---

## 🔍 2. SEO & GitHub Metadata Blueprint

When setting up the GitHub repository, fill in the repository details exactly as structured below to rank #1 on Google and GitHub search:

### A. Repository Description (About section - Max 350 chars)
```text
Fast, context-aware, offline image renamer for Windows. Uses local AI vision models (Florence-2) to rename photos by their content. 1-click Windows Explorer context menu integration, 0 MB VRAM retention, and zero cloud dependencies.
```

### B. Repository Website URL (if no custom domain yet)
Point to: `https://github.com/<your-username>/local-ai-renamer#readme` or a GitHub Pages release page.

### C. Recommended GitHub Repository Topics / Tags
Add all of these tags directly in the "About" settings gear icon on GitHub:
* `ai-image-renamer`
* `local-ai`
* `batch-renamer`
* `florence-2`
* `image-renaming`
* `windows-utility`
* `computer-vision`
* `offline-ai`
* `context-menu`
* `photo-organizer`
* `privacy-first`
* `pytorch-cuda`

---

## 📝 3. README SEO Header Formula

Place this at the very top of your `README.md` to capture search engines:

```markdown
# ⚡ Local AI Renamer

> **Offline, GPU-accelerated batch image renaming for Windows Explorer powered by local computer vision AI.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows%2010%20%2F%2011-0078D6.svg)](https://microsoft.com)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![Model: Florence-2](https://img.shields.io/badge/Model-Florence--2--base-orange.svg)](https://huggingface.co/microsoft/Florence-2-base)
[![Local & Offline](https://img.shields.io/badge/Privacy-100%25%20Offline%20%26%20Private-success.svg)](#)
```

---

## 🎯 4. Target Search Keywords & User Intent

These are the primary search queries potential users type into Google, YouTube, and GitHub. Ensure these phrases naturally appear in the README headers and text:

| Target Query Type | Search Phrase | Why This Tool Wins |
|---|---|---|
| **High-Intent Technical** | `local ai image renamer` | Exact match for our brand and function |
| **Problem-Solving** | `rename photos based on what is in them` | People with thousands of unorganized `IMG_001.jpg` files |
| **Privacy / Offline** | `offline ai photo renamer windows` | No cloud subscription, no uploading private photos |
| **Utility / Workflow** | `windows explorer right click ai rename` | The convenience of right-clicking a folder directly |
| **Hardware-Specific** | `gpu accelerated batch file rename cuda` | Fast Florence-2 inference with automatic VRAM clearing |

---

## 📢 5. Social Launch & Community Positioning

When sharing on forums, use the following angles tailored to each community:

### Reddit (r/LocalLLaMA, r/selfhosted, r/windows, r/photography)
* **Title idea**: *"I built an open-source tool that renames your photos using local vision AI (Florence-2) directly from Windows Explorer right-click"*
* **Key talking points**:
  * 100% offline & private (no cloud API key needed).
  * Strict VRAM unloading: loads on click, unloads completely to 0 MB VRAM right after.
  * Handles subfolders recursively, collision counters (`_1`, `_2`), and cleans filler phrases.

### Product Hunt / Hacker News (Show HN)
* **Title idea**: `Show HN: Local AI Renamer – Offline Vision-Based Image Renaming for Windows`
* **One-liner**: `Batch rename photos based on what's actually in them using local AI on your GPU.`

---

## ✅ 6. Pre-Publish Checklist (Before Pushing to GitHub)

Before running `git push` to make the repository public:

1. **Clean Private Keys & Secrets**:
   - Verify `config.json` has `gemini_api_key: ""` (empty).
   - Ensure `.gitignore` ignores `.venv/`, `dist/`, `build/`, `*.log`, `scratch/`, and `__pycache__/`.
2. **Add an Open Source License**:
   - Add a standard `LICENSE` file (MIT or Apache 2.0 recommended for maximum adoption).
3. **Screenshots / GIF Demo**:
   - Add a 10-second screen recording GIF showing:
     1. Right-click folder -> "Rename with Local AI".
     2. GUI processing with live thumbnail preview.
     3. Files successfully renamed.
   - Place image in `assets/demo.gif` and embed it in the README.
4. **Releases & Binary Distribution**:
   - Compile `AutoImageRenamer_Setup.exe` (or `LocalAIRenamer_Setup.exe`) via Inno Setup.
   - Create a GitHub Release (e.g. `v1.0.0`) and attach the `.exe` so non-Python users can simply download and install it in 1 click.
