from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import random

Base = declarative_base()

# Tabela de Clientes
class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    estado = Column(String, nullable=False)
    saldo = Column(Float, nullable=False, default=0.0)
    transacoes = relationship("Transacao", back_populates="cliente")

# Tabela de Produtos
class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    transacoes = relationship("Transacao", back_populates="produto")

# Tabela de Transações
class Transacao(Base):
    __tablename__ = 'transacoes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
    
    cliente = relationship("Cliente", back_populates="transacoes")
    produto = relationship("Produto", back_populates="transacoes")

# Criando o banco de dados SQLite e as tabelas
def criar_banco():
    engine = create_engine('sqlite:///local.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Inserindo dados aleatórios
    nomes_clientes = ["Usuario1", "Usuario2", "Usuario3", "Usuario4", "Usuario5"]
    emails_clientes = ["usuario1@gmail.com", "usuario2@email.com", "usuario3@email.com", "usuario4@email.com", "usuario5@email.com"]
    estados_clientes = ["SP", "RJ", "MG", "BA", "RS"]
    saldos_clientes = [random.uniform(100, 5000) for _ in range(len(nomes_clientes))]
    
    produtos_lista = [
        "Notebook", "Monitor", "Teclado", "Mouse", "Impressora",
        "Papel A4", "Caneta Azul", "Caneta Vermelha", "Lapis", "Borracha",
        "Caderno", "Estojo", "Grampeador", "Clips", "Post-it",
        "Calculadora", "Fone de Ouvido", "HD Externo", "Pendrive", "Roteador",
        "Webcam", "Mesa Digitalizadora", "Toner de Impressora", "Cartucho de Tinta", "Suporte para Monitor",
        "Mousepad", "Organizador de Mesa", "Pasta Catalogo", "Envelope", "Etiqueta adesiva",
        "Projetor", "Tela de Projeçao", "Mesa para Escritorio", "Cadeira Ergonomica", "Armario Arquivo",
        "Bloco de Notas", "Agenda", "Telefone Fixo", "Extensao Eletrica", "Nobreak",
        "Scanner", "Softwares Office", "Licença de Antivirus", "Placa de Video", "Memoria RAM",
        "Processador", "Placa-Mae", "Fonte de Alimentação", "Gabinete", "Suporte para CPU"
    ]
    produtos = [(nome, random.uniform(10, 3000)) for nome in produtos_lista]  # 50 produtos reais

    # Adicionando clientes
    clientes = [
        Cliente(nome=nomes_clientes[i], email=emails_clientes[i], estado=estados_clientes[i], saldo=saldos_clientes[i])
        for i in range(len(nomes_clientes))
    ]
    session.add_all(clientes)
    session.commit()

    # Adicionando produtos
    produtos_objs = [Produto(nome=p[0], preco=p[1]) for p in produtos]
    session.add_all(produtos_objs)
    session.commit()

    # Adicionando transações aleatórias
    for _ in range(300):  # 300 transações
        cliente = random.choice(clientes)
        produto = random.choice(produtos_objs)
        quantidade = random.randint(1, 5)
        total = quantidade * produto.preco
        transacao = Transacao(cliente_id=cliente.id, produto_id=produto.id, quantidade=quantidade, total=total)
        session.add(transacao)
    session.commit()

    print("Banco de dados criado com sucesso")

if __name__ == "__main__":
    criar_banco()