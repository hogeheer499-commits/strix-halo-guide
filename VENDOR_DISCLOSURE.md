# Vendor Disclosure Policy

This guide is independent and evidence-first. Vendor support can improve the quality of public testing, but it must be visible to readers and must not control benchmark conclusions.

## Disclosure Categories

Use the most specific category near the relevant result:

- Self-purchased hardware.
- Loaner/review unit.
- Gifted/permanent hardware.
- Paid sponsorship.
- Affiliate links.
- Early-access software/firmware.
- Unpaid community contribution.
- Vendor technical feedback.

## Rules

- Every sponsored, loaned, or gifted item must be disclosed near the relevant results.
- Benchmark data must remain reproducible where possible.
- Raw logs and data should be published unless there is a clear privacy or security reason not to.
- Vendors may correct factual errors but do not get editorial control.
- Negative results stay if they are accurate.
- Affiliate links, if ever used, must be disclosed clearly next to the relevant
  link or product table, not only on a separate policy page.
- Early-access firmware or software must be marked clearly when it affects results.
- Community results must remain separated from first-party results unless clearly validated and labeled.
- First-party Beelink results, community-submitted results, server/API results, MTP/speculative results, and direct `llama-bench` results must remain clearly scoped.
- Official AMD, Beelink, OEM, or vendor endorsement must not be implied unless it is explicitly documented.

## Current Relationships And Hardware Provenance

As of September 26, 2026: the first-party test system (Beelink GTR9 Pro, 128GB)
was purchased by the maintainer. No loaned, gifted, sponsored or early-access
hardware is used for first-party results, and no paid sponsorship or affiliate
relationship is recorded in this repository. Any future relationship will be
disclosed here and next to the affected results.

## How We Work With Vendors

- **Independence.** A vendor relationship, a payment, a loaned unit or early
  access does not change how a result is measured or what it concludes. The
  disclosure categories above apply to every relationship.
- **Hardware provenance.** The first-party test system (Beelink GTR9 Pro,
  128GB) was purchased by the maintainer (statement as of 2026-09-26, see
  above). Results from other systems are community results and are labeled as
  such.
- **Reporting a factual error.** A vendor, or anyone else, can report a factual
  error about a product or a claim by email to the maintainer (address in
  [`SERVICES.md`](SERVICES.md#how-to-request-a-scope)) or, for a technical
  correction that can be public, with the
  [bug report template](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=bug-report.md).
  Name the page and the claim, what is wrong, and the primary source (a vendor
  document, a firmware version, or a measurement with its command).
- **What happens next.** A confirmed factual error is corrected, with a dated
  entry in [`EVIDENCE_CORRECTIONS.md`](EVIDENCE_CORRECTIONS.md); no fixed
  turnaround is promised. A claim that cannot be
  checked is labeled "not measured here" or "claim of a third party" instead of
  being removed or silently changed.
- **A vendor response is kept apart.** If a vendor response is published, it is
  recorded apart from the guide's own measurements, labeled as a vendor
  statement and dated. It does not replace a measurement.
- **Negative results stay.** Accurate negative results remain published, also
  after a vendor response or a firmware fix. A later result that supersedes
  them is added with its own date and the earlier one is kept.
- **Review is limited to facts.** A vendor may be asked to check a draft for
  factual accuracy; that is disclosed in the report (see the template below).
  A vendor does not edit or approve conclusions.

## Affiliate Link Rules

This repository contains no affiliate links as of September 19, 2026. The public
registry is [`data/affiliate_link_registry.csv`](data/affiliate_link_registry.csv).

If affiliate links are added later:

- label the link or table row as `affiliate link` where a buyer sees it;
- record the vendor, product, region, relationship, destination, review date,
  and disclosure location in the registry;
- keep a normal non-affiliate manufacturer or evidence link when practical;
- do not rank a machine higher because its program pays more or tracks better;
- keep out-of-stock, unavailable, unsupported, slower, or failed evidence when
  it materially affects the recommendation;
- separate observed affiliate-platform clicks/conversions from GitHub traffic,
  estimated buyer intent, and benchmark evidence;
- recheck destination, region, price/configuration, stock wording, and
  disclosure after a merchant or program change.

Affiliate commission does not determine benchmark inclusion, product ranking,
evidence selection, negative-result retention, or conclusions. A future vendor
may correct factual errors, but neither affiliate terms nor sponsorship buys
editorial control.

## Ranking Firewall

Buyer recommendations should state the decision criteria before evaluating the
available links. For Strix Halo systems those criteria currently include memory
configuration, measured or community evidence depth, price and region at a
dated snapshot, availability, cooling/thermals, firmware/support, ports,
expandability, and workload fit. Commission rate is not a ranking input.

If two systems are otherwise equivalent and link availability affects where a
reader can purchase, describe that as link or regional availability—not as a
technical advantage.

## Reusable Disclosure Template

```text
This test used [self-purchased / loaned / gifted / sponsored] hardware from [vendor].
The vendor [did / did not] review the report for factual accuracy before publication.
The vendor did not receive editorial control over benchmark results or conclusions.
```

Optional additions:

```text
This test used [public / early-access] [BIOS / firmware / driver / software] version [version].
Because this component affects benchmark behavior, results should not be compared directly with public-release results unless the version difference is accounted for.
```

```text
This page contains affiliate links. Affiliate links do not affect benchmark conclusions, result selection, or negative findings.
```

For a buyer-facing comparison, prefer the fuller wording:

```text
Disclosure: links marked "affiliate link" may earn this project a commission.
Commission does not determine benchmark inclusion, ranking, conclusions, or
whether accurate negative results remain published.
```
