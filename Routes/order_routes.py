# ==============================================================================
# ARQUIVO: order_routes.py
# OBJETIVO: Gerenciar todas as operações relacionadas aos pedidos da pizzaria.
# 
# SEGURANÇA E ARQUITETURA:
# - Proteção Global: Utiliza dependencies=[Depends(verificar_token)] no APIRouter 
#   para garantir que NENHUMA rota deste arquivo seja acessada sem um token válido.
# - Controle de Acesso (RBAC): Valida se o usuário autenticado é o dono do pedido 
#   (usuario.id == pedido.usuario) ou se possui privilégios de administrador (admin).
# - Tratamento de Erros: Uso rigoroso de códigos HTTP semânticos (404 para recursos 
#   não encontrados e 403 para acessos negados por falta de permissão).
# - Integridade: Validação da existência prévia de itens e pedidos antes de manipular
#   o banco de dados, evitando erros de servidor (HTTP 500).
# ==============================================================================


#imports
from fastapi import APIRouter, Depends, HTTPException
from dependencies import verificar_token, pegar_sessao
from sqlalchemy.orm import Session
from schemas import ItemPedidoSchema, ResponsePedidoSchema
from models import Pedido, Usuario, ItemPedido
from typing import List

# Inicia o router que vamos usar para criar todos os endpoints em um prefixo específico e declara que todos os endpoints desse router exigem login:
order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verificar_token)])


#Cria routes:
@order_router.get("/")
async def orders():
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas de pedidas precisam de autenticação para serem acessadas.
    """
    return {"message": "Você acessou a rota de pedidos!"}


# criar um pedido
@order_router.post("/pedido")
async def criar_pedido(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    novo_pedido = Pedido(usuario=usuario.id)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso pelo usuário {usuario.id}. ID do pedido: {novo_pedido.id}"}


# cancelar um pedido
@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    # user.admin = True?
    # usuario.id = pedido.usuario ?
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação.")
    elif pedido.status == "FINALIZADO":
        raise HTTPException(status_code=401, detail="Você não tem permissão para cancelar um pedido já finalizado.")

    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido Nº {pedido.id} cancelado com sucesso.", 
        "pedido": pedido
    }



# listar todos os pedidos
@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação.")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }



# adicionar item a um pedido
@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, item_pedido_schema: ItemPedidoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não existente.")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação.")
    elif pedido.status != "PENDENTE":
        raise HTTPException(status_code=401, detail="Você não tem permissão para adicionar itens a um pedido FINALIZADO ou CANCELADO.")

    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": "Item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }



# remover item de um pedido
@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=404, detail="Item do pedido não encontrado.")
    
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="O pedido referente ao item não foi encontrado.")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail="Você não tem autorização para fazer essa operação.")
    elif pedido.status != "PENDENTE":
        raise HTTPException(status_code=401, detail="Você não tem permissão para remover itens de um pedido FINALIZADO ou CANCELADO.")

    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": f"Item removido com sucesso do pedido Nº {pedido.id}",
        "pedido": pedido
    }



# finalizar um pedido
@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail="Você não tem autorização para fazer essa modificação.")

    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "mensagem": f"Pedido Nº {pedido.id} finalizado com sucesso.", 
        "pedido": pedido
    }



# visualizar 1 pedido
@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail="Você não tem autorização para fazer essa modificação.")

    return {
        "quantidade_itens_pedido": len(pedido.itens),
        "detalhes_pedido": pedido
    }



# visualizar todos os pedidos de 1 usuário
@order_router.get("/listar/pedidos-usuario", response_model=List[ResponsePedidoSchema])
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id).all()
    return pedidos