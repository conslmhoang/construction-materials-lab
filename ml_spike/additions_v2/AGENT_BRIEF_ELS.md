# Brief for wave 6: Elsevier full texts already on disk

Read `ml_spike\additions_v2\AGENT_BRIEF.md` first. Every rule there applies (21 materials, inclusion,
99-column TEMPLATE header, conventions, checks). Only the source of the papers is different.

## Source
- The papers are plain-text dumps of ScienceDirect full-text pages, one file per paper:
  `Papers\Paper news\elsevier_txt\ELS_<doi with / and . replaced by _>.txt`.
  Line 1 = `DOI: https://doi.org/...`. Tables appear as `[[TABLE]] <caption>` followed by tab-separated rows,
  then `NOTE:` with the table footnotes. Figures appear only as `[[FIGURE]] <caption>` (no data).
- Do NOT use the web or a browser. Work only from these files. Use Grep / Read with offsets: files are 30-90 KB,
  so first grep for `[[TABLE]]`, "mix proportion", "curing", "compressive strength", "tensile strain", then read
  only the needed parts.
- You get a fixed list of files (below in your prompt). Decide for each file: extract or reject.

## Quick reject (one line in the rejected file, no deep reading)
- No mix proportions table/text, or results of interest only in figures (no number in text or table).
- Every mix uses a material outside the 21 (check the materials section).
- No compressive strength and no direct-tension strain capacity.
- Special exposure only (fire, sulfate, impact, freeze-thaw ...). If the paper also reports reference specimens
  under ordinary conditions with numbers, keep those rows.
- Review / modelling paper, or structural members only.

## Output
- `ml_spike\additions_v2\w6_<yourname>.csv` (pandas, utf-8-sig, exact TEMPLATE header, same order),
  builder script `ml_spike\extract_scripts\w6_<yourname>.py`, rejected list `ml_spike\additions_v2\w6_<yourname>_rejected.txt`.
- Values from text where the paper states them; values read off a figure are NOT allowed in this wave.
- Same final pandas checks as AGENT_BRIEF.md. Final report: papers added (count), rows, rejected count, doubtful values.
