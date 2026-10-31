# O arquivo models.py na estrutura do FastAPI serve para que possamos fazer 3 coisas:
# 1 - Gerar a variável que gera a engine de conexão com o banco de dados via URL do DB (nesse caso, normalmente isso é feito do database.py)
# 2 - Gerar a variável que recebe a declarative_base() que retorna pra ela a classe-mãe que dá origem a classes que podem gerar tabelas pelo SQLAlchemy (nesse caso, normalmente isso é feito do database.py)
# 3 - Gerar as classes que geram tabelas dentro do banco de dados podendo codar isso em Python ao invés de SQL

# __tablename__ define o nome que a tabela daquela classe terá dentro do meu DB. Por convenção, é ideal que a classe seja no singular e CamelCase e
# o da tabela no db seja no plural em snake_case.

# Gera-se o código com os nomes das colunas e criando as colunas passando o nome como string, o tipo, e os parâmetros convenientes como se é primary_key e etc.
# Gera-se o init da classe como qualquer outra do python para que os objetos possam ser gerados e manipulados dentro do python.

# Essas classes podem conter métodos como qualquer outra classe, para que possamos gerar automações e regras quando os dados do banco de dados forem resgatados,
# inseridos, editados, etc.

# Especificamente falando de do tipo relationship, ele recebe como string o nome de uma classe que recebe como chave estrangeira a primary_key da tabela em questão.
# Aquela propriedade do objeto que recebe esse relashionship não vira uma coluna, mas quando se faz uma consulta de um item que possui esse relationship, ele traz
# os detalhes do registro que possui a primary_key dos registros consultados como chave estrangeira.
# O parâmetro cascade="all, delete" faz com que se o registro que tem a primary key for deletado, ele delete em cascata todos os registros que tem essa primary key
# como chave estrangeira, limpando o banco

# Sempre que uma coluna for adicionada, removida, ou um tipo de dado for alterado, etc., usar a biblioteca alembic para gerar as revisões e adaptações do db
# através de migrações para não destruir ou corromper o banco.
# Para fazer migração do banco de dados:
#   cria a migração: alembic revision --autogenerate -m "Escreve aqui alteração feita"
#   executar a migração: alembic upgrade head


#imports
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from Database.database import Base



# Cria as classes/tabelas do banco
# Usuario
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin
        


# Pedido
class Pedido(Base):
    __tablename__ = "pedidos"

    #STATUS_PEDIDOS = (
    #    ("PENDENTE", "PENDENTE"),
    #    ("CANCELADO", "CANCELADO"),
    #    ("FINALIZADO", "FINALIZADO")
    #)

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    itens = relationship("ItemPedido", cascade="all, delete")

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status


    # Método que altera a propriedade preço no objeto baseado nos preços unitários vezes a quantidade de cada item relacionado com esse pedido
    def calcular_preco(self):
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)



# ItensPedido
class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido