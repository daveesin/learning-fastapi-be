# Arquivos de schema na estrutura do FastAPI tem por objetivo gerar classes que tem como classe-mãe a classe BaseModel importada do Pydantic
# Essas classes servem como modelo tanto de entrada de dados (no caso dos ModelSchema) quanto de resposta do endpoint (os ResponseModelSchema)

# Quando criamos uma classe Schema e passamos os dados esperados e os tipos de dado, conseguimos passar como parâmetro das rotas de post e como response_model
# das rotas de get os tipos de dado que são as classes do schema, fazendo com que a função da rota só precise de um parâmetro ao invés de vários e padronizando
# e validando assim, os tipos de dados, tanto recebidos como resposta, como enviados para a requisição

# class Config: from_attributes = True -> Permite que o Pydantic leia dados vindos de objetos ORM (como o SQLAlchemy do banco de dados) e os converta 
# para o modelo do Schema, em vez de aceitar apenas dicionários.

# Quando um dos tipos de dados for uma lista, é necessário fazer o import do typing do tipo List, e passar ele como tipo do dado e, dentro dele, qual é o tipo de
# dado que vem dentro daquela lista. Se for um objeto com o formato de outro schema, passar o nome dessa classe, como o exmeplo da linha 61.

# Quando um dos dados de um schema não precisar ser preenchido necessariamente por já ter um valor default, importar o Optional do typing e passar para o dado o 
# tipo de dado Optional[tipo_de_dado], como nas linhas 24 e 25

# imports
from pydantic import BaseModel
from typing import List


# Schema de envio para cadastro de novos usuários:
class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str

    class Config:
        from_attributes = True



# Schema que padroniza o envio de dados para criar um pedido:
class PedidoSchema(BaseModel):
    usuario: int

    class Config:
        from_attributes = True



# Schema que padroniza o envio de dados para realizar login:
class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True



# Schema que padroniza o envio de dados para criar um novo item em um pedido:
class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float

    class Config:
        from_attributes = True



# Schema que padroniza o formato no qual chega a resposta quando buscamos os dados de um pedido:
class ResponsePedidoSchema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[ItemPedidoSchema]

    class Config:
        from_attributes = True