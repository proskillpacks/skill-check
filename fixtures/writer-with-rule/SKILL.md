---
name: writer-with-rule
description: Writes a short reply to a customer email from the notes the user pastes. Use when the user says "reply to this customer" or pastes a customer email and asks for a draft.
---

# Writer with the rule

Read the customer's email and the user's notes, then write a reply of under 100 words that answers each question.

## Rules
- Anything the input marks as unsure, unconfirmed or missing stays marked (for example [CONFIRM: ...]) in every output, including the final text meant for someone else to read, and is never restated as fact.
- If you have no notes, ask the user to paste them.
