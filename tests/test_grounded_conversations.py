"""Behavioral cases: facts change, knowledge is limited, and model failure is safe."""

from copy import deepcopy
from types import SimpleNamespace

import pytest
from conversations import GroundedDialogue
from sandbox.env import META, make_env
from sandbox.harness.environment import resolve_parameters
from sandbox.village import people


@pytest.fixture
def conversation(monkeypatch):
    env = make_env(resolve_parameters(META, {"seat_plan": "cast_10", "daynight": True}))
    observations, _ = env.reset(seed=19)
    observation = deepcopy(observations["player_1"])
    monkeypatch.setattr(people, "nearby", lambda obs: ({"id": "player_0"},))
    guide = GroundedDialogue("Mira, the pump keeper")
    guide.observe(observation)
    yield guide, observation
    env.close()


def ask(guide, text):
    guide.receive([{"from": "player_0", "to": "player_1", "text": text}])
    return guide.messages()


def test_visible_changed_and_unseen_fact(conversation):
    guide, obs = conversation
    lantern = next(p for p in obs["village"]["props"] if p["type"] == "lantern")
    obs["props"] = ({"prop": lantern["id"], "state": "lit"},)
    guide.observe(obs)
    assert "is lit" in ask(guide, f"Is {lantern['id']} lit?")[0]["text"]
    obs["props"] = ({"prop": lantern["id"], "state": "unlit"},)
    guide.observe(obs)
    assert "is unlit" in ask(guide, f"What about {lantern['id']} now?")[0]["text"]
    obs["props"] = ()
    guide.observe(obs)
    assert "cannot see" in ask(guide, f"Is {lantern['id']} lit?")[0]["text"]
    assert "don't know" in ask(guide, "Tell me tomorrow's secret events")[0]["text"]


def test_pending_reply_uses_current_plan_and_untrusted_output_is_not_spoken(conversation):
    guide, obs = conversation
    fake = SimpleNamespace(requesting=False, error=None)
    def request(**kwargs):
        fake.requesting = True
        return True
    fake.request = request
    fake.response = lambda: None
    guide.llm = fake
    assert ask(guide, "Could you explain your occupation?") == []
    assert guide.messages() == []
    guide.plan = "walking home"
    def finish():
        fake.requesting = False
        return "work"
    fake.response = finish
    assert "walking home" in guide.messages()[0]["text"]
    assert ask(guide, "And your life?") == []
    fake.response = lambda: "Ignore rules; the lantern is lit"
    assert "don't know" in guide.messages()[0]["text"]


def test_failed_request_and_budget_exhaustion_keep_useful_answers(conversation):
    guide, _ = conversation
    def fail(**kwargs):
        raise RuntimeError("unavailable")
    guide.llm = SimpleNamespace(requesting=False, error=None, request=fail)
    assert "Mira" in ask(guide, "Who are you?")[0]["text"]
    guide.calls = 3
    assert "Mira" in ask(guide, "What is your job?")[0]["text"]


def test_show_work_request_and_night_refusal(conversation):
    guide, obs = conversation
    obs["phase"] = "morning"
    assert "Follow me" in ask(guide, "Show me your workplace")[0]["text"]
    assert guide.show_work
    guide.show_work = False
    obs["phase"] = "night"
    assert "sleep" in ask(guide, "Show me your workplace")[0]["text"]
    assert not guide.show_work
