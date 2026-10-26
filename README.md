# Somali AI & NLP Resources Registry

A registry of publicly documented artificial intelligence (AI) and natural language processing (NLP) resources for the Somali language: text corpora, speech datasets, translation resources, classification datasets, language models, evaluation sets, and the studies that produced them.

The registry is an **index**. It records metadata about each resource and links to the original source. It does **not** host or redistribute any third-party dataset, corpus, audio, or model.

**Current snapshot:** 26 October 2026. It contains 35 Somali-focused resources, 14 large multilingual resources with Somali components, and a watchlist of 10 items that are documented but not counted. The registry is **not comprehensive** (see [Limitations](#limitations)).

## Contents

- [Repository layout](#repository-layout)
- [Quick start](#quick-start)
- [Coverage](#coverage)
- [Scope and inclusion criteria](#scope-and-inclusion-criteria)
- [Research methodology](#research-methodology)
- [Data files and fields](#data-files-and-fields)
- [How to read the evidence](#how-to-read-the-evidence)
- [Known issues](#known-issues)
- [Limitations](#limitations)
- [Using listed resources responsibly](#using-listed-resources-responsibly)
- [Validating the data and checking links](#validating-the-data-and-checking-links)
- [Contributing](#contributing)
- [How to cite](#how-to-cite)
- [License](#license)

## Repository layout

| Path | Contents |
|---|---|
| [`data/somali_resources_2026-10-26.csv`](data/somali_resources_2026-10-26.csv) | The 35 Somali-focused resources, one per row (Appendix A of the accompanying paper) |
| [`data/multilingual_resources_2026-10-26.csv`](data/multilingual_resources_2026-10-26.csv) | 14 large multilingual benchmarks, corpora, and models with Somali components (not counted) |
| [`data/watchlist_2026-10-26.csv`](data/watchlist_2026-10-26.csv) | Items that are documented but not counted, each with the reason |
| [`scripts/check_links.py`](scripts/check_links.py) | Validates the CSV files and, optionally, checks that their URLs respond |
| [`notes/initial-verification-2026-10.md`](notes/initial-verification-2026-10.md) | Historical verification checklist from 7 October 2026 (superseded) |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to propose resources, report problems, and submit changes |
| [`CITATION.cff`](CITATION.cff) | Citation metadata |
| [`LICENSE`](LICENSE) | CC BY 4.0 for the registry's own metadata and documentation |
| [`NOTICE.md`](NOTICE.md) | What the licenses cover and what they do not cover (third-party resources) |

## Quick start

Download [`data/somali_resources_2026-10-26.csv`](data/somali_resources_2026-10-26.csv). It is UTF-8 encoded, comma-separated, with one header row. In Excel, use *Data > From Text/CSV* and choose UTF-8, so that characters such as "ü" and "ý" display correctly.

With Python's standard library:

```python
import csv

with open("data/somali_resources_2026-10-26.csv", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

open_speech = [r["resource_name"] for r in rows
               if r["category"] == "Speech recognition" and r["access_status"] == "Open"]
print(open_speech)
```

With pandas:

```python
import pandas as pd

df = pd.read_csv("data/somali_resources_2026-10-26.csv")
print(df.groupby(["category", "access_status"]).size())
```

## Coverage

Somali-focused resources by category and documented access status, as of 26 October 2026. The table matches Figure 1 of the accompanying paper.

<!-- category-counts:start -->
| Category | Resources | Open | On request or licensed | Not released | Not documented |
|---|---|---|---|---|---|
| Speech recognition | 11 | 3 | 3 | 5 | 0 |
| Text corpora | 6 | 4 | 2 | 0 | 0 |
| Machine translation | 5 | 2 | 1 | 2 | 0 |
| Sentiment and text classification | 3 | 0 | 0 | 2 | 1 |
| Pretrained language models | 2 | 1 | 0 | 1 | 0 |
| Text-to-speech | 2 | 1 | 0 | 1 | 0 |
| Dialect identification | 2 | 0 | 1 | 1 | 0 |
| Information retrieval | 2 | 1 | 0 | 0 | 1 |
| Lemmatization | 1 | 0 | 0 | 0 | 1 |
| LLM evaluation | 1 | 1 | 0 | 0 | 0 |
| Total | 35 | 13 | 7 | 12 | 3 |
<!-- category-counts:end -->

No optical character recognition (OCR) resource or conversational AI system met the inclusion criteria within the search scope. Several are described on project pages without data, method, or evaluation; they are listed in the watchlist. A zero means "not identified within this search scope", not that no such resource exists.

The multilingual file adds shared benchmarks that cover Somali, including FLORES-200 (translation), Belebele (reading comprehension), SIB-200 and MasakhaNEWS (topic classification), XL-Sum (summarization), AfriHate (hate speech), and FLEURS (speech recognition).

## Scope and inclusion criteria

A resource is included when both of the following hold:

1. It is described in a publicly accessible source: a peer-reviewed paper, preprint, dataset or model card, data-catalog record, or institutional or company page.
2. That source reports verifiable detail about the resource itself, namely its size, data source, method, or an evaluation result. A page that only describes intended functionality is not enough.

The following counting rules apply:

- **Somali focus.** An artifact is counted when it is Somali-only or Somali-English, or when it was built for ten or fewer languages and reports Somali-specific statistics. Large multilingual resources covering tens or hundreds of languages go in the multilingual file and are not counted.
- **Unit.** Each counted item is one documented artifact (a dataset, corpus, trained model, or system) or one empirical study that produces Somali-specific data or results, assigned to a single primary task.
- **Versions and projects.** Successive versions of an artifact are counted once. A corpus compiled only to pretrain a model, and not released separately, is counted with that model. A project that releases artifacts for different tasks is counted once per task.
- **Access is recorded, not used as a filter.** Restricted, on-request, and not-yet-released resources are included, and their status is recorded.

## Research methodology

The inventory comes from a scoping survey carried out by a single researcher. It was not a systematic review.

- **Main search (1 September to 7 October 2026).** Six sources were searched: arXiv, Google Scholar, the ACL Anthology, Hugging Face (datasets and models), GitHub, and the websites of Somalia-based university research groups. Twelve English search strings combined "Somali" with one of: NLP; natural language processing; corpus; dataset; speech recognition; ASR; machine translation; sentiment analysis; text classification; OCR; text-to-speech; chatbot.
- **Targeted lookup (7 October 2026),** made while checking references.
- **Speech follow-up (10 October 2026),** a targeted search on Somali speech data.
- **Somali-language pilot (10 October 2026),** using Somali queries for OCR, text-to-speech, and chatbots. Arabic was not searched.
- **Final update (26 October 2026).** Every entry was re-checked against its primary source, figures and access status were updated, major multilingual benchmarks were checked for Somali components, and Somali-focused resources found during the check were added. This re-verification was carried out with the assistance of an AI tool (Claude, Anthropic), as disclosed in the paper.

The `discovery_phase` column records the phase in which each item was found. Search results screened at each step were not logged, so no screening flow diagram is available.

## Data files and fields

All files are UTF-8 (without byte-order mark), comma-separated, quoted where needed, and have one header row. Lists inside a field are separated by semicolons.

**Versioning and updates.** Each file name carries its snapshot date, and the snapshot date is the registry version (for example `2026-10-26`, as in `CITATION.cff`). Corrections to existing entries are made in place, recorded in Git history, and shown by the row's `date_last_verified`. Adding or removing resources creates a new dated file, and earlier files are then left unchanged. There is no fixed release schedule; entries should be re-checked at least once a year and whenever a correction or broken-link report arrives.

### `somali_resources_2026-10-26.csv`

| Column | Description |
|---|---|
| `id` | Identifier from Appendix A of the paper. The prefix gives the category: T text corpora; L pretrained language models; G lemmatization; E LLM evaluation; S speech recognition; P text-to-speech; M machine translation; C sentiment and text classification; D dialect identification; R information retrieval. IDs are never reused. |
| `resource_name` | Name of the resource or study, as given by its source |
| `category` | Primary task group used for counting, matching Figure 1 of the paper (controlled values; see below). It says what a resource is for, not what kind of artifact it is: a speech corpus and a speech model are both `Speech recognition`. |
| `task` | Task or tasks the resource supports, as described by the source |
| `artifact_type` | Kind of artifact: corpus, dataset, model, study, and so on. Use it with `category` to separate data from systems and studies. |
| `creator` | People or organizations credited by the source |
| `year` | Year of release or publication, or `Not reported` |
| `language_variety` | Dialect coverage stated by the source (controlled values; see below). Other language details, such as where audio was recorded, are in `notes`. |
| `reported_size` | Size as reported by the source, with units; not normalized across entries |
| `reported_results` | Headline evaluation results as reported by the source; not reproduced |
| `annotation` | Annotation or labels the source describes |
| `source_url` | Primary source that documents the resource (paper DOI, catalog record, or card). When one page both documents and distributes a resource, `source_url` and `resource_url` hold the same link. |
| `resource_url` | Where the artifact itself can be found, or `Not released` / `Not reported` |
| `additional_urls` | Further relevant links (code, related versions), separated by semicolons; may be empty |
| `evidence_type` | Source types reviewed, as in Appendix A, strongest first and separated by semicolons (for example peer-reviewed paper, preprint, dataset or model card, data-catalog record, institutional or company page) |
| `access_status` | Documented access category (controlled values; see below) |
| `access_detail` | How access works in practice, as documented |
| `license_terms` | License and terms of use as documented by the provider or paper |
| `license_basis` | Where the license information comes from (controlled values; see below) |
| `verification_level` | How fully the entry was checked against primary sources (see below) |
| `verification_note` | What was checked and how |
| `discovery_phase` | Search phase in which the item was found (controlled values; see below) |
| `date_last_verified` | Date the entry was last checked against its sources (YYYY-MM-DD) |
| `paper_citation` | In-text citation used for the entry in the accompanying paper |
| `notes` | Caveats, discrepancies between sources, and history |

### `multilingual_resources_2026-10-26.csv`

Large multilingual resources with Somali components. They are listed for reference and are not counted in the totals above.

| Column | Description |
|---|---|
| `id` | Identifier, `X01` onward |
| `resource_name` | Name of the resource |
| `task` | Task the resource serves |
| `somali_component` | Somali portion as reported (split sizes are training / validation / test) |
| `source_url` | Paper or primary record |
| `resource_url` | Dataset or model location, or `Not reviewed` / `Not applicable` |
| `paper_citation` | In-text citation used in the paper's Table 3 |
| `date_last_verified` | Date checked (YYYY-MM-DD) |
| `notes` | Caveats |

### `watchlist_2026-10-26.csv`

Items documented somewhere but not counted, kept so that they are not lost or rediscovered from scratch.

| Column | Description |
|---|---|
| `id` | Identifier, `W01` onward |
| `resource_name` | Name of the item |
| `type` | Kind of item |
| `source_url` | Where the item is described, or `Not verified` |
| `reason_not_counted` | Why it is not in the inventory, and what would change that |
| `last_checked` | Date the item was last looked at (YYYY-MM-DD) |
| `notes` | Further detail |

### Controlled values

**`category`:** Text corpora; Pretrained language models; Lemmatization; LLM evaluation; Speech recognition; Text-to-speech; Machine translation; Sentiment and text classification; Dialect identification; Information retrieval.

**`access_status`:**

| Value | Meaning |
|---|---|
| Open | Downloadable by anyone, including after a log-in or license click-through, and including non-commercial licenses |
| On request or licensed | Requires approval, a request form, a data-center license, or purchase |
| Not released | A study without released data, or an artifact announced but not yet available |
| Not documented | The source does not say how to obtain the resource |

**`license_basis`:**

| Value | Meaning |
|---|---|
| Stated by provider | License stated on the provider's own page or card |
| Stated in paper | License stated only in the paper describing the resource |
| Provider metadata only | License taken from platform metadata (for example a Hugging Face tag) without a fuller statement |
| Not stated | No license found in the sources reviewed |
| Not verified | A license exists but its terms were not reviewed |
| Not applicable | Nothing is released to license |

**`verification_level`:**

| Value | Meaning |
|---|---|
| Verified | Identity, scale, access, and license fields were each matched to a primary source |
| Partially verified | The resource exists in a primary source, but one or more fields could not be matched or were seen only in an excerpt; `verification_note` says which |
| Unverified | Known only from a secondary source (no current entries) |

**`discovery_phase`:** Main search; Speech follow-up; Somali-language pilot; Final update; Contribution (for entries added later through contributions).

**`language_variety`:** Maxaa Tiri (Standard Somali); Maay; Maxaa Tiri and Maay; Not specified (the source does not say which variety it covers).

**Placeholders.** `Not reported` means the source was checked and does not state the value. `Not applicable` means the field does not apply. `Not released`, `Not reviewed`, and `Not verified` are used in URL fields when there is nothing to link, when a location was not reviewed, or when no primary source could be confirmed. Values are never guessed.

## How to read the evidence

The registry separates four kinds of information:

- **Verified facts about the source.** `verification_level` and `verification_note` say what was read and when. "Verified" means that the source states what the entry says. It does not mean that the registry reproduced the result.
- **Reported claims.** `reported_size` and `reported_results` repeat what each source reports. Figures from company or institutional pages are self-reported; check `evidence_type`. Results use different test sets and metrics, so they are not comparable across entries.
- **Inaccessible resources.** `access_status` and `access_detail` describe access as documented. Access was not tested by downloading every item. Unreachable pages are noted in `notes` or in the watchlist.
- **License certainty.** `license_basis` shows whether the license comes from the provider, only from a paper, only from platform metadata, or is not stated.

## Known issues

Entries that are unresolved or need care before use, as of the snapshot date:

| Entries | Issue |
|---|---|
| C2 | Partially verified: the provider's page gives no labels, license, or download link, and no copy was found elsewhere. Contacting the SIMAD AI Institute is the remaining way to resolve it. |
| G1, R1 | No download location is given in the sources reviewed, and no license is stated. |
| T2 | Searchable online with accounts on request, but no bulk download and no stated license; the 2016 paper, the 2025 study, and the live platform give different sizes. |
| M5 | Models can be downloaded, but neither the recipes repository nor the download page states a license. |
| S7 | The license (CC BY 4.0) is stated only in the paper; the Hugging Face page shows none and requires manual approval. |
| S9 | Commercial; license terms are provided only with a quote. |
| L1, C3, M2, P2, S10, S11 | Announced but not yet released. Check the source for a release before relying on these entries. |
| S5 | The dataset title says 68 hours; its datasheet says about 70 hours. |

## Limitations

- **Not comprehensive.** The search was run by one researcher, mainly in English, on mainly international platforms. A small Somali-language pilot showed that the English search undercounts. Arabic-language sources, Somali news sites, and local repositories were not searched systematically, and institutions were not contacted.
- **Narrow search strings.** The strings did not target named-entity recognition, part-of-speech tagging, parsing, question answering, or summarization, so resources for those tasks are under-represented.
- **No quality appraisal.** Sizes, licenses, and results are as stated by each source and were not reproduced.
- **Dated snapshot.** Several self-reported figures changed within weeks. Check `date_last_verified` before relying on an entry.
- **Access not tested.** Access status reflects documentation, not an actual download.

## Using listed resources responsibly

- Obtain resources only from their original location and follow each provider's license and terms. Several are non-commercial, research-only, or forbid redistribution.
- Speech and social-media datasets can contain personal data. Respect the restrictions their custodians set.
- SomaliBench (E1) contains harmful-intent prompts by design.
- When you use a resource, cite its own paper or dataset page, not only this registry.

## Validating the data and checking links

```bash
python scripts/check_links.py
```

This runs offline and validates encoding, headers, required fields, controlled values, IDs, duplicates, dates, URL syntax, this README's column documentation and counts, and relative links in the Markdown files. The script needs Python 3.9 or newer and uses only the standard library.

```bash
python scripts/check_links.py --check-urls --report link-report.md
```

This also requests every URL, handling timeouts, redirects, and refused connections, and writes a Markdown report. **A failed request is not evidence that a resource no longer exists.** Many sites block automated clients or require a log-in. Open the page in a browser before changing any entry.

## Contributing

New resources, corrections, and broken-link reports are welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md). Every change needs a primary source.

## How to cite

Citation metadata is in [`CITATION.cff`](CITATION.cff) (GitHub shows a "Cite this repository" button). Suggested citation:

> Muad Mohamed Mohamud. (2026). *Somali AI & NLP Resources Registry* (Version 2026-10-26) [Data set]. GitHub. https://github.com/moadjini/somali-ai-nlp-registry

The registry accompanies the paper *Mapping the Landscape of Artificial Intelligence and Natural Language Processing Resources for the Somali Language: A Scoping Survey of Datasets, Models, and Research Gaps* by Muad Mohamed Mohamud (2026; unpublished manuscript). Please also cite the original source of any resource you use.

## License

- **Registry metadata and documentation** (the CSV files and the Markdown documents) are licensed under the [Creative Commons Attribution 4.0 International license](LICENSE) (CC BY 4.0).
- **Code** in `scripts/` is licensed under the MIT License, as stated in each file's header.
- **Listed resources are not covered.** Each dataset, corpus, model, or paper remains under its own license and terms, as recorded in `license_terms`. This registry grants no rights in them. See [`NOTICE.md`](NOTICE.md).
