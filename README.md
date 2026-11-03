# 🍕 FastPizzaria API

API RESTful completa para gerenciamento de pedidos de uma pizzaria, desenvolvida em **FastAPI**, com arquitetura modular, autenticação via **JWT (OAuth2PasswordBearer)**, controle de acesso baseado em funções (**RBAC**) e validação rigorosa de dados.

---

## 🛠️ Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/):** Framework web moderno e de altíssima performance para construção de APIs com Python.
- **[Uvicorn](https://www.uvicorn.org/):** Servidor ASGI rápido para rodar a aplicação.
- **[Pydantic v2](https://docs.pydantic.dev/):** Validação de esquemas e proteção contra injeções adicionais (`extra = "forbid"`).
- **[SQLAlchemy](https://www.sqlalchemy.org/):** ORM para comunicação com o banco de dados.
- **[Alembic](https://alembic.sqlalchemy.org/):** Ferramenta para controle e execução de migrações de banco de dados.
- **[python-jose](https://python-jose.readthedocs.io/) & [Passlib](https://passlib.readthedocs.io/):** Criptografia de senhas com `bcrypt` e gerenciamento de tokens **JWT (HS256)**.
- **[SQLite](https://www.sqlite.org/):** Banco de dados relacional padrão para testes e desenvolvimento local.

---

## 🔒 Arquitetura de Segurança

1. **OAuth2PasswordBearer:** O backend utiliza o fluxo padrão da indústria para extrair tokens Bearer dinamicamente a partir dos cabeçalhos HTTP (`Authorization: Bearer <TOKEN>`).
2. **Proteção Pentesting / Extra Forbid:** Todos os schemas Pydantic estão configurados para rejeitar parâmetros arbitrários não declarados, impedindo injeção indesejada de parâmetros.
3. **Stateless JWT:** Os tokens de acesso mantêm a aplicação sem estado (stateless), carregando apenas as informações essenciais (`sub` / ID do usuário) e validados cirurgicamente pela `SECRET_KEY`.

---

## 📂 Estrutura do Projeto

```text
.
├── app/
│   ├── database.py       # Conexão do SQLAlchemy e sessão do banco
│   ├── security.py       # Criptografia de senhas (bcrypt) e rotinas de JWT
│   ├── models.py         # Tabelas e relacionamentos do banco de dados
│   ├── schemas.py        # Validações Pydantic (com extra='forbid')
│   ├── dependencies.py   # Injeção de dependências (ex: verificar_token)
│   └── Routes/           # Módulos de endpoints divididos por contexto
│       ├── auth.py
│       ├── users.py
│       ├── orders.py
│       └── pizzas.py
├── alembic/              # Histórico e scripts de migração do banco
├── seed.py               # Script de inicialização do administrador mestre
├── alembic.ini           # Configurações do Alembic
├── .env.example          # Modelo de variáveis de ambiente
├── .gitignore            # Arquivos ignorados pelo controle de versão
├── requirements.txt      # Dependências do projeto
└── main.py               # Ponto de entrada da aplicação FastAPI
```

---

## 🚀 Como Executar o Projeto Localmente

### 1. Clonar o Repositório
```bash
git clone https://github.com/SEU_USUARIO/learning-fastapi-be.git
cd learning-fastapi-be
```

### 2. Criar e Ativar o Ambiente Virtual
- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate
  ```
- **Linux / Mac:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com base no arquivo `.env.example`:

```env
SECRET_KEY=SUA_CHAVE_SECRETA_GERADA_VIA_SECRETS
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./pizzaria.db

# Credenciais para a carga inicial de Admin (seed.py)
ADMIN_USERNAME=admin@pizzaria.com
ADMIN_PASSWORD=SuaSenhaForteAqui123
```

> **Dica:** Para gerar uma `SECRET_KEY` segura no Python, execute no terminal:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

### 5. Executar as Migrações do Banco de Dados (Alembic)
```bash
alembic upgrade head
```

### 6. (Opcional) Popular o Administrador Inicial
```bash
python seed.py
```

### 7. Iniciar o Servidor de Desenvolvimento
```bash
uvicorn main:app --reload
```

Acesse a documentação interativa da API no seu navegador:
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

---

## 🧪 Testando os Endpoints de Autenticação

1. Acesse o **`/docs`** e localize o botão verde **Authorize**.
2. Digite o seu **username/email** e **password** e clique em **Authorize**.
3. O Swagger salvará o token retornado pela rota `/auth/login-form`.
4. Todas as rotas que exigem o `Depends(verificar_token)` agora passarão automaticamente o cabeçalho `Authorization: Bearer <TOKEN>`.