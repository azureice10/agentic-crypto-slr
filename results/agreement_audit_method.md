# Arithmetic audit of the author-supplied Stage 3 summary

> **Pembaruan setelah paket mentah diterima:** uraian di bawah merekam tahap awal audit dan bukan status terkini. Data mentah, aturan klaim pertama, serta skrip kini telah diperiksa dan direproduksi. PQC yang benar adalah 431/442; koefisien support sebelumnya ternyata memakai tiga label. Lihat [laporan reproduksi terbaru](../results/stage3_irr_reproduction_report.md). Penulis kemudian menegaskan bahwa Herman sudah memeriksa/mengesahkan berkas sebelum adjudikasi; catatan pengesahan masih dicari. Label AI-draft/UNASSIGNED adalah metadata historis, bukan dasar menyatakan review manusia tidak berlangsung.

This audit asks a narrow question: can any complete, unweighted binary table with N = 442 and the stated exact-match count yield the reported rounded coefficients? It does not reconstruct the real reviewer table.

For cells (a,b,c,d), with a+d = A and b+c = N−A:

```
Po = (a+d)/N
p1 = (a+b)/N
p2 = (a+c)/N
pbar = (p1+p2)/2
Pe_kappa = p1*p2 + (1-p1)*(1-p2)
Pe_AC1 = 2*pbar*(1-pbar)
kappa = (Po-Pe_kappa)/(1-Pe_kappa)
AC1 = (Po-Pe_AC1)/(1-Pe_AC1)
```

The script enumerates a = 0…A and b = 0…N−A, derives c,d and compares each coefficient rounded to four decimals. Definitions follow the conventional two-rater binary coefficients; see [Gwet's original methodological paper](https://doi.org/10.1348/000711006X126600). Missing-data exclusions, different denominators, weights, category counts, batch averaging or coefficients computed before a recoding would represent a different calculation and need to be documented.

| Dimension | Exact matches | Reported κ / AC1 | Compatible binary tables |
|---|---:|---|---:|
| Grouped PQC | 427/442 | .6399 / .9654 | 0 |
| AD incidence | 396/442 | .0681 / .8835 | 4 |
| Multiple/single boundary | 387/442 | .3632 / .8454 | 4 |
| Binary support | 367/442 | .2878 / .8074 | 0 |
| DG incidence | 297/442 | .1697 / .4582 | 4 |

For grouped PQC and binary support, neither coefficient individually matches any feasible table at the stated precision. Thus rounding alone does not explain the discrepancy under these assumptions. Symmetric relabelings account for compatible alternatives in other rows; the four feasible tables are not four observed datasets. Multiclass coefficients remain unchecked because marginal category counts are unavailable. All raw-agreement percentages match the supplied fractions to two decimal places.

The JSON's nearest feasible coefficient pair is a diagnostic, **not a proposed correction**. Corrected values must come from the actual raw pairs and declared calculation, never from selecting a convenient feasible table. No confidence intervals or qualitative labels such as substantial reliability are inferred from the available summary.
