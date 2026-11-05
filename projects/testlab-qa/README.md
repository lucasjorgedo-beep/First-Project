# TestLab QA

Laboratório de qualidade de software com uma aplicação de exemplo e testes automatizados em unittest.

## Cenários cobertos
- Cálculo de desconto: valores comuns, limites e entradas inválidas.
- Validação de e-mail: formatos válidos e inválidos.
- Normalização de nomes de produtos: espaços extras e texto vazio.

## Executar testes
\`\`\`bash
python -m unittest discover -s tests -v
\`\`\`
Python 3.9+. Laboratório didático local; não valida um serviço externo nem substitui testes de integração ou segurança.
