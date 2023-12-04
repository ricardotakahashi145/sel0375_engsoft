import sqlite3
from datetime import datetime

class Produto:
    def __init__(self, codigo, nome, preco, quantidade_estoque):
        self.codigo = codigo
        self.nome = nome
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque

    def __str__(self):
        return f"Código: {self.codigo}, Nome: {self.nome}, Preço: R${self.preco:.2f}, Estoque: {self.quantidade_estoque}"

class Estoque:
    def __init__(self):
        self.produtos = {}

    def adicionar_produto(self, produto):
        if produto.codigo in self.produtos:
            self.produtos[produto.codigo].quantidade_estoque += 1
        else:
            self.produtos[produto.codigo] = produto

    def exibir_estoque(self):
        if not self.produtos:
            print("Estoque vazio.")
        else:
            print("\nEstoque Atual:")
            for produto in self.produtos.values():
                print(produto)

    def descontar_do_estoque(self, codigo):
        if codigo in self.produtos:
            if self.produtos[codigo].quantidade_estoque > 0:
                self.produtos[codigo].quantidade_estoque -= 1
            else:
                print("Produto fora de estoque.")
        else:
            print("Produto não encontrado no estoque.")

class ListaDeCompras:
    def __init__(self, estoque):
        self.compras = []
        self.estoque = estoque

    def adicionar_produto(self, produto):
        if produto.codigo in self.estoque.produtos:
            self.estoque.descontar_do_estoque(produto.codigo)
            self.compras.append(produto)
        else:
            print("Produto não encontrado no estoque.")

    def calcular_subtotal(self):
        return sum(produto.preco for produto in self.compras)

    def exibir_compras(self):
        if not self.compras:
            print("Lista de compras vazia.")
        else:
            print("\nLista de Compras:")
            for produto in self.compras:
                print(produto)
            subtotal = self.calcular_subtotal()
            print(f"Subtotal: R${subtotal:.2f}")


def registrar_compra_no_banco(cpf, data_hora, subtotal):
    conn = sqlite3.connect("registros_compras.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT,
            data_hora TEXT,
            subtotal REAL
        )
    ''')

    cursor.execute('''
        INSERT INTO compras (cpf, data_hora, subtotal) VALUES (?, ?, ?)
    ''', (cpf, data_hora, subtotal))

    conn.commit()
    conn.close()


# Criar instância do Estoque
estoque_loja = Estoque()

# Adicionar produtos ao estoque
produto1 = Produto("001", "Camiseta", 29.99, 10)
produto2 = Produto("002", "Calça Jeans", 59.99, 5)

estoque_loja.adicionar_produto(produto1)
estoque_loja.adicionar_produto(produto2)

# Obter CPF do usuário
cpf = input("Digite seu CPF (ou deixe em branco para não informar): ")

# Exemplo de uso
lista_compras = ListaDeCompras(estoque_loja)

while True:
    codigo_barras = input("Digite o código de barras do produto (ou 'sair' para encerrar): ")

    if codigo_barras.lower() == 'sair':
        break

    if codigo_barras in estoque_loja.produtos:
        lista_compras.adicionar_produto(estoque_loja.produtos[codigo_barras])
    else:
        print("Produto não encontrado no estoque.")

# Exibir lista de compras final com o subtotal
print("\nResumo da Compra:")
if cpf:
    print(f"CPF: {cpf}")
lista_compras.exibir_compras()

# Seção de Pagamento
print("\nSeção de Pagamento:")
print("Opções de pagamento:")
print("1. PIX")
print("2. Cartão de Crédito")
print("3. Cartão de Débito")

opcao_pagamento = input("Escolha a forma de pagamento (1/2/3): ")

if opcao_pagamento == "1":
    print("Realize o pagamento PIX para a seguinte chave: xxxxxxxxx")
elif opcao_pagamento == "2":
    print("Realize o pagamento com cartão de crédito.")
elif opcao_pagamento == "3":
    print("Realize o pagamento com cartão de débito.")
else:
    print("Opção de pagamento inválida.")

# Perguntar se o usuário deseja CPF na nota fiscal
cpf_nota_fiscal = input("Deseja incluir seu CPF na nota fiscal? (s/n): ")

# Simulação da emissão da nota fiscal
print("\nNota Fiscal:")
if cpf_nota_fiscal.lower() == 's':
    print(f"CPF na Nota Fiscal: {cpf}")

lista_compras.exibir_compras()

# Registrar a compra no banco de dados
data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
subtotal = lista_compras.calcular_subtotal()

registrar_compra_no_banco(cpf, data_hora, subtotal)
