# Table 3.2. Extraction batch accounting

Historical numerical table retained from release 3.6.3. In the RQ3 column, Released means numeric records attached to READY claims, not eligibility for latency aggregation.

| Extraction batch | Evidence tier | `Stage3_ID` range | Unique studies (`n = 442`) | Extracted claims (`n = 584`) | `SUPPORTED_WITHIN_SCOPE` claims | `PARTIALLY` / `NOT_SUPPORTED` claims | Released `READY` claims (`n = 530`) | Retained `FLAGGED` claims (`n = 54`) | `RQ3` metrics (`Released / Total`) | `RQ4` deps (`Released / Total`) | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| **`BATCH_E01`** | `TIER_1_PEER_REVIEWED` | `S3-001`..`S3-050` | 50 | 62 | 57 (`91.9%`) | 5 (`8.1%`) | **60 (`96.8%`)** | 2 (`3.2%`) | `114 / 114` | `13 / 13` | 
| **`BATCH_E02`** | `TIER_1_PEER_REVIEWED` | `S3-051`..`S3-100` | 50 | 65 | 55 (`84.6%`) | 10 (`15.4%`) | **58 (`89.2%`)** | 7 (`10.8%`) | `154 / 162` | `32 / 41` | 
| **`BATCH_E03`** | `TIER_1_PEER_REVIEWED` | `S3-101`..`S3-150` | 50 | 60 | 46 (`76.7%`) | 14 (`23.3%`) | **53 (`88.3%`)** | 7 (`11.7%`) | `153 / 187` | `33 / 40` | 
| **`BATCH_E04`** | `TIER_1_PEER_REVIEWED` | `S3-151`..`S3-212` | 62 | 84 | 64 (`76.2%`) | 20 (`23.8%`) | **72 (`85.7%`)** | 12 (`14.3%`) | `247 / 270` | `42 / 56` | 
| **`BATCH_E05`** *(Pilot)* | `TIER_2_ARXIV_PREPRINT` | `S3-213`..`S3-236` | 24 | 39 | 34 (`87.2%`) | 5 (`12.8%`) | **36 (`92.3%`)** | 3 (`7.7%`) | `91 / 96` | `19 / 21` | 
| **`BATCH_E06`** | `TIER_2_ARXIV_PREPRINT` | `S3-237`..`S3-286` | 50 | 68 | 61 (`89.7%`) | 7 (`10.3%`) | **67 (`98.5%`)** | 1 (`1.5%`) | `66 / 70` | `26 / 26` | 
| **`BATCH_E07`** | `TIER_2_ARXIV_PREPRINT` | `S3-287`..`S3-336` | 50 | 67 | 52 (`77.6%`) | 15 (`22.4%`) | **57 (`85.1%`)** | 10 (`14.9%`) | `54 / 67` | `24 / 28` | 
| **`BATCH_E08`** | `TIER_2_ARXIV_PREPRINT` | `S3-337`..`S3-386` | 50 | 65 | 53 (`81.5%`) | 12 (`18.5%`) | **60 (`92.3%`)** | 5 (`7.7%`) | `59 / 65` | `28 / 31` | 
| **`BATCH_E09`** | `TIER_2_ARXIV_PREPRINT` | `S3-387`..`S3-442` | 56 | 74 | 60 (`81.1%`) | 14 (`18.9%`) | **67 (`90.5%`)** | 7 (`9.5%`) | `70 / 80` | `24 / 27` | 
| **Total (All Batches)** | **Tier 1 (`212`) + Tier 2 (`230`)** | **`S3-001`..`S3-442`** | **442** | **584** | **482 (`82.5%`)** | **102 (`17.5%`)** | **530 (`90.8%`)** | **54 (`9.2%`)** | **`1,008 / 1,111` (`90.7%`)** | **`241 / 283` (`85.2%`)** | 
