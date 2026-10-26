> **Historical record. Superseded on 26 October 2026.**
>
> This checklist documents a verification pass made on 7 October 2026 for an earlier 22-entry draft of the registry. It is kept unchanged below for provenance. **It is not the current inventory.** The current inventory is [`data/somali_resources_2026-10-26.csv`](../data/somali_resources_2026-10-26.csv), which follows the paper's Appendix A and was re-verified on 26 October 2026. Where this checklist and the current data differ, the current data apply.
>
> **How the open items below were resolved:**
>
> - IDs `SOMREG-001` to `SOMREG-022` were replaced by the paper's Appendix A IDs (crosswalk below).
> - MATERIAL hours: the inventory uses the LDC catalog's ~80 h (S4).
> - planwise-data: recorded as a 100-row public sample, with the full set on request (M4).
> - CC-100: moved to the multilingual file (X01), not counted. Its Somali size (~62M tokens) was checked against the XLM-R paper.
> - Ogaal ASR: training data recorded as private. Hugging Face metadata showed an Apache-2.0 license on 26 October 2026, not "other" (S6).
> - Research-study entries are counted under the paper's rules, with access status "Not released".
> - Omissions: soWaC (T4), the LORELEI Somali pack (T5), AfriVoices-KE (S7), and the lemmatization corpus (G1) were added. The LREC 2020 MT benchmark is on the watchlist (W02).
> - Files mentioned below: `data/watchlist.csv` is replaced by `data/watchlist_2026-10-26.csv`, and `scripts/check_links.py` has been rewritten. `CODE_OF_CONDUCT.md` is not included; conduct is covered in `CONTRIBUTING.md`.
> - Licenses: CC BY 4.0 for registry metadata and documentation, MIT for scripts (see `LICENSE`). The repository URL is in `CITATION.cff`. No survey DOI exists yet.
>
> | Former ID | Entry | Current ID |
> |---|---|---|
> | SOMREG-001 | SomaliWeb v1 | T1 |
> | SOMREG-002 | RCF-SC | T2 |
> | SOMREG-003 | SomNLP-Corpus (now Somali NLP Corpus) | T3 |
> | SOMREG-004 | CC-100 Somali | X01 (multilingual file; not counted) |
> | SOMREG-005 | SomBERTa pretraining corpus | L1 (counted with the model) |
> | SOMREG-006 | Somali IR corpus | R1 |
> | SOMREG-007 | Menon et al. (2018) | S2 |
> | SOMREG-008 | Biswas et al. (2019) | S3 |
> | SOMREG-009 | MATERIAL pack | S4 |
> | SOMREG-010 | Digital Divide Data set | S5 |
> | SOMREG-011 | Ogaal ASR | S6 |
> | SOMREG-012 | Ali (2026) | D1 |
> | SOMREG-013 | tufaax pairs | M1 |
> | SOMREG-014 | Thiomi Somali-English | M2 |
> | SOMREG-015 | Kuwanto et al. | M3 |
> | SOMREG-016 | planwise-data STEM lexicon | M4 |
> | SOMREG-017 | JUST machine translation system | W06 (watchlist; no data, method, or evaluation) |
> | SOMREG-018 | Abdirahman et al. (2023) | C1 |
> | SOMREG-019 | SIMAD Twitter hate-speech set | C2 |
> | SOMREG-020 | SomBERTa datasets | C3 |
> | SOMREG-021 | Ahmad et al. (2025) | X11 (multilingual file; not counted) |
> | SOMREG-022 | Gedi et al. (2026) | D2 |

---

# Initial verification report (2026-10-07)

Reviewer checklist for the 22 initial entries. Written for the maintainer's final human review; delete or keep as provenance before publishing.

## Method and limits

- Each entry was compared with original sources found by web search: papers (arXiv, ACL Anthology, Springer, journal pages), Hugging Face cards, LDC catalog, Mozilla Data Collective, institutional pages.
- **Link checking was limited.** Only these were fetched directly and returned content: Hugging Face (SomaliWeb, tufaax, Ogaal ASR), Springer (Gedi et al.), Academia.edu (RCF-SC). The three GitHub repositories (SomaliWeb code, SomNLP-Corpus, Ogaal-ASR) returned HTTP 200 from the sandbox. All other URLs were seen **only in search results** and are listed below as "search only". Nothing could be tested for dead links beyond that. Run `python scripts/check_links.py` from a normal network to complete this.
- `github.com/goobolabs` returned HTTP 404 from the sandbox although search results showed it; recheck.
- Figures such as BLEU, accuracy and segment counts were checked only where stated below.

## Summary table

| ID | Original source found | Verified | Links | Uncertain fields | Discrepancy with the survey | Double-check |
|---|---|---|---|---|---|---|
| 001 SomaliWeb v1 | Yes (arXiv, HF card, GitHub) | Verified | HF fetched; GitHub 200; arXiv search only | none material | Token count is an estimate (words x 1.3); 233M whitespace words | Whether to quote tokens or words |
| 002 RCF-SC | Yes (Academia paper) | Partially | Academia fetched; somalicorpus.com **not checked** | year, licence, availability, current size | Source says ten sub-corpora but lists nine; later paper says 7M tagged words vs 1.5M | Is somalicorpus.com live? Which size to report |
| 003 SomNLP-Corpus | Yes (GitHub README excerpt) | Partially | GitHub 200 | creator names, code licence, first-release date | Survey credits "contributors"; repo belongs to Goobo Labs. It is a pipeline, not a hosted dataset | Open the README and confirm 13 sources and the licence |
| 004 CC-100 Somali | Yes (HF card) | Partially | search only | Somali token count | Survey ~62M tokens, HF card lists "78M" (unit unclear). Licence statements conflict across sources | Check the XLM-R paper table for the Somali figure |
| 005 SomBERTa corpus | Paper yes; corpus no | Partially | search only | size, licence, availability, component list | Component list is from the survey, not checked in the full text | Read the paper's data section |
| 006 Somali IR corpus | Yes (ACL Anthology) | Partially | search only | affiliations, licence, download link | none | Find the corpus download, if any |
| 007 Menon 2018 | Yes | Verified | search only | none | none | none |
| 008 Biswas 2019 | Yes | Verified | search only | none | none | none |
| 009 LDC MATERIAL | Yes (LDC catalog) | Verified | search only | none | **Survey says ~50 h; LDC says ~80 h.** Only ~10% is transcribed and the pack targets CLIR | See "Items that touch the paper" |
| 010 DDD 68 h | Yes (Mozilla DC page) | Partially | search only | licence label, year | Survey ok; "68 h" in title, "~70 h" in datasheet | Open the page; confirm licence and access |
| 011 Ogaal ASR | Yes (HF fetched) | Verified | HF fetched; GitHub 200 | release date | Training data is partly private and unreleased; licence is "other" | Survey comparison of "hours" |
| 012 Ali 2026 | Partly (landing excerpt) | Partially | search only | author name, affiliation, 180 segments, 81.48%, availability | Not checked | Read the preprint |
| 013 tufaax | Yes (HF fetched) | Verified | HF fetched | creation date, provenance of translations | Content is mostly short phrases and words | Survey wording on "8k pairs" |
| 014 Thiomi NLLB | Paper yes (abstract) | Partially | search only | Somali BLEU, 60k pairs, release | Dataset "will be published"; no release found | Read Somali MT section |
| 015 Kuwanto | Yes | Verified | search only | none | Published at PRICAI 2023 (dblp); survey cites arXiv only | Update citation; is it a "resource"? |
| 016 planwise STEM | Yes (HF card) | Verified | search only | date | **Public release is a 100-row sample; full 3,000+ terms on request** | Survey wording |
| 017 JUST MT | Institution page only | Partially | search only | pair, data, availability | Page found is on the SAIL domain | Open the portal; find a stable URL |
| 018 Abdirahman 2023 | Yes (journal page) | Partially | search only | affiliation, figures, dataset used | CC-100 usage not confirmed | Read the paper |
| 019 SIMAD tweets | Yes (SIMAD AI page) | Partially | search only | labels, download, licence, release date | Host calls itself "SIMAD AI Institute" | See note below |
| 020 SomBERTa datasets | Paper yes; datasets no | Partially | search only | sizes, labels, licence, location | none | Read the paper |
| 021 Ahmad 2025 | Yes (arXiv) | Verified | search only | Somali data source | Multilingual study, not Somali-specific | Inclusion decision |
| 022 Gedi 2026 | Yes (Springer fetched) | Verified | Springer fetched | none | Earlier preprints said ~3,000 samples; final says 8,947 (matches survey) | none |

## Items that touch the paper (for your decision, not changed)

1. **MATERIAL pack hours.** The LDC catalog states about 80 hours of Somali telephone speech, not about 50. If the survey says Ogaal's 72.1 hours is the largest documented speech resource, this needs qualification (LDC speech is mostly untranscribed, and Ogaal's data is unreleased).
2. **planwise-data** is a 100-row sample publicly; the survey should say so.
3. **CC-100 Somali size and licence:** sources disagree; see entry notes.
4. **Ogaal ASR training data** is not public.
5. **Not Somali-specific or no released artifact:** SOMREG-007, 008, 015, 018, 021 (and 012, 014 unreleased). Decide whether the registry should include "Research study" entries.
6. **Omissions found:** soWaC, LORELEI Somali (LDC2026T03), AfriVoices-KE, a Somali lemmatization corpus, a 2020 LREC MT benchmark. They are in `data/watchlist.csv`, not in the 22.

## Things only you can settle before publishing

- **Author name spelling** in `CITATION.cff` and README (I used the survey's "Muad Mohamed Mohamud").
- **Licence choices:** MIT for code and CC BY 4.0 for metadata are my proposals.
- **Maintainer contact** in `CODE_OF_CONDUCT.md` is a placeholder; the **repository URL** for citation is also missing.
- **Survey citation/DOI** in the README is not yet filled.
- **ai.simad.edu.so pages** contained unrelated injected advertising links (appeared in the page text). I did not follow them. The site may be compromised and worth reporting to SIMAD IT; the link in SOMREG-019 may change.
- Open the "search only" links yourself before publishing.
