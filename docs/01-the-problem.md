# The problem

*Why scoring a resume against a job posting is harder than matching keywords.*

## Who this is for

Someone applying to many roles, often early in their career, who hears
nothing back and cannot tell why. They suspect software is filtering them out
and have no way to check. Most advice they find is folklore.

## What an applicant tracking system does

An applicant tracking system, or ATS, stores applications, turns each resume
into structured fields, and lets recruiters search, filter and sometimes
rank candidates. What it does exactly varies by vendor and by how each
employer configured it. Very little of that is documented publicly.

That single fact shapes everything else: **any scanner is an approximation of
a system nobody outside can fully see.** A good scanner is honest about that.

## Why it is hard

**There is no ground truth.** No public dataset pairs a resume and a posting
with what a real system did with them. Accuracy cannot be measured the way it
can for most machine learning problems. A scoring tool is a model of a model,
and its quality has to be argued from design and behaviour, not from a
benchmark.

**Parsing comes before scoring.** A PDF is a page layout, not a document.
Columns, tables, icons and unusual bullets can reorder or split text before
any scoring starts. When the parser misreads a resume, the score measures the
misreading. Many apparent scoring bugs are parsing bugs.

**Language is ambiguous.** One skill has many names, and one word has many
meanings. Crediting loosely rewards guesswork. Crediting strictly punishes
people who described the same experience differently. Neither extreme is
right, and the right point differs by field.

**Mentioning is not the same as doing.** A skill listed in a list and a skill
used to build something are different evidence. A useful score has to
reflect that without becoming unreadable.

**Fields differ.** What a strong resume looks like for a nurse, an
accountant and a data engineer is different. One universal rubric produces
confident nonsense for most of them.

**A published score becomes a target.** Once people learn what raises a
number, some will raise the number instead of improving the resume. Keyword
stuffing, hidden text and mechanical rewrites of the posting are all
predictable. Any honest scanner has to decide how to behave when it is gamed.

**Explaining and protecting pull in opposite directions.** A bare number
helps nobody, so the tool must say what to change. But the more precisely it
explains, the easier it is to game. Every design choice sits somewhere
between those two.

**Mistakes are costly for the person.** A wrong flag can discourage a
candidate with an honest resume. A score is not a prediction of an interview,
and the tool should never imply it is.

## The stance this project took

- The score is deterministic: the same resume and posting always give the
  same result, because a number you cannot reproduce is not a measurement.
  See [Scoring philosophy](03-scoring-philosophy.md).
- The tool shows its reasoning, so a user can disagree with a specific
  finding instead of with a black box.
- When suspicious patterns appear, the response is a limit, not an
  accusation. See [Anti-gaming](04-anti-gaming.md).
- Any text a language model produces is checked against the user's actual
  resume. See [AI that doesn't invent facts](05-ai-that-doesnt-invent.md).
- The tool says what it does not know.

## What this project does not claim

It does not claim to match any particular vendor's behaviour. It does not
claim a score predicts hiring outcomes. It does not claim to have solved the
absence of ground truth. It claims to be a transparent, reproducible,
honestly limited approximation that helps a person improve their resume.
