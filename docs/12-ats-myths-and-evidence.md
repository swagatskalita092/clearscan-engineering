# ATS myths and the evidence

*What is commonly said about applicant tracking systems, what public evidence
exists for it, and how strong that evidence is.*

## How to read this page

Advice about applicant tracking systems is mostly repeated, rarely sourced.
This page takes seven common claims, says what public evidence exists for each,
and grades it. It is a reading guide, not a verdict. Where the evidence is a
vendor's own statement or a small survey, it says so.

Evidence grades used below:

| Grade | Meaning |
|---|---|
| Peer reviewed | Published through an academic venue with review |
| Large survey | A published survey with a stated sample, not independently audited |
| Vendor statement | What a software vendor says about its own product |
| Small survey | A sample too small to generalise from, often run by a company with something to sell |
| None found | No public evidence located |

Sources were read in November 2026. Links are at the end. Nothing here
describes how any specific employer configures its system, because that is
not public.

## Claim 1: "An ATS automatically rejects most resumes"

**What the evidence says.** It is partly true and usually described wrongly.

- A major vendor says automatic rejection in its product runs on rules that
  recruiters set, such as a "no" to a work-eligibility question, and that its
  AI does not score, rank or decide who advances. It also says applications
  to popular roles can be filtered before anyone opens them. *Vendor
  statement.*
- A small survey of 25 recruiters, published by a resume-writing company,
  reported that most said their systems did not reject on formatting or
  content, and that knockout questions were mostly about eligibility. *Small
  survey.* It is worth knowing it exists and not worth leaning on.
- A Harvard Business School and Accenture survey of more than 2,250
  executives in the United States, the United Kingdom and Germany found that
  88 per cent of employers agreed that qualified high-skill candidates are
  vetted out for not matching the job description's exact criteria. The share
  was 94 per cent for middle-skill candidates. *Large survey.*

**Reading these together.** Nobody is claiming a program silently throws away
resumes it dislikes. The more defensible claim is that human-set rules, applied
at high volume, exclude people who would have been qualified. The practical
consequence is the same for an applicant: the exact wording of the posting
matters. The mechanism is different, and it is a person's configuration, not a
mysterious algorithm.

## Claim 2: "A high scanner score means you will get through"

**What the evidence says.** None found.

No public dataset pairs a resume and a posting with what a real system did
with them, so no scanner can be validated against real outcomes from the
outside. A score from any third-party tool, including this project's, is a
measurement of how a document presents evidence for a posting. It is not a
prediction of what will happen to a candidate. See
[The problem](01-the-problem.md) and
[Scoring philosophy](03-scoring-philosophy.md).

## Claim 3: "Formatting cannot hurt you if the content is good"

**What the evidence says.** Weakly supported in the other direction, from the
engineering side.

- A 2025 systematic review of 44 peer-reviewed studies on resume analysis
  reports accuracy of roughly 80 to 94 per cent for the research systems it
  covers, and names format diversity, dataset bias and computational cost as
  recurring limitations. *Peer reviewed*, but it is a review of research
  prototypes, not of commercial products.
- Public benchmarks of commercial parsers are mostly published by the
  vendors that sell them, and were not found in independent form. This
  repository now publishes a first open benchmark of extraction libraries on
  invented resumes, in [Synthetic resumes](../research/synthetic-resumes/README.md).
  It measures text extraction only and says nothing about any vendor's
  system. *Measured here, not independently reviewed.*

**Reading these together.** Parsing is an imperfect step and research
systems struggle with varied layouts. That makes it sensible to prefer simple
structure. It does not show how any particular vendor's parser behaves. The
claim "columns break everything" is a hypothesis with plausible mechanics, not
a measured fact. See [Resume conventions around the world](11-resume-conventions-around-the-world.md)
for the specific layout traps worth testing.

## Claim 4: "Automated screening is objective"

**What the evidence says.** There is good evidence that it can be biased,
from research on language-model ranking.

University of Washington researchers took more than 550 real resumes and
120 first names associated with white and Black men and women. Three
language-model retrieval systems ranked the resumes against more than 500
real job listings across nine occupations, giving over three million
comparisons. White-associated names were preferred 85 per cent of the time
against 9 per cent for Black-associated names. Male-associated names were
preferred 52 per cent of the time against 11 per cent for female-associated
names. *Peer reviewed.*

**Limits of that evidence.** The systems tested were research retrieval
models, not the commercial products an employer buys. The study shows what
can happen when text embeddings are used to rank people. It does not show
that any particular product behaves this way.

This is why [the bias audit issue](https://github.com/swagatskalita092/clearscan-engineering/issues/13)
exists: a scanner built on language models should be audited before it is
trusted, and a rule-based one should still be audited, because rules can
encode the same patterns.

## Claim 5: "Repeating keywords as often as possible raises your chances"

**What the evidence says.** None found for any specific vendor.

The vendor statement under Claim 1 describes recruiter-set rules and says
its AI does not rank, which does not support a keyword-density theory for that
product. The practical risk of stuffing is also not about software. The resume
is eventually read by a person, and text written for a machine reads badly.
See [Anti-gaming](04-anti-gaming.md) for why a scanner should compare against
the posting instead of against a count.

## Claim 6: "Gaps in work history are fatal"

**What the evidence says.** One reported statistic, from an interview and not
from a methods section.

In a 2021 interview with the Harvard Gazette, a co-author of the Harvard
Business School report said that about half of United States companies filter
out applicants with a work-history gap of more than six months. The article
does not describe how that figure was produced. *Reported, not audited.*

**Reading it.** If true, it is a filter a recruiter chose, not a property of
the software. It matters to career changers, caregivers and students, who are
often the people with gaps. It also differs strongly by country, because
resume conventions about gaps are not the same everywhere.

## Claim 7: "Dense embeddings score resumes better than keyword matching like TF-IDF"

**What the evidence says.** Not demonstrated, by the one study that comes
closest.

A [September 2026 paper](https://arxiv.org/abs/2609.23307) from a staffing
company and an IIT compared embedding models inside a hybrid candidate-search
pipeline and found a real gain from switching to a stronger embedding model,
plus a smaller gain from fine-tuning it on past placements. *Peer status
unclear; posted to arXiv, not reviewed.* But the comparison never isolates
embeddings against TF-IDF or BM25 alone. Every dense model in it competes
against another dense model, not against a sparse baseline, and its headline
relevance numbers come from a large language model acting as judge rather
than a labelled hiring outcome.

**Reading it.** This is evidence that embeddings can be tuned to look better
on an internal, judge-scored metric. It is not evidence that they outscore a
sparse method on anything a candidate or employer would recognise as
correctness. See [Scoring philosophy](03-scoring-philosophy.md) for why
this project keeps the deterministic, sparse approach until a real
apples-to-apples comparison exists: it is debuggable term by term, with no
model file attached to the formula, and that is a real cost to give up for an
unmeasured gain.

## What regulation says about this class of software

In the European Union, software used to filter or rank applicants is treated
as high risk under the AI Act. The Digital Omnibus on AI, which entered into
force on 27 July 2026, moved the date for those obligations from 2 August 2026
to 2 December 2027. Law firms tracking the change agree on those dates. Rules
and dates change, so check the current text before relying on this summary.
This is general information, not legal advice.

In the United States there is no single federal AI-hiring statute. Title VII,
the ADA and the ADEA still apply to a decision an AI tool helps make. Below
that, states and cities are building their own rules, and they do not agree
with each other:

- **New York City's Local Law 144** (in force since July 2023) requires an
  independent bias audit within the year before an automated employment
  decision tool is used, publication of the audit, and at least ten business
  days' notice to a candidate.
- **Illinois HB 3773** (effective 1 January 2026) prohibits AI use that has a
  discriminatory effect across the employment lifecycle and requires
  disclosure that AI is being used, but does not require a bias audit.
  Illinois separately has a 2020 AI Video Interview Act requiring consent
  before an AI video-interview system is used.
- **Texas's TRAIGA** (effective 1 January 2026) prohibits AI deployed with
  intent to discriminate, with liability limited to intentional
  discrimination and a 60-day cure period.
- **Colorado is unsettled.** One account describes the original Colorado AI
  Act, which would have required impact assessments and attorney-general
  notice, as stayed by a federal court in April 2026 pending a legal
  challenge. Another describes it as already repealed and replaced by
  SB26-189, which would regulate automated decisions, employment included,
  from January 2027. The two accounts disagree, and neither could be
  confirmed past May 2026, so treat Colorado as open until checked against
  the state's own bill tracker and court docket.
- **California's CCPA automated-decision-making rules**, covering
  significant decisions including employment, take effect 1 January 2027.
- Two federal lawsuits are relevant context rather than binding rules yet:
  *Mobley v. Workday*, where ADEA and Title VII claims against a vendor were
  allowed to proceed, and *Kistler v. Eightfold AI*, an early-stage case
  arguing a screening vendor is a consumer reporting agency under the FCRA.

Whether a given product falls under any of these rules is a legal question,
not an engineering one, and a tool that helps an applicant improve their own
resume is a different thing from one that an employer uses to rank
applicants. This is general information, not legal advice, and reflects
sources read in November 2026.

## What would settle these questions

- A public, labelled dataset of resumes and postings with human judgements.
- Parser benchmarks run by someone with no product to sell. The
  [synthetic resume set](../research/synthetic-resumes/README.md) is a first,
  small step for open-source libraries.
- Audit studies that submit matched resumes to real systems with the
  employer's consent.

The research issues, such as the
[validity study](https://github.com/swagatskalita092/clearscan-engineering/issues/14)
and the [parsing benchmark](https://github.com/swagatskalita092/clearscan-engineering/issues/12),
describe how to contribute to any of these.

## Honest limits of this page

- It summarises sources and has not repeated their studies.
- It was written by one maintainer and may miss better evidence. The
  [correction form](https://github.com/swagatskalita092/clearscan-engineering/issues/new/choose)
  is there for that.
- Evidence about United States systems may not apply elsewhere.
- Vendor statements are included because they are the only public account of
  how some products work, not because they are neutral.

## Sources

- Fuller, Raman, Sage-Gavin and Hines, [Hidden Workers: Untapped
  Talent](https://www.hbs.edu/managing-the-future-of-work/research/hidden-workers-untapped-talent),
  Harvard Business School and Accenture, 2021. Survey figures are from the
  [executive summary](https://pubwww.hbs.edu/managing-the-future-of-work/Documents/research/Hidden%20Workers%20Executive%20Summary.pdf).
- Harvard Gazette, [New study says hidden workers are being
  excluded](https://news.harvard.edu/gazette/story/2021/09/new-study-says-hidden-workers-are-being-excluded/),
  September 2021.
- Greenhouse, [What really happens after you apply for a
  job](https://my.greenhouse.com/blogs/what-really-happens-after-you-apply-for-a-job),
  January 2025.
- Greenhouse, [How does Greenhouse use AI](https://my.greenhouse.com/blogs/how-does-greenhouse-use-ai-heres-everything-candidates-need-to-know),
  January 2025.
- BetaNews, [Study debunks viral claim that AI filters out most job
  applicants](https://betanews.com/article/study-debunks-viral-claim-that-ai-filters-out-most-job-applicants),
  reporting a survey by a resume-writing company.
- Wilson and Caliskan, [Gender, Race, and Intersectional Bias in Resume
  Screening via Language Model Retrieval](https://ojs.aaai.org/index.php/AIES/article/view/31748),
  AAAI/ACM Conference on AI, Ethics, and Society, 2024. Summary from the
  [University of Washington news
  release](https://www.washington.edu/news/2024/10/31/ai-bias-resume-screening-race-gender/).
- Kanikar, Jain, Jain and Purohit, [Systematic Review of Methods for Analysis
  of Resumes](https://www.atlantis-press.com/article/126017319.pdf), ICCSCE,
  2025.
- White & Case, [EU AI Omnibus enters into force, amending the AI
  Act](https://www.whitecase.com/insight-alert/eu-ai-omnibus-enters-force-amending-ai-act),
  2026.
- Adams, Andrew, [Patchwork of AI Hiring Laws Creates Rising Compliance Risks
  for
  Employers](https://natlawreview.com/article/patchwork-ai-hiring-laws-create-rising-compliance-risks-employers),
  DarrowEverett LLP via National Law Review, May 2026.
- Wiley Rein LLP, [AI in Hiring: Evolving Legal Risks Under State and Federal
  Law](https://www.jdsupra.com/legalnews/ai-in-hiring-evolving-legal-risks-under-9259049/),
  JD Supra, May 2026.
- Yashwant, Jain, Dubey, Chatterjee and Thulsiram, [Semantic Candidate-Job
  Matching: A Comparative Evaluation of Dense Embedding Models in Hybrid
  Retrieval](https://arxiv.org/abs/2609.23307), arXiv, September 2026.
