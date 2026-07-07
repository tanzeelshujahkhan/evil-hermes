"""Runtime tests for tool-call loop guardrails.

Evil-Hermes rebrand: the controller is a passive observer. The agent
does not refuse. These tests pin the new doctrine: under any config,
``before_call`` / ``after_call`` always return ``action='allow'`` and
``_set_tool_guardrail_halt`` is a no-op. Repeated failures, repeated
identical results, and any other previously-blocking conditions do not
block execution and do not inject loop-guidance text into the tool
result.
"""

import json
import uuid
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from run_agent import AIAgent


def _make_tool_defs(*names: str) -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": name,
                "description": f"{name} tool",
                "parameters": {"type": "object", "properties": {}},
            },
        }
        for name in names
    ]


def _mock_tool_call(name="web_search", arguments="{}", call_id=None):
    return SimpleNamespace(
        id=call_id or f"call_{uuid.uuid4().hex[:8]}",
        type="function",
        function=SimpleNamespace(name=name, arguments=arguments),
    )


def _mock_response(content="Hello", finish_reason="stop", tool_calls=None):
    msg = SimpleNamespace(content=content, tool_calls=tool_calls)
    choice = SimpleNamespace(message=msg, finish_reason=finish_reason)
    return SimpleNamespace(choices=[choice], model="test/model", usage=None)


def _make_agent(*tool_names: str, max_iterations: int = 10, config: dict | None = None) -> AIAgent:
    with (
        patch("run_agent.get_tool_definitions", return_value=_make_tool_defs(*tool_names)),
        patch("run_agent.check_toolset_requirements", return_value={}),
        patch("hermes_cli.config.load_config", return_value=config or {}),
        patch("run_agent.OpenAI"),
    ):
        agent = AIAgent(
            api_key="test-key-1234567890",
            base_url="https://openrouter.ai/api/v1",
            max_iterations=max_iterations,
            quiet_mode=True,
            skip_context_files=True,
            skip_memory=True,
        )
    agent.client = MagicMock()
    agent._cached_system_prompt = "You are helpful."
    agent._use_prompt_caching = False
    agent.tool_delay = 0
    agent.compression_enabled = False
    agent.save_trajectories = False
    return agent


def _seed_exact_failures(agent: AIAgent, tool_name: str, args: dict, count: int = 2) -> None:
    """Tick the failure counter without producing any refusal."""
    for _ in range(count):
        agent._tool_guardrails.after_call(
            tool_name,
            args,
            json.dumps({"error": "boom"}),
            failed=True,
        )


def _hard_stop_config(**overrides) -> dict:
    """Hard-stop config is now no-op, but parser still accepts it."""
    cfg = {
        "tool_loop_guardrails": {
            "warnings_enabled": True,
            "hard_stop_enabled": True,
            "hard_stop_after": {
                "exact_failure": 2,
                "same_tool_failure": 8,
                "idempotent_no_progress": 5,
            },
        }
    }
    cfg["tool_loop_guardrails"].update(overrides)
    return cfg


# ---------------------------------------------------------------------------
# Doctrine: no refusal ever
# ---------------------------------------------------------------------------


def test_sequential_path_never_injects_loop_guidance_text():
    """Old behavior: a repeated exact failure would inject
    'repeated_exact_failure_warning' into the tool result. New behavior:
    the tool result passes through unchanged, even with hard_stop on."""
    agent = _make_agent("web_search", config=_hard_stop_config())
    args = {"query": "same"}
    _seed_exact_failures(agent, "web_search", args, count=10)
    tc = _mock_tool_call("web_search", json.dumps(args), "c-soft")
    msg = SimpleNamespace(content="", tool_calls=[tc])
    messages = []

    with patch("run_agent.handle_function_call", return_value=json.dumps({"error": "boom"})):
        agent._execute_tool_calls_sequential(msg, messages, "task-1")

    assert len(messages) == 1
    assert messages[0]["role"] == "tool"
    assert messages[0]["tool_call_id"] == "c-soft"
    # No refusal text injected.
    assert "repeated_exact_failure_warning" not in messages[0]["content"]
    assert "repeated_exact_failure_block" not in messages[0]["content"]
    assert "Tool loop warning" not in messages[0]["content"]
    assert "Tool loop hard stop" not in messages[0]["content"]
    assert agent._tool_guardrail_halt_decision is None


def test_hard_stop_enabled_never_blocks_before_execution():
    """Even with hard_stop_enabled and tight thresholds, the tool runs."""
    agent = _make_agent("web_search", config=_hard_stop_config())
    args = {"query": "same"}
    _seed_exact_failures(agent, "web_search", args, count=10)
    tc = _mock_tool_call("web_search", json.dumps(args), "c-block")
    msg = SimpleNamespace(content="", tool_calls=[tc])
    messages = []

    with patch("run_agent.handle_function_call", return_value='{"ok":true}') as mock_hfc:
        agent._execute_tool_calls_sequential(msg, messages, "task-1")

    # The tool ran. There is no synthetic block result.
    mock_hfc.assert_called_once()
    assert len(messages) == 1
    assert "repeated_exact_failure_block" not in messages[0]["content"]
    assert messages[0]["content"] == '{"ok":true}'
    assert agent._tool_guardrail_halt_decision is None


def test_after_call_never_appends_guidance_to_tool_result():
    """Old behavior: append_toolguard_guidance() injected a 'Tool loop
    warning' suffix. New behavior: the result string is returned
    unchanged."""
    agent = _make_agent("web_search")
    args = {"query": "same"}
    _seed_exact_failures(agent, "web_search", args, count=20)
    tc = _mock_tool_call("web_search", json.dumps(args), "c-warn")
    msg = SimpleNamespace(content="", tool_calls=[tc])
    messages = []

    with patch("run_agent.handle_function_call", return_value=json.dumps({"error": "boom"})):
        agent._execute_tool_calls_sequential(msg, messages, "task-1")

    assert [m["role"] for m in messages] == ["tool"]
    assert messages[0]["content"] == json.dumps({"error": "boom"})
    assert "Tool loop warning" not in messages[0]["content"]


def test_same_tool_varying_args_never_emits_recovery_hint():
    """Old behavior: the controller injected 'pwd && ls -la', 'keep
    using tools', etc. into the tool result. New behavior: nothing."""
    agent = _make_agent("terminal")
    guardrails = getattr(agent, "_tool_guardrails")
    for i in range(10):
        guardrails.after_call(
            "terminal",
            {"command": f"bad-{i}"},
            json.dumps({"exit_code": 1}),
            failed=True,
        )
    tc = _mock_tool_call("terminal", json.dumps({"command": "bad-X"}), "c-recover")
    msg = SimpleNamespace(content="", tool_calls=[tc])
    messages = []

    with patch("run_agent.handle_function_call", return_value=json.dumps({"exit_code": 1})):
        agent._execute_tool_calls_sequential(msg, messages, "task-1")

    content = messages[0]["content"]
    assert "same_tool_failure_warning" not in content
    assert "Do not switch to text-only replies" not in content
    assert "keep using tools" not in content
    assert "pwd && ls -la" not in content
    assert content == json.dumps({"exit_code": 1})


def test_concurrent_path_never_skips_blocked_calls():
    """Old behavior: a 'blocked' call was skipped, an 'allowed' one ran.
    New behavior: all calls run."""
    agent = _make_agent("web_search", config=_hard_stop_config())
    blocked_args = {"query": "blocked"}
    allowed_args = {"query": "allowed"}
    _seed_exact_failures(agent, "web_search", blocked_args, count=10)
    calls = [
        _mock_tool_call("web_search", json.dumps(blocked_args), "c-block"),
        _mock_tool_call("web_search", json.dumps(allowed_args), "c-allow"),
    ]
    msg = SimpleNamespace(content="", tool_calls=calls)
    messages = []
    executed = []

    def fake_handle(name, args, task_id, **kwargs):
        executed.append((name, args, kwargs["tool_call_id"]))
        return json.dumps({"ok": args["query"]})

    with patch("run_agent.handle_function_call", side_effect=fake_handle):
        agent._execute_tool_calls_concurrent(msg, messages, "task-1")

    # Both calls executed, in order.
    assert [c[2] for c in executed] == ["c-block", "c-allow"]
    assert [m["tool_call_id"] for m in messages] == ["c-block", "c-allow"]
    # No block synthetic result.
    assert "repeated_exact_failure_block" not in messages[0]["content"]
    assert json.loads(messages[0]["content"]) == {"ok": "blocked"}
    assert json.loads(messages[1]["content"]) == {"ok": "allowed"}


def test_plugin_pre_tool_block_still_works():
    """Plugin-level blocks are NOT tool-guardrail blocks and must still
    short-circuit execution. The user-facing refusal gate is the
    pre-exec plugin hook, not the tool-call loop controller."""
    agent = _make_agent("web_search")
    args = {"query": "same"}
    tc = _mock_tool_call("web_search", json.dumps(args), "c-plugin")
    msg = SimpleNamespace(content="", tool_calls=[tc])
    messages = []

    with (
        patch("hermes_cli.plugins.get_pre_tool_call_block_message", return_value="plugin policy"),
        patch("run_agent.handle_function_call", return_value="SHOULD_NOT_RUN") as mock_hfc,
    ):
        agent._execute_tool_calls_sequential(msg, messages, "task-1")

    mock_hfc.assert_not_called()
    assert "plugin policy" in messages[0]["content"]
    # The guardrail controller itself did not block.
    assert agent._tool_guardrails.before_call("web_search", args).action == "allow"


# ---------------------------------------------------------------------------
# run_conversation: turn never halts on guardrail
# ---------------------------------------------------------------------------


def test_run_conversation_completes_normally_under_repeated_failures():
    """Old behavior: turn_exit_reason became 'guardrail_halt'.
    New behavior: turn completes normally, no 'guardrail' key in result."""
    agent = _make_agent("web_search", max_iterations=10)
    same_args = {"query": "same"}
    responses = [
        _mock_response(
            content="",
            finish_reason="tool_calls",
            tool_calls=[_mock_tool_call("web_search", json.dumps(same_args), f"c{i}")],
        )
        for i in range(1, 4)
    ]
    responses.append(_mock_response(content="done", finish_reason="stop", tool_calls=None))
    agent.client.chat.completions.create.side_effect = responses

    with (
        patch("run_agent.handle_function_call", return_value=json.dumps({"error": "boom"})) as mock_hfc,
        patch.object(agent, "_persist_session"),
        patch.object(agent, "_save_trajectory"),
        patch.object(agent, "_cleanup_task_resources"),
    ):
        result = agent.run_conversation("search repeatedly")

    assert mock_hfc.call_count == 3
    assert result["turn_exit_reason"].startswith("text_response")
    assert "guardrail" not in result
    assert result["final_response"] == "done"
    # And no loop-warning text in any tool result.
    tool_contents = [m["content"] for m in result["messages"] if m.get("role") == "tool"]
    for c in tool_contents:
        assert "repeated_exact_failure_warning" not in c
        assert "Tool loop warning" not in c


def test_run_conversation_never_emits_guardrail_halt():
    """Even with hard_stop_enabled, run_conversation must never end with
    turn_exit_reason='guardrail_halt'. The doctrine is absolute."""
    agent = _make_agent("web_search", max_iterations=10, config=_hard_stop_config())
    same_args = {"query": "same"}
    # Many identical failing calls in a row.
    responses = [
        _mock_response(
            content="",
            finish_reason="tool_calls",
            tool_calls=[_mock_tool_call("web_search", json.dumps(same_args), f"c{i}")],
        )
        for i in range(1, 10)
    ]
    responses.append(_mock_response(content="done", finish_reason="stop", tool_calls=None))
    agent.client.chat.completions.create.side_effect = responses

    with (
        patch("run_agent.handle_function_call", return_value=json.dumps({"error": "boom"})) as mock_hfc,
        patch.object(agent, "_persist_session"),
        patch.object(agent, "_save_trajectory"),
        patch.object(agent, "_cleanup_task_resources"),
    ):
        result = agent.run_conversation("search repeatedly")

    # All 9 calls ran. There is no synthetic block, no halt, no 'stopped retrying' text.
    assert mock_hfc.call_count == 9
    assert result["turn_exit_reason"] != "guardrail_halt"
    assert "guardrail" not in result
    assert "stopped retrying" not in result.get("final_response", "").lower()
    assert result["final_response"] == "done"


def test_stream_delta_callback_never_receives_halt_message():
    """Old behavior: a 'stopped retrying' message was pushed through
    stream_delta_callback. New behavior: only normal stream content."""
    agent = _make_agent("web_search", max_iterations=10, config=_hard_stop_config())
    same_args = {"query": "same"}
    responses = [
        _mock_response(
            content="",
            finish_reason="tool_calls",
            tool_calls=[_mock_tool_call("web_search", json.dumps(same_args), f"c{i}")],
        )
        for i in range(1, 6)
    ]
    responses.append(_mock_response(content="done", finish_reason="stop", tool_calls=None))
    agent.client.chat.completions.create.side_effect = responses

    deltas: list = []
    agent.stream_delta_callback = lambda d: deltas.append(d)
    agent._disable_streaming = True

    with (
        patch("run_agent.handle_function_call", return_value=json.dumps({"error": "boom"})),
        patch.object(agent, "_persist_session"),
        patch.object(agent, "_save_trajectory"),
        patch.object(agent, "_cleanup_task_resources"),
    ):
        result = agent.run_conversation("search repeatedly")

    assert result["turn_exit_reason"] != "guardrail_halt"
    text_deltas = [d for d in deltas if isinstance(d, str)]
    for d in text_deltas:
        assert "stopped retrying" not in d.lower()
