"""Regras de negócio e persistência local do CRUD de clientes.

O arquivo JSON contém `proximo_id` e `clientes`. Não é indicado para
acesso concorrente nem substitui um banco de dados em produção.
"""

import json
import re
from pathlib import Path


class DadosInvalidos(ValueError):
    """Dados fornecidos violam uma regra do cadastro."""


class ClienteNaoEncontrado(LookupError):
    """Identificador não pertence a nenhum cliente cadastrado."""


class CadastroClientes:
    """CRUD de clientes com IDs incrementais e e-mails únicos."""

    def __init__(self, arquivo: str | Path = "clientes.json"):
        self.arquivo = Path(arquivo)

    def _ler(self) -> dict:
        """Carrega o estado ou devolve um cadastro vazio."""
        if not self.arquivo.exists():
            return {"proximo_id": 1, "clientes": []}
        with self.arquivo.open(encoding="utf-8") as entrada:
            return json.load(entrada)

    def _salvar(self, dados: dict) -> None:
        """Grava o estado em UTF-8 preservando caracteres portugueses."""
        self.arquivo.parent.mkdir(parents=True, exist_ok=True)
        temporario = self.arquivo.with_suffix(self.arquivo.suffix + ".tmp")
        with temporario.open("w", encoding="utf-8") as saida:
            json.dump(dados, saida, ensure_ascii=False, indent=2)
        temporario.replace(self.arquivo)

    @staticmethod
    def _validar(nome: str, email: str) -> tuple[str, str]:
        """Normaliza espaços e e-mail; recusa campos vazios ou malformados."""
        nome = nome.strip()
        email = email.strip().lower()
        if not nome:
            raise DadosInvalidos("O nome não pode estar vazio.")
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
            raise DadosInvalidos("Informe um e-mail válido.")
        return nome, email

    @staticmethod
    def _localizar(dados: dict, identificador: int) -> dict:
        """Retorna o cliente ou lança ClienteNaoEncontrado."""
        for cliente in dados["clientes"]:
            if cliente["id"] == identificador:
                return cliente
        raise ClienteNaoEncontrado(f"Cliente {identificador} não encontrado.")

    def cadastrar(self, nome: str, email: str) -> dict:
        """Cria um cliente e devolve cópia do registro, incluindo seu ID."""
        dados = self._ler()
        nome, email = self._validar(nome, email)
        if any(c["email"] == email for c in dados["clientes"]):
            raise DadosInvalidos("Este e-mail já está cadastrado.")
        cliente = {"id": dados["proximo_id"], "nome": nome, "email": email}
        dados["clientes"].append(cliente)
        dados["proximo_id"] += 1
        self._salvar(dados)
        return cliente.copy()

    def listar(self) -> list[dict]:
        """Retorna todos os clientes sem expor o estado interno."""
        return [c.copy() for c in self._ler()["clientes"]]

    def consultar(self, identificador: int) -> dict:
        """Consulta um cliente pelo ID."""
        return self._localizar(self._ler(), identificador).copy()

    def atualizar(self, identificador: int, *, nome: str | None = None,
                  email: str | None = None) -> dict:
        """Altera nome e/ou e-mail, preservando os outros campos."""
        dados = self._ler()
        cliente = self._localizar(dados, identificador)
        novo_nome, novo_email = self._validar(
            nome if nome is not None else cliente["nome"],
            email if email is not None else cliente["email"],
        )
        if any(c["id"] != identificador and c["email"] == novo_email
               for c in dados["clientes"]):
            raise DadosInvalidos("Este e-mail já está cadastrado.")
        cliente.update(nome=novo_nome, email=novo_email)
        self._salvar(dados)
        return cliente.copy()

    def excluir(self, identificador: int) -> None:
        """Remove um cliente; um ID excluído não será reutilizado."""
        dados = self._ler()
        self._localizar(dados, identificador)
        dados["clientes"] = [c for c in dados["clientes"] if c["id"] != identificador]
        self._salvar(dados)
