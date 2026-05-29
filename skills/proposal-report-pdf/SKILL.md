# Proposal Report PDF — Client-Ready PDF Generator

Converts a `PROPOSAL-[Client].md` file into a polished, branded PDF. Invoked by `/proposal report-pdf`.

## Steps
1. Find the proposal markdown in the working directory (`PROPOSAL-*.md`). If multiple, ask which one or use the most recent.
2. Run the generator:
   ```
   Bash(python3 ~/.claude/skills/proposal/scripts/generate_proposal_pdf.py PROPOSAL-[Client].md)
   ```
3. Output: `PROPOSAL-[Client].pdf` in the same directory.

## What the PDF Includes
- Branded cover (deep-indigo band, sky accent, title, client, dates)
- Auto-styled headings, paragraphs, bullet/numbered lists
- Tables with the **RECOMMENDED** pricing column highlighted in gold
- "CONFIDENTIAL" footer with page numbers

## Requirements
`reportlab` (`pip install reportlab`). If missing, tell the user to install it. The script auto-extracts the title, client, agency, date, and validity from the markdown header — so the proposal markdown should keep the standard "Prepared for: / Prepared by: / Date: / Valid Until:" block near the top.

## Demo
`python3 ~/.claude/skills/proposal/scripts/generate_proposal_pdf.py --demo` produces a sample to preview the styling.
