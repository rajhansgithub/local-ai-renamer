# 🤝 Contributing to Local AI Renamer

Thank you for your interest in contributing to **Local AI Renamer**! We welcome community contributions, bug reports, feature requests, and documentation improvements.

---

## 🧭 Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## 🛠️ Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rajhansgithub/local-ai-renamer.git
   cd local-ai-renamer
   ```

2. **Initialize Environment**:
   Run the automated setup script on Windows:
   ```cmd
   setup_environment.bat
   ```
   Or manually create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install --upgrade pip
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
   pip install -r requirements.txt
   ```

3. **Run Unit Tests**:
   ```bash
   python test_renamer.py
   ```
   Ensure all tests pass before making changes.

---

## 🧪 Testing Guidelines

Whenever you add or modify functionality:
- Add corresponding unit tests in `test_renamer.py`.
- Verify filename sanitization edge cases (special characters, unicode, trailing spaces).
- Test duplicate counter increments (`_1`, `_2`).
- Verify non-image file safety (non-image files must NEVER be renamed or modified).
- Verify VRAM cleanup behaviour when touching inference code.

---

## 📦 Pull Request Process

1. Fork the repo and create your branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Commit your changes with clear, descriptive commit messages:
   ```bash
   git commit -m "feat(engine): add support for custom prompt templates"
   ```
3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
4. Open a Pull Request on GitHub detailing your changes, motivation, and test coverage.

---

## 💬 Community & Questions

Feel free to open an issue for questions, design discussions, or feature requests!
