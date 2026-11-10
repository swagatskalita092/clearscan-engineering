# Resume conventions around the world

*How resumes and CVs differ by country, and what that does to a parser.*

Most resume-scanner advice quietly assumes one kind of document. Real users
write many kinds. A resume in one country is a CV in another, and the same
section can be expected in one place and discouraged in the next. This page
lists the differences that matter to anyone building a parser or a scorer, so
that you can design for them early instead of discovering them in production.

Nothing here says one style is better. It describes common conventions, not
rules. Employers differ, and the examples are patterns to test against, not
guarantees.

## Conventions differ

The table summarises guidance published by university career services and
expatriate advice sites. Treat it as a starting point and check local guidance
for the market you serve.

| | United States | United Kingdom | Germany |
|---|---|---|---|
| Usual name | Resume | CV | Lebenslauf |
| Typical length | One to two pages | About two pages | One to two pages |
| Photo | Generally left out | Generally left out | Common, but optional |
| Personal details | Name and contact details only | Name and contact details, often a professional profile link | Name and contact details, with address, nationality and birth details common but optional |
| Layout habit | Reverse chronological, short bullet points | Reverse chronological, skills woven through experience | Reverse chronological, often a two-column layout with dates on the left |
| Extras | Short summary is common | Summary is optional, references usually "on request" | Signature and date at the end are common |

Sources:
[LSHTM comparison of a US resume and a UK CV](https://ble.lshtm.ac.uk/pluginfile.php/298474/mod_page/content/50/US%20resume%20v%20UK%20CV.pdf),
[Expatica on CV tips by country](https://www.expatica.com/global/working/finding-a-job/cv-tips-for-different-countries-105713/)
and the
[TU Ilmenau CV checklist](https://www.tu-ilmenau.de/fileadmin/Bereiche/International/Dateien/01.08.2025_CV_Checklist.pdf).
Other regions follow other habits, and some publish standard templates, such
as the EU's Europass.

## What this does to a parser

| Convention | What can go wrong | What to do |
|---|---|---|
| A photo or logo in the header | Text extraction order breaks, and the header may be read as the first line of a column | Test with images present. Do not rely on reading order alone |
| Dates in a left column | A table-like layout is flattened, and dates end up detached from the job they belong to | Reconstruct pairs from position, not only from text order |
| Day-first and month-first dates, such as 03.2023, 15/03/2023 or 03/15/2023 | A parser built for one order reads the other wrongly, or fails | Support the common formats explicitly, and say which are ambiguous |
| Local words for "ongoing", such as "since" or "to date" | An open-ended job looks as if it has no end date | Treat local words for ongoing as open dates |
| Accented and non-Latin characters | Characters are dropped or replaced when a PDF uses unusual encoding | Test with real extracted text, not typed examples |
| Compound words, common in several languages | A keyword match for a part of the word finds nothing | Match on word parts as well as whole words, and state this in your limits |
| Titles with suffixes or gender markers, such as the "(m/w/d)" seen in German job adverts | Titles look different from the posting they are compared to | Strip or normalise the suffix before matching |
| Section headings in other languages | A section is not recognised, so it counts as missing | Map common headings in the languages you support to the same sections |
| A personal details block | Birth date and similar details are treated as skills or experience | Recognise the block and keep it out of scoring |
| A signature or declaration line | The last line of the document is read as content | Ignore trailing signature, date and declaration lines |
| Different page lengths | A one-page assumption cuts off real content on page three | Never truncate on length alone |

## Language levels

Many resumes describe language skill with a standard scale, most often the
Common European Framework of Reference, A1 to C2. A resume that says "A2" or
"C1" is making a precise statement, and a scorer should read it that way
instead of as a keyword. Other resumes use words such as "fluent" or
"native". Handle both, and treat a stated level as structured data.

## Mixed-language documents

Many people write in one language and keep names, degrees or section headings
in another. The same applies to postings. A system built only around one
language's keywords will miss real evidence in these documents and should say
so plainly.

The scoring described in these notes was built for English-language resumes.
That is a design limit and not a feature, and it is stated here so nobody has
to discover it.

## Taxonomies

Occupation lists carry the assumptions of the country that wrote them. See
[Occupational data](10-occupational-data.md) for what two public sources offer
and where each falls short.

## A test set worth building

Before you trust a parser on a wider audience, build a small, fully synthetic
set that covers the patterns above. A starting point covering layout and
character traps, with ground truth, is in
[Synthetic resumes](../research/synthetic-resumes/README.md). It includes a
German-language CV and Russian, Greek, Japanese, Arabic, Hindi and Thai
resumes. Its results show that scripts needing text shaping are the hardest
case for many text extractors, and that the outcome depends on the program
that produced the file. It does not yet cover date conventions or
right-to-left layouts with columns or tables. The patterns to cover:

1. A two-column layout with dates on the left.
2. A photo or logo in the header.
3. Day-first and month-first dates, and a local word for "ongoing".
4. Accented characters in names and employers.
5. A title with a gender or suffix marker.
6. Section headings in a second language.
7. A language section using a level scale.
8. A one-page, a two-page and a three-page version of the same resume.

Use invented people only. Never test with real resumes. Keep the set in
version control, and add a case every time a real failure teaches you
something.

## Honest limits

- The conventions above come from public career-service and advice guidance,
  and describe typical documents. They are not a complete or official
  standard.
- Practice varies by industry, company and region.
- Only a few markets are summarised here. Check local guidance for the others.

## For your own system

Decide which resume styles you support, and say so. Test with the formats your
users actually send. Treat dates, language levels and section names as data
that differ by place. Write down what you do not handle.

See also: [Occupational data](10-occupational-data.md),
[Anti-gaming](04-anti-gaming.md) and
[Build your own](../build-your-own/README.md).
