# Security Best Practices for API Keys

## 🚨 Critical Security Policy

This document outlines how to handle API keys and secrets safely in this project.

## ✅ What You MUST Do

### 1. **Never Commit API Keys**
- ❌ **NEVER** hardcode API keys in code, documentation, or any committed files
- ❌ **NEVER** paste actual API keys into `.md`, `.txt`, `.py`, or any version-controlled file
- ✅ **Always** use environment variables (`os.getenv("GROQ_API_KEY")`)
- ✅ **Always** use `.env` file (which is `.gitignore`'d)

### 2. **Environment Variable Pattern** 
Approved way to access API keys:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")
```

### 3. **File Rules**
- ✅ `.env` - **ONLY** for local development (in `.gitignore`, never committed)
- ✅ `.env.example` - Template with placeholder values (safe to commit)
- ❌ Never commit actual `.env` file
- ❌ Never commit files ending in `.key`, `.pem`, `.secret`

### 4. **Documentation**
When documenting configuration:
```bash
# ✅ GOOD - Show the placeholder from .env.example
GROQ_API_KEY=gsk_your-api-key-here

# ✅ GOOD - Use placeholder notation
GROQ_API_KEY=<your-actual-groq-api-key>

# ❌ BAD - Never show this pattern (DO NOT USE REAL KEYS)
# Real keys follow these patterns:
# Groq: gsk_xxxxxxxxxxxxxxxxxxxxxx (32+ chars after "gsk_")
# OpenAI: sk_xxxxxxxxxxxxxxxxxxxx (48+ chars after "sk_")
# Anthropic: sk-ant-xxxxxxxxxxxxxxxxx (longer key with "sk-ant-")
```

## 📋 Gitignore Policy

Ensure `.gitignore` includes:
```
# Environment & Secrets (CRITICAL)
.env
.env.local
.env.*.local
.env.production
.env.staging
.env.development
secrets/
*.key
*.pem
```

**Current status**: `.gitignore` is configured correctly ✅

## 🔄 What If You Accidentally Commit a Secret?

If you accidentally commit an API key:

### Immediate Steps (Within Seconds of Realizing)
1. **Rotate the API key** - This is the MOST IMPORTANT step
   - Go to console.groq.com, console.openai.com, or console.anthropic.com
   - Delete/revoke the exposed key immediately
   - Generate a new API key
   - Update `.env` with new key locally

2. **Remove from Recent Commits**
   ```bash
   # If only in the last commit (not pushed yet)
   git reset --soft HEAD~1
   git restore --staged .env
   git restore .env
   # Then add .env to .gitignore and recommit
   ```

3. **Force Push to GitHub** (Only if not pushed yet)
   ```bash
   git filter-branch --tree-filter "sed -i 's/old_key/placeholder/g' .env" --force -- --all
   git push --force-with-lease origin master
   ```

### Already Pushed to GitHub?
1. **Rotate the API key immediately** ⚠️
2. Use GitHub's Secret Scanning to verify removal
3. Contact Groq/OpenAI/Anthropic support to invalidate the exposed key

## 🛡️ Pre-Commit Checklist

Before using `git add` and `git commit`:

- [ ] I am NOT committing a `.env` file (it should be `.gitignore`'d)
- [ ] My documentation shows examples with `gsk_your-api-key-here`, not real keys
- [ ] No `GROQ_API_KEY`, `OPENAI_API_KEY`, or `ANTHROPIC_API_KEY` has actual values (except in `.env`)
- [ ] No `.key`, `.pem`, or `.secret` files are being committed
- [ ] I've run `git status` to verify only intended files are staged

## 📝 Code Review Guidelines

When reviewing pull requests:
1. Check for hardcoded API keys in diffs
2. Verify all secrets use `os.getenv()` access pattern
3. Ensure documentation uses placeholders, not real keys
4. Require `.env.example` updates if env vars change

## 🔑 Retrieving Your API Keys

### Groq
1. Visit https://console.groq.com
2. Navigate to "Keys" in the left sidebar
3. Generate or copy your API key
4. Add to `.env`: `GROQ_API_KEY=<your-key-here>`

### OpenAI
1. Visit https://platform.openai.com/account/api-keys
2. Generate new secret key
3. Add to `.env`: `OPENAI_API_KEY=<your-key-here>`

### Anthropic
1. Visit https://console.anthropic.com
2. Navigate to "API Keys"
3. Generate new API key
4. Add to `.env`: `ANTHROPIC_API_KEY=<your-key-here>`

## ✅ Verification

To verify secrets are not leaked:
```bash
# Check current files for secrets
git grep "gsk_" -- '*.py' '*.md' || echo "✓ No Groq keys found"
git grep "sk-ant-" -- '*.py' '*.md' || echo "✓ No Anthropic keys found"  
git grep "sk_" -- '*.py' '*.md' | grep -v "sk_your" || echo "✓ No real OpenAI keys found"

# Search git history
git log --all -S "gsk_" --oneline || echo "✓ No Groq keys in history"
```

## 📚 References

- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [OWASP: Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [Best Practices for API Key Management](https://blog.jscrambler.com/best-practices-for-keeping-api-keys-secure/)

---

**Last Updated**: March 28, 2026  
**Status**: ✅ Active (after incident recovery)
