# Occupational data: using O*NET, and why Europe needs more

*What a public occupational database gives a resume scanner, what it cannot, and the licence you take on.*

A scorer needs some idea of what a role usually involves. The alternative to
inventing that from opinion is to borrow it from public occupational data. This
page explains what that data looks like, where it helps, where it quietly
misleads, and what you owe its authors when you use it.

It describes the data and the engineering around it. How ClearScan combines it
with a posting, and how that combination is tuned, is private and is not
described here.

## What O*NET is

[O*NET](https://www.onetcenter.org/) is a database of occupations published by
the U.S. Department of Labor. Each occupation has a descriptive record that is
built from surveys of workers and occupation experts. For a resume scanner the
useful parts are:

| Part | What it holds | What it is good for |
|---|---|---|
| Occupation titles and alternate titles | The official title plus many names people use for the same job | Recognising that two job titles mean the same thing |
| Tasks | Sentences describing what people in the role do | Understanding the verbs and objects a role typically involves |
| Skills, knowledge and abilities | Survey ratings of importance and level | A rough picture of what the role emphasises |
| Technology skills | Software and tools used in the occupation | Knowing which products belong to which kind of work |
| Hot Technology and In Demand flags | Tools that appear often in employer postings | A snapshot of what employers currently ask for |
| Related occupations | Neighbouring occupations | Sensible fallbacks when a title is unusual |

At the time of writing, the release is O*NET 31.0 (August 2026). The project
publishes several releases a year, and its own
[What's New page](https://onetcenter.org/whatsnew.html) lists what changed in
each. Of the occupations in the database, 912 have data collected from workers
and occupation experts; the rest carry less. These figures change with every
release, so check the source rather than this page.

## What it gives you

- **An assumption you can point at.** "This is what the role typically
  involves, according to a public source" is easier to argue with than "this is
  what we decided".
- **A shared vocabulary.** Titles, tasks and tools arrive already organised.
- **A cheap start.** Building your own expectations for hundreds of occupations
  takes a team years.

## What it cannot give you

This is the section most write-ups skip.

- **It is American.** The occupations, titles and wording follow the U.S.
  labour market. A German or Indian job advert often does not use the same
  title, and some roles have no clean counterpart.
- **Titles do not map one to one.** A single posting title can fit several
  occupations, and many real titles fit none well. Matching is a judgement, and
  it needs a fallback for when nothing fits.
- **Coverage is uneven.** Occupations with full data are served well. Newer or
  niche roles, which is where many early-career job seekers apply, are thinner.
- **Technology lists are product names, not meaning.** Knowing that a tool
  belongs to an occupation does not tell you how a person describes using it.
- **Survey ratings are blunt.** They describe a typical worker, not the
  particular posting in front of you. Always weigh them against what the
  posting actually says.
- **Hot Technology is a snapshot.** It reflects a period of postings. A tool
  that was in demand when a release was built may be fading by the time you
  rely on it.
- **It ages.** Occupations change faster than a database release does.

The right reading is that O*NET describes a typical role. It is a prior, not a
verdict. The posting always has the last word.

## Working with it as an engineer

These habits come from living with a public dataset inside a product.

1. **Pin the version.** Record which release you used. A silent upgrade can
   move behaviour, and your licence asks you to name the version anyway.
2. **Treat an update as a change to be reviewed.** Compare the old and new
   releases, read what moved, and only then adopt it.
3. **Curate, do not just import.** Raw data contains entries that are too
   generic to help. Someone has to decide what is worth using.
4. **Test the mapping.** Pin a set of known titles and the occupations you
   expect for them. A data update that changes a mapping should fail a test, not
   surprise a user.
5. **Plan for no match.** Decide in advance what the system does when a title
   fits nothing. Silence is not an answer a user can use.
6. **Keep it out of the user's way.** The benchmark informs the score. It
   should never become an unexplained number on the screen.

## The licence you take on

The O*NET database files are published under the
[Creative Commons Attribution 4.0 licence](https://creativecommons.org/licenses/by/4.0/).
The [database licence page](https://onetcenter.org/license_db.html) has the
exact terms. In plain terms, as of the release described above:

- You may use the data, including in a product, if you give credit.
- The credit names the database and its version, and names the U.S. Department
  of Labor, Employment and Training Administration as the source, with a link
  to the licence.
- If you change or add to the data, you must say so, and the modified wording
  states that the department has not approved, endorsed or tested your changes.
- "O*NET" is a trademark. Use it as an adjective, as in "with O*NET data", and
  show the trademark symbol.

This is a summary and not legal advice. Read the licence page for the wording
you must use, and recheck it when you move to a new release.

> [!NOTE]
> This page refers to the O*NET&reg; database.
> Used under the CC BY 4.0 license. O*NET&reg; is a trademark of USDOL/ETA.

## The European counterpart

If your users are in Europe, O*NET alone will not fit. The European
Commission publishes [ESCO](https://esco.ec.europa.eu/), a multilingual
classification of occupations and skills. Its portal currently lists 3,039
occupations and 13,939 skills in 28 languages, which include all official EU
languages. Check the ESCO site for current counts and for the terms that
apply to downloading and reusing it, because the portal itself does not spell
them out on its overview page.

| | O*NET | ESCO |
|---|---|---|
| Publisher | U.S. Department of Labor | European Commission |
| Market it reflects | United States | European Union and neighbours |
| Languages | English, with Spanish resources | 28 |
| Strength | Rich descriptive detail per occupation, tools and tasks | Multilingual, and skills linked to occupations |
| Weakness for a scanner | Titles and wording differ from European postings | Less descriptive text per occupation |
| Reuse terms | CC BY 4.0 with attribution | Check the ESCO download page |

Neither is a complete answer. A careful system treats both as inputs, keeps
them separate so you can tell which one said what, and never lets either
replace the text of the posting.

## For your own system

Use a public source for your assumptions so they can be debated. Pin the
version, review every update, and test the mappings. Decide what happens when
nothing matches. Credit the source properly. Be honest that a database of
typical roles describes the average, and that the person in front of you is not
average.

See also: [Scoring philosophy](03-scoring-philosophy.md),
[Technology choices](06-technology-choices.md) and
[Resume conventions around the world](11-resume-conventions-around-the-world.md).
