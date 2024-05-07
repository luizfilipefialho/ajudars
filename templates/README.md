
# Sistema de Doações para Afetados no Rio Grande do Sul

Este é um aplicativo Flask desenvolvido para facilitar doações para as pessoas afetadas por calamidades no Rio Grande do Sul. A plataforma permite que usuários se registrem para solicitar ajuda e que doadores contribuam diretamente através de chaves PIX.

## Funcionalidades

- **Registro de Usuários**: Usuários podem criar contas, fornecer informações pessoais e detalhar suas necessidades.
- **Autenticação**: Sistema de login/logout para usuários e administradores.
- **Administração**: Administradores podem validar e gerenciar solicitações de usuários.
- **Doações**: Interface para visualizar solicitações e realizar doações utilizando chaves PIX.

## Tecnologias Utilizadas

- **Flask**: Framework web para construção das interfaces e lógica do servidor.
- **SQLAlchemy**: ORM utilizado para interação com banco de dados SQLite.
- **Bootstrap**: Framework de front-end para design responsivo e atraente.
- **Python-dotenv**: Utilizado para gerenciar configurações sensíveis fora do código.

## Configuração do Projeto

### Pré-requisitos

- Python 3.8+
- pip
- venv (recomendado)

### Instalação

1. Clone o repositório e entre na pasta do projeto:
   ```bash
   git clone https://github.com/seu-usuario/meu-projeto-flask.git
   cd meu-projeto-flask
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Copie o arquivo `.env.example` para `.env` e ajuste as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Abra o .env e ajuste as configurações conforme necessário
   ```

4. Inicialize o banco de dados:
   ```bash
   flask db upgrade
   ```

5. Execute o aplicativo:
   ```bash
   flask run
   ```

6. Acesse o aplicativo em `http://127.0.0.1:5000/` em seu navegador.

## Como Contribuir

Estamos abertos a contribuições! Para contribuir, por favor:
1. Faça um fork do projeto.
2. Crie uma branch para sua funcionalidade (`git checkout -b feature/amazing-feature`).
3. Faça commit de suas mudanças (`git commit -m 'Add some amazing feature'`).
4. Faça push para a branch (`git push origin feature/amazing-feature`).
5. Abra um Pull Request.

## Contato

Luiz Fialho - luizfilipefialho@gmail.com
