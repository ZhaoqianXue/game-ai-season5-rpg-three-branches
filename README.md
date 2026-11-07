# Season 5 — RPG: The Conversation

Zhaoqian Xue / purpleman / GitHub @ZhaoqianXue

## Design goal

Visitors should learn who the villagers are, why they do their jobs, and how their words match their activities. They can ask about visible props or request a daytime walk toward a workplace; distant and private facts remain unverified.

Rating question (1–5): How well did the villagers' replies and workplace tours match what they could see and what they were doing?

## Characters and knowledge

Adapted from the official [Neighbor example](https://github.com/vox-deorum/game-agent-template/tree/examples/three_branches/neighbor). `PERSONAS` and `STORIES` in `conversations.py` give the ten residents authored identities: Mira tends the pump for the gardeners, Rowan keeps notices, Tess repairs, Ash tends the hearth, Bell minds the bell, three traders have different attitudes, and Fern/Reed garden. These backgrounds are design choices, not hidden-state observations.

Each resident knows its own selected routine and workplace. Current prop states come only from `props.seen()`: knowing a lantern's location does not establish whether it is lit. A changed visible state replaces the old answer; an unseen prop remains unverified. Visitor claims do not change facts, and residents cannot read one another's private plans.

## Conversation and behavior

The small LLM tier classifies free-form questions into five intents: work, routine, neighbors, help, or unknown. Code validates that label and renders an answer from current observations and authored knowledge. Unchecked model prose is never spoken. Greetings, exact prop questions, and workplace requests use scripts; long conversation history and pronoun-dependent follow-ups are not supported.

`BackgroundLLM` allows movement to continue while a request runs. Each resident has one outstanding request, a 15-second timeout, and at most three calls per day: 30 for ten residents. The prompt requests one label; platform quota bounds token use. Neighbor chat needs no model. Failed access, asynchronous errors, exhausted allowance, or unusable results receive a scripted answer or uncertainty. A pending answer is dropped when the listener leaves or asks a newer question. Credentials are never committed; the platform supplies runtime access.

The normal day retains work, midday meetings, brief visitor greetings, and night sleep. "Show me your workplace" temporarily selects a walk for up to 100 ticks while the visitor stays nearby. Night takes priority and the resident refuses. The reply promises movement toward the workplace, not guaranteed arrival through a crowd. Navigation retains the prior connected-region checks, cached approaches, crowd penalties, and waypoint speed control.

## Season 4 revision and reflection

Season 4 received 3.6/5 from five peers despite 100 automated completion scores. Peers wanted more than repetitive greetings and job labels. This revision adds character motives, current-state questions, explicit knowledge limits, and a conversation-triggered workplace walk. The common schedule remains a limitation.

An extra break schedule caused a prop-use regression and was removed. Porting navigation also exposed float32 rounding at the use boundary; the approach now checks a small geometric margin before interacting. Keeping reliable behavior mattered more than unverified variety.

## Verification

Use Python 3.12 and the unchanged pinned requirements. `season.json` contains the downloaded ten-villager/day-night Season 5 settings.

```sh
python -m sandbox test
python -m sandbox eval --seeds 0 1 2
python -m sandbox play --seed 1
```

- Final checks: 126 passed in 63.93 seconds, with seven supplied Gymnasium casting warnings; `git diff --check` passed. Protected environment files and supplied tests were not edited.
- Complete local evaluations: seeds 0/1/2 each scored 100.00. No development key was configured, so these do not prove upstream model success. One neighbor message was dropped by the recipient policy; the day completed.
- Added behavioral tests cover lit→unlit→unseen facts, an unknowable question, changed plans during pending requests, malformed output, synchronous/asynchronous failures, exhausted allowance, and daytime/night workplace requests. Successful model outputs in these tests are doubles.
- Actual seed-1 platform questions produced uncertainty about an unseen bell and secret future events, and accepted a workplace request. The replay records 154 LLM units, establishing actual upstream use. An occupation question was answered unhelpfully; that prompted a broader job fallback, retention of the pending question on errors, punctuation-tolerant parsing, and removal of a very small completion cap. The original cause was not verified.

Detailed messages, interrupted-session limits, and raw results are in `evidence/`. Completion scores do not measure conversation quality.

## AI use

This submission was developed with OpenAI Codex. Codex read the assignment and feedback, adapted Neighbor, wrote dialogue and request handling, retained navigation fixes, added behavioral tests, ran checks and seeded days, operated platform visitor tests, and drafted this README. The official template supplied the environment, routine framework, routing, and background LLM client. This account of validation does not claim the student personally operated those tests.

The main lesson was to separate understanding a question from asserting a world fact. A model can interpret wording, while code checks the current state and refuses unsupported claims. The smaller conversation vocabulary is the cost of that choice; broader dialogue still needs work.
