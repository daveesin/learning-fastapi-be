# Esse arquivo serve na estrutura do FastAPI para que possamos criar funções que vão ser reutilizadas em várias partes de códigos das rotas
# Essas funções vão retornar algo que a rota precisa para funcionar, como uma sessão dentro do DB ou o registro de um usuário após validação de credenciais
# Podemos nas nossas rotas passar como parâmetro da função da rota o que precisamos, o tipo de dado que vai ser e um Depends(funcao_que_retorna_o_dado)
# Ex: Nesse caso, quando eu precisar da minha sessão por querer consultar ou alterar o DB, eu passo como parâmetro da função da rota:
#   session(o que preciso): Session(tipo do dado) = Depends(pegar_sessao) (função que retorna a sessão)


# imports
from Database.database import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from security import SECRET_KEY, ALGORITHM, oauth2_schema



# Função que abre uma sessão no banco de dados e, de forma segura, garante que, independente do que acontecer quando for chamada, ela será encerrada
def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()



# Função que recebe um token usando a biblioteca do oauth2 para garantir que chege em um header na estrutura correta e verifica a validade desse token e
# retorna o usuário dono do token em questão
def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")
    
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    
    return usuario