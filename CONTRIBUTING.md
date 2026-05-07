# Contributing

Thanks for considering contributing to the Strix Halo LLM Guide!

## How to Contribute

### Report a Finding
The most valuable contributions are **benchmark results** from your own Strix Halo system. If you find something that contradicts or improves upon this guide, open an issue with:
- Your hardware (Beelink GTR9 Pro, Framework Desktop, GMKtec EVO-X2, etc.)
- Your RAM size and BIOS UMA setting
- Your kernel version (`uname -r`)
- Your Mesa version (`vulkaninfo --summary 2>&1 | grep driverInfo`)
- Your ROCm version, if relevant
- Your backend, build/container version, model file, quant, context length, prompt size, and generated token count
- The exact benchmark command and output
- CSV or raw log output when possible
- What you expected vs what you got

### Fix an Error
If you find incorrect information, outdated commands, or broken links:
1. Fork the repo
2. Fix the issue
3. Open a PR with a clear description of what was wrong

### Add New Content
Before writing new sections, open an issue first to discuss scope. This prevents duplicate work and ensures the content fits the guide's structure.

### Test the Setup Script
Run `bash setup.sh` on your Strix Halo system and report any issues. Testing on different Ubuntu versions, kernel versions, and hardware variants is especially valuable.

### Request a Model or Backend
Open a model request issue if there is a model/backend combination that should be tested. Include why the result would help other Strix Halo users and whether the model requires gated access or unusual setup.

### Discuss Early Results
Use GitHub Discussions for setup questions, early benchmark notes, and comparisons that are not ready for a clean issue yet.

## What We Look For

- **Measured, not estimated.** Every performance claim needs a benchmark number.
- **Reproducible.** Someone else should be able to run your commands and get similar results.
- **Negative results matter.** "I tried X and it didn't work because Y" is valuable content.
- **Copy-paste ready.** Commands should work without modification.
- **Comparable.** Include enough setup detail for someone else to understand why your result differs.

## Style Guidelines

- Write in English
- No emoji in technical content
- Use `> blockquotes` for warnings and tips
- Use `tee` instead of `nano` for file creation commands
- Include version numbers and dates
- When referencing community work, credit the author and link to the source

## Code of Conduct

Be respectful. We're all here because we want local AI to work well on AMD hardware.
