# 01 Import the cheat sheet page

Status: needs-triage
Type: task

- Write `course/exams/schrijven-spiekbriefje.md` with the five sections as Markdown tables and lists, Dutch with the English glosses, header marked imported and needs-review. Keep the Notion wording; fix nothing silently (list any doubts under a "Review notes" heading).
- Link it from the exams README, the course README and the oefenexamen page. Use root-relative links so `validate` passes.

Done when: `validate` passes, no orphan page, tests pass, and a test asserts the five tables parse non-empty.
