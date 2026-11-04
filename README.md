<div align="center">

<h1>FinTrack</h1>
<p><strong>Gestão financeira pessoal — inteligente, visual e sem dependências.</strong></p>

<p>
  <img alt="status" src="https://img.shields.io/badge/status-em%20desenvolvimento-orange?style=flat-square">
  <img alt="version" src="https://img.shields.io/badge/version-2.2.3-blue?style=flat-square">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square">
  <img alt="ci" src="https://img.shields.io/github/actions/workflow/status/wadsonsamuelov/controle_financeiro/ci.yml?label=CI%2FCD&style=flat-square">
  <img alt="html" src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white">
  <img alt="js" src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black">
  <img alt="supabase" src="https://img.shields.io/badge/Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white">
</p>

</div>

---
https://wadsonsamuelov.github.io/controle_financeiro/
## Por que usar o FinTrack?

A maioria das pessoas sabe que precisa controlar as finanças. Poucas realmente fazem isso — porque as ferramentas disponíveis são ou complexas demais, ou pagas, ou exigem cadastro em serviços que ninguém confia.

**O FinTrack resolve isso.**

É uma aplicação web completa que roda direto no navegador. Sem instalar nada. Sem pagar nada. Sem depender de um app de terceiro que some depois. Você abre, cadastra suas movimentações e em segundos tem um painel com tudo que precisa saber sobre sua saúde financeira.

> Saldo disponível. Receitas vs despesas. Metas de economia. Cotação do dólar em tempo real. Calendário de vencimentos. Tudo em um único lugar, com uma interface que não envergonha.

Se você já quis parar de usar planilha mas nunca encontrou uma alternativa gratuita e decente — essa é ela.

---

## Funcionalidades

| Módulo | O que faz |
|---|---|
| **Home** | Painel de boas-vindas com saldo, ações rápidas e últimas movimentações |
| **Dashboard** | KPIs (receita, despesa, taxa de poupança), gráfico histórico de 6 meses e resumo mensal |
| **Transações** | Cadastro, edição e exclusão de receitas e despesas com filtros por tipo e método de pagamento |
| **Projetos & Metas** | Criação de objetivos financeiros com progresso visual em barra |
| **Calendário** | Eventos financeiros por data (salário, gastos fixos, vencimentos, recorrências) |
| **Distribuição** | Análise de gastos por categoria e por método de pagamento via gráficos de pizza |
| **Câmbio** | Cotações em tempo real (USD, EUR, BTC) + conversor de moedas com swap |
| **Configurações** | Perfil, conta, aparência, notificações, preferências financeiras, privacidade e plano |
| **Tema** | Modo claro e escuro com persistência |
| **Persistência** | Transações sincronizadas via Supabase; metas e eventos salvos em `localStorage` |

---

## Stack técnica

| Camada | Tecnologia | Detalhes |
|---|---|---|
| Estrutura | HTML5 | SPA sem framework, roteamento manual via JS |
| Estilo | CSS3 | Custom properties, grid, modo escuro nativo |
| Lógica | JavaScript (ES2022) | Vanilla JS, async/await, sem bundler |
| Gráficos | Chart.js 4.4 | Bar e doughnut charts via CDN |
| Backend | Supabase | Banco PostgreSQL gerenciado, SDK JS v2 |
| Câmbio | AwesomeAPI | REST público para cotações BRL/USD/EUR/BTC |
| Tipografia | Plus Jakarta Sans + JetBrains Mono | Google Fonts |
| CI/CD | GitHub Actions | Testes + deploy automático no GitHub Pages |
| Hospedagem | GitHub Pages | Deploy disparado a cada push na `main` |

---

## Arquitetura

O FinTrack é uma **SPA (Single Page Application)** construída sem framework. O roteamento é feito via JavaScript puro com a função `goto()`, que ativa/desativa seções `div.page` conforme a navegação.

```
controle_financeiro/
├── src/
│   ├── index.html          # Shell da aplicação — todo o HTML vive aqui
│   ├── script.js           # Toda a lógica: estado, CRUD, gráficos, API calls
│   └── style.css           # Design system via CSS custom properties
├── tests/
│   └── api.tests.js        # Testes de integração da API de câmbio
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline: test → deploy
├── package.json
└── README.md
```

### Fluxo de dados

```
Usuário
  │
  ├─ Transações ──► Supabase (PostgreSQL)  ← fonte de verdade para TX
  │                      ↓
  │              loadTransacoes() na inicialização
  │
  ├─ Metas / Eventos ──► localStorage  ← persistência local
  │
  └─ Câmbio ──► AwesomeAPI REST  ← chamada sob demanda
```

### Estado da aplicação

O estado global é mantido em variáveis module-level (`TX`, `GOALS`, `CEVS`) e sincronizado com Supabase (transações) e `localStorage` (demais dados). Não há gerenciador de estado externo — o re-render é acionado diretamente após cada mutação via funções de render (`renderTxList`, `renderGoals`, etc.).

---

## Como rodar localmente

O projeto não precisa de build. Basta servir o diretório `src/`:

```bash
# Com Python
python -m http.server 8080 --directory src

# Com Node.js (npx)
npx serve src

# Com VS Code — instale a extensão Live Server e abra index.html
```

Acesse em `http://localhost:8080`.

> As transações são salvas no Supabase configurado. Para usar sua própria instância, edite `SUPABASE_URL` e `SUPABASE_KEY` no início de `src/script.js`.

---

## Testes

### Docker: site e testes

Com Docker Desktop aberto, inicie o site:

```bash
docker compose up -d --build --wait web
```

Acesse http://localhost:8080. O servidor fica em segundo plano, com verificação
de saúde e reinício automático enquanto o Docker estiver funcionando.
Use `docker compose ps` para conferir, `docker compose logs -f web` para os logs
e `docker compose stop web` para parar. Após editar o site, repita o comando
com `--build`. Chart.js, Supabase e cotações mantêm as dependências externas
da aplicação; os testes usam simulações e funcionam sem rede.

### Pytest

Com Docker Desktop aberto, execute as duas suítes em um ambiente isolado:

```bash
docker compose run --build --rm tests
```

A primeira construção baixa as dependências; a execução dos testes não usa rede.

Para apresentar nesta máquina Windows, execute `.\apresentar-testes.cmd`.
Veja o roteiro e as explicações em [APRESENTACAO.md](APRESENTACAO.md).

Requisitos: Python 3.10+ e Node.js 20+ no PATH. O pytest executa o JavaScript
real da aplicação com um ambiente simulado, sem acessar Supabase ou AwesomeAPI.

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

A suíte cobre saldo, receitas e despesas, formatação em reais, persistência
local e conversão de moedas (incluindo valores inválidos). Os testes não
substituem testes visuais em um navegador. Também são executados no GitHub Actions.

Os testes validam a integração com a API de câmbio (AwesomeAPI):

```bash
npm test
# ou diretamente:
node tests/api.tests.js
```

---

## CI/CD

O pipeline é definido em [.github/workflows/ci.yml](.github/workflows/ci.yml) e roda automaticamente em todo push e pull request para `main`:

```
push → main
  │
  ├─ [test]   Testes de integração (Node 20)
  │
  └─ [deploy] Upload do diretório src/ → GitHub Pages
               (só executa se os testes passarem)
```

---

## Variáveis de ambiente

Não há arquivo `.env`. As credenciais do Supabase estão diretamente em `script.js` com a chave `publishable` (segura para uso client-side, conforme [documentação do Supabase](https://supabase.com/docs/guides/api/api-keys)).

Para produção com sua própria instância:

| Variável | Onde alterar | Descrição |
|---|---|---|
| `SUPABASE_URL` | `src/script.js:7` | URL do projeto Supabase |
| `SUPABASE_KEY` | `src/script.js:8` | Chave anon/publishable |

---

## Schema do banco (Supabase)

A tabela `transacoes` no PostgreSQL:

```sql
create table transacoes (
  id    bigint generated always as identity primary key,
  desc  text        not null,
  val   numeric     not null,
  tipo  text        not null,  -- 'receita' | 'despesa'
  met   text,                  -- 'pix' | 'cartao' | 'dinheiro' | 'boleto' | 'ted' | 'debito'
  cat   text,                  -- 'alimentação' | 'moradia' | 'transporte' | ...
  data  date        not null
);
```

---

## Contribuindo

1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/minha-melhoria`
3. Commit suas mudanças: `git commit -m 'feat: adiciona X'`
4. Push: `git push origin feature/minha-melhoria`
5. Abra um Pull Request

Siga o padrão [Conventional Commits](https://www.conventionalcommits.org/) nas mensagens.

---

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais informações.

---

<div align="center">
  <sub>Feito por <a href="https://github.com/wadsonsamuelov">Wadson Samuel</a></sub>
  <sub> e <a href="https://github.com/rth-ur">Arthur Clemente</a></sub>
</div>
