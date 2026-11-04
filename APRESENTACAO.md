# Apresentação dos testes do FinTrack

## Executar na frente do professor

### Com Docker

Para demonstrar o site no navegador, execute `docker compose up -d --build --wait web`
e abra http://localhost:8080. O site permanece em segundo plano enquanto os
testes são executados. Para parar o servidor, use `docker compose stop web`.
O site usa serviços externos; a execução dos testes usa simulações.

Abra o Docker Desktop e espere o mecanismo iniciar. No terminal do projeto:

```powershell
docker compose run --build --rm tests
```

Ou, no PowerShell, use o caminho completo, mesmo se estiver em outra pasta:

```powershell
& "D:\GitHub\controle_financeiro\apresentar-docker.cmd"
```

O Docker prepara Python, Node.js e pytest e executa as duas suítes. A primeira
construção precisa de internet; faça isso antes da apresentação. Depois, com a
imagem pronta, pode executar sem reconstruir:

```powershell
docker compose run --rm tests
```

Os testes rodam sem rede, com a imagem somente para leitura e uma pasta `/tmp`
temporária em memória para o pytest. O contêiner é removido ao terminar.
Após alterar o código ou os testes,
use novamente `--build` para atualizar a imagem.

### Com as instalações locais

No terminal do VS Code, na pasta do projeto:

```powershell
.\apresentar-testes.cmd
```

O comando mostra as versões, executa os 16 casos do pytest e depois os 5
testes JavaScript existentes. Se uma suíte falhar, ele encerra com erro.
As dependências já estão instaladas nesta máquina; a demonstração dos testes
não precisa de internet, Docker ou conexão com o banco.

Alternativa no VS Code: `Ctrl+Shift+P` → `Tasks: Run Test Task` →
`Apresentar testes FinTrack`.

Para executar apenas o pytest:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

## Roteiro de três minutos

1. Abra `tests/test_fintrack.py` e explique: “O pytest organiza os cenários,
   executa cada caso e compara o resultado obtido com o esperado.”
2. Mostre `test_totals`: uma receita de 1.000 e uma despesa de 250 devem resultar
   em saldo de 750. Mostre também o caso sem transações e o saldo negativo.
3. Mostre `@pytest.mark.parametrize`: a mesma função recebe diferentes entradas.
   Por isso quatro funções de teste geram 16 casos.
4. Execute `apresentar-testes.cmd` e mostre os resultados `PASSED`.
5. Abra `tests/run_app.cjs`: “O Node.js carrega o código real de `src/script.js`.
   O ambiente do navegador e o armazenamento são simulados e cada caso roda
   em um processo separado. A inicialização automática é desativada para
   não conectar ao Supabase.”

## O que cada grupo verifica

| Grupo | Casos | Comportamento verificado |
|---|---:|---|
| Saldo | 4 | Sem transações, saldo positivo, negativo e valores com centavos |
| Formatação | 3 | Zero, separador de milhares e exibição do valor absoluto em reais |
| Persistência | 1 | Salvar e recuperar metas, eventos, tema e barra lateral |
| Conversor | 8 | Cinco conversões e rejeição de zero, negativo e texto |

## Perguntas que podem aparecer

**Por que usar Node.js com pytest?**
O projeto usa JavaScript. O pytest controla os casos em Python e chama o Node.js
para executar as funções existentes, sem reescrever a lógica em Python.

**O que é um assert?**
É a comparação que define se o caso passou. Por exemplo, o saldo calculado
precisa ser igual ao saldo esperado.

**Por que simular as dependências?**
Para ter resultados repetíveis e testar a lógica sem depender de internet,
cotações variáveis ou dados do banco.

**Isso testa tudo?**
Não. A suíte pytest testa a lógica com ambiente simulado. Não verifica cliques,
aparência, WebGL ou integração real com Supabase e AwesomeAPI. Os cinco testes
JavaScript existentes também usam uma resposta simulada da API.

## Demonstração opcional de uma falha

Em `test_totals`, altere somente o saldo esperado do caso de 1.000 menos 250,
de `750` para `751`. Execute:

```powershell
.\.venv\Scripts\python.exe -m pytest -v -k totals
```

O caso deve falhar: a aplicação continua calculando 750. Restaure o esperado
para `750` e execute novamente para mostrar os quatro casos passando.
Essa alteração é apenas uma demonstração e não deve ficar salva no resultado final.

## Preparar em outra máquina Windows

Instale Python 3.10+ e Node.js 20+, reabra o terminal e execute:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\apresentar-testes.cmd
```

A instalação precisa de internet. O ambiente `.venv` e os ajustes locais do
VS Code estão ignorados pelo Git; recrie o ambiente se trocar de computador.
