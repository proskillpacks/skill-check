# Changelog

## v1.1.0 (2026-10-04)
- New warning SC017: the description says the skill writes text for other people to read (a reply, email, quote, page, summary and so on), but nothing in the skill says what to do with input that is unsure or unconfirmed. The message suggests a one-line rule. Reason: in our own tests, three of four defects were an unsure fact restated as fact in text meant for a customer.
- Two new fixtures and tests for it. Existing rules and exit codes are unchanged. Skills that already carry such a rule see no change.

## v1.0.0 (2026-10-04)
- First release: checker, GitHub Action, pre-commit hook, fixtures and tests. Rules SC001 to SC016 and SC100 to SC103.
