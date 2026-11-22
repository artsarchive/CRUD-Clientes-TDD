# Cadastro de Clientes com TDD

Atividade individual sobre testes e *Test-Driven Development* (TDD), do curso de Ciência da Computação da Universidade Estadual de Santa Cruz (UESC).

## Descrição

Aplicação de linha de comando em Python que realiza as operações CRUD (cadastrar, listar/consultar, atualizar e excluir) de clientes. Os dados são salvos no arquivo local `clientes.json`, criado automaticamente. O objetivo é demonstrar como escrever testes antes do código de produção e implementar somente o necessário para atendê-los.

**Tecnologias:** Python 3.10+; biblioteca padrão `unittest` para testes; `json` para persistência; `argparse` para a interface. **Não exige instalação de bibliotecas externas.**

## Como executar

Abra um terminal na pasta do projeto e execute:

```bash
python -m clientes cadastrar "Ana Silva" ana@exemplo.com
python -m clientes listar
python -m clientes consultar 1
python -m clientes atualizar 1 --nome "Ana Maria"
python -m clientes atualizar 1 --email ana.maria@exemplo.com
python -m clientes excluir 1
```

Dependendo da instalação, use `python3` no lugar de `python`. Para testar sem afetar o arquivo padrão, acrescente `--arquivo teste.json` **antes** do comando (por exemplo, `python -m clientes --arquivo teste.json listar`).

## Executar os testes

```bash
python -m unittest discover -s tests -v
```

O conjunto inclui nove testes sobre cadastro, consulta, listagem, persistência, atualização, exclusão, identificação e validações. Os dados de teste são isolados em diretórios temporários.

## Processo TDD demonstrado

1. **Red:** foram escritos os testes em `tests/test_clientes.py` antes da implementação. A execução apresentou `ModuleNotFoundError`, pois o pacote `clientes` não existia.
2. **Green:** o módulo `clientes/servico.py` e a interface foram implementados. Todos os nove testes passaram.
3. **Refactor:** a lógica foi organizada em métodos auxiliares (`_validar`, `_localizar`, `_ler` e `_salvar`), mantendo os testes verdes.

O histórico local do Git conserva os commits `test: definir comportamentos esperados do CRUD (fase red)` e `feat: implementar CRUD para satisfazer testes (fase green)`. A fase vermelha inicial comprova ausência de implementação, não uma falha de asserção; isso é registrado de forma transparente no relatório.

## Estrutura

```text
clientes/
  __init__.py        pacote Python
  __main__.py        interface de comandos
  servico.py         regras de negócio e persistência
tests/
  test_clientes.py   testes automatizados
docs/
  codigo.html        documentação navegável gerada a partir das docstrings
README.md
.gitignore
```

## Documentação do código

Abra [`docs/codigo.html`](docs/codigo.html) no navegador. O arquivo foi gerado a partir das docstrings do módulo `clientes.servico` usando `pydoc`. Para regenerar:

```bash
python -m pydoc -w clientes.servico
```

O comando cria `clientes.servico.html` na pasta atual. Alternativamente, visualize no terminal:

```bash
python -m pydoc clientes.servico
```

## Regras e limitações

- Nome obrigatório e e-mail com validação simplificada de formato.
- E-mail único, sem diferença entre maiúsculas e minúsculas.
- IDs sequenciais nunca reutilizados após exclusão.
- Operações simultâneas em processos distintos não são suportadas; JSON foi escolhido por ser suficiente para o exercício.
- Não há autenticação nem armazenamento seguro de dados sensíveis. Use somente dados fictícios na demonstração.

## Referências

- BECK, Kent. *Test-Driven Development: By Example*. Addison-Wesley, 2002.
- PYTHON SOFTWARE FOUNDATION. *unittest — Unit testing framework*. https://docs.python.org/3/library/unittest.html
- PYTHON SOFTWARE FOUNDATION. *pydoc — Documentation generator and online help system*. https://docs.python.org/3/library/pydoc.html
