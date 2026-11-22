"""Testes de comportamento escritos antes da implementação (TDD)."""
import tempfile
import unittest
from pathlib import Path

from clientes.servico import CadastroClientes, ClienteNaoEncontrado, DadosInvalidos


class TestCadastroClientes(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.arquivo = Path(self.pasta.name) / "clientes.json"
        self.cadastro = CadastroClientes(self.arquivo)

    def tearDown(self):
        self.pasta.cleanup()

    def test_cadastrar_e_consultar_cliente(self):
        cliente = self.cadastro.cadastrar("Ana Silva", "ana@exemplo.com")
        self.assertEqual(cliente["id"], 1)
        self.assertEqual(self.cadastro.consultar(1)["nome"], "Ana Silva")

    def test_listar_e_persistir_clientes(self):
        self.cadastro.cadastrar("Ana", "ana@exemplo.com")
        self.cadastro.cadastrar("Bruno", "bruno@exemplo.com")
        reaberto = CadastroClientes(self.arquivo)
        self.assertEqual(len(reaberto.listar()), 2)
        self.assertEqual(reaberto.consultar(2)["nome"], "Bruno")

    def test_impedir_email_duplicado(self):
        self.cadastro.cadastrar("Ana", "ANA@exemplo.com")
        with self.assertRaises(DadosInvalidos):
            self.cadastro.cadastrar("Outra Ana", "ana@exemplo.com")

    def test_rejeitar_nome_ou_email_invalidos(self):
        for nome, email in [(" ", "a@exemplo.com"), ("Ana", "email-invalido")]:
            with self.subTest(nome=nome, email=email):
                with self.assertRaises(DadosInvalidos):
                    self.cadastro.cadastrar(nome, email)

    def test_atualizar_cliente(self):
        self.cadastro.cadastrar("Ana", "ana@exemplo.com")
        atualizado = self.cadastro.atualizar(1, nome="Ana Maria")
        self.assertEqual(atualizado["nome"], "Ana Maria")
        self.assertEqual(atualizado["email"], "ana@exemplo.com")

    def test_atualizacao_nao_aceita_email_ja_utilizado(self):
        self.cadastro.cadastrar("Ana", "ana@exemplo.com")
        self.cadastro.cadastrar("Bruno", "bruno@exemplo.com")
        with self.assertRaises(DadosInvalidos):
            self.cadastro.atualizar(2, email="ANA@exemplo.com")

    def test_excluir_cliente(self):
        self.cadastro.cadastrar("Ana", "ana@exemplo.com")
        self.cadastro.excluir(1)
        self.assertEqual(self.cadastro.listar(), [])
        with self.assertRaises(ClienteNaoEncontrado):
            self.cadastro.consultar(1)

    def test_cliente_inexistente(self):
        with self.assertRaises(ClienteNaoEncontrado):
            self.cadastro.consultar(999)
        with self.assertRaises(ClienteNaoEncontrado):
            self.cadastro.atualizar(999, nome="Teste")
        with self.assertRaises(ClienteNaoEncontrado):
            self.cadastro.excluir(999)

    def test_ids_nao_sao_reutilizados_apos_exclusao(self):
        self.cadastro.cadastrar("Ana", "ana@exemplo.com")
        self.cadastro.excluir(1)
        self.assertEqual(self.cadastro.cadastrar("Bia", "bia@exemplo.com")["id"], 2)


if __name__ == "__main__":
    unittest.main()
