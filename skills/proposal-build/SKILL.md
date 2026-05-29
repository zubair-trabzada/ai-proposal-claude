# Proposal Build — Flagship Multi-Agent Proposal Generator

You generate a complete, winning, client-ready proposal by launching 5 parallel agents and aggregating their work into one document with a composite Proposal Strength Score (0-100). Invoked by `/proposal build <client>`.

## Step 1: Detect Context
Scan the working directory for existing audit/analysis reports and read them as the evidence base:
`GEO-AUDIT-REPORT.md`, `GEO-REPORT.md`, `SEO-*.md`, `REPUTATION-AUDIT.md`, `RESTAURANT-AUDIT-*.md`, `RECRUIT-*.md`, `REALESTATE-*.md`, `FINANCE-*.md`, `*-AUDIT-*.md`, `*-ANALYSIS-*.md`.

If found, tell the user and anchor the proposal to the real findings. If not, gather: client name/URL, service, engagement model, core problem — and offer to research the client live.

## Step 2: Launch 5 Parallel Agents
Use the Agent tool to launch all simultaneously, passing each the client context and any audit findings:

| Agent | Produces | Scores |
|-------|----------|--------|
| proposal-research | Situation Analysis, pain points, competitive context | Problem-Solution Fit (20%) |
| proposal-pricing | 3-tier Investment table + ROI math | Pricing & ROI Clarity (20%) |
| proposal-scope | Proposed Solution, Scope & Deliverables, Timeline | Scope & Deliverables (20%) |
| proposal-value | ROI Projection, cost of inaction | Value & Business Case (20%) |
| proposal-positioning | Executive Summary, Why Us/Proof, objections, Next Steps | Persuasion & Close (20%) |

## Step 3: Compute Composite Score
Weighted average of the 5 category scores. Apply the grade scale:
85-100 A+ (Send it) · 70-84 A (minor polish) · 55-69 B (gaps to fix) · 40-54 C (rework) · 25-39 D (rebuild) · 0-24 F (start over).

## Step 4: Assemble PROPOSAL-[Client].md
Order: Title block → Proposal Strength Score + breakdown → Executive Summary → Situation Analysis → Proposed Solution → Scope & Deliverables → Timeline → Investment → ROI Projection → Why Us/Proof → Next Steps → Appendix (Follow-Up Sequence). Keep under 12 pages.

## Step 5: Present & Offer PDF
Show the score prominently, then:
> "Generate the client-ready PDF: `Bash(python3 ~/.claude/skills/proposal/scripts/generate_proposal_pdf.py PROPOSAL-[Client].md)`"

## Rules
- Lead with their problem; use real audit numbers; anchor every price to ROI.
- Three tiers mandatory (middle = RECOMMENDED, top = anchor).
- Conservative ROI must still be positive. Frame as opportunity, never failure.
- Fill agency details with placeholders ([YOUR AGENCY], [YOUR NAME], [YOUR EMAIL]).
- Always include the follow-up sequence.
