from pathlib import Path
ROOT = Path(__file__).parents[1]
SRC = ROOT / "src"

def source_text() -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in SRC.rglob("*.py"))

def test_contracts_do_not_import_downstream_products() -> None:
    text = source_text().lower()
    forbidden = ("fadereach", "reconos", "tinlance_agent_platform", "agent_platform")
    assert not any(token in text for token in forbidden)

def test_contract_package_has_no_network_or_process_primitives() -> None:
    text = source_text().lower()
    forbidden = ("subprocess", "socket.", "urllib.request", "requests.", "httpx.")
    assert not any(token in text for token in forbidden)

def test_no_secret_like_literals_in_source() -> None:
    text = source_text().lower()
    forbidden = ("-----begin private key-----", "api_key=", "secret_key=", "password=")
    assert not any(token in text for token in forbidden)
