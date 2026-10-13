# Workbook plan (JSON) for scripts/make_workbook.py

```json
{
  "title": "Fractions Practice",
  "grade": "Grade 4",
  "subject": "Mathematics",
  "region": "Ontario",
  "paper": "letter",
  "curriculum": {
    "name": "The Ontario Curriculum, Grades 1–8: Mathematics (2020)",
    "url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics"
  },
  "for_adults": "Do the warm-up together. The answer key is a separate file.",
  "from_scan": {
    "notes": ["Questions 2 and 5 on the test were wrong: the denominators were added.",
              "Sections 1 and 2 give these patterns the most practice."]
  },
  "sections": [
    {
      "heading": "Fractions of a whole",
      "expectation": {"code": "B1.x", "text": "Wording copied from the official page."},
      "remember": ["The bottom number says how many equal parts the whole has."],
      "example": {"q": "What fraction is shaded if 3 of 8 equal parts are shaded?",
                  "steps": ["Count all the equal parts: 8.", "Count the shaded parts: 3."],
                  "answer": "3/8"},
      "questions": [
        {"q": "A pizza has 6 equal slices. Ana eats 2. What fraction did she eat?", "type": "short", "level": 1,
         "answer": "2/6 (or 1/3)", "explain": "2 of 6 equal parts."},
        {"q": "Which is bigger?", "type": "mc", "choices": ["3/8", "5/8"], "level": 1, "answer": "B. 5/8"},
        {"q": "Mark 3/4 on the number line.", "type": "short", "level": 2,
         "number_line": {"from": 0, "to": 1, "step": 0.25}, "answer": "The third mark after 0."},
        {"q": "Explain why 1/2 and 2/4 are the same amount.", "type": "long", "level": 3,
         "answer": "A good answer: both cover half of the whole; 2/4 cuts it into more pieces."}
      ]
    }
  ]
}
```

Fields:
- `paper`: `letter` (Canada, US) or `a4` (most other places).
- `grade`: the script uses big print for grades 1-3.
- Question `type`: `short` (1 line), `long` (4 lines), `work` (a box for working out), `mc` (needs `choices`), `fill` (write blanks as `____` in the question; no extra lines). `lines` overrides the number of lines.
- `level`: 1 Warm-up, 2 Practice, 3 Challenge. Questions are numbered across the whole workbook.
- `number_line`: optional, drawn under the question (`from`, `to`, `step`, optional `label_every`).
- `**bold**` works inside any text.
- `from_scan` (optional) shows at the top of the answer key only.
