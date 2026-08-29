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

## Affiliate Link Rules

This repository contains no affiliate links as of August 30, 2026. The public
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
