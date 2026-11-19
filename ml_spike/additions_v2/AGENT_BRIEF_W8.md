# Brief for wave 8: alkali-activated (AAS) and geopolymer composites

Read `ml_spike\additions_v2\AGENT_BRIEF.md` first, then `ml_spike\additions_v2\AGENT_BRIEF_ELS.md` (quick-reject rules,
output files, checks). Every rule there applies, with the changes below.

## Source
- Elsevier: `Papers\Paper news\elsevier_txt\ELS_<doi>.txt` (format in AGENT_BRIEF_ELS.md).
- MDPI: `Papers\Paper news\mdpi_txt\MDPI_<doi>.txt`. Line 1 = `DOI: ...`. The body text comes first; ALL tables are at the
  end under "TABLES (from the article's table pop-ups):" as `[[TABLE]] <caption>` + tab-separated rows (a table can
  appear twice; use it once).
- Other publishers: `Papers\Paper news\other_txt\OTHER_<doi>.txt`: plain page text; tables as `[[TABLE]] <caption>` +
  tab-separated rows (the caption can also be the line just before).
- Do NOT use the web or a browser. Work only from these files.

## Scope
- These papers are about alkali-activated slag / fly ash / geopolymer composites. Mixes WITH cement in the same paper are
  welcome too. Binder must contain cement, fly ash or GGBS (a metakaolin-only binder cannot be used).
- Fibers: PE, PVA and steel only (any mix with another fiber type, incl. PBO, PP, basalt, glass, carbon, natural,
  "selvage", is skipped and listed in the rejected file).
- Concrete with coarse aggregate: skip (coarse aggregate is not one of the materials).

## Activators: only values the paper states
- Solid NaOH, Na2SiO3 (anhydrous, or pentahydrate converted as in AGENT_BRIEF.md), Na2SO4, Ca(OH)2: mass ratio to binder.
- Water glass (sodium silicate solution): "WG / B (Water glass)" = solution mass / binder; note its modulus and solids if given.
- NaOH given as a SOLUTION (e.g. "10 M NaOH solution, 0.15 of binder"):
  - if the paper states the NaOH solids (mass or %) of that solution, use them;
  - otherwise, if it states the MOLARITY and the solution amount (mass, or volume), convert with
    `ml_spike\additions_v2\naoh_solution.py` (`naoh_split(molarity, solution_mass=...)` or `solution_volume_L=...`;
    the user allowed this conversion, table from the OxyChem Caustic Soda Handbook). NaOH / B = the NaOH solids; the
    solution water goes into W / B. Copy the function's `note` into "Conversions / notes".
  - Molarity must be stated by the paper; the solution amount must be stated per mix (not split from a total of
    NaOH solution + water glass unless both amounts or their mass ratio AND the total are stated in the paper: then
    say so in the notes).
  - Anything else (no molarity, no amount): REJECT the mix.
- Never estimate an amount, split a stated total into parts, or assume a curing condition or test age.

## Accuracy
- Every number must be traceable to a table or sentence of the paper; put the table/section in the source column.
- Results only in figures: not allowed. Curing, test age and (for strain) the direct tension test must be stated.
- Fiber length, diameter, tensile strength, elastic modulus: copy exactly from the paper; blank when not stated.
- If text and table disagree, or a value looks implausible, reject that mix/paper and say why.

## Output names
- `ml_spike\additions_v2\w8_<yourname>.csv`, `ml_spike\extract_scripts\w8_<yourname>.py`,
  `ml_spike\additions_v2\w8_<yourname>_rejected.txt`.
