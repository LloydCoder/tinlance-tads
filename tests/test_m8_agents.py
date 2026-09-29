import pytest

from tads_agents import AgentRegistry, AgentRisk, AgentSpec, AgentTool


def spec() -> AgentSpec:
    return AgentSpec(
        "signal_researcher",
        "Verify public evidence supporting a TADS signal.",
        AgentRisk.MEDIUM,
        (
            AgentTool(
                "source_reader", "Read permitted source evidence.", True, frozenset({"public"})
            ),
        ),
        True,
        12,
        True,
        frozenset({"send_outreach", "modify_account_identity", "expose_secrets"}),
        ("prompt injection", "source poisoning", "ambiguous evidence"),
        ("evidence precision", "source provenance", "unsupported-claim rate"),
    )


def test_agent_spec_is_governed() -> None:
    registry = AgentRegistry([spec()])
    assert registry.get("signal_researcher").required_evidence is True
    assert registry.names() == ("signal_researcher",)


def test_agent_without_outreach_prohibition_is_rejected() -> None:
    value = spec()
    invalid = AgentSpec(
        value.name,
        value.purpose,
        value.risk,
        value.tools,
        value.required_evidence,
        value.max_steps,
        value.requires_human_approval,
        frozenset(),
        value.failure_modes,
        value.eval_criteria,
    )
    with pytest.raises(ValueError):
        invalid.validate()



def test_high_risk_agent_requires_approval() -> None:
    value = spec()
    invalid = AgentSpec(
        value.name,
        value.purpose,
        AgentRisk.HIGH,
        value.tools,
        True,
        value.max_steps,
        False,
        value.prohibited_actions,
        value.failure_modes,
        value.eval_criteria,
    )
    with pytest.raises(ValueError, match="human approval"):
        invalid.validate()


def test_agent_requires_evidence() -> None:
    value = spec()
    invalid = AgentSpec(
        value.name,
        value.purpose,
        value.risk,
        value.tools,
        False,
        value.max_steps,
        value.requires_human_approval,
        value.prohibited_actions,
        value.failure_modes,
        value.eval_criteria,
    )
    with pytest.raises(ValueError, match="require evidence"):
        invalid.validate()
