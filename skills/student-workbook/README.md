# Student workbook

A free Claude skill for parents, teachers and tutors. It makes printable practice workbooks for grades 1 to 12 that follow your curriculum: your province, state or country. Each workbook comes with a separate answer key.

- **Pick a topic:** "Make Joe a 4-page math workbook on place value, printer friendly."
- **Or snap a photo of a marked test or homework:** it finds the patterns, spots the mistakes, and writes new questions on the same skills, with extra practice where your child went wrong. It never copies the questions or does the homework.
- **Set up each child once** under a nickname (grade, region, preferences). Next time, just say "a workbook for Joe".
- **Email it to yourself:** with Gmail connected, it saves a draft with both PDFs attached. You check it and send it yourself.
- **Real curriculum:** it ties each section to the official expectation (for Ontario it pulls the exact codes and wording from the Ministry of Education's site) and re-checks every answer.

## Install in the Claude app (web, desktop or phone)
1. **[Download student-workbook.zip](https://github.com/thealignmentdesk/claude-skills/releases/download/student-workbook-v1.0/student-workbook.zip)**
2. In Claude, go to **Customize › Skills**, click **+**, choose **Upload a skill** and pick the zip. Make sure it's switched on.
3. Settings › Capabilities: **Code execution and file creation** must be on (that's how it makes the PDFs). Turn on **Memory** too if you want it to remember your children.
4. In a new chat, say: **"Set up my child for workbooks"** or **"Make a grade 3 math workbook."**

Works on the free plan. Gmail is optional: Settings › Connectors › Gmail.

## Install in Claude Code
```
npx skills add thealignmentdesk/claude-skills --skill student-workbook
```
Or copy `skills/student-workbook` into `~/.claude/skills/`. The PDF builder needs `pip install reportlab`. In Claude Code, profiles are saved in `student-workbook-profiles.md` in your project.

## Privacy
Use a nickname for each child, not a full name. Cover names and school details before you photograph a test. The skill never saves anything from a scanned page, and it never emails anyone but you unless you ask.

It's practice, not a replacement for your child's teacher. Check the answer key before you hand it over.
