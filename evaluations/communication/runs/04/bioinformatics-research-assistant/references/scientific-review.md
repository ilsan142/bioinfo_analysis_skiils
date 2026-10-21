# Scientific review for the current situation

Read only the sections needed for the present decision. These are conditional decision rules, not a fixed pipeline or a checklist to recite for every analysis. Set numerical thresholds from experimental and methodological evidence or prior criteria, not as universal defaults.

## Input meaning and preprocessing

Check how values were generated, their processing stage, units, and prior transformations. Integer status is diagnostic information, not proof of a measurement type. Decimals may be normalized values or estimated counts from probabilistic read assignment. Do not round values or reconstruct supposed raw data merely to run a count model. For estimated counts, check import routes and offsets supported by the quantification tool and analysis method. DESeq2 documents count inputs and transcript-quantification imports separately. [DESeq2 documentation](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html)

Determine whether missingness means unmeasured data, a detection limit, technical failure, or filtering, and whether zero means absence, nondetection, or a reference point on a transformed scale. If unknown, record possible meanings and defer imputation or tests that depend on them. Changes in relative quantities alone do not establish changes in absolute quantities or kinetic rate constants.

Connect filtering, normalization, aggregation, and imputation to the question. Record sample and feature counts and any change in units before and after processing. Assess exclusions using measurement quality, identifier errors, experimental records, and agreed criteria. Do not report only a version with inconvenient samples removed. If a consequential, reasonable alternative remains, retain the primary analysis and conduct a focused sensitivity analysis.

## Independent units and model identifiability

Distinguish assignment, sampling, and measurement units. Verify the individual-to-specimen-to-library/cell/spot relationships. Technical replicates do not automatically increase independent n. Choose aggregation, paired models, mixed models, or other approaches appropriate to the biological comparison after establishing dependence. Report n with its unit.

State the effect of interest before fitting a model. A mean change before and after treatment in the same patients differs from a comparison between different patient groups. Check contrast direction, reference levels, covariates, and paired or nested terms in the actual design matrix and code.

Inspect the condition-by-batch table and independence of design-matrix columns. With complete confounding, an observed group difference may be described, but it cannot be attributed uniquely to condition. Dropping a term or obtaining numbers from a pseudoinverse or integration algorithm does not separate the effects. Explain whether an identifiable comparison or additional samples crossing conditions and batches are needed. DESeq2's “Model matrix not full rank” section covers linear dependence and batch/condition confounding. [DESeq2 documentation](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html)

## Effects, uncertainty, and exploration

Where possible, state the comparison direction, effect and units, confidence interval or another justified uncertainty summary, and independent n. Do not hide low precision at small n. Descriptive summaries and an explanation of why inference is unavailable may be more appropriate than a test. Do not invent p-values.

For multiple testing, record which features and contrasts form the testing family and how correction was applied. Testing after selection, repeated exploration, and changing thresholds after seeing results affect uncertainty interpretation. Nonsignificance does not establish no effect. Claims of no effect or equivalence require an appropriate design, precision, and criteria.

Separate initial choices from later revisions. State whether a revision corrects an error, incorporates new experimental information, or explores a new hypothesis. Keep observations, candidate explanations, and further validation distinct. Enrichment depends on the background set, identifier mapping and duplication, and feature-selection process; it does not prove a mechanism.

## Prediction models

Define whether the target is new individuals, institutions, studies, time periods, or sequence groups. Inspect the split manifest for overlap at the relevant level. Consider chronological separation for future prediction and homology or similarity groups for related sequences. Do not default to random row splits.

Fit learned imputation, scaling, feature selection, and dimension reduction within each training fold. Use validation folds only for transformation and evaluation. Tune and select models using internal validation on the training side, and do not repeatedly reuse the final holdout for selection. Resplitting already selected features does not undo selection on the full dataset; rebuild from the original feature set. Scikit-learn documents feature-selection leakage and separation using a Pipeline. [Official common pitfalls guide](https://scikit-learn.org/stable/common_pitfalls.html)

Choose splits, baseline models, metrics, and uncertainty measures that match the generalization unit. Improved performance supports prediction within the evaluated scope; it is distinct from validation of mechanism or clinical utility.

## Additional checks by data type

| Context | Concrete checks | Interpretation boundary |
| --- | --- | --- |
| Bulk RNA-seq | Count generation or estimation, prior normalization, composition and library size, annotation, comparison design | Do not treat TPM or log values as raw counts. Do not equate abundance with degradation rate or translation. |
| Single-cell | Donor-to-cell mapping, condition and cell-type counts per donor, QC and doublet evidence, original counts versus integrated embeddings | Do not count cells as independent donors. Consider pseudobulk or mixed models according to the design and inputs; many cells cannot replace missing donor replication. |
| Spatial | Donor-to-section-to-spot/cell hierarchy, coordinates and resolution, neighboring dependence and tissue composition | Do not treat neighboring spots as independent biological replicates or spatial co-occurrence as proof of interaction. |
| Genomic variants | Genome build, REF/ALT and strand, sample and ploidy, coverage and callability, genotype QC, ancestry and kinship | Do not convert missing calls to reference alleles. Candidate pathogenic annotations are not validated functional effects. |
| Microbiome | Counts versus relative abundance, contamination and negative controls, sampling depth, composition, repeated sampling, taxonomic reference | Increased proportion does not establish increased absolute microbial abundance. Do not interpret every zero as absence. |
| Biological prediction | Target population, splitting unit, fit scope of feature selection and preprocessing, label generation and measurement | Do not present label leakage or study/institution discrimination as the intended biological prediction capability. |

Dependence among cells from the same individual can cause pseudoreplication. Choose a response appropriate to the design and goal rather than declaring one model universally correct for single-cell analysis. [Zimmerman et al., 2021, original paper](https://www.nature.com/articles/s41467-021-21038-1)

## Annotation and evidence for claims

Check identifier species, reference version, and namespace. Record input counts, mapping successes and failures, one-to-many and many-to-one relationships, and resolution rules. Do not silently collapse identifiers to a convenient symbol. Consider whether tissue or cell composition, time, species, or measurement bias changes the interpretation.

Use official documentation or original papers that were actually opened and checked. Connect each claim to its source and relevant version or access date. Separate literature findings from observations and interpretations in the current analysis. Mark inaccessible evidence as unverified.

The linked sources were checked on 2026-10-17 and support the specific claims attached to them. The remaining table entries are review rules for this skill, not a literature review validating every domain method. Check sources appropriate to the conditions of each actual analysis before making specific methodological or biological claims.
