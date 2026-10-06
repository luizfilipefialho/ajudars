from werkzeug.security import check_password_hash

from app import User, db, load_user


def test_usuario_e_persistido_com_todos_os_campos(app, usuario, dados_usuario):
    salvo = User.query.filter_by(cpf=dados_usuario["cpf"]).one()

    assert salvo.id is not None
    for campo in ("nome", "telefone", "email", "endereco", "bairro", "cidade",
                  "descricao", "categoria_perda", "pix"):
        assert getattr(salvo, campo) == dados_usuario[campo]
    assert check_password_hash(salvo.senha, dados_usuario["senha"])


def test_repr_mostra_nome_cpf_e_telefone(app, usuario):
    assert repr(usuario) == "User('Maria da Silva', '123.456.789-00', '(51) 99999-0000')"


def test_cpf_e_unico(app, usuario, dados_usuario):
    import pytest
    from sqlalchemy.exc import IntegrityError

    duplicado = User(**{**dados_usuario, "email": "outra@example.com"})
    db.session.add(duplicado)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()


def test_load_user_retorna_usuario_pelo_id(app, usuario):
    assert load_user(str(usuario.id)) is usuario


def test_load_user_retorna_none_para_id_inexistente(app):
    assert load_user("999") is None
