# 📜 Changelog

All notable changes to **Local AI Renamer** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-09-28

### 🎉 Initial Release

#### ✨ Core Features
- **Local Vision AI Inference**: Offline batch image renaming powered by Microsoft's `Florence-2-base` vision-language model.
- **Windows Explorer Context Menu**: Seamless 1-click integration into Windows 10 / 11 right-click context menu (`Rename with Local AI`).
- **Strict VRAM Purge**: Immediate model deallocation, garbage collection, and CUDA cache flushing upon task completion (0 MB VRAM retention).
- **Subfolder Recursion**: Deep directory traversal processing images in-place.
- **Strict File Type Filtering**: Only processes valid image extensions (`.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tiff`, `.tif`); preserves all other files untouched.
- **Collision Protection**: Automatic counter incrementing (`_1`, `_2`) for duplicate descriptive names.
- **Sanitizer Pipeline**: Filler phrase stripping, stop-word reduction, and 1-to-5 word boundary enforcement.
- **Modern Dark GUI**: Real-time thumbnail preview, progress bar, before/after filename display, and color-coded activity logs.
- **CLI & Headless Mode**: Scriptable execution via `--cli` argument.
- **Optional Cloud Fallback**: Google Gemini API engine option for low-spec machines without dedicated GPUs.
- **Portable Distribution**: C# native zero-console launchers and Inno Setup installer compilation support.
