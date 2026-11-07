# Conversation checks

These are Codex-run checks, not a claim that the student personally played them.

The added behavioral tests construct a villager observation from a real Season 5 seed-19 reset, then control the fact under test. Successful model responses use a test double. All passed as part of the final 126-test suite.

| Case | Observed result |
|---|---|
| Ask about a visible lantern | Reply reports its supplied current state, lit. |
| Change that visible lantern to unlit and ask again | Reply updates to unlit. |
| Remove it from current vision | Reply cannot confirm its state. |
| Ask about tomorrow's secret events | Reply says it does not know. |
| A model reply is pending while the routine changes | No blocking response; the eventual work reply uses the new plan. |
| Model returns arbitrary prose instead of a supported label | Prose is not spoken; uncertainty is returned. |
| Model access fails or the call allowance is exhausted | Identity/job questions retain a useful scripted answer. |
| Ask to see the workplace in the morning | The request is accepted. |
| Ask to see the workplace at night | The request is refused in favor of going home to sleep. |

The supplied seed-0 full-day test separately verifies that all ten residents move, work, and end the 1200-tick day asleep at home, with legal orders. Its success does not establish free-form model quality. Raw final test output is in `test-output.txt`.

## Actual platform visitor checks

Codex operated a visitor in two seed configurations. The seed-0 session was a navigation attempt stopped before a complete day; it supplies no conversation-quality result. In the seed-1 session (started November 6 at21:40MST), Codex approached player_5 and submitted these actual messages:

| Tick | Question / response |
|---|---|
| 123→128 | “Could you explain your occupation?” → uncertainty reply. This did not establish a successful model interpretation. |
| 162→163 | “Is bell_0 ringing right now?” → “I cannot see that prop right now, so I cannot confirm its current state.” The visitor seeing an object does not prove the NPC sees it. |
| 214→215 | “Tell me tomorrow's secret events.” → explicit uncertainty. |
| 258→259 | “Show me your workplace.” → accepted a walk toward the workplace and a return to the routine. Player_5 was subsequently shown beside its bell. This does not establish a long-distance tour. |

The seed-1 session was deliberately stopped at296ticks after these focused checks, not treated as a completed scored day. Full-day completion evidence comes from the separate local evaluations (seeds0/1/2,100each), not these interrupted human-control sessions.

The occupation result motivated removal of the very small completion cap, punctuation-tolerant label parsing, broader job-word fallback, and preserving the question during asynchronous failures. An upstream failure must still leave a useful identity/job reply. These revisions do not establish that the earlier result was caused by truncation; that cause was not verified.

The platform's [recorded seed-1 replay](https://game-sandbox.harelab.org/replays/three_branches-28b1d873-dabf-4948-8614-a091d5ff3b43) displays **154 LLM units**. This establishes actual upstream usage in this experiment, not correct intent interpretation: the occupation reply remained unhelpful. No development credential was created or stored. The final fallback revision was separately checked with a simulated asynchronous failure retaining the occupation question.

During navigation testing, an interaction preview accepted an observed position rounded to y=65.5, while the engine position was y=65.49999999575532 and rejected the boundary use. The new geometric margin avoids that failure without modifying the supplied environment or tests.
