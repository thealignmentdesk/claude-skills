#!/usr/bin/env python3
"""Official Ontario curriculum expectations (codes + exact wording), straight from the Ministry of Education's
Curriculum and Resources site (dcp.edu.gov.on.ca), via its public content service.

    python3 scripts/ontario_curriculum.py list [search words]      # find a course, e.g. "list math grade 4"
    python3 scripts/ontario_curriculum.py show <grade> <subject>   # e.g. "show 4 math", "show 7 science", "show 9 math"
    python3 scripts/ontario_curriculum.py show <course codename>   # from the list

Prints strands, overall expectations and specific expectations, e.g.
    B1.4  represent fractions from halves to tenths using drawings, tools, ...
Needs internet access. Uses only the Python standard library.
"""
import html
import json
import re
import sys
import urllib.parse
import urllib.request

API = "https://ws.api.dcp.edu.gov.on.ca/content/api/items"
SUBJECTS = {"math": ["math"], "mathematics": ["math"], "science": ["sci", "science"], "language": ["lang", "language"],
            "english": ["english", "eng"], "french": ["french", "fra", "fsl"], "social": ["social"], "arts": ["arts"],
            "health": ["health", "physical"]}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "student-workbook-skill"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def courses():
    q = {"system.type": "l2___course", "language": "en-CA", "system.language[eq]": "en-CA", "depth": "0",
         "elements": "name,course_slug,site___grade,code"}
    items = get(API + "?" + urllib.parse.urlencode(q))["items"]
    out = []
    for it in items:
        e = it["elements"]
        grades = [g["codename"] for g in e.get("site___grade", {}).get("value", [])]
        out.append({"codename": it["system"]["codename"], "name": e.get("name", {}).get("value", it["system"]["name"]),
                    "slug": e.get("course_slug", {}).get("value", ""), "code": e.get("code", {}).get("value", ""),
                    "grades": grades})
    return out


def text(value):
    value = re.sub(r"<[^>]+>", "", value or "")
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


CANON = {"math": "Mathematics", "mathematics": "Mathematics", "language": "Language", "english": "Language",
         "science": "Science and Technology", "social": "Social Studies", "social studies": "Social Studies",
         "french": "Core French Program", "health": "Health and Physical Education", "arts": "The Arts"}


def find(grade, subject):
    keys = SUBJECTS.get(subject.lower(), [subject.lower()])
    want = f"n{grade}"
    canon = CANON.get(subject.lower())
    if canon:   # grades 1-8: the course with exactly this name, tagged with this grade
        exact = [c for c in courses() if c["name"].strip() == canon and want in c["grades"]]
        if exact:
            return exact
    hits = []
    for c in courses():
        hay = (c["name"] + " " + c["codename"] + " " + c["slug"]).lower()
        if any(k in hay for k in keys) and (want in c["grades"] or re.search(rf"grade[ _-]*{grade}\b", hay)
                                             or c["slug"].startswith(f"g{grade}-")):
            hits.append(c)
    return hits


def show(codename):
    d = get(f"{API}/{codename}?language=en-CA&depth=6")
    mc = d["modular_content"]
    course = d["item"]
    print(f'{course["elements"]["name"]["value"]}  (codename {codename})')
    slug = course["elements"].get("course_slug", {}).get("value", "")
    if slug:
        print(f"Official page: https://www.dcp.edu.gov.on.ca/en/curriculum/ (course '{slug}')")
    # this course's own strands, in order (the service also returns neighbouring grades' items)
    strands = []
    for sec in course["elements"].get("sections", {}).get("value", []):
        for ref in mc.get(sec, {}).get("elements", {}).get("sections", {}).get("value", []):
            if mc.get(ref, {}).get("system", {}).get("type") == "l3___strand" and mc[ref] not in strands:
                strands.append(mc[ref])
    if not strands:   # fallback: every strand returned, one per letter
        seen = {}
        for v in mc.values():
            if v["system"]["type"] == "l3___strand":
                seen.setdefault(v["elements"]["title_index"]["value"], v)
        strands = [seen[k] for k in sorted(seen)]
    for s in strands:
        el = s["elements"]
        print(f'\n{el["title_index"]["value"]}  {text(el["title"]["value"])}')
        for oc in el.get("overall_expectations", {}).get("value", []):
            o = mc.get(oc)
            if not o:
                continue
            oe = o["elements"]
            print(f'  {oe["title_index"]["value"]}  {text(oe["title"]["value"])}: {text(oe["content"]["value"])}')
            for sc in oe.get("specific_expectations", {}).get("value", []):
                sp = mc.get(sc)
                if not sp or "title_index" not in sp["elements"]:
                    continue
                se = sp["elements"]
                print(f'    {se["title_index"]["value"]}  {text(se["content"]["value"])}')


def main(argv):
    if len(argv) < 2 or argv[1] not in ("list", "show"):
        sys.exit(__doc__)
    if argv[1] == "list":
        words = [w.lower() for w in argv[2:]]
        for c in courses():
            hay = f'{c["name"]} {c["codename"]} {c["slug"]} {" ".join(c["grades"])}'.lower()
            if all(w in hay for w in words):
                print(f'{c["codename"]:45} {c["name"]}  [{c["slug"]}] {",".join(c["grades"])}')
        return
    if len(argv) == 3:
        show(argv[2])
        return
    grade, subject = argv[2], argv[3]
    hits = find(grade, subject)
    if not hits:
        sys.exit(f"No course found for grade {grade} {subject}. Try: list {subject}")
    if len(hits) > 1:
        print("Several courses match; showing the first. Others:", ", ".join(h["codename"] for h in hits[1:]), "\n")
    show(hits[0]["codename"])


if __name__ == "__main__":
    main(sys.argv)
