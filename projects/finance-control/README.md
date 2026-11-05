# FinanceControl

Aplicação de linha de comando para registrar despesas pessoais e consultar totais por categoria. Projeto de estudo em Python, com persistência local em CSV e testes automatizados usando a biblioteca padrão.

## Funcionalidades

- Registrar despesas com data automática, descrição, categoria e valor.
- Validar valores positivos, inclusive no formato brasileiro (ex.: `1.234,56`).
- Listar lançamentos salvos.
- Exibir total de despesas e totais por categoria.
- Escolher o caminho do arquivo CSV pela linha de comando.

## Tecnologias

- Python 3.10+
- CSV e pathlib (biblioteca padrão)
- unittest (testes)

## Como executar

Não requer instalação de dependências externas.

```bash
python main.py
```

Para salvar os dados em outro local:

```bash
python main.py --file dados/minhas-despesas.csv
```

## Como executar os testes

Na pasta `projects/finance-control`:

```bash
python -m unittest discover -s tests -v
```

## Estrutura

```text
finance-control/
├── main.py
├── README.md
└── tests/
    └── test_main.py
```

## Limitações conhecidas

- O projeto é local e não possui login, banco de dados ou sincronização em nuvem.
- Os dados são armazenados em CSV; faça cópias de segurança do arquivo.
- Não é um sistema de aconselhamento financeiro.

## Próximas melhorias

- Filtros por período.
- Edição e exclusão de lançamentos.
- Exportação de relatórios.
- Interface gráfica ou API.
