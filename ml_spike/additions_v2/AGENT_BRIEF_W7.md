# Brief for wave 7: papers of Prof. Bang Yeon Lee's lab (Chonnam National University)

Read `ml_spike\additions_v2\AGENT_BRIEF.md` first, then `ml_spike\additions_v2\AGENT_BRIEF_ELS.md` (quick-reject rules,
output files, checks). Every rule there applies, with the changes below.

## Source
- Plain-text files in `Papers\Paper news\download\` (one per paper, file name = number_author_year_DOI.txt).
  Line 1 = `# <title>`, line 2 = `URL: ...`. Tables appear as a line `Table N. <caption>` followed by the rows.
  A PDF-only paper was converted to text in the scratchpad path given in your prompt.
- The DOI is in the file name (first `_` after the year = `/`) and in `Papers\Paper news\download\papers_list.csv`.
- Do NOT use the web or a browser. Work only from these files (Grep / Read with offsets).

## Fibers: only PE and PVA
- Extract a mix only if every fiber in it is PE (polyethylene, incl. UHMWPE) or PVA. Skip mixes with steel, PBO, glass,
  basalt, PET, PP, carbon, or "selvage"/"selvedge" fibers (these are PE + glass/PET blends), and list them in the
  rejected file with the reason.
- Fiber length (mm), diameter (µm), tensile strength (MPa) and elastic modulus (GPa): copy EXACTLY from the paper's fiber
  table/text into the template columns `PE length (mm)`, `PE diameter (µm)`, `PE tensile strength (MPa)`,
  `PE elastic modulus (GPa)` (same for PVA). Leave blank when the paper does not state it. Never fill from general
  knowledge or from another paper.

## Accuracy
- Every number must be traceable to a table or sentence of the paper; put the table/section in the source column.
- Results only in figures: not allowed. Test age, curing and tensile test type must be stated in the paper.
- If the text and a table disagree, or a value looks implausible, reject the mix/paper and say why.

## Output names
- `ml_spike\additions_v2\w7_<yourname>.csv`, `ml_spike\extract_scripts\w7_<yourname>.py`,
  `ml_spike\additions_v2\w7_<yourname>_rejected.txt`.
