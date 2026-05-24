# Project Structure

This file provides a short overview of the folder structure and the individual
files included in the project. Since the folders could not be uploaded
separately, all project materials were placed together. The present file is
therefore intended as a structural metadata guide that explains where each part
of the workflow is documented and what can be found in the respective files.

---

## 1. Raw Data

### `textmessages.xlsx`
This file contains the raw data of the project. It includes the collected text
messages that form the basis of the normalization experiment. The file
represents the starting point of the workflow before further annotation,
normalization, and lexicon extraction were carried out.

---

## 2. Processed Data

### `mapping_dictionary.py`
This file contains the processed mapping dictionary resource used for the final
normalization pipeline. It represents the cleaned and finalized version of the
mapping correspondences used by the rule-based system.

### `multiword_mapping.xlsx`
This file contains the multi-word mapping entries. These are phrase-level or
collocational correspondences that must be treated together during the
normalization process. They are separated from the single-word mappings because
they need to be applied first in the rule-based pipeline.

### `singleword_mapping.xlsx`
This file contains the single-word mapping entries. These entries represent
token-level correspondences between Kosovo-Albanian forms and codified Standard
Albanian forms.

### `textmessages_spreadsheet_.xlsx`
This spreadsheet also contains the annotation-related work carried out during the
project. In addition to the raw messages, it documents normalization decisions,
change annotations, comments, and more general coding of the data. It therefore
serves not only as the data source, but also as a core documentation file for
the manual linguistic processing stages of the project.

### `readme.md`
This file contains the main project write-up. It documents the overall project
idea, methodological procedure, implementation logic, evaluation design,
results, limitations, reflection, references, and AI log. In this sense, it
serves as the main descriptive and report-like document of the project.

---

## 3. Results

### `normalization_results.xlsx`
This file contains the output of the rule-based normalizer on the held-out test
data. It includes the formatted system output and the corresponding evaluation
information. The file therefore provides the basis for interpreting the results
of the pilot normalization experiment.

---

## 4. Scripts

### `gold_data.xlsx`
This file contains the gold normalized reference data used for evaluation. It is
read by the normalization script in order to compare the system output against
the manually verified target normalization.

### `normalizer.py`
This is the main Python script of the project. It implements the rule-based
normalization pipeline and performs the comparison between automatic system
output and gold normalized reference data.

### `mapping_dictionary.py`
This file contains the Python dictionaries used by the normalization script. It
includes both the single-word and multi-word mappings that form the core
lexical resource of the rule-based baseline.

### `test_data.xlsx`
This file contains the held-out test data used as input for the normalization
script. Together with `gold_data.xlsx`, it allows the normalization pipeline to
be run and evaluated.

---

## 5. General Note

Taken together, these files document the full project workflow, from raw data
collection and manual annotation to lexicon construction, Python-based
normalization, and final evaluation. Because all files had to be stored in one
place rather than in separate folders, this structure file is intended to make
the organization of the materials easier to understand and navigate.
