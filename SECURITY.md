# 🔒 Security Policy

## Privacy & Local Execution Guarantee

**Local AI Renamer** is architected with privacy and security as first-class principles:
- **100% Offline Processing**: When running with the default `local_florence2` engine, no image or metadata leaves your machine. No telemetry or analytics are collected.
- **Zero Background Retention**: Models are explicitly purged from memory upon task completion.
- **Strict File Safety**: The file renamer exclusively operates on supported image file extensions. Executables, scripts, documents, and system files are never renamed or modified.

---

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

---

## Reporting a Vulnerability

If you discover a security vulnerability or security bug, please **do not open a public issue**. 

Instead, please report it via [GitHub Private Vulnerability Reporting](https://github.com/rajhansgithub/local-ai-renamer/security/advisories/new) or contact the maintainer directly. We will review and respond to reports promptly.
