# TaskFlow

Gerenciador de tarefas em linha de comando, desenvolvido em Python para praticar funções, persistência de dados, tratamento de erros e testes.

## Recursos
- Adicionar tarefas, listar, concluir e excluir.
- Persistência local em JSON.
- Caminho alternativo de dados com --file.

## Executar
\`\`\`bash
python main.py add "Estudar lógica de programação"
python main.py list
python main.py done 1
python main.py delete 1
\`\`\`

## Testes
\`\`\`bash
python -m unittest discover -s tests -v
\`\`\`
Requer Python 3.9+ e não utiliza dependências externas. Os dados ficam localmente; não há sincronização em nuvem.
