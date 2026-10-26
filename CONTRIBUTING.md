# Contributing

Thank you for helping make Somali AI and NLP resources easier to find. The registry records **metadata and links only**. Please read this page before you open an issue or a pull request.

## Contents

- [Ways to contribute](#ways-to-contribute)
- [What qualifies](#what-qualifies)
- [Evidence requirements](#evidence-requirements)
- [Proposing a new resource](#proposing-a-new-resource)
- [Correcting an entry](#correcting-an-entry)
- [Reporting a broken link](#reporting-a-broken-link)
- [Editing the CSV files](#editing-the-csv-files)
- [Review process](#review-process)
- [What is never accepted](#what-is-never-accepted)
- [Conduct](#conduct)

## Ways to contribute

| You want to | Use |
|---|---|
| Suggest a resource that is missing | The *New resource* issue form, or a pull request |
| Fix a wrong or outdated value | The *Correction* issue form, or a pull request |
| Report a link that no longer works | The *Broken link* issue form |
| Improve documentation or the script | A pull request |

## What qualifies

The inclusion criteria are the same as in the accompanying paper (see the [README](README.md#scope-and-inclusion-criteria)):

1. **Somali focus.** The artifact is Somali-only or Somali-English, or it was built for ten or fewer languages and reports Somali-specific statistics. Large multilingual resources with a Somali subset go in `data/multilingual_resources_*.csv`.
2. **AI or NLP relevance.** Examples are text corpora, speech data, parallel text, annotated datasets, lexicons, language models, ASR, TTS, MT and OCR systems, benchmarks, evaluation sets, and empirical studies that produce Somali-specific data or results.
3. **A public primary source with verifiable detail.** A paper, preprint, dataset or model card, data-catalog record, or institutional or company page has to report the resource's size, data source, method, or an evaluation result. A page that only describes intended functionality goes on the watchlist instead.
4. **Restricted access is fine.** Licensed, on-request, and announced-but-unreleased resources are accepted, with their access status recorded accurately.

## Evidence requirements

Every proposed addition or change must include:

- the **primary source URL** you checked (not a blog post, aggregator, or search result);
- the **date** you checked it;
- for each value you add or change, the value **as the source states it**, including units.

Rules for values:

- Copy what the source says and do not infer. If the source does not give a value, write `Not reported`.
- If a value comes only from a secondary source, say so in `verification_note` and set `verification_level` to `Partially verified` or `Unverified`.
- Licenses: record the provider's wording in `license_terms`, and set `license_basis` to show where it came from. Never assume a license.
- Never guess a URL. If you cannot confirm a location, use `Not verified`.

## Proposing a new resource

**Option A: issue.** Open a *New resource* issue and fill in the form.

**Option B: pull request.**

1. Add one row to the newest `data/somali_resources_YYYY-MM-DD.csv` file.
2. Use the next free ID for the category, for example `S12` for a new speech recognition resource. Never reuse or renumber IDs.
3. Fill every required column (see the [README field table](README.md#data-files-and-fields)). Set `discovery_phase` to `Contribution` and `date_last_verified` to the date you checked the source.
4. If the item is documented but does not meet the inclusion criteria, add it to `data/watchlist_*.csv` with a clear `reason_not_counted`.
5. Update the README count table if the counts change.
6. Run `python scripts/check_links.py` and make sure it reports `Validation OK`.

## Correcting an entry

Open a *Correction* issue or a pull request. Give the entry `id`, the column, the current value, the correct value, and a primary source that shows the correct value. A statement by the creators on their own page counts as a primary source. When you change a row, update `date_last_verified` and explain the change in `notes` if earlier figures differ.

## Reporting a broken link

Open a *Broken link* issue with the entry `id`, the URL, what happened, and the date you tried. If you know the resource's new official location, give it with a source.

A link that fails for an automated checker, or once for you, does not mean the resource has gone. Many sites block scripts or require a log-in. Maintainers confirm by hand before changing any entry. A confirmed dead link is recorded in `notes` and is never replaced by a guessed address.

## Editing the CSV files

- Keep UTF-8 encoding without a byte-order mark. Spreadsheet programs sometimes add one; the validator reports it.
- Keep the column order and header row exactly as they are.
- Quote fields that contain commas, quotation marks, or line breaks (standard CSV quoting). Separate list items with semicolons.
- One resource per row. A dataset and the paper that describes it are one entry. Mirrors and forks belong in `notes`, not in new rows.
- Do not edit an earlier dated snapshot. A new release copies the newest file to a new dated file name and edits that copy.

## Review process

A maintainer opens the primary source, compares each changed value with it, and either merges the change, edits it to match the source, or explains what is missing. Values that cannot be confirmed are marked as unconfirmed rather than removed silently. Git history keeps the record of every change.

## What is never accepted

- Uploads of datasets, audio, text dumps, or model weights created by other people. This registry stores metadata and links only, because of license terms, personal data in speech and social-media data, and the need for one authoritative source.
- Links to unauthorized copies of data.
- Values that cannot be traced to a source.
- Promotional descriptions. Keep descriptions factual.

## Conduct

Be respectful and constructive, assume good faith, and focus discussion on evidence. Maintainers may edit or close contributions that do not follow these guidelines.
