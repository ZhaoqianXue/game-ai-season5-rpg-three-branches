# Season 5 — RPG: The Conversation

**Zhaoqian Xue / purpleman / GitHub @ZhaoqianXue**

## Design goal

Visitors should learn who the villagers are, why they do their jobs, and how their words match their current activities. They can ask about a visible prop or request a daytime walk toward a villager's workplace; distant or private facts receive an honest uncertainty statement.

**Rating question (1–5):** How well did the villagers' replies and workplace tours match what they could see and what they were doing?

## Characters, knowledge, and behavior

The ten villagers retain the Neighbor template's work, midday meeting, brief visitor greeting, and night sleep. `PERSONAS` and `STORIES` in `conversations.py` provide authored identities and motives: Mira tends the pump for the gardeners, Rowan cares for notices, Tess repairs, Ash tends the hearth, Bell minds the bell, three traders have different attitudes, and Fern/Reed garden. These are authored character backgrounds, not claims inferred from hidden game state.

Each character knows its own selected routine and workplace. Current prop states come **only** from `props.seen()`; static placement does not establish a prop's current state. For example, a visible lantern is described from this tick's observation, a changed state replaces the old answer, and an unseen lantern remains unverified. The agent makes no claim to know another villager's private plans. Visitor statements never change world facts.

Free-form questions may use the platform's **small** LLM tier to choose one of five intents: work, routine, neighbors, help, or unknown. The code validates that label and renders the reply from current observations and authored knowledge. It does not speak unvalidated model prose. This trades conversational breadth for reliable facts. Exact prop questions, greetings, and workplace requests are scripted. Follow-ups requiring long conversation memory are not supported.

`BackgroundLLM` keeps movement running during requests. There is one outstanding call per resident, a 15-second request timeout, at most **three calls per resident per day** (30 for ten villagers), and a 16-token completion request. Neighbor small talk costs no model tokens. Missing credentials, exhausted quota, invalid responses, or exhausted call allowance fall back to a short scripted explanation or uncertainty. Replies are dropped when the listener leaves or a newer question supersedes them; answers are rendered against current facts when they arrive. Secrets belong in ignored `.env`, never source control; the platform supplies runtime credentials.

“Show me your workplace” starts a temporary walk during the day, for up to 100 ticks while the visitor remains nearby. Night takes priority and the character refuses the request. The reply promises a walk toward the workplace, not guaranteed arrival through a crowd. Existing work and sleep resume afterward. Navigation retains the previous season's connected-region checks, cached approaches, soft crowd avoidance, and waypoint speed control.

## Season 4 feedback and revision

Season 4 received 3.6/5 from five peers, despite 100 automated completion scores. Peers found the schedules repetitive and wanted more than greetings and job labels. This revision adds distinct character motives, current-state questions, explicit limits on knowledge, and a conversation-triggered workplace walk. Neighbor greetings now identify the speaker and their work. The common day schedule remains a limitation; a completion score does not measure conversation quality.

An attempted extra break schedule caused a prop-use regression in the full-day test and was removed. Porting the prior navigation also exposed float32 rounding at the interaction boundary: a prop could appear just within reach while the engine still rejected use. The approach now checks a small geometric margin and takes a short inward step before using a boundary prop. The route caller retains the standard three-argument interface while applying crowd costs to its graph. Keeping the day reliable mattered more than adding unverified variety.

## Reproduce and verification

Based on the official [Neighbor example](https://github.com/vox-deorum/game-agent-template/tree/examples/three_branches/neighbor), with the platform's downloaded ten-villager/day-night Season 5 settings. Use Python 3.12 and unchanged requirements.

```sh
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m sandbox test
python -m sandbox eval --seeds 0 1 2
python -m sandbox play --seed 0
```

`tests/test_grounded_conversations.py` checks a lit→unlit→unseen prop, an unknowable question, a pending reply with a changed plan, malformed model text, failed access, exhausted call allowance, and daytime/night workplace requests. Those model responses are test doubles, not evidence of successful upstream LLM calls. The supplied full-day check verifies movement, work in morning/evening, legal actions, and sleeping at home. Additional run results and visitor observations are recorded in `evidence/`.

Final project checks: **125 passed**, with seven supplied Gymnasium input-casting warnings, in 76.74 seconds. `git diff --check` passed; the environment, manifest, dependencies, and supplied tests were not edited.

## AI use and reflection

This submission was developed with **OpenAI Codex**. Codex read the assignment and Season 4 feedback, adapted Neighbor, wrote the grounded dialogue and request handler, retained prior navigation fixes, added behavioral tests, ran checks, and drafted this README. The official template supplied the environment, routines, routing framework, and background LLM client. No sandbox, manifest, or dependency files were manually changed. Verification combines deterministic conversation scenarios, full seeded days, and recorded visitor observations; it does not imply that the student personally operated those tests.

The main design lesson was to separate understanding a question from asserting a world fact. A model can recognize wording, while code reads the current visible state and refuses unsupported claims. The tradeoff is a smaller conversation vocabulary; open-ended storytelling and multi-turn references need further work.
