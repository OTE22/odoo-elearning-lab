# Learning design approach

How the three NovaTechAI Academy courses are designed, what a learner does in them, and how their impact is measured. Live site: https://learn.novatechai.site/slides

## Design principles

| Principle | How it shows up in the courses |
|---|---|
| **Scenario-based learning** | Every lesson is a professional decision in a fictional but realistic cultural organisation: a funding call, an exhibition text, a festival box office. |
| **Worked example after attempt** | Each lesson ends with a task the learner writes first. The comparison and the model answer are folded behind "reveal after you try" buttons. |
| **Retrieval practice** | Six retrieval cards per course, unit checks and a final quiz whose every option carries feedback explaining why it is right or wrong. |
| **Universal Design for Learning (UDL 3.0, CAST 2024)** | Multiple means of representation: text, illustrated lesson guides, a short film with a written transcript, a bilingual glossary. Learner choice: a readiness self-check recommends where to start. |
| **Accessible interface (WCAG 2.2 guidance)** | Native disclosure elements and form controls, visible keyboard focus, live-region feedback, text alternatives for films, mobile layouts and reduced-motion support. The interface is built with WCAG 2.2 in mind; it has not been formally audited. |
| **Authentic assessment** | A capstone project scored with a ten-point rubric, plus Excel job aids the learner keeps using at work. |

## Course structure

Each course has three units. Every article lesson follows the same sequence:

1. **Objective**, with its level: foundational, intermediate or advanced.
2. **Case**: the situation and its constraints.
3. **Method**: how a professional reasons through it.
4. **Guided task**: written by the learner.
5. **Compare your approach**, then reveal it.
6. **Common mistake** and **lesson summary**.
7. **Check your understanding**, then reveal the suggested answer.
8. **Guided reading**: an official source, where relevant.

| Course | Lessons | Advanced lab (2026) |
|---|---|---|
| Fundable cultural proposals | 5 lessons, 2 unit checks, capstone, 6-question final quiz | Co-financing, in-kind contributions and a funding risk register with a worst-case cash test |
| AI-assisted cultural editing under human oversight | 5 lessons, 2 unit checks, capstone, 6-question final quiz | AI disclosure and content labelling under Article 50 of the EU AI Act (applicable since 2 August 2026) |
| Digital risk and continuity for cultural work | 4 lessons, 2 unit checks, capstone, 5-question final quiz | Deepfake payment fraud (the 2024 Arup case) and an out-of-band payment verification procedure |

## Course landing pages

Every course page includes:

- **Competency map:** four competencies, each with its level in the revised Bloom taxonomy and the evidence the learner produces.
- **Readiness self-check:** five statements; the page recommends starting at unit 1, at unit 2 or at the advanced lab.
- **Deliverables:** the four work products a learner leaves with.
- **Job aids:** two Excel workbooks per course. They are right-to-left, with live formulas and drop-down lists, pre-filled with the course's own worked example (built by `tools/build_downloads.py`).
- **Retrieval cards** and a **bilingual Arabic–English glossary** of ten terms.
- **Audience, prerequisites, FAQ** and **official references**, each link checked before publishing.

## Measuring impact (Kirkpatrick model)

| Level | What is measured |
|---|---|
| 1. Reaction | Course ratings and reviews after each unit (built into Odoo eLearning). |
| 2. Learning | Unit checks, the final quiz and the capstone rubric score. |
| 3. Behaviour | Course-specific: the decision memo and cash-flow table used in a real application; the claim log and disclosure policy adopted; the payment procedure applied and a restore drill run, each within three months. |
| 4. Results | Course-specific: eligible applications and funder feedback; fewer post-publication corrections; recovery time against target and no unverified transfers. |

Levels 1 and 2 are collected by the platform. Levels 3 and 4 need a short follow-up with the learner's organisation, typically a three-month survey.

## Content standards

- **Fictional cases:** all organisations, figures and dates in the cases are fictional, so learners can practise without exposing any real organisation's data.
- **Real-world facts:** facts are taken from primary or official sources: OECD, UNESCO, NIST, CISA, the EU AI Act text and the confirmed reporting on the Arup case.
- **Time-sensitive details:** funding amounts and deadlines are not quoted, because they change every cycle; learners are sent to the current official call.
- **Not legal advice:** the AI disclosure lab helps learners ask the right questions before publishing. Organisations should confirm their obligations with counsel.

## Technology

The platform runs on Odoo 17 eLearning in Docker, with the courses packaged as installable modules. Each module ships with automated tests: course structure, quiz validity, media files, rendered components, download files and working in-page links. Presentation changes are progressive enhancements, so every page stays readable without JavaScript.
