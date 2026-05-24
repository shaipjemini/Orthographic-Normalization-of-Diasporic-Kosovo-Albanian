# Orthographic Normalization of Diasporic Kosovo-Albanian in Switzerland for Low-Resource NLP

## Abstract

Kosovo-Albanian is a very present language variety in Swiss society given the
demographic presence of the diaspora, yet it remains a predominantly spoken
language that has not undergone full standardization processes in terms of a
writing system. It is also important to highlight that there can be great
dialectal differences to what one might intuitively assume to be “Albanian”,
especially in a diasporic context outside its original geographic context. What
one might call Standard-Albanian can be very different from dialectal Kosovar
varieties of the language on various linguistic levels (orthography, phonology
& phonetics, morphology, lexicology, etc.). This divergence creates a problem
for NLP purposes given current language technologies rely on standardized
systems of the language, in this case, codified Standard Albanian, which raises
a question of adequacy and representation given the lack of data for the
variety at hand.

The project therefore aims to create a small normalization pipeline that maps
non-standard written Kosovo-Albanian forms onto codified Standard Albanian. To
do so, a manually curated pilot dataset of informal text messages was compiled,
normalized, and manually annotated for change tokens and types. Based on these
annotations, a mapping lexicon of single-word and multi-word correspondences
was created and implemented in a rule-based Python normalizer script. The
system was then evaluated on held-out test data by comparing automatic system
outputs to manually verified gold normalizations. The present document outlines
the methodological procedure, summarizes the implemented workflow, and provides
a structured skeleton for the final report and later result interpretation.

---

## 1. Problem Identification and General Idea

The project addresses the question of how informal written Kosovo-Albanian in
the Swiss diaspora can be made more computationally accessible for NLP
purposes without erasing the original linguistic form. Especially in the speech
and writing of younger heritage speakers of Kosovo Albanian who neither
received formal education in the Standard variety nor were born in the country,
written forms of the language may diverge substantially from codified Standard
Albanian. Rather than treating non-standard forms as mere errors, the project
assumes that they represent a meaningful and underrepresented language variety.
The purpose of orthographic normalization in this context is therefore not
corrective in a prescriptive sense, but rather translational in a computational
sense: a standard-aligned version is created in parallel so that downstream NLP
tools can work more effectively with the data.

The project is conceived as a pilot study. It does not attempt to model the
full complexity of Kosovo-Albanian variation, nor does it propose a full-scale
machine learning architecture. Instead, it develops a small manually curated
normalization resource and a rule-based baseline prototype. As such, the
project constitutes a first exploratory attempt to address this underrepresented
low-resource variety computationally and, at the same time, lays the groundwork
for a wider range of future research on normalization, corpus building, and
downstream NLP applications.

---

## 2. Methodological Procedure

### 2.1 Overview

The project followed a stepwise pipeline beginning with data collection and
ending with rule-based normalization and evaluation. The central logic of the
project can be summarized as follows:

1. Collect informal written Kosovo-Albanian messages from speakers that meet
   the criteria in terms of the aspired sociolinguistic profile.
2. Create normalized Standard Albanian equivalents and split into training and
   test data sets.
3. Manually annotate the changes between original and normalized forms in the
   training data.
4. Derive a mapping lexicon from these changes.
5. Implement a rule-based normalizer in Python.
6. Test the system on unseen data (i.e., the test data set).
7. Compare system output against manually curated gold normalizations.

### 2.2 Data Collection

The first step consisted of assembling a small pilot dataset of informal
written Kosovo-Albanian messages. The data mainly consisted of short WhatsApp
text messages, produced in diasporic contexts in Switzerland. The emphasis was
placed on naturally occurring, colloquial written forms rather than polished
written Albanian.

The resulting dataset was structured so that each row represented one
analyzable item, typically one short message or one short utterance. The
project prioritized practical usability over large-scale corpus design. At this
pilot stage, the goal was not full sociolinguistic representativeness, but
rather the construction of a manageable dataset containing enough recurring
variation to support a first normalization experiment. 

As part of the preprocessing procedure, all emojis had already been removed from
the raw data spreadsheet before annotation and normalization.

### 2.3 Participants

The participant profile had to be defined somewhat differently from the initial
idea. While the original plan had been to capture a broader age range across
multiple generations, this proved difficult in practice given the historical
conditions of Albanian-speaking migration to Switzerland and the small scale of
the present pilot study. The final participant criteria therefore focused on
speakers who were born in Switzerland and had not received formal education in
codified Standard Albanian.

With regard to age and sex, the study aimed for a roughly balanced distribution,
although such balance can only be interpreted cautiously in a dataset of five
participants. The age of the participants ranged from 14 to 29. All speakers
can be described as more dominant in Swiss German or German than in their
heritage language across most linguistic domains, which is relevant for
understanding the orthographic and lexical variability found in the collected
messages.

### 2.4 Manual Normalization

In the second step, each original message was manually paired with a normalized
version in codified Standard Albanian with the help of LLMs (ChatGPT, 2026).
This normalization was carried out conservatively: the intention was to
preserve the original meaning while adjusting the form toward the codified
written standard. The aim was not to freely paraphrase the data, but to create
a standard-aligned reference version that could function as a gold target for
later evaluation. All AI-generated translation versions were manually checked
and adjusted by the author.

This step effectively created a small parallel normalization dataset with two
aligned columns:

- original non-standard Kosovo-Albanian text
- manually normalized Standard Albanian text

These manually verified normalized forms constitute the gold reference for the
later evaluation of the system output.

### 2.5 Annotation of Change Types

Once the normalized versions had been established, the changes between original
and normalized text were annotated manually. The purpose of this stage was to
make the normalization process transparent and to identify recurring patterns
of variation. Each row was therefore examined for the lexical, orthographic, or
morphological material that had changed.

The annotation process focused on extracting the concrete items that differed
between the original and normalized versions. These change items later served
as the basis for a mapping lexicon. In other words, this stage transformed the
manually curated normalization dataset into a more explicit resource of
recurrent form correspondences.

### 2.6 Construction of the Mapping Lexicon

Based on the annotated change column, a mapping lexicon was created. This
lexicon captured recurrent form correspondences from Kosovo-Albanian to
codified Standard Albanian. Two mapping categories were distinguished:

- **single-word mappings**: one source token corresponds to one standard target
  token
- **multi-word mappings**: short phrase-level units or collocations that need
  to be treated together

This distinction was necessary because phrase-level correspondences would
otherwise be broken if single-word mappings were applied first. This decision
was proposed by ChatGPT during the implementation phase. The final lexicon
therefore consisted of two manually curated dictionaries:

- `single_word_mapping`
- `multi_word_mapping`

These dictionaries formed the core resource for the rule-based prototype.
Ambiguous or uncertain cases were not considered for the final analysis.
Instances of code-switching between Kosovo-Albanian and Swiss German dialects
were not considered. In total, the dictionaries together consist of 148 change
type entries.

### 2.7 Train / Test Logic

To maintain a basic evaluation logic, the dataset was divided into
developmentally distinct subsets. The training portion was used to establish
the normalization correspondences and to derive the mapping lexicon. A held-out
test set was reserved for the final evaluation.

The important methodological principle here is that the test data were not used
to construct the mapping lexicon. This allowed the final evaluation to be
carried out on unseen instances, thereby making the pilot study more
methodologically defensible.

### 2.8 Rule-Based Python Implementation

The prototype was implemented as a rule-based Python normalizer. The system
takes original test messages as input and produces normalized system output.
The skeleton code and hyperparameters were generated by ChatGPT. The main
processing steps are:

1. Load test data.
2. Load gold normalized reference data.
3. Load the manually curated mapping dictionaries.
4. Apply multi-word mappings first.
5. Apply single-word mappings second.
6. Return a normalized output.
7. Compare system output to the gold normalized reference.

This design was chosen because it is transparent, interpretable, and
appropriate for a pilot project in a low-resource setting. Rather than training
a statistically or neurally complex model, the project deliberately prioritizes
explicit linguistic correspondences and manual interpretability given the lack
of labelled data and linguistic description from the variety.

### 2.9 Evaluation Design

The system was evaluated by comparing automatic outputs against manually
verified gold normalizations on a held-out test set. Evaluation was designed to
be case-insensitive and punctuation-insensitive, since the data consisted of
colloquial text messages and punctuation practices in such data are highly
variable.

Two principal evaluation measures were used:

- **Sentence exact match**: whether the full normalized system output matches
  the gold normalized reference once case and punctuation are ignored (0 = not
  (entirely) exact match, 1 = exact match)
- **Word Error Rate (WER)**: the word-level edit distance between system output
  and gold reference, normalized by gold length

This combination allows both a strict metric (exact sentence match) and a more
graded metric (WER). In addition, the resulting outputs can be inspected
qualitatively in order to identify systematic error types such as:

- missing lexicon item
- ambiguous lexical mapping
- insufficient handling of morphology
- context-sensitive cases not captured by the rule-based baseline

---

## 3. Results & Analysis

The rule-based normalization system was evaluated on a held-out test set of 20
items. Under case-insensitive and punctuation-insensitive evaluation, the
system achieved an exact sentence match rate of 15.0% (3/20 items). The average
Word Error Rate (WER) was 0.365, with a median WER of 0.343. These results
suggest that the prototype was able to capture some recurring normalization
correspondences, but overall performance remained limited, indicating that a
purely rule-based baseline is only partially sufficient for the variability
found in informal written Kosovo-Albanian diasporic text.

Descriptive stats:

- 20 test items
- 3/20 exact matches
- Exact match rate: 15.0%
- Average WER: 0.365
- Median WER: 0.343

---

The relatively low exact match rate indicates that full-sentence normalization
is difficult to achieve with a small manually curated mapping lexicon alone. At
the same time, the WER results suggest that the system often moved outputs in
the right direction, even when it did not fully reproduce the gold
normalization. This points to the usefulness of the lexicon-based approach as a
first proof of concept, while also showing that a small rule-based baseline can
only capture part of the variability present in informal written
Kosovo-Albanian.

One major challenge concerned clitic constructions and other cases in which a
single surface form in Kosovo-Albanian corresponds to a multi-word form in
codified Standard Albanian. These cases are difficult for a simple token-based
dictionary because they involve dialect-specific fusion that is not always
transparent at the orthographic level. The system also had difficulty with
inflected verb forms when these were not represented in the annotated training
data and therefore did not enter the mapping lexicon. As a result, the
prototype had only limited ability to generalize beyond the exact forms that
had been manually observed and encoded.

Further difficulties arose from code-switching and lexical borrowing,
especially from German or Swiss German, since such items do not fit neatly into
a one-to-one Kosovo-Albanian to Standard Albanian correspondence. In addition,
orthographic variability itself posed a problem, particularly where heritage
speakers use reduced or alternative graphemic representations that diverge from
the codified Albanian alphabet. If such forms were not present in the training
data, the system predictably performed more weakly on unseen test examples.
Taken together, these findings suggest that the current pilot baseline is
useful as an initial step, but that broader lexical coverage, more
context-sensitive rules, and a more systematic treatment of morphology,
clitics, and contact-induced forms would be necessary for stronger
normalization performance.

## 5. Limitations

This project should be framed clearly as a pilot study. The dataset is small,
manually curated, and not representative of all Kosovo-Albanian usage in
Switzerland. The normalization decisions themselves are also necessarily
selective, since codified Standard Albanian does not always stand in a simple
one-to-one relation to non-standard Kosovo-Albanian forms.

Several limitations should therefore be acknowledged:

- the dataset is small and only intended as a proof of concept
- the lexicon is manually derived and therefore limited by the observed sample
- the lexicon-rule-based approach is rather superficial in terms of pattern
  matching
- the variety lacks documentation by trained speakers/linguists
- the system is rule-based and cannot generalize beyond listed or easily
  patternable correspondences
- some source forms are inherently ambiguous and require contextual
  interpretation by experts
- evaluation remains dependent on a manually curated gold standard by a
  heritage speaker with no formal instruction in the target (Standard) language

At the same time, these limitations do not invalidate the project. On the
contrary, they are characteristic of low-resource pilot work. The main
contribution of the project lies in showing that a small, transparent
normalization pipeline can be built for an underrepresented diasporic variety
and that such a pipeline can serve as a first computational baseline for
further work.

---

## 6. What Could Be Improved in Future Work

A possible future-work section could include the following points:

- expand the dataset with more speakers and more message types
- refine the annotation scheme for change types
- aim to capture more linguistic depth: distinguish more systematically between
  orthographic, lexical, and morphological change
- add more sophisticated context-sensitive normalization rules (e.g. regex)
- compare a purely manual lexicon with semi-automatic lexicon induction
- test whether a small sequence-to-sequence model could improve on the
  rule-based baseline
- evaluate inter-annotator agreement on the normalized gold forms
- investigate whether normalization improves downstream NLP tasks such as
  search, tagging, or classification

---

## 7. Reflection

Overall, I consider the central aim of the project to have been achieved. A
first pilot normalization pipeline was developed that maps non-standard written
Kosovo-Albanian onto codified Standard Albanian and thus provides a small proof
of concept for the computational treatment of this underrepresented variety. At
the same time, the project made clear that such work is methodologically and
linguistically demanding, especially in a low-resource setting where both data
and reference materials are limited.

One important limitation concerns my own positionality in relation to the
target variety. As a heritage speaker, I have strong intuitive access to
meaning, use, and pragmatic interpretation, but I do not have formal academic
training in Standard Albanian. This means that, although the normalization
decisions were manually checked and grounded in speaker intuition, some of them
would ideally also be reviewed by a speaker or linguist with stronger formal
expertise in the codified standard. In this sense, the project should be
understood as a pilot resource rather than as a definitive normalization
standard.

With respect to the original project idea, one aspect that developed somewhat
differently in practice was the implementation strategy. Initially, it seemed
possible that the normalization system might rely more strongly on
pattern-based rules, for instance through broader regex-style generalizations.
In practice, however, I remained closer to the surface orthographic level and
relied more on explicit lexical and phrase-level mappings than on deeper formal
abstraction. This was partly a methodological choice, but it was also shaped by
the limits of my own grammatical expertise in the target standard and by the
difficulty of deciding which forms could be generalized safely and which needed
to remain context-specific. A more abstract rule system would likely require
stronger formal linguistic knowledge and more extensive validation resources
than were available in the present project.

The available resources were in general quite limited. In many cases, the work
had to proceed through a combination of speaker intuition, manual comparison,
consultation of online sources, and assisted problem-solving. In practice, this
meant relying on tools such as reference websites, including Fjalor/Fjala-type
online Albanian resources, as well as iterative external support for technical
brainstorming, debugging, and workflow design. From a computational
perspective, the implementation was therefore also a learning process: the
project did not only involve linguistic annotation and normalization, but also
the practical challenge of translating those decisions into a functioning
rule-based pipeline.

Despite these limitations, the project was particularly valuable because it
made it possible to analyze my own heritage language in a
computational-linguistic frame. This was both personally meaningful and
academically revealing. In the Swiss context, Kosovo-Albanian is highly present
socially, yet the forms that are actually spoken and written in diasporic
everyday life remain largely invisible in formal linguistic description and in
NLP. The dataset suggests that these written practices are shaped not only by
dialectal features, but also by language contact, limited access to formal
standard-language education, and a tendency to represent speech through the
orthographic habits available in the local environment, especially German or
Swiss German. In this sense, the project can also be understood as a first step
toward documenting a diasporic sociolect that is socially widespread but still
insufficiently described.

From a broader computational-linguistic perspective, the project highlights how
important small, transparent pilot studies can be for low-resource and
marginalized varieties. Even if the present system remains limited in scale and
performance, it establishes a first manually curated corpus, a normalization
baseline, and a methodological workflow that could be expanded in future work.
There is therefore clear potential for follow-up research, whether in the form
of larger corpora, more systematic linguistic annotation, expert validation of
the gold standard, or more advanced context-sensitive normalization methods.

## 9. References

- Aepli, N. and Sennrich, R. (2022). Improving Zero-Shot Cross-lingual Transfer
  Between Closely Related Languages by Injecting Character-Level Noise. In
  Findings of the Association for Computational Linguistics: ACL 2022, pages
  4074–4083, Dublin, Ireland. Association for Computational Linguistics.
- Dedvukaj, L., & Gehringer, P. (2023). Morphological and phonological origins
  of Albanian nasals and its parallels with other laws. Proceedings of the
  Linguistic Society of America, 8(1), 5508-5508.
- Dedvukaj, L., & Ndoci, R. (2023). Linguistic variation within the Northwestern
  Gheg Albanian dialect. Proceedings of the Linguistic Society of America,
  8(1), 5501-5501.
- Draçini, R., & Murati, R. (2018). Current Trends and Issues in Albanian
  Language Use. Social Research, 8(1).
- Klippenstein, R. (2010). Word-initial consonant clusters in Albanian. In
  M. Lesho, B. J. Smith, K. Campbell-Kibler, & P. W. Culicover (Eds.), Working
  Papers in Linguistics
- NIMANI, A. (2015). Unified Orthography Rules of the Albanian Language.
  International Advisory Board, 191.
- Riverin-Coutlée, J., Kapia, E., Cunha, C., & Harrington, J. (2022). Vowels in
  urban and rural Albanian: The case of the Southern Gheg dialect. Phonetica,
  79(5), 459-512.
- UCLA Phonological Segment Inventory Database. (2019). Gheg Albanian sound
  inventory (UPSID). In S. Moran & D. McCloy (Eds.), PHOIBLE 2.0. Jena: Max
  Planck Institute for the Science of Human History. (Available online at
  https://phoible.org/inventories/view/2358#tsegments, Accessed on 10.05.2026.)

## 8. AI log

Generative AI tools, in particular ChatGPT, were used in this project as
support instruments during selected stages of the workflow. Their use was
primarily limited to technical problem-solving, debugging support, workflow
brainstorming, and the generation of initial structural drafts. This included
not only early versions of the Python scripts, but also the initial structural
skeleton of the README file. The latter was produced in an AI-assisted drafting
process and then manually reviewed, analyzed, revised, and adapted by the
author in accordance with the actual project design and final written argument.

The initial gold normalization suggestions were likewise produced in a
model-assisted workflow. However, these suggestions were not adopted
uncritically. All normalized forms were manually reviewed, checked, and revised
by the researcher on the basis of intended meaning, speaker intuition, and,
where necessary, consultation of external reference materials, including online
sources such as Fjalë/Fjalor-type Albanian websites and other internet-based
resources. The final gold-standard normalizations used in the project therefore
reflect manual verification and researcher judgment rather than automatic
output alone.

The annotation of the dataset, including the identification of change types,
was carried out manually by the researcher. This was done in order to minimize
errors, identify typos, account for code-switching and contact-induced forms,
and ensure closer control over the linguistic decisions entering the mapping
lexicon. Likewise, all lexicon entries, normalization correspondences, and
final evaluation-relevant materials were manually checked before use in the
rule-based pipeline.

More generally, AI-generated material was treated as provisional support rather
than final content. Suggestions, code drafts, structural templates, and README
skeletons produced with ChatGPT were critically reviewed, substantially
adjusted, and, where necessary, corrected before being incorporated into the
project. All final analytical, linguistic, methodological, and editorial
decisions remained the responsibility of the researcher.
