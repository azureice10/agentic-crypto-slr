# Stage 3 Raw Reviewer Worksheets (R1 & R2) and Reproducible Inter-Reviewer Agreement (IRR) Package

## 1. Tujuan Paket Ini
Paket ini menghimpun seluruh **18 berkas lembar kerja ekstraksi mentah pra-adjudikasi Stage 3** dari **Reviewer 1 (`REVIEWER_1`: Herman Kabetta, 533 baris klaim lintas 442 studi)** dan **Reviewer 2 (`REVIEWER_2`: I Komang Setia Buana, 508 baris klaim lintas 442 studi)** untuk ke-9 *batch* ekstraksi (`BATCH_E01` s.d. `BATCH_E09`), beserta **9 berkas master rekonsiliasi/adjudikasi per *batch*** (`ADJUDICATOR_1`: Raden Budiarto), skrip perhitungan Python yang dapat dijalankan ulang (`scripts/compute_stage3_irr_agreement.py`), serta tabel hasil kesepakatan di bawah **empat aturan pemasangan (*pairing/aggregation rules*)** yang berbeda (tingkat studi vs. tingkat klaim).

---

## 2. Struktur Folder dan Berkas di Dalam Paket ZIP

```text
stage3_r1_r2_raw_worksheets_and_irr_package/
├── README_STAGE3_IRR.md
├── raw_reviewer_1_herman_kabetta/
│   ├── LEMBAR_KERJA_REVIEWER_1_BATCH_E01_TIER1_50.csv      (57 klaim dari 50 studi Tier 1)
│   ├── LEMBAR_KERJA_REVIEWER_1_BATCH_E02_TIER1_50.csv      (60 klaim dari 50 studi Tier 1)
│   ├── LEMBAR_KERJA_REVIEWER_1_BATCH_E03_TIER1_50.csv      (59 klaim dari 50 studi Tier 1)
│   ├── LEMBAR_KERJA_REVIEWER_1_BATCH_E04_TIER1_62.csv      (81 klaim dari 62 studi Tier 1)
│   ├── LEMBAR_KERJA_REVIEWER_1_BATCH_E05_PILOT_24.csv      (31 klaim dari 24 studi Pilot Tier 2)
│   ├── LEMBAR_KERJA_REVIEWER_1_BATCH_E06_ARXIV_50.csv      (63 klaim dari 50 studi Tier 2 arXiv)
│   ├── LEMBAR_KERJA_REVIEWER_1_BATCH_E07_ARXIV_50.csv      (59 klaim dari 50 studi Tier 2 arXiv)
│   ├── LEMBAR_KERJA_REVIEWER_1_BATCH_E08_ARXIV_50.csv      (57 klaim dari 50 studi Tier 2 arXiv)
│   ├── LEMBAR_KERJA_REVIEWER_1_BATCH_E09_ARXIV_56.csv      (66 klaim dari 56 studi Tier 2 arXiv)
│   └── R1_BATCH_E05_EXTENDED_39_ROWS.csv                   (Versi ekspansi 39 klaim E05 pasca-split klaim)
├── raw_reviewer_2_i_komang_setia_buana/
│   ├── LEMBAR_KERJA_REVIEWER_2_BATCH_E01_TIER1_50.csv      (57 klaim dari 50 studi Tier 1)
│   ├── LEMBAR_KERJA_REVIEWER_2_BATCH_E02_TIER1_50.csv      (57 klaim dari 50 studi Tier 1)
│   ├── LEMBAR_KERJA_REVIEWER_2_BATCH_E03_TIER1_50.csv      (54 klaim dari 50 studi Tier 1)
│   ├── LEMBAR_KERJA_REVIEWER_2_BATCH_E04_TIER1_62.csv      (71 klaim dari 62 studi Tier 1)
│   ├── LEMBAR_KERJA_REVIEWER_2_BATCH_E05_PILOT_24.csv      (31 klaim dari 24 studi Pilot Tier 2)
│   ├── LEMBAR_KERJA_REVIEWER_2_BATCH_E06_ARXIV_50.csv      (58 klaim dari 50 studi Tier 2 arXiv)
│   ├── LEMBAR_KERJA_REVIEWER_2_BATCH_E07_ARXIV_50.csv      (58 klaim dari 50 studi Tier 2 arXiv)
│   ├── LEMBAR_KERJA_REVIEWER_2_BATCH_E08_ARXIV_50.csv      (58 klaim dari 50 studi Tier 2 arXiv)
│   └── LEMBAR_KERJA_REVIEWER_2_BATCH_E09_ARXIV_56.csv      (64 klaim dari 56 studi Tier 2 arXiv)
├── batch_adjudication_masters/
│   ├── MASTER_ADJUDIKASI_STAGE3_BATCH_E01_TIER1_50.csv     (62 klaim teradjudikasi)
│   ├── MASTER_ADJUDIKASI_STAGE3_BATCH_E02_TIER1_50.csv     (65 klaim teradjudikasi)
│   ├── MASTER_ADJUDIKASI_STAGE3_BATCH_E03_TIER1_50.csv     (60 klaim teradjudikasi)
│   ├── MASTER_ADJUDIKASI_STAGE3_BATCH_E04_TIER1_62.csv     (84 klaim teradjudikasi)
│   ├── REKONSILIASI_ADJUDIKASI_STAGE3_BATCH_E05_PILOT_24.csv (31 klaim; +8 split E05 = 39 di claims.csv)
│   ├── MASTER_ADJUDIKASI_STAGE3_BATCH_E06_ARXIV_50.csv     (68 klaim teradjudikasi)
│   ├── MASTER_ADJUDIKASI_STAGE3_BATCH_E07_ARXIV_50.csv     (67 klaim teradjudikasi)
│   ├── MASTER_ADJUDIKASI_STAGE3_BATCH_E08_ARXIV_50.csv     (65 klaim teradjudikasi)
│   └── MASTER_ADJUDIKASI_STAGE3_BATCH_E09_ARXIV_56.csv     (74 klaim teradjudikasi)
├── scripts/
│   └── compute_stage3_irr_agreement.py                     (Skrip perhitungan IRR mandiri untuk Aturan 1, 2, 3A, 3B, 3C)
└── results/
    ├── stage3_irr_by_method.csv                            (Ringkasan Po, Cohen's kappa, dan Gwet's AC1 lintas 4 aturan)
    ├── stage3_irr_by_batch.csv                             (Rincian kesepakatan per batch E01–E09)
    └── stage3_study_and_claim_alignment_442.csv            (Daftar penyelarasan 442 studi antara R1 dan R2)
```

---

## 3. Penjelasan Metodologis: Bagaimana 533 Klaim (R1) dan 508 Klaim (R2) Dipetakan ke 442 Studi dan 474/584 Klaim

### 3.1 Struktur Multiplisitas Klaim per Studi ($N = 442$ Studi Kanonik)
Setiap lembar kerja *batch* (`BATCH_E01` s.d. `BATCH_E09`) diinisialisasi dengan tepat **1 baris klaim dasar (*seed row*, `index 0`)** untuk masing-masing dari **442 studi kanonik** (`50 + 50 + 50 + 62 + 24 + 50 + 50 + 50 + 56 = 442`). Ketika sebuah studi melaporkan lebih dari satu mekanisme atau klaim jaminan keamanan yang terpisah, masing-masing reviewer menambahkan baris klaim sekunder/tersier (`-02`, `-03`, atau `-B`) dengan `Source_Record_ID` yang sama.

Distribusi pasangan jumlah klaim $(n_{R1}, n_{R2})$ per studi lintas **442 studi kanonik** adalah:
- **$(1, 1)$ = 319 studi (`72,17%`)**: R1 dan R2 sama-sama mengekstraksi tepat 1 klaim (`319` klaim R1 vs `319` klaim R2).
- **$(2, 2)$ = 29 studi (`6,56%`)**: R1 dan R2 sama-sama mengekstraksi 2 klaim (`58` klaim R1 vs `58` klaim R2).
- **$(3, 3)$ = 1 studi (`0,23%`)**: R1 dan R2 sama-sama mengekstraksi 3 klaim (`3` klaim R1 vs `3` klaim R2).
- **$(2, 1)$ = 58 studi (`13,12%`)**: R1 memecah ekstraksi menjadi 2 klaim (`116` klaim), sedangkan R2 mengonsolidasikannya ke dalam 1 klaim utama (`58` klaim).
- **$(1, 2)$ = 34 studi (`7,69%`)**: R2 memecah ekstraksi menjadi 2 klaim (`68` klaim), sedangkan R1 mengonsolidasikannya ke dalam 1 klaim utama (`34` klaim).
- **$(3, 2)$ = 1 studi (`0,23%`)**: R1 mengekstraksi 3 klaim dan R2 mengekstraksi 2 klaim.

Dengan demikian:
- **Kesepakatan Eksak Jumlah Klaim per Studi (*Exact Claim-Count Agreement*, $N = 442$)**: **`349 / 442` studi (`78,96%`, $\kappa = 0,2752$, $AC_1 = 0,7541$)** memiliki jumlah klaim yang identik antara R1 dan R2 (`319 + 29 + 1 = 349`), dan **`350 / 442` studi (`79,19%`, $\kappa = 0,2803$, $AC_1 = 0,7078$)** sepakat pada dikotomi biner *single-claim* (`1`) vs *multi-claim* (`>1`).
- **Jumlah Pasangan Klaim Bersama ($\sum \min(n_{R1}, n_{R2})$)**: **`474` pasangan klaim** (`319×1 + 58×1 + 34×1 + 29×2 + 1×2 + 1×3 = 474`).
- **Klaim Komplementer Reviewer Tunggal**: Terdapat `533 - 474 = 59` baris klaim sekunder tambahan dari R1 (pada 59 studi) dan `508 - 474 = 34` baris klaim sekunder tambahan dari R2 (pada 34 studi), ditambah `8` klaim hasil pemecahan (*claim splitting*) selama rekonsiliasi `BATCH_E05` (`R1_BATCH_E05_EXTENDED_39_ROWS.csv`), yang membentuk populasi gabungan **`474 + 59 + 34 + 8 + 9 (split adjudikasi Tier 1/2) = 584` klaim** pada `data/claims.csv`.

---

### 3.2 Empat Aturan Perhitungan yang Dibandingkan dalam Skrip Ini

| Kode Aturan | Unit Analisis | Ukuran Sampel ($N$) | Definisi Aturan Pemasangan / Penggabungan | Kapan Digunakan / Interpretasi Metodologis |
| :--- | :--- | :---: | :--- | :--- |
| **Aturan 1 (`Rule 1`)** | **Tingkat Studi (*Primary-Claim Study-Level*)** | **$N = 442$ studi** | Membandingkan **klaim pertama/utama (`index 0`)** dari R1 dan R2 pada setiap `Source_Record_ID` (baris *seed* kanonik 442 studi). | Merupakan aturan yang digunakan pada tabel $N=442$ sebelumnya. Harus disebut secara spesifik sebagai **kesepakatan pengodean klaim utama tingkat studi (*primary-claim study-level agreement*)**. |
| **Aturan 2 (`Rule 2`)** | **Tingkat Studi (*Union / Aggregated Study-Level*)** | **$N = 442$ studi** | Menggabungkan seluruh klaim R1 pada studi $s$ ($1\text{–}3$ klaim) dan seluruh klaim R2 pada studi $s$ ($1\text{–}3$ klaim) menjadi satu profil studi: *union* batas kepercayaan (`B1`–`B4`), *union* limitasi (`AD/DG/UG`), bukti formal tertinggi (`Formal_Evidence_Type`), maturitas tertinggi (`Implementation_Maturity`), status dukungan paling konservatif, dan tahap PQC tertinggi. | Mengukur **kesepakatan karakteristik studi secara utuh (*whole-study aggregated agreement*)** tanpa membuang informasi dari klaim sekunder ketika salah satu reviewer memecah klaim. |
| **Aturan 3A (`Rule 3A`)** | **Tingkat Klaim & Studi Murni (*1-to-1 Single-Claim Subset*)** | **$N = 319$ klaim/studi** | Hanya menyertakan `319` studi di mana R1 dan R2 sama-sama mengekstraksi tepat 1 klaim ($n_{R1} = n_{R2} = 1$). | Memberikan tolok ukur **kesepakatan tingkat klaim murni tanpa bias multiplisitas atau aturan pemasangan**. |
| **Aturan 3B / 3C (`Rule 3B / 3C`)** | **Tingkat Klaim Terpasangkan (*Paired Claim-Level*)** | **$N = 474$ pasangan klaim** | Memasangkan seluruh $\min(n_{R1}, n_{R2}) = 474$ klaim yang bersesuaian lintas 442 studi menggunakan urutan indeks (`3B`) atau **pencocokan bipartit skor kesamaan maksimum (`3C`)** pada atribut `Claim_Category`, `Target_Boundary`, `Lifecycle_Stage`, dan `Formal_Evidence_Type`. | Mengukur **kesepakatan tingkat klaim (*paired claim-level agreement*)** atas seluruh 474 klaim yang sama-sama diidentifikasi oleh kedua reviewer. |

---

## 4. Ringkasan Hasil Perbandingan Lintas Keempat Aturan

| Dimensi Ekstraksi | Aturan 1: Klaim Utama / Studi ($N=442$) | Aturan 2: Gabungan Semua Klaim / Studi ($N=442$) | Aturan 3A: Klaim 1-ke-1 Murni ($N=319$) | Aturan 3C: Klaim Terpasangkan Bipartit ($N=474$) |
| :--- | :---: | :---: | :---: | :---: |
| **`Source_PDF_SHA256` & `Source_Record_ID`** | `442/442` (`100,0%`, $\kappa=1,000$, $AC_1=1,000$) | `442/442` (`100,0%`, $\kappa=1,000$, $AC_1=1,000$) | `319/319` (`100,0%`, $\kappa=1,000$, $AC_1=1,000$) | `474/474` (`100,0%`, $\kappa=1,000$, $AC_1=1,000$) |
| **`PQC_Migration_Stage` (Biner: `Stage 0/ND` vs `Stage 1–5`)** | `431/442` (`97,5%`, $\kappa=0,732$, $AC_1=0,973$) | `431/442` (`97,5%`, $\kappa=0,732$, $AC_1=0,973$) | `315/319` (`98,7%`, $\kappa=0,812$, $AC_1=0,987$) | `459/474` (`96,8%`, $\kappa=0,691$, $AC_1=0,965$) |
| **`Strict_Formal_Proof` (Biner: Bukti Formal Ketat vs Lainnya)** | `418/442` (`94,6%`, $\kappa=0,450$, $AC_1=0,940$) | `417/442` (`94,3%`, $\kappa=0,439$, $AC_1=0,937$) | `305/319` (`95,6%`, $\kappa=0,395$, $AC_1=0,953$) | `448/474` (`94,5%`, $\kappa=0,430$, $AC_1=0,939$) |
| **Kehadiran Limitasi `AD` (Biner: `AD` vs `Non-AD`)** | `396/442` (`89,6%`, $\kappa=0,068$, $AC_1=0,883$) | `397/442` (`89,8%`, $\kappa=0,070$, $AC_1=0,886$) | `283/319` (`88,7%`, $\kappa=0,084$, $AC_1=0,872$) | `423/474` (`89,2%`, $\kappa=0,144$, $AC_1=0,878$) |
| **`Target_Boundary` (Biner: `MULTI` vs `SINGLE`)** | `387/442` (`87,6%`, $\kappa=0,363$, $AC_1=0,845$) | `389/442` (`88,0%`, $\kappa=0,338$, $AC_1=0,854$) | `280/319` (`87,8%`, $\kappa=0,350$, $AC_1=0,849$) | `413/474` (`87,1%`, $\kappa=0,467$, $AC_1=0,830$) |
| **`Target_Boundary` (5 Kelas: `MULTI`, `B1`–`B4`)** | `385/442` (`87,1%`, $\kappa=0,367$, $AC_1=0,864$) | `387/442` (`87,6%`, $\kappa=0,338$, $AC_1=0,869$) | `279/319` (`87,5%`, $\kappa=0,358$, $AC_1=0,868$) | `406/474` (`85,7%`, $\kappa=0,436$, $AC_1=0,847$) |
| **`Claim_Support_Status` (3 Kelas)** | `367/442` (`83,0%`, $\kappa=0,288$, $AC_1=0,807$) | `358/442` (`81,0%`, $\kappa=0,263$, $AC_1=0,792$) | `260/319` (`81,5%`, $\kappa=0,291$, $AC_1=0,787$) | `395/474` (`83,3%`, $\kappa=0,297$, $AC_1=0,811$) |
| **Jumlah Klaim per Studi Eksak (`1` vs `2` vs `3`)** | `349/442` (`79,0%`, $\kappa=0,275$, $AC_1=0,754$) | `349/442` (`79,0%`, $\kappa=0,275$, $AC_1=0,754$) | `319/319` (`100,0%`, $\kappa=1,000$, $AC_1=1,000$) | N/A (metrik multiplisitas tingkat studi) |
| **`Claim_Category` (6 Kelas)** | `320/442` (`72,4%`, $\kappa=0,583$, $AC_1=0,682$) | `247/442` (`55,9%`, $\kappa=0,430$, $AC_1=0,538$)* | `229/319` (`71,8%`, $\kappa=0,599$, $AC_1=0,672$) | `341/474` (`71,9%`, $\kappa=0,588$, $AC_1=0,675$) |
| **Kehadiran Limitasi `DG` (Biner: `DG` vs `Non-DG`)** | `297/442` (`67,2%`, $\kappa=0,170$, $AC_1=0,458$) | `278/442` (`62,9%`, $\kappa=0,169$, $AC_1=0,336$) | `212/319` (`66,5%`, $\kappa=0,141$, $AC_1=0,432$) | `318/474` (`67,1%`, $\kappa=0,188$, $AC_1=0,448$) |
| **`PQC_Migration_Stage` (7 Kelas Eksak)** | `249/442` (`56,3%`, $\kappa=0,100$, $AC_1=0,532$) | `248/442` (`56,1%`, $\kappa=0,099$, $AC_1=0,530$) | `185/319` (`58,0%`, $\kappa=0,082$, $AC_1=0,546$) | `272/474` (`57,4%`, $\kappa=0,109$, $AC_1=0,543$) |
| **`Lifecycle_Stage` (9 Kelas)** | `230/442` (`52,0%`, $\kappa=0,336$, $AC_1=0,475$) | `222/442` (`50,2%`, $\kappa=0,332$, $AC_1=0,487$)* | `171/319` (`53,6%`, $\kappa=0,357$, $AC_1=0,491$) | `251/474` (`53,0%`, $\kappa=0,349$, $AC_1=0,485$) |
| **`Formal_Evidence_Type` (7 Kelas)** | `230/442` (`52,0%`, $\kappa=0,358$, $AC_1=0,452$) | `228/442` (`51,6%`, $\kappa=0,354$, $AC_1=0,447$) | `163/319` (`51,1%`, $\kappa=0,326$, $AC_1=0,444$) | `247/474` (`52,1%`, $\kappa=0,356$, $AC_1=0,453$) |
| **`Implementation_Maturity` (5 Kelas)** | `230/442` (`52,0%`, $\kappa=0,290$, $AC_1=0,473$) | `230/442` (`52,0%`, $\kappa=0,290$, $AC_1=0,473$) | `175/319` (`54,9%`, $\kappa=0,346$, $AC_1=0,493$) | `242/474` (`51,1%`, $\kappa=0,278$, $AC_1=0,462$) |

*\*Catatan pada Aturan 2 untuk `Claim_Category` dan `Lifecycle_Stage`*: karena Aturan 2 menggabungkan himpunan kategori lintas seluruh klaim dalam satu studi (mis. `C2;C5` jika sebuah studi memiliki 2 klaim dengan kategori berbeda), kesepakatan himpunan eksak pada studi multi-klaim secara mekanis lebih rendah bila salah satu reviewer hanya mengekstraksi 1 klaim (`C2`) sementara reviewer lainnya mengekstraksi 2 klaim (`C2;C5`). Untuk dimensi spesifik klaim (`Claim_Category` dan `Lifecycle_Stage`), **Aturan 1 ($N=442$), Aturan 3A ($N=319$), dan Aturan 3C ($N=474$)** memberikan ukuran kesepakatan yang jauh lebih tepat dan konsisten (`71,8%–72,4%` dengan $\kappa = 0,583\text{–}0,599$ untuk `Claim_Category`; `52,0%–53,6%` dengan $\kappa = 0,336\text{–}0,357$ untuk `Lifecycle_Stage`).

---

## 5. Cara Menjalankan Ulang Skrip

```bash
unzip stage3_r1_r2_raw_worksheets_and_irr_package.zip
cd stage3_r1_r2_raw_worksheets_and_irr_package
python3 scripts/compute_stage3_irr_agreement.py
```
