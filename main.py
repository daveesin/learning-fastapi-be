# O main.py é o arquivo que deve ser rodado para gerar o servidor e deixar os endpoints online
# Nesse arquivo é importante a ordem na qual as coisas acontecem
# Aqui são declaradas as variáveis buscadas do .env, como chaves secretas e etc., variáveis que vão ser usadas em todo o app
# É iniciada a variável app = FastAPI() que inicia o servidor backend
# Questões de segurança como OAuth2 para gerar headers corretos para validar tokens e criar o CryptContext usado para senhas também são no main.py
# app.include_router e passar os routers iniciados no arquivos de routes inserem esses routers e esses endpoints no servidor online
# Para rodar o servidor localmente podemos usar a biblioteca uvicorn. Basta rodar o comando uvicorn main:app --reload (--reload faz com que eu possa adaptar o código
# enquanto o servidor continua rodando e vá atualizando)


# imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Inicia a variável que inicia o servidor
app = FastAPI()


#Define as origens permitidas para requisições CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Permite requisições destas origens
    allow_credentials=True,
    allow_methods=["*"],            # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],            # Permite todos os headers (Content-Type, Authorization, etc.)
)


# Importa os routers dos arquivos de rota
from Routes.auth_routes import auth_router
from Routes.order_routes import order_router


# Inclui as rotas no app
app.include_router(auth_router)
app.include_router(order_router)

# uvicorn main:app --reload (comando para rodar no terminal)