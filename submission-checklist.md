# Submission Checklist

## Completed

- GitHub repository pushed: https://github.com/Kigen29/code5-knowledge-assistant
- Flask RAG app implemented with `/`, `/chat`, `/health`, `/library`, and document reader pages.
- Synthetic Code 5 Developers corpus included in the repo.
- PDF manuals generated and included in `policies/`.
- CI workflow included in `.github/workflows/ci.yml`.
- Render deployment config included in `render.yaml`.
- Tests pass locally: `5 passed`.
- Evaluation set includes 30 questions.
- Latest local evaluation:
  - Groundedness auto-check: 100%
  - Citation accuracy auto-check: 100%
  - Latency p50: 20 ms
  - Latency p95: 21 ms

## Still To Do Outside The Repo

1. Share the GitHub repository with `quantic-grader`.
2. Deploy on Render or another host if you want the optional public deployment.
3. Add the deployed URL to `deployed.md`.
4. Record the 5-10 minute demo video.
5. Create the final submission PDF containing:
   - GitHub repo link: https://github.com/Kigen29/code5-knowledge-assistant
   - Demo video link
   - Deployed app link, if used
6. Submit the final PDF through the Quantic dashboard.

## Demo Flow

1. Open the app and show the Code 5 Developers branding.
2. Open `/library` and show Markdown and PDF documents.
3. Ask: "What is Code 5 Developers' standard software delivery workflow?"
4. Show answer, citations, and retrieved snippets.
5. Ask: "What should be included in a maintenance handover?"
6. Ask an unrelated question to show the refusal guardrail.
7. Show `design-and-evaluation.md`, `eval/questions.jsonl`, and the GitHub Actions workflow.
