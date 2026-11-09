# Pre-screening removal accounting clarified in R3

4 November 2026. The author directed the review to the root `search_strategy.md` and confirmed no subsequent audit of filtered-out entries. Its normalization section and the maintained copy `../protocol/search_strategy.md` distinguish the following mutually exclusive reported categories:

| Removal category | Count | Recorded composition |
|---|---:|---|
| Duplicate entries | 1,182 | 53 Scopus overlaps + 70 IEEE overlaps + 101 IEEE/Scopus matches + 687 ACM overlaps + 23 ACM cross-database matches + 248 arXiv overlaps |
| Containers/podcasts | 624 | 608 proceedings + 9 books + 7 AI-generated podcast summaries |
| Relevance filtering | 4,093 | **728 ACM + 3,365 arXiv** |
| Superseded preprints | 35 | Linked to Tier 1 reports |
| Total pre-screening removals | 5,934 | 6,860 returns minus 926 screening records |

The arXiv component also reconciles as 4,142 query occurrences minus 248 overlaps = 3,894 unique IDs; 3,894 minus 529 unique gate passes = 3,365 removals. Gate passes minus 35 superseded versions = 494 Tier 2 screening entries. The compact retrieval registers corroborate these arXiv counts; a record-count identity is not a validation of relevance judgments.

The root strategy describes ACM fallback retrieval and the post-export title/abstract/keyword relevance gate. The maintained protocol qualifies the unrecovered historical interface field/proximity settings. The claimed reason for a record's removal should not be inferred from its query string alone.

**Conclusion:** the earlier tentative recollection that the 4,093 might be duplicates is not the classification in the search record. The manuscript now states the documented relevance breakdown. No filter recall, false-negative rate, or independently verified correctness of all removals is inferred. The 10-seed retrieval check does not establish complete coverage of the literature. Recovery of full exports and an appropriately documented sample audit could quantify this remaining selection risk; neither has been fabricated in R3.
