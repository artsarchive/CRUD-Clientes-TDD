"""Interface de linha de comando do cadastro de clientes."""
import argparse

from .servico import CadastroClientes, ClienteNaoEncontrado, DadosInvalidos


def main() -> None:
    parser = argparse.ArgumentParser(description="CRUD de clientes com TDD")
    parser.add_argument("--arquivo", default="clientes.json", help="Caminho do banco JSON")
    comandos = parser.add_subparsers(dest="acao", required=True)
    criar = comandos.add_parser("cadastrar", help="Cria um cliente")
    criar.add_argument("nome")
    criar.add_argument("email")
    comandos.add_parser("listar", help="Lista clientes")
    consultar = comandos.add_parser("consultar", help="Consulta cliente por ID")
    consultar.add_argument("id", type=int)
    atualizar = comandos.add_parser("atualizar", help="Atualiza cliente por ID")
    atualizar.add_argument("id", type=int)
    atualizar.add_argument("--nome")
    atualizar.add_argument("--email")
    excluir = comandos.add_parser("excluir", help="Exclui cliente por ID")
    excluir.add_argument("id", type=int)
    args = parser.parse_args()
    cadastro = CadastroClientes(args.arquivo)
    try:
        if args.acao == "cadastrar":
            print(cadastro.cadastrar(args.nome, args.email))
        elif args.acao == "listar":
            for cliente in cadastro.listar():
                print(cliente)
        elif args.acao == "consultar":
            print(cadastro.consultar(args.id))
        elif args.acao == "atualizar":
            print(cadastro.atualizar(args.id, nome=args.nome, email=args.email))
        elif args.acao == "excluir":
            cadastro.excluir(args.id)
            print("Cliente excluído.")
    except (DadosInvalidos, ClienteNaoEncontrado) as erro:
        parser.exit(1, f"Erro: {erro}\n")


if __name__ == "__main__":
    main()
