from datetime import datetime
import os

def transformar_clientes(dados):
    clientes = {}
    cpf = ''
    for line in dados:
        line = line.replace('\n','').strip()
        if line.startswith('-'): #startwith ele verifica se a linha começa com caracter especificado
            line = line.replace('-','') # retirando o "-" da linha
            cpf = line

            clientes[cpf] = {}
        elif ':' in line and cpf != '':
            propriedade, valor = [l.strip() for l in line.split(':')]

            valor = valor.strip()
            propriedade = propriedade.strip()
            eh_lista = valor.startswith('[') and valor.endswith(']')
            if not '.' in propriedade and not eh_lista:
                clientes[cpf][propriedade] = valor
                continue
            if eh_lista:
                valor = valor.replace('[','').replace(']','') 
                lista = []
                for item in valor.split(';'):
                    pares = [parte.strip() for parte in item.split(',')]

                    valor_item = {}

                    for par in pares:
                        chave, sub_valor = par.split('-')
                        sub_valor = sub_valor.strip()
                        valor_item[chave.strip()] = int(sub_valor) if sub_valor.isdigit() else sub_valor
                    lista.append(valor_item)
                clientes[cpf][propriedade] = lista
            else:
                propriedade, sub_propriedade = propriedade.split('.')
                if not clientes[cpf].get(propriedade):
                    clientes[cpf][propriedade] = {}
                clientes[cpf][propriedade][sub_propriedade] = int(valor) if valor.isdigit() else valor
    return clientes


def gravar_clientes(clientes):
    linhas = []

    for cliente in clientes.values():
        cpf = cliente.get('cpf') # get serve para não dar erro se um item não existir no dicionário
        nome = cliente.get('nome')
        senha = cliente.get('senha')

        linhas.append(f'-{cpf}')
        linhas.append(f'cpf: {cpf}')
        linhas.append(f'senha: {senha}')
        linhas.append(f'nome: {nome}')
        if cliente.get('pedido', {}) is not None:
            for cod_produto, quantidade in cliente.get('pedido', {}).items():
                linhas.append(f'pedido.{cod_produto}: {quantidade}')
        
        extrato = []

        if cliente.get('extrato', {}) is not None:
            for item_extrato in cliente.get('extrato', []):
                item_extrato_str = []

                for chave, valor in item_extrato.items():
                    item_extrato_str.append(f'{chave} - {valor}')
                item_extrato_str = ','.join(item_extrato_str)
                extrato.append(item_extrato_str)
            extrato = ';'.join(extrato)
            extrato = f'[{extrato}]'

            linhas.append(extrato)
        linhas.append('')
    linhas =  '\n'.join(linhas)
    return linhas

def salvar_dados(arquivo, dados):  
    with open(arquivo, 'w+') as f: # With abre e fecha o arquivo json no modo write w+ cria um arquivo novo se não existir, e sobrepõe o arquivo se existir
        f.write(gravar_clientes(dados))
        return dados
# Carrega um arquivo json e retorna um dicionario ou lista, default- valor padrão do arquivo que vai ler  
def ler_dados(arquivo, default = {}):
    dados = default # dados = default
    try:
        with open(arquivo, 'r') as f: # abre o arquivo no modo read
            dados = open('pedidos.txt').readlines()

            return transformar_clientes(dados)
    except Exception as e:
        salvar_dados(arquivo, dados) # Se não existir o arquivo, criá-lo, e salvar os dados padrões nele
        return dados # retorna o default

# receber um input do usuário, validá-lo e retornar o valor transformado de uma função passada como parametro. 
# Se essa função levantar uma exceção, mostra uma mensagem de erro
def validated_input(prompt, transformar):
    while True: # rodar isso enquanto não houver um input satisfatório
        try: # lidar com exceções dentro deste bloco
            valor = transformar(input(prompt)) # chama a função transformar com o input do usuário, usando a mensagem de prompt
            return valor # retorna o valor transformado
        except Exception as e: # se a função transformar levantar uma exceção, mostra a mensagem de erro
            print(e) # mostra o erro 

# constantes pra referenciar os arquivos
ARQUIVO_CLIENTES = 'pedidos.txt' 

produtos = {
    "1":{
        "codigo": "1",
        "nome": "X-salada",
        "preco": 10.00
      },
    "2":{
        "codigo":"2",
        "nome": "X-burguer",
        "preco": 10.00
    },
    "3":{
        "codigo":"3",
        "nome":"Cachorro-quente",
        "preco":7.50
    },

    "4":{
        "codigo":"4",
        "nome":"Misto Quente",
        "preco":8.00
    },
    "5":{
        "codigo":"5",
        "nome":"Salada de Frutas",
        "preco":5.50
    },
    "6":{
        "codigo":"6",
        "nome":"Refrigerante",
        "preco":4.50
    },
    "7":{
        "codigo":"7",
        "nome":"Suco Natural",
        "preco":6.25
    }   
}
 # carrega o arquivo json com os clientes 
clientes = ler_dados(ARQUIVO_CLIENTES, {})

ACAO_ADICIONAR_PRODUTO = 'adicionar_produto'
ACAO_REMOVER_PRODUTO = 'remover_produto'

opcoes_menu = [ # variável que retorna uma lista com o menu do pedido
    'Sair',
    'Novo pedido',
    'Cancela pedido',
    'Insere produto',
    'Cancela produto',
    'Valor do pedido',
    'Extrato do pedido'
]

#função para validar uma opção do menu de opções
def validar_opcao(op):
    op = int(op) # precisa ser um número inteiro
    if op < 0 or op >= len(opcoes_menu): # se op for menor que 0 ou op maior ou igual ao numero de opçoes do menu de opções  
        # lança uma exceção, que sera interecepta pela validate_input, 
        # e mostrada como mensagem  de erro
        raise Exception('Opção inválida') 
    return op # retorna a variável op


def validar_cpf(cpf): # função para validar o cpf
    if len(cpf) != 11: # se o cpf for diferente de 11 dígitos retornará a mensagem de erro!
        raise Exception('CPF deve ter 11 digitos')
    
    for caracter in cpf.strip(): # faz um loop passando por cada caracter do cpf, ignorando os espaços no inicio e fim- (Strip)
        if not caracter.isdigit(): # se a variável caracter não for um número retornará uma mensagem de erro
            raise Exception('CPF deve conter apenas números')
    return cpf # se verdadeiro retornará o número do cpf

def validar_senha(senha): # função para validar a senha 
    if len(senha.strip()) < 0: # se o tamanho da variável senha inserida pelo usuário for menor que 0, retornará uma mensagem de erro
        raise Exception('Senha inválida') # Mensagem de ERRO!
    return senha # se não retornará a senha inserida

def validar_codigo_produto(codigo): # função para validar o código do produto 
    if codigo.strip() not in produtos: # verifica se o codigo do produto existe, ou seja, se é uma chave do dicionario de produtos
        raise Exception('Código de produto inválido') # se não existir retornará uma mensagem de erro
    return codigo.strip() # se existir retornará o código inserido, ignorando espaços no começo e no fim 

def validar_quantidade(quantidade): # função para verificar se a quantidade inserida pelo usuário é valida
    try: # tente
        quantidade = int(quantidade.strip()) # a variável quantidade deverá ser inserida como número inteiro e sem espaços no começo e no fim 
        return quantidade #se correto retornará o valor inserido
    except Exception as e: # se não retornará uma mensagem de erro
        raise Exception('Quantidade deve ser um número')

def validar_sim_nao(opcao):
    if opcao.strip().lower() not in ['s','n']: # transforma a variável opcao em minúsculo, e verifica se o usuário digitar 's' ou 'n'
        raise Exception('Opção inválida') # se o usuário não digitar 's' ou 'n' irá retornar a mensagem de erro
    return opcao.strip().lower() == 's' # retorna True se for 's' (sim), False se for 'n' (nao)

def menu_pedido(): # variável que retorna a lista menu do pedido com um espaço (\n)
    print('\n')
    for produto in produtos.values(): # percorre todos os produtos
        print(f'{produto["codigo"]} - {produto["nome"]} - R$ {produto["preco"]}') # mostra na tela do usuário o código do produto, o nome do produto e o preço do mesmo 
    print('\n') #Pula linha

def autenticar(nome): 
    # return clientes["12345678910"]
    while True: # laço de repetição ao inserir algo errado perguntará novamente até a resposta for verdadeira
        cpf = validated_input('CPF: ', validar_cpf) # cpf = a função de validar o input (cpf = escreverá dentro do dicionário o que o usuário digitar, se for menor que 11 terá que digitar novamente)
        senha = validated_input('Senha: ', validar_senha) # senha = a função de validar a senha (senha = escreverá dentro do dicionário a senha que o usuário digitar,
        # se o usuário não digitar nada, os mesmo terá que digitar novamente )

        if cpf in clientes: # veriifica se o cliente existe
            if clientes[cpf]['senha'] == senha: # verifica se a senha inserida é a mesma da cadastrada

                if nome != clientes[cpf]['nome']: # verifica se o nome mudou, e se sim, salva o novo
                    clientes[cpf]['nome'] = nome
                    salvar_dados(ARQUIVO_CLIENTES, clientes) # Se o nome mudar irá subscrever o antigo pelo novo

                return clientes[cpf] # Após essa autenticação irá para else
        else: # cria um novo cliente
            clientes[cpf] = { # se o usuário digitar um outro cpf criará outro pedido
                'nome': nome, 
                'senha': senha,
                'cpf': cpf,
                'pedido': None,# pedido não é nada porque o usuário acabou de se cadastrar
                'extrato': [] # extrato lista vazia para ser escrita dps
            }
            salvar_dados(ARQUIVO_CLIENTES, clientes) # salva os dados no clientes.json
            return clientes[cpf]

def calcular_total(pedido): # variavél para calcular o total que o usuário deverá pagar no final no pedido
    total = 0 # Valor inicial sem fazer nenhum pedido
    for cod_produto, quantidade in pedido.items(): # Laço para subscrever o dicionário pedido que se encontra dentro do clientes.json.  cod_produto - código de cada item do cardápio, quantidade- quantidade que o usuário deseja 
        produto = produtos[cod_produto] # Verifica se o código que irá ser inserido será igual ao cod_produto
        total += produto['preco'] * quantidade # Total- irá calcular o preço de cada produto. Preço- item dentro de um dicionário. Nesse caso será o código , armazenado no produtos.json
    return total # Retorna o valor total 

# O produtos.json armazena um dicionário com o cardápio, dentro deele terá o nome, preço e o código do produto
# O clientes.json armazena um dicionário com o cpf do usuário. Dentro dele armazenará o nome, cpf e senha inseridos pelo usuário com seus respectivos valores.
# Além de armazenar um outro dicionário com o pedido do usuário, dentro dele pegará os valores dentro do produtos.json e armazenará a quantidade e o código do produto inserido.
# por fim armazenará o extrato no final do pedido. Ao adicionar, ou remover um produto aparecerá dentro do dicionário extrato os item adicionados ou removidos, além da quantidade.


def opcao1(cliente): # função para fazer o pedido, se o pedido já for feito e o usuário querer adicionar mais um pedido, deve ir na opção inserir produto (3)
# Caso contrário irá aparecer a mensagem "Pedido já existe e retornará a paginá inicial (Menu de opções)"

    if not cliente['pedido'] is None:  # se o pedido já for feito retornará a mensagem
        print('Pedido já existe') # Mensagem 
        return
   
    # Se o pedido não tiver sido feito retornará a variável aicionando e apresentará o cardápio, um input pedindo pro usuário digitar o código e a quantidade do produto
    cliente['pedido'] = {
    }

    adicionando = True

    while adicionando:
        menu_pedido() # Aparecerá o cardápio
        
        codigo_produto = validated_input('Código do produto: ', validar_codigo_produto) # se o usuário não digitar o código aparecerá código de produto inválido

        quantidade = validated_input('Deseja adicionar quantas unidades?  ', validar_quantidade) #se o usuário não digitar a quantidade correta apresentará Código de produto inválido
        

        if not codigo_produto in cliente['pedido']: 
            cliente['pedido'][codigo_produto] = 0 # inicializa o produto com 0 unidades dentro do pedido

        # adiciona o produto ao pedido do cliente, se o produto já estava lá, aumenta a quantidade
        cliente['pedido'][codigo_produto] += quantidade
        cliente['extrato'].append({
            'acao': ACAO_ADICIONAR_PRODUTO,
            'codigo_produto': codigo_produto,
            'quantidade': quantidade
        })
        
        salvar_dados(ARQUIVO_CLIENTES, clientes)

        adicionando = validated_input('Deseja adicionar mais algum produto? (S/N) ', validar_sim_nao)

def opcao2(cliente):
    if cliente['pedido'] is None:
        print('Não há pedido para cancelar')
        return
    resposta = validated_input('Deseja cancelar o pedido? (S/N) ', validar_sim_nao)
    
    if resposta:
        cliente['pedido'] = None
        cliente['extrato'] = []
        salvar_dados(ARQUIVO_CLIENTES, clientes)

        print('Pedido cancelado')

def opcao3(cliente):
    if cliente['pedido'] is None:
        print('Não há pedido para inserir produto')
        return
    
    menu_pedido()
        
    codigo_produto = validated_input('Código do produto: ', validar_codigo_produto)

    quantidade = validated_input('Deseja adicionar quantas unidades?  ', validar_quantidade)
    

    if not codigo_produto in cliente['pedido']:
        cliente['pedido'][codigo_produto] = 0

    cliente['pedido'][codigo_produto] += quantidade
    cliente['extrato'].append({
        'acao': ACAO_ADICIONAR_PRODUTO,
        'codigo_produto': codigo_produto,
        'quantidade': quantidade
    })
    
    salvar_dados(ARQUIVO_CLIENTES, clientes)
    print('Produto adicionado')

def opcao4(cliente):
    if cliente['pedido'] is None:
        print('Não há pedido para remover produto')
        return
    
    # percorre todos os produtos do pedido (cada item é uma tupla com codigo e quantidade)
    for cod_produto, quantidade in cliente['pedido'].items(): 
        print(f'{cod_produto} - {produtos[cod_produto]["nome"]} - {quantidade} unidades')

    def validar_produto_no_pedido(codigo_produto):
        if not codigo_produto in cliente['pedido']:
            raise Exception('Produto não está no pedido')
        return codigo_produto

    codigo_produto = validated_input('Código do produto: ', validar_produto_no_pedido)
    
    def validar_quantidade_no_pedido(quantidade):
        try:
            quantidade = int(quantidade)
        except:
            raise Exception('Quantidade deve ser um número')

        if 0 < quantidade <= cliente['pedido'][codigo_produto]:
            return quantidade
        raise Exception('Quantidade deve ser maior que 0 e menor ou igual a quantidade no pedido')

    quantidade = validated_input('Deseja remover quantas unidades?  ', validar_quantidade_no_pedido)

    cliente['pedido'][codigo_produto] -= quantidade

    if cliente['pedido'][codigo_produto] == 0:
        del cliente['pedido'][codigo_produto]

    cliente['extrato'].append({
        'acao': ACAO_REMOVER_PRODUTO,
        'codigo_produto': codigo_produto,
        'quantidade': quantidade
    })

    salvar_dados(ARQUIVO_CLIENTES, clientes)



def opcao5(cliente):
    if cliente['pedido'] is None:
        print('Não há pedido para mostrar o total')
        return
    
    total = calcular_total(cliente['pedido'])

    print(f'Total: R$ {total:.2f}')


def opcao6(cliente):
    if cliente['pedido'] is None:
        print('Não há pedido para mostrar o extrato')
        return

    total = calcular_total(cliente['pedido'])

    '''
    %Y - Ano (4 dígitos)
    %m - Mês (2 dígitos)
    %d - Dia (2 dígitos)
    %H - Hora (2 dígitos)
    %M - Minuto (2 dígitos)
    '''
    data = datetime.now().strftime('%Y-%m-%d %H:%M')

    dados = [
        'Nome: ' + cliente.get('nome'),
        f'CPF: '+ cliente.get("cpf"),
        f'Total: R$ {total:.2f}',
        f'Data: {data}',
        'Itens do pedido:',
    ]

    for entrada in cliente['extrato']:
        acao = entrada['acao']
        produto = produtos[entrada['codigo_produto']]
        preco_produto = produto.get('preco')
        total_produto = entrada.get('quantidade') * preco_produto

      
        nova_linha = [str(entrada.get('quantidade')), produto.get('nome'), 'Preço unitário: ', f'{preco_produto:.2f}']
        if acao == ACAO_ADICIONAR_PRODUTO:
            nova_linha.append(f'Valor: + {total_produto:.2f}')
        else:
            nova_linha.append(f'Valor: - {total_produto:.2f} - Cancelado')
        
        dados.append(' - '.join(nova_linha))
    
    print('\n'.join(dados))
def main():
    nome = input('Nome: ').strip()
    # nome = "Paulo"

    # pede cpf e senha do cliente, o criando se não existir,
    #  e altera o nome se ele tiver mudado
    
    
    while True:
        print('\n')
        print('\n'.join([f'{op} - {opcoes_menu[op]}' for op in range(1, len(opcoes_menu))])) # mostrar as opções a partir do index 1
        print(f'\n0 - {opcoes_menu[0]}') # mostrar a opção de sair (index 0)
        
        op = validated_input("\nDigite sua opção: ", validar_opcao)

        if op == 0: # se a opção for 0, sair
            break

        cliente = autenticar(nome) # autentica o cliente
        if op == 1: # se a opção for 1, criar um novo pedido
            opcao1(cliente)
          
        if op == 2: # se a opção for 2, cancelar o pedido
            opcao2(cliente)
        
        if op == 3:
            opcao3(cliente)

        if op == 4:
            opcao4(cliente)

        if op == 5:
            opcao5(cliente)

        if op == 6:
            opcao6(cliente)
try:  
    # with open('test.json','w+') as f:
    #     json.dump(ler_dados(ARQUIVO_CLIENTES),f,indent=2)
    main()
except Exception as e:
    print(e)
    salvar_dados(ARQUIVO_CLIENTES, clientes)