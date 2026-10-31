import os
from dotenv import load_dotenv
from Database.database import db
from sqlalchemy.orm import sessionmaker
from models import Usuario
from security import bcrypt_context

load_dotenv()

def criar_admin_inicial():
    # Puxa o e-mail e a senha direto das variáveis de ambiente:
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_senha = os.getenv("ADMIN_SENHA")

    Session = sessionmaker(bind=db)
    session = Session()
    
    try:
        admin_existente = session.query(Usuario).filter(Usuario.email == admin_email).first()
        if not admin_existente:
            print("Criando usuário administrador inicial...")
            senha_hash = bcrypt_context.hash(admin_senha)
            novo_admin = Usuario(
                nome="Administrador Master",
                email=admin_email,
                senha=senha_hash
            )
            novo_admin.admin = True
            session.add(novo_admin)
            session.commit()
            print("Administrador criado com sucesso!")
        else:
            print("Administrador já existe no banco.")
    finally:
        session.close()

if __name__ == "__main__":
    criar_admin_inicial()