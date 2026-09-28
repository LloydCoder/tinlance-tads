import ast
from pathlib import Path

ROOT = Path(__file__).parents[1]
SRC = ROOT / "src"


def python_files() -> list[Path]:
    return list(SRC.rglob("*.py"))


def test_contracts_do_not_import_product_implementations() -> None:
    forbidden = {"fadereach", "reconos", "tinlance_agent_platform", "agent_platform"}
    for path in python_files():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert all(alias.name.lower() not in forbidden for alias in node.names)
            if isinstance(node, ast.ImportFrom) and node.module:
                assert node.module.lower() not in forbidden


def test_contract_package_has_no_network_or_process_primitives() -> None:
    contract_files = list((SRC / "tads_contracts").rglob("*.py"))
    text = "\n".join(path.read_text(encoding="utf-8") for path in contract_files).lower()
    forbidden = ("subprocess", "socket.", "urllib.request", "requests.", "httpx.")
    assert not any(token in text for token in forbidden)


def test_no_secret_like_literals_in_source() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in python_files()).lower()
    forbidden = ("-----begin private key-----", "api_key=", "secret_key=", "password=")
    assert not any(token in text for token in forbidden)
