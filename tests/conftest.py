"""Fixtures compartilhadas pela suíte de testes.

As variáveis de ambiente precisam existir ANTES de importar ``app``, porque a
configuração do Flask é lida no momento do import. Forçamos um SQLite em memória
para que os testes nunca toquem um banco real, mesmo que exista um ``.env`` ou
um ``DATABASE_URL`` exportado no shell.
"""
import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "chave-de-teste"

import pytest  # noqa: E402

from app import app as flask_app, db, User  # noqa: E402
from werkzeug.security import generate_password_hash  # noqa: E402


DADOS_USUARIO = {
    "nome": "Maria da Silva",
    "cpf": "123.456.789-00",
    "telefone": "(51) 99999-0000",
    "email": "maria@example.com",
    "endereco": "Rua das Flores, 100",
    "bairro": "Centro",
    "cidade": "Porto Alegre",
    "descricao": "Perdi minha casa na enchente.",
    "categoria_perda": "casa_destruida",
    "pix": "maria@example.com",
    "senha": "senha-secreta",
}


@pytest.fixture
def app():
    flask_app.config.update(TESTING=True)
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def dados_usuario():
    """Cópia dos dados de formulário de um usuário válido."""
    return dict(DADOS_USUARIO)


@pytest.fixture
def usuario(app, dados_usuario):
    """Usuário já persistido no banco, com a senha armazenada como hash."""
    campos = dict(dados_usuario)
    campos["senha"] = generate_password_hash(campos["senha"])
    user = User(**campos)
    db.session.add(user)
    db.session.commit()
    return user


def fazer_login(client, email=DADOS_USUARIO["email"], senha=DADOS_USUARIO["senha"]):
    return client.post("/login", data={"email": email, "senha": senha})
