# GitHub Push Plan

## 1. Prepare the repository

```bash
git init
git add .
git status
git commit -m "Build Code 5 Developers RAG knowledge assistant"
```

## 2. Create the GitHub repository

Create an empty GitHub repository, for example:

`code5-knowledge-assistant`

Do not initialize it with a README, license, or `.gitignore` because this project already includes those files.

## 3. Connect local repo to GitHub

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/code5-knowledge-assistant.git
git push -u origin main
```

## 4. Verify CI

Open the repository Actions tab and confirm the `ci` workflow passes.

## 5. Add deployment secrets

If deploying to Render, add `GROQ_API_KEY` in Render environment variables. Keep the key out of GitHub commits.

## 6. Share for grading or review

Confirm the GitHub repository is accessible to the intended reviewer, then add the final deployed URL to `deployed.md`.
