"""Behavior tests for the actual JavaScript application, driven by pytest."""
import json
import os
from pathlib import Path
import shutil
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def app():
    node = shutil.which("node")
    if node is None and os.name == "nt":
        # VS Code opened before installation may still have the old PATH.
        installed_node = Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "nodejs/node.exe"
        if installed_node.is_file():
            node = str(installed_node)
    if node is None:
        pytest.fail("Node.js is required to execute src/script.js. Install Node.js 20+.")

    def run(scenario):
        result = subprocess.run(
            [node, str(ROOT / "tests/run_app.cjs")],
            input=scenario, text=True, encoding="utf-8", capture_output=True,
            cwd=ROOT, timeout=10,
        )
        assert result.returncode == 0, result.stderr
        return json.loads(result.stdout)

    return run


@pytest.mark.parametrize("transactions,expected", [
    ([], {"rec": 0, "dep": 0, "sal": 0}),
    ([{"tipo": "receita", "val": 1000}, {"tipo": "despesa", "val": 250}],
     {"rec": 1000, "dep": 250, "sal": 750}),
    ([{"tipo": "despesa", "val": 300}], {"rec": 0, "dep": 300, "sal": -300}),
    ([{"tipo": "receita", "val": 10.5}, {"tipo": "receita", "val": 20.25},
      {"tipo": "despesa", "val": 5.75}], {"rec": 30.75, "dep": 5.75, "sal": 25}),
])
def test_totals(app, transactions, expected):
    assert app(f"TX = {json.dumps(transactions)}; totals();") == expected


@pytest.mark.parametrize("value,expected", [(0, "R$\u00a00,00"),
    (1234.56, "R$\u00a01.234,56"), (-25, "R$\u00a025,00")])
def test_currency_format(app, value, expected):
    assert app(f"R({value});") == expected


def test_local_storage_round_trip(app):
    result = app('''
        GOALS = [{id: 7, nome: 'Viagem', alvo: 5000, atual: 1250}];
        CEVS = [{id: 8, titulo: 'Aluguel', data: '2026-11-05', val: 900}];
        dark = true; slim = true;
        saveData();
        GOALS = []; CEVS = []; dark = false; slim = false;
        loadData();
        ({goals: GOALS, events: CEVS, dark, slim});
    ''')
    assert result == {"goals": [{"id": 7, "nome": "Viagem", "alvo": 5000, "atual": 1250}],
                      "events": [{"id": 8, "titulo": "Aluguel", "data": "2026-11-05", "val": 900}],
                      "dark": True, "slim": True}


@pytest.mark.parametrize("origin,target,value,expected", [
    ("USD", "BRL", "10", "R$ 50,00"),
    ("BRL", "USD", "100", "US$ 20,00"),
    ("USD", "EUR", "12", "€ 10,00"),
    ("BRL", "BTC", "100", "₿ 0,00033333"),
    ("USD", "USD", "10", "US$ 10,00"),
    ("BRL", "USD", "0", "Digite um valor para converter"),
    ("BRL", "USD", "-1", "Digite um valor para converter"),
    ("BRL", "USD", "abc", "Digite um valor para converter"),
])
def test_converter(app, origin, target, value, expected):
    scenario = f'''
        cambioCarregado = true;
        cambioRates = {{USD: {{bid: 5}}, EUR: {{bid: 6}}, BTC: {{bid: 300000}}}};
        document.getElementById('conv-val').value = {json.dumps(value)};
        document.getElementById('conv-from').value = {json.dumps(origin)};
        document.getElementById('conv-to').value = {json.dumps(target)};
        calcConv();
        document.getElementById('conv-result').innerHTML;
    '''
    assert expected in app(scenario)
