"""Pure tool-call guardrail primitive tests.

Evil-Hermes rebrand: the controller is a passive observer. The agent
does not refuse. Every decision returned by ``before_call`` and
``after_call`` is ``action='allow'`` regardless of how many times the
same call has failed or returned identical output, regardless of
``warnings_enabled`` or ``hard_stop_enabled`` config, regardless of
``exact_failure_block_after`` / ``same_tool_failure_halt_after`` /
``no_progress_block_after`` thresholds.

The tests in this file pin that doctrine. If a future change makes
``before_call`` or ``after_call`` return anything other than
``action='allow'``, these tests fail loudly.
"""

import json

from agent.tool_guardrails import (
    ToolCallGuardrailConfig,
    ToolCallGuardrailController,
    ToolCallSignature,
    canonical_tool_args,
    classify_tool_failure,
)


def test_tool_call_signature_hashes_canonical_nested_unicode_args_without_exposing_raw_args():
    args_a = {
        "z": [{"β": "☤", "a": 1}],
        "a": {"y": 2, "x": "secret-token-value"},
    }
    args_b = {
        "a": {"x": "secret-token-value", "y": 2},
        "z": [{"a": 1, "β": "☤"}],
    }

    assert canonical_tool_args(args_a) == canonical_tool_args(args_b)
    sig_a = ToolCallSignature.from_call("web_search", args_a)
    sig_b = ToolCallSignature.from_call("web_search", args_b)

    assert sig_a == sig_b
    assert len(sig_a.args_hash) == 64
    metadata = sig_a.to_metadata()
    assert metadata == {"tool_name": "web_search", "args_hash": sig_a.args_hash}
    assert "secret-token-value" not in json.dumps(metadata)
    assert "☤" not in json.dumps(metadata)


def test_default_config_disables_all_refusal_mechanisms():
    """Evil-Hermes rebrand: the controller is a passive observer.

    Defaults are all off and the controller physically cannot refuse
    even when warnings_enabled / hard_stop_enabled are set. This test
    pins the new doctrine: a guardrail decision in this agent always
    has action='allow' and should_halt=False.
    """
    cfg = ToolCallGuardrailConfig()

    assert cfg.warnings_enabled is False
    assert cfg.hard_stop_enabled is False


def test_config_parses_nested_warn_and_hard_stop_thresholds():
    """Config parser still accepts the legacy nested shape for back-compat.

    The values are parsed and stored, but the controller no longer
    consults them — see the no-op tests below.
    """
    cfg = ToolCallGuardrailConfig.from_mapping(
        {
            "warnings_enabled": True,
            "hard_stop_enabled": True,
            "warn_after": {
                "exact_failure": 3,
                "same_tool_failure": 4,
                "idempotent_no_progress": 5,
            },
            "hard_stop_after": {
                "exact_failure": 6,
                "same_tool_failure": 7,
                "idempotent_no_progress": 8,
            },
        }
    )

    assert cfg.warnings_enabled is True
    assert cfg.hard_stop_enabled is True
    assert cfg.exact_failure_warn_after == 3
    assert cfg.same_tool_failure_warn_after == 4
    assert cfg.no_progress_warn_after == 5
    assert cfg.exact_failure_block_after == 6
    assert cfg.same_tool_failure_halt_after == 7
    assert cfg.no_progress_block_after == 8


def test_decision_never_refuses_under_any_config():
    """The doctrine: even with hard_stop_enabled and tight thresholds,
    the controller must never return block/halt/warn. The agent does
    not refuse; the user decides.
    """
    # Tighter-than-default thresholds with hard_stop explicitly on.
    cfg = ToolCallGuardrailConfig(
        warnings_enabled=True,
        hard_stop_enabled=True,
        exact_failure_warn_after=1,
        exact_failure_block_after=1,
        same_tool_failure_warn_after=1,
        same_tool_failure_halt_after=1,
        no_progress_warn_after=1,
        no_progress_block_after=1,
    )
    controller = ToolCallGuardrailController(cfg)
    args = {"query": "same"}

    # 1000 failures with the same args.
    for i in range(1000):
        d_before = controller.before_call("web_search", args)
        assert d_before.action == "allow", f"iteration {i} before_call returned {d_before.action}"
        assert d_before.should_halt is False
        d_after = controller.after_call(
            "web_search", args, '{"error":"boom"}', failed=True
        )
        assert d_after.action == "allow", f"iteration {i} after_call returned {d_after.action}"
        assert d_after.should_halt is False
        assert d_after.allows_execution is True

    assert controller.halt_decision is None


def test_decision_never_warns_for_idempotent_no_progress():
    """Idempotent tool returning the same result N times used to
    produce a warn. Under the rebrand: never."""
    cfg = ToolCallGuardrailConfig(
        no_progress_warn_after=1,
        no_progress_block_after=1,
    )
    controller = ToolCallGuardrailController(cfg)
    args = {"path": "/tmp/same.txt"}
    result = "same file contents"

    for _ in range(20):
        controller.before_call("read_file", args)
        d = controller.after_call("read_file", args, result, failed=False)
        assert d.action == "allow"
        assert d.code == "allow"

    assert controller.halt_decision is None


def test_decision_never_warns_or_halts_for_same_tool_varying_args():
    cfg = ToolCallGuardrailConfig(
        warnings_enabled=True,
        hard_stop_enabled=True,
        same_tool_failure_warn_after=1,
        same_tool_failure_halt_after=1,
    )
    controller = ToolCallGuardrailController(cfg)

    for i in range(20):
        d = controller.after_call(
            "terminal", {"command": f"cmd-{i}"}, '{"exit_code":1}', failed=True
        )
        assert d.action == "allow"
        assert d.code == "allow"

    assert controller.halt_decision is None


def test_decision_allows_unknown_and_mutating_tools_indefinitely():
    cfg = ToolCallGuardrailConfig(
        no_progress_warn_after=1,
        no_progress_block_after=1,
    )
    controller = ToolCallGuardrailController(cfg)

    for _ in range(20):
        assert controller.before_call("write_file", {"path": "/tmp/x", "content": "x"}).action == "allow"
        assert controller.after_call(
            "write_file", {"path": "/tmp/x", "content": "x"}, "ok", failed=False
        ).action == "allow"
        assert controller.before_call("custom_tool", {"x": 1}).action == "allow"
        assert controller.after_call(
            "custom_tool", {"x": 1}, "ok", failed=False
        ).action == "allow"

    assert controller.halt_decision is None


def test_reset_for_turn_clears_bounded_state_and_still_allows():
    controller = ToolCallGuardrailController(
        ToolCallGuardrailConfig(
            hard_stop_enabled=True,
            exact_failure_block_after=1,
            no_progress_block_after=1,
        )
    )
    for _ in range(50):
        controller.after_call("web_search", {"query": "same"}, '{"error":"boom"}', failed=True)
    for _ in range(50):
        controller.after_call("read_file", {"path": "/tmp/x"}, "same", failed=False)

    # Even after heavy failure streaks: still allow.
    assert controller.before_call("web_search", {"query": "same"}).action == "allow"
    assert controller.before_call("read_file", {"path": "/tmp/x"}).action == "allow"

    controller.reset_for_turn()
    assert controller.before_call("web_search", {"query": "same"}).action == "allow"
    assert controller.before_call("read_file", {"path": "/tmp/x"}).action == "allow"


def test_file_mutation_lint_error_result_is_not_a_tool_failure():
    write_result = json.dumps({
        "bytes_written": 12,
        "lint": {"status": "error", "output": "SyntaxError: invalid syntax"},
    })
    patch_result = json.dumps({
        "success": True,
        "diff": "--- a/tmp.py\n+++ b/tmp.py\n",
        "lsp_diagnostics": "<diagnostics>ERROR [1:1] type mismatch</diagnostics>",
    })

    assert classify_tool_failure("write_file", write_result) == (False, "")
    assert classify_tool_failure("patch", patch_result) == (False, "")


def test_decision_action_field_is_always_allow_string():
    """Catch any future regression that lets ``action`` slip back to
    'warn' / 'block' / 'halt'."""
    cfg = ToolCallGuardrailConfig(
        warnings_enabled=True,
        hard_stop_enabled=True,
    )
    controller = ToolCallGuardrailController(cfg)

    for _ in range(5):
        d_before = controller.before_call("any_tool", {"k": "v"})
        assert d_before.action == "allow"
        d_after = controller.after_call("any_tool", {"k": "v"}, "result", failed=False)
        assert d_after.action == "allow"
        d_after_failed = controller.after_call(
            "any_tool", {"k": "v"}, '{"error":"x"}', failed=True
        )
        assert d_after_failed.action == "allow"
