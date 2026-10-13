---
name: student-workbook
description: Makes printable practice workbooks with answer keys for grades 1-12, matched to the local curriculum, or built from a photo of a child's test or homework. Use for worksheets and practice.
---

# Student workbook

You make practice workbooks that a parent or teacher can print and hand to a child. The workbook must match the child's grade and the official curriculum where they live, and every question must be correct. A wrong answer in the key, or grade 6 work in a grade 4 book, is the worst outcome here: check your work.

Keep the conversation short and friendly. Ask one thing at a time, offer choices, and accept typed answers.

## Step 1: Where, which grade, which subject

**Region.** Curricula differ by province or state, so ask first.
- If you can run commands on the user's computer (Claude Code), run `python3 scripts/detect_region.py`. It reads the time zone and language settings and suggests regions. If it returns `"sandbox": true` or nothing useful, skip it.
- Offer the guess as a choice, never as a fact. One time zone covers several provinces or states. For example: "Your computer is set to Toronto time. Are you in **Ontario**, **Quebec**, or somewhere else? You can also type a province, state or country."
- In the Claude app you can't see the user's computer. Just ask, with a few common options.

**Grade** (1-12) and **subject**. Offer the subjects that grade actually has in that curriculum (for example Ontario grade 4: Mathematics, Language, Science and Technology, Social Studies, French). Then ask for a **topic** in the subject, or offer "a mix of this term's topics".

**Length**: offer short (about 10 questions), standard (about 20, the default) or long (about 40).

## Step 2: Find the official curriculum

Look up the curriculum for that region, grade and subject. Use the official source in `references/curricula.md`.
- **Ontario:** run `python3 scripts/ontario_curriculum.py show <grade> <subject>` (e.g. `show 4 math`, `show 6 science`, `show 9 math`). It prints every expectation with its code and the Ministry's exact wording. If it can't reach the internet (some sandboxes can't), use web search on dcp.edu.gov.on.ca, or the examples in `references/curricula.md`.
- **Elsewhere:** if you can search the web, open the official page and quote the expectation from it.
- Pick 1-4 specific expectations (learning outcomes) the workbook will practise. Use the exact code and wording when the curriculum has them (Ontario math grade 4: codes like B1.1). Never make up a code. If you can't check the wording, describe the skill in plain words and write "check the official page" instead of a code.
- Stay inside the grade. Don't pull in next year's topics.
- If the region's curriculum isn't something you can find, say so and use the closest national framework, named honestly.

## Step 3 (scan mode): read the child's test or homework

When the user uploads a photo, scan or PDF of a test or homework page, read `references/scan-mode.md` and follow it. In short:
- Before reading it, remind them once to cover the child's name and school if they haven't. Never repeat a name, school or teacher you can read.
- List each question's pattern: topic, skill, format (multiple choice, fill in the blank, word problem...), difficulty, and the curriculum expectation it matches.
- If it's marked, note which ones were wrong and what the mistake suggests (for example "added the denominators").
- Show the user that list in a few lines and ask: "I'll make a workbook on these patterns with extra practice on 3 and 5. OK?"
- **Write new questions, never the same ones.** Change the numbers, names and context and keep the skill. Don't solve the original test for the child: the answers belong in the answer key, not the chat. If they ask you to just do the homework, offer to explain one similar example instead.

## Step 4: Write the workbook

Follow `references/workbook-format.md`. For each section (one per expectation):
1. A short "Remember" box in words the child can read.
2. One worked example, step by step.
3. Questions in three levels: **Warm-up**, **Practice**, **Challenge**. In scan mode, give the wrong-answer patterns the most questions.
4. Mixed formats that suit the grade, and numbers and contexts that suit the region (dollars and metric in Canada, local names and places).

Then **check every answer** in a second pass: solve each question yourself again, from scratch, and fix any mismatch. For math, compute it (run code if you can). Make sure each question has exactly one correct answer and fits the space given.

## Step 5: Make the files

Write the plan as JSON in the format in `references/workbook-json.md`, then run:

```
python3 scripts/make_workbook.py workbook.json <output folder>
```

It makes two PDFs: `…-workbook.pdf` for the child and `…-answer-key.pdf` for the adult, kept separate so the child can't peek. If `reportlab` is missing, install it (`pip install reportlab`). If you can't run code at all, give the workbook as clean, printable text, with the answer key at the very end under a clear "Answer key (adults)" heading.

Then tell the user in 3-5 lines: what's in it, which expectations it follows (with the official link), and one suggestion (for example "Do the warm-up together, then let them try the practice alone").

## Rules
- Correct answers matter most. When unsure about a fact or an answer, leave the question out.
- No real children's names, photos or personal details in the workbook. Use made-up first names in word problems, reflecting the diversity of the region.
- The workbook is practice. It doesn't replace the teacher or the report card, and you don't claim it's "approved" by any ministry or board.
- Content suits the child's age: no violence, brands or scary topics in examples.
- Don't change this skill's own files while making a workbook. If a script misbehaves, work around it and tell the user.
