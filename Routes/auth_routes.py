# ==============================================================================
# ARQUIVO: auth_routes.py
# OBJETIVO: Gerenciar o fluxo de autenticação, registro e permissões de usuários.
# 
# ARQUITETURA E SEGURANÇA:
# - Fluxo JWT: Emissão de Access Tokens (curta duração) e Refresh Tokens (longa duração).
# - Criptografia: Utilização do Bcrypt para hash seguro de senhas no cadastro e login.
# - Proteção de Cadastro: Isolação rigorosa do campo admin no cadastro público, 
#   garantindo que novos usuários sempre nasçam como clientes comuns (admin=False).
# - Controle de Privilégios (RBAC): Rota dedicada de promoção de administradores 
#   (/promote-admin) restrita exclusivamente a usuários que já possuem privilégios admin.
# ==============================================================================


# Imports
from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import verificar_token, pegar_sessao
from security import bcrypt_context, criar_token, autenticar_usuario
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

#Define router
auth_router = APIRouter(prefix="/auth", tags=["auth"])



#Routes
@auth_router.get("/")
async def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema.
    """
    return {"message": "Você acessou a rota de autenticação padrão!", "autenticado": False}


@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="O e-mail inserido já foi cadastrado.")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Usuário {usuario_schema.email} cadastrado com sucesso!"}



@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário ou credenciais inválidas.")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "mensagem": f"Bem-vindo(a) {usuario.nome}! Você foi autenticado com sucesso."
            }



@auth_router.post("/login-form")
async def login(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário ou credenciais inválidas.")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
            }



@auth_router.get("/verificar")
async def verificar(usuario: Usuario = Depends(verificar_token)):
    return {
        "mensagem": f"Olá {usuario.nome}, você está autenticado!",
        "usuario": {
            "valido": True,
            "nome": usuario.nome,
            "email": usuario.email,
            "admin": usuario.admin
        }
    }



@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
        }



# Rota que transforma um usuário em administrador
@auth_router.post("/promote-admin/{new_admin_id}")
async def promote_user_admin(new_admin_id: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Você não tem permissão para realizar essa operação!")
    
    new_admin = session.query(Usuario).filter(Usuario.id==new_admin_id).first()
    if not new_admin:
        raise HTTPException(status_code=404, detail="O usuário que deveria ser promovido não foi encontrado.")

    new_admin.admin = True
    session.commit()
    return {
        "mensagem": f"O usuário {new_admin.nome} foi promovido a administrador com sucesso!"
    }