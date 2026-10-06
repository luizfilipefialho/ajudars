from flask import session
from werkzeug.security import check_password_hash

from app import User
from tests.conftest import fazer_login


# ---------------------------------------------------------------- index

def test_index_responde_200(client):
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert "Bem-vindo ao Sistema de Doações" in resposta.get_data(as_text=True)


def test_index_lista_usuarios_registrados(client, usuario):
    html = client.get("/").get_data(as_text=True)

    assert usuario.nome in html
    assert f"{usuario.bairro}, {usuario.cidade}" in html
    assert usuario.pix in html


def test_index_sem_usuarios_nao_quebra(client):
    html = client.get("/").get_data(as_text=True)

    assert "Solicitações Registradas" in html


# ------------------------------------------------------------- register

def test_register_get_exibe_formulario(client):
    resposta = client.get("/register")

    assert resposta.status_code == 200
    assert 'name="cpf"' in resposta.get_data(as_text=True)


def test_register_post_cria_usuario_e_redireciona(client, dados_usuario):
    resposta = client.post("/register", data=dados_usuario)

    assert resposta.status_code == 302
    assert resposta.headers["Location"] == "/"
    assert User.query.count() == 1


def test_register_armazena_senha_como_hash(client, dados_usuario):
    client.post("/register", data=dados_usuario)

    user = User.query.filter_by(email=dados_usuario["email"]).one()
    assert user.senha != dados_usuario["senha"]
    assert check_password_hash(user.senha, dados_usuario["senha"])


def test_register_com_cpf_duplicado_nao_cria_segundo_usuario(client, usuario, dados_usuario):
    resposta = client.post("/register", data={**dados_usuario, "email": "outra@example.com"})

    assert resposta.status_code == 200  # a view devolve a exceção como texto
    assert User.query.count() == 1


def test_register_sem_campo_obrigatorio_retorna_400(client, dados_usuario):
    del dados_usuario["pix"]

    resposta = client.post("/register", data=dados_usuario)

    assert resposta.status_code == 400
    assert User.query.count() == 0


# ---------------------------------------------------------------- login

def test_login_get_exibe_formulario(client):
    resposta = client.get("/login")

    assert resposta.status_code == 200
    assert 'name="senha"' in resposta.get_data(as_text=True)


def test_login_com_credenciais_validas_autentica_e_redireciona(client, usuario):
    with client:
        resposta = fazer_login(client)

        assert resposta.status_code == 302
        assert resposta.headers["Location"] == "/update"
        assert session["_user_id"] == str(usuario.id)


def test_login_com_senha_errada_nao_autentica(client, usuario):
    with client:
        resposta = fazer_login(client, senha="errada")

        assert resposta.status_code == 200
        assert "_user_id" not in session
        assert session["_flashes"][0][1] == "Login failed. Check your credentials."


def test_login_com_email_desconhecido_nao_autentica(client, usuario):
    with client:
        resposta = fazer_login(client, email="ninguem@example.com")

        assert resposta.status_code == 200
        assert "_user_id" not in session


# --------------------------------------------------------------- logout

def test_logout_exige_login(client):
    resposta = client.get("/logout")

    assert resposta.status_code == 302
    assert resposta.headers["Location"].startswith("/login")


def test_logout_encerra_sessao_e_redireciona_para_index(client, usuario):
    with client:
        fazer_login(client)
        resposta = client.get("/logout")

        assert resposta.status_code == 302
        assert resposta.headers["Location"] == "/"
        assert "_user_id" not in session


# --------------------------------------------------------------- update

def test_update_exige_login(client):
    resposta = client.get("/update")

    assert resposta.status_code == 302
    assert resposta.headers["Location"].startswith("/login")


def test_update_get_mostra_dados_do_usuario_logado(client, usuario):
    fazer_login(client)

    html = client.get("/update").get_data(as_text=True)

    assert f'value="{usuario.nome}"' in html
    assert f'value="{usuario.email}"' in html


def test_update_post_altera_nome_e_email(client, usuario):
    fazer_login(client)

    resposta = client.post("/update", data={"nome": "Maria Souza", "email": "souza@example.com"})

    assert resposta.status_code == 302
    assert resposta.headers["Location"] == "/update"
    atualizado = User.query.get(usuario.id)
    assert atualizado.nome == "Maria Souza"
    assert atualizado.email == "souza@example.com"


def test_update_post_nao_altera_outros_campos(client, usuario):
    fazer_login(client)
    pix_original = usuario.pix

    client.post("/update", data={"nome": "Maria Souza", "email": "souza@example.com", "pix": "novo-pix"})

    assert User.query.get(usuario.id).pix == pix_original
