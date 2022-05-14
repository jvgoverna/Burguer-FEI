from fileinput import close
from ntpath import join
from operator import index
import os.path
from posixpath import split
import sys
from time import sleep
from turtle import back


menu_do_pedido=[ # Criei uma variável e coloquei todos os produtos do predido em uma lista
    False, # False meramente lustrativo,para pular o indice 0
    ["x-salada", 10.00],
    ["x-burguer", 10.00],
    ["cachorro-quente", 7.50],
    ["misto quente", 8.00],
    ["salada de frutas", 5.50],
    ["refrigerante", 4.50],
    ["suco natural", 6.25]
]
prompt = "" # variável para chamar novamente no decorrer do código
for index, menu in enumerate(menu_do_pedido): # criei uma estrutura de repetição, e coloquei a variável index, e enumerate para contar cada linha do pedido 
    if menu != False: 
        prompt += f"{index}, {menu[0]}, {menu[1]}\n" # a variável prompt irá armazenar o contador para cada linha do pedido, o que o pedido se trata e o valor de cada item do pedido


def ler_txt(arquivo, default=None): # criei a  função ler_txt para chamar o pedidos.txt que será criado ao fazer um novo pedido ou ao inserir um novo produto
    data = default

    if os.path.isfile(arquivo):
        with open(arquivo, 'r') as f:
            data = f.read()
    else:
        salvar_txt(arquivo,data)
    return data

def salvar_txt(arquivo, data): # criei a função de salvar o pedidos.txt ao criar e inserir um produto. Dentro dela coloquei os parâmetros data e arquivo
    with open(arquivo, "w+") as f:# aqui usei o comando with que basicamente é usado para garantir finalização de recursos adquiridos. É necessário para usar o with uma varíavel para poder, por exemplo escrever dentro do arquivo, nesse caso usei f. Dentro dele coloquei o parâmetro arquivo e o w+ que cria um arquivo novo se não existir, e sobrepõe o arquivo se existir
        f.write(data) # a variável f irá ser usada para escrever dentro do txt


def append_txt(arquivo, data): #criei a função append_txt que irá colocar no final do arquivo o novo pedido, inserir produto , entre outros. Dentro dele coloquei os parâmetros, arquivo e data  
    with open(arquivo, "a") as f: # Abri o parâmetro arquivo , o "a" é usado para é usado para escrever, preservando o conteúdo existente (append).
        f.write(data)  # a variável f irá ser usada para escrever dentro do txt

def validated_input(prompt, validator, error_msg): # criei a função validated_input que irá receber o número que o usuário colocar. Dentro dela coloquei os parâmetros do prompt que seria o menu_do_pedido,o validator para verificar se está certo o input e uma mensagem de erro que falará para digitar novamente caso o usuário não digite um número 
    while True: # Laço de repetição caso for verdadeiro o argumento
        value = input(prompt) # a variável valor irá armazenar o input de um número inteiro do usuário.
        if validator(value): # se digitar o número retornará  o valor
            return value
        else: # se não irá aparecer a mensagem de erro e fará com que o usuário digitar novamente, até que o valor seje correto
            print(error_msg)

def validate_cpf(cpf): # função que fará a verificação se o cpf for correto
    if len(cpf) != 11:# Se o cpf que o usuário irá digitar for maior ou menor que 11 retornará errado e o usuário terá que digitar novamente 
        return False
    else:# se retornar verdadeiro, o all faz com que todos os valores sejam verdadeiros, o map faz com que pegue todos os elementos dentro da lista, que nesse caso será o cpf , o lambda fará com que todos dos valores da lista, que nesse caso será o cpf sejam número(is.digit), e por o strip fim irá separar o cpf da senha e do nome por vírgula dentro do arquivo cadastro.txt
        return all(map(lambda x: x.isdigit(), cpf.strip()))
        
def validate_opcoes(op):
    try:
        valor = int(op)
        return valor in list (range(0,7))
    except:
        return False

def validated_menu(op):
    try:
        valor = int(op)
        return valor in list (range(1,3))
    except:
        return False


def validate_codigo(op):
    try:
        valor = int(op)
        return valor in list (range(0,8))
    except:
        return False


def validate_quantidade(qtd):
    try:
        valor = int(qtd)
        return valor >0
    except:
        return False

def validate_cancela(qtd):
    try:
        valor = int(qtd)
        return valor >= 0
    except:
        return False


def op1():
    try:
        cpf = validated_input("Digite o CPF: ", validate_cpf, "CPF deve ter 11 dígitos")
        cliente = encontrar_client(cpf)
        senha = ""

        if cliente is None:
            senha = validated_input("Crie uma senha: ", lambda x: len(x.strip()) > 0, "Senha inválida")
            nome = validated_input("Digite o nome: ", lambda x: len(x.strip()) > 0, "Nome inválido")
            cliente = [cpf, nome, senha]

            clientes.append(cliente)

            salvar_clientes()
        else:
            senha  = validated_input("Digite a senha: ", lambda x: x == cliente[2], "Senha inválida")
    except Exception as e :
        print(e)
        salvar_txt("clientes.txt", clientes_txt)
    
    
    ler_txt("pedidos.txt", "")
    codigo= validated_input("Digite o código do produto: ", validate_codigo, "Produto inválido digite novamente")
    quantidade = validated_input ("Digite a quantidade que você deseja: ", validate_quantidade, "ERRO! Digite um número maior que 0! ")
    quantidade = int(quantidade)
    codigo = int(codigo)
    multi = quantidade * menu_do_pedido[codigo][1]
    opcao1= f"Pedido: {quantidade}x {menu_do_pedido[codigo][0]} Preco unitario: R${menu_do_pedido[codigo][1]} Total: R${multi}\n" 
    print(f"Pedido: {quantidade}x {menu_do_pedido[codigo][0]}\nPreço unitário: R${menu_do_pedido[codigo][1]}\nTotal: R${multi}" )
    salvar_txt("pedidos.txt",opcao1)
    os.system('cls' if os.name == 'nt' else 'clear')
    adicionar= validated_input("Deseja adicionar mais alguma coisa?\n1 - sim\n2 - não ", validated_menu, "ERRO! Digite 1 ou 2! ")
    if adicionar == "1":
        os.system('cls' if os.name == 'nt' else 'clear')
        print(prompt)
        print(f"{opcao1}\n")
        ler_txt("pedidos.txt","")
        codigo= validated_input("Digite o código do produto: ", validate_codigo, "Produto inválido digite novamente")
        quantidade = validated_input ('Digite a quantidade que você deseja:', validate_quantidade, "ERRO! Digite um número maior que 0! ")
        print("\n")
        quantidade = int(quantidade)
        codigo = int(codigo)
        multi = quantidade * menu_do_pedido[codigo][1]
        retorno= f"Pedido: {quantidade}x {menu_do_pedido[codigo][0]} Preco unitario: R${menu_do_pedido[codigo][1]} Total: R${multi}\n" 
        print(f"Pedido: {quantidade}x {menu_do_pedido[codigo][0]}, Preço unitário: R${menu_do_pedido[codigo][1]} Total: R${multi}")
        append_txt("pedidos.txt",retorno)
        print("\n")
        menu_de_opcoes()
        
    else:
        print("Ok. Voltando para o menu de opções\n")
        menu_de_opcoes()
        


def op2():
    try:
        cpf = validated_input("Digite o CPF: ", validate_cpf, "CPF deve ter 11 dígitos")
        cliente = encontrar_client(cpf)
        senha = ""

        if cliente is None:
            senha = validated_input("Crie uma senha: ", lambda x: len(x.strip()) > 0, "Senha inválida")
            nome = validated_input("Digite o nome: ", lambda x: len(x.strip()) > 0, "Nome inválido")
            cliente = [cpf, nome, senha]

            clientes.append(cliente)

            salvar_clientes()
        else:
            senha  = validated_input("Digite a senha: ", lambda x: x == cliente[2], "Senha inválida")
    except Exception as e :
        print(e)
        salvar_txt("clientes.txt", clientes_txt)

    
    cancelar= validated_input("Você deseja cancelar o pedido?\n1 - sim\n2 - não ", validated_menu, "ERRO! Digite 1 ou 2! ")
    if cancelar == "1":
        confirmar= validated_input("Você realmente deseja cancelar o pedido?\n1 - sim\n2 - não ", validated_menu, "ERRO! Digite 1 ou 2! ")
        if confirmar == "1":
            with open("pedidos.txt","w") as f:
                print("Pedido Cancelado")
                os.system('cls' if os.name == 'nt' else 'clear')
                print(prompt)
                menu_de_opcoes()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(prompt)
            menu_de_opcoes()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(prompt)
        menu_de_opcoes()

def op3():
    try:
        cpf = validated_input("Digite o CPF: ", validate_cpf, "CPF deve ter 11 dígitos")
        cliente = encontrar_client(cpf)
        senha = ""

        if cliente is None:
            senha = validated_input("Crie uma senha: ", lambda x: len(x.strip()) > 0, "Senha inválida")
            nome = validated_input("Digite o nome: ", lambda x: len(x.strip()) > 0, "Nome inválido")
            cliente = [cpf, nome, senha]

            clientes.append(cliente)

            salvar_clientes()
        else:
            senha  = validated_input("Digite a senha: ", lambda x: x == cliente[2], "Senha inválida")
    except Exception as e :
        print(e)
        salvar_txt("clientes.txt", clientes_txt)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(prompt)
    
    ler_txt("pedidos.txt", "")
    codigo= validated_input("Digite o código do produto: ", validate_codigo, "Produto inválido digite novamente")
    quantidade = validated_input ("Digite a quantidade que você deseja: ", validate_quantidade, "ERRO! Digite um número maior que 0! ")
    quantidade = int(quantidade)
    codigo = int(codigo)
    multi = quantidade * menu_do_pedido[codigo][1]
    opcao1= f"Pedido: {quantidade}x {menu_do_pedido[codigo][0]} Preco unitario: R${menu_do_pedido[codigo][1]} Total: R${multi}\n" 
    print(f"Pedido: {quantidade}x {menu_do_pedido[codigo][0]}\nPreço unitário: R${menu_do_pedido[codigo][1]}\nTotal: R${multi}")
    append_txt("pedidos.txt",opcao1)
    os.system('cls' if os.name == 'nt' else 'clear')
    adicionar= validated_input("Deseja adicionar mais alguma coisa?\n1 - sim\n2 - não ", validated_menu, "ERRO! Digite 1 ou 2! ")
    if adicionar == "1":
        os.system('cls' if os.name == 'nt' else 'clear')
        print(prompt)
        print(f"{opcao1}\n")
        ler_txt("pedidos.txt","")
        codigo= validated_input("Digite o código do produto: ", validate_codigo, "Produto inválido digite novamente")
        quantidade = validated_input ('Digite a quantidade que você deseja:', validate_quantidade, "ERRO! Digite um número maior que 0! ")
        print("\n")
        quantidade = int(quantidade)
        codigo = int(codigo)
        multi = quantidade * menu_do_pedido[codigo][1]
        retorno= f"Pedido: {quantidade}x {menu_do_pedido[codigo][0]} Preco unitario: R${menu_do_pedido[codigo][1]} Total: R${multi}\n" 
        print(f"Pedido: {quantidade}x {menu_do_pedido[codigo][0]}Preço unitário: R${menu_do_pedido[codigo][1]}Total: R${multi}")
        append_txt("pedidos.txt",retorno)
        print("\n")
        menu_de_opcoes()
    else:
        print("Ok. Voltando para o menu de opções\n")
        menu_de_opcoes()

def op4():
    try:
        cpf = validated_input("Digite o CPF: ", validate_cpf, "CPF deve ter 11 dígitos")
        cliente = encontrar_client(cpf)
        senha = ""

        if cliente is None:
            senha = validated_input("Crie uma senha: ", lambda x: len(x.strip()) > 0, "Senha inválida")
            nome = validated_input("Digite o nome: ", lambda x: len(x.strip()) > 0, "Nome inválido")
            cliente = [cpf, nome, senha]

            clientes.append(cliente)

            salvar_clientes()
        else:
            senha  = validated_input("Digite a senha: ", lambda x: x == cliente[2], "Senha inválida")
    except Exception as e :
        print(e)
        salvar_txt("clientes.txt", clientes_txt)
        os.system('cls' if os.name == 'nt' else 'clear')
    
    ler_txt("pedidos.txt","")
    if ler_txt("pedidos.txt") == "":
        print("ERRO! Você não fez nenhum pedido!")
        os.system('cls' if os.name == 'nt' else 'clear')
        print(prompt)
        menu_de_opcoes() 
    
    with open("pedidos.txt","r") as f:
            #lines = [l.replace('\n','').split(',') for l in f.readlines()]
            #cancela= []
            #mensagem = '\n'.join(['    ' + ','+"\n".join(l) for l in lines ])
            #print(mensagem )
            lines = f.readlines()
            pedido_cancelado = open("pedidos.txt","a") 
            for index,l in enumerate(lines):
                print(f"{index}- {l}")
            
            cancelar_produto = validated_input("Qual pedido deseja cancelar? ", validate_cancela,"ERRO! Digite o código! ")
            # quantidade = validated_input("Quantas unidades deseja cancelar?", validate_quantidade,"ERRO! Digite o código!")
            # alterado = ','.join([','.join(l) for l in lines]) # l linha do arquivo cancelado;join faz uma lista virar uma string
            # alterado = '\n'.join([''+'\n'.join(l) for l in lines])
            # if -1 < int(cancelar_produto) < len(lines):
                # cancela = " - cancelado"
                # lines[int(cancelar_produto)].append(cancela)
                # alterado = '\n'.join([','.join(l) for l in lines]) # l linha do arquivo cancelado;join faz uma lista virar uma string
                # print("Pedido Cancelado")
                # salvar_txt("pedidos.txt",alterado)
                # menu_de_opcoes()
            # if index == index:
            #     quantidade = validated_input("Quantas unidades deseja cancelar?", validate_codigo,"ERRO! Digite o código! ")
            #     cancelar = " - Cancelado" 
            #     pedido_cancelado= (f"Pedido: {quantidade}x {menu_do_pedido [index][0]}Preço unitário: R${menu_do_pedido[index][1]} {cancelar}\n")
            #     print(pedido_cancelado)
            #     append_txt("pedidos.txt",teste)
            #     pergunta = validated_input("Deseja Cancelar mais algum pedido? 1-sim 2-não ", validate_codigo,"ERRO! Digite 1/2!")
                        
            if -1 < int(cancelar_produto) < len(lines):
                quantidade = validated_input("Quantas unidades deseja cancelar?", validate_codigo,"ERRO! Digite o código! ")
                cancelar = " - Cancelado" 
                pedido_cancelado= (f"Pedido: {quantidade}x {menu_do_pedido [index][0]}Preço unitário: R${menu_do_pedido[index][1]}{cancelar}\n")
                print(pedido_cancelado)
                append_txt("pedidos.txt",pedido_cancelado)
                pergunta = validated_input("Deseja Cancelar mais algum pedido? 1-sim 2-não ", validate_codigo,"ERRO! Digite 1/2!")
                if pergunta =="1":
                    op4()
                else:
                    print("Voltando para o menu de opções!\n")
                    menu_de_opcoes()

                        

                    
def op5():
    try:
        cpf = validated_input("Digite o CPF: ", validate_cpf, "CPF deve ter 11 dígitos")
        cliente = encontrar_client(cpf)
        senha = ""

        if cliente is None:
            senha = validated_input("Crie uma senha: ", lambda x: len(x.strip()) > 0, "Senha inválida")
            nome = validated_input("Digite o nome: ", lambda x: len(x.strip()) > 0, "Nome inválido")
            cliente = [cpf, nome, senha]

            clientes.append(cliente)

            salvar_clientes()
        else:
            senha  = validated_input("Digite a senha: ", lambda x: x == cliente[2], "Senha inválida")
    except Exception as e :
        print(e)
        salvar_txt("clientes.txt", clientes_txt)
        os.system('cls' if os.name == 'nt' else 'clear')
    
    if ler_txt("pedidos.txt","") == "":
        print("Não foi feito nenhum pedido!\n")
        print(prompt)
        menu_de_opcoes()
    else:
        with open("pedidos.txt","r") as f:
            lines = [l.split(',') for l in f.readlines()]
            cancela=[]
            mensagem = '\n'.join(['    ' + ','+"\n".join(l) for l in lines ])
            print(mensagem)
            menu_de_opcoes()

def op6():
    try:
        cpf = validated_input("Digite o CPF: ", validate_cpf, "CPF deve ter 11 dígitos")
        cliente = encontrar_client(cpf)
        senha = ""

        if cliente is None:
            senha = validated_input("Crie uma senha: ", lambda x: len(x.strip()) > 0, "Senha inválida")
            nome = validated_input("Digite o nome: ", lambda x: len(x.strip()) > 0, "Nome inválido")
            cliente = [cpf, nome, senha]

            clientes.append(cliente)

            salvar_clientes()
        else:
            senha  = validated_input("Digite a senha: ", lambda x: x == cliente[2], "Senha inválida")
    except Exception as e :
        print(e)
        salvar_txt("clientes.txt", clientes_txt)
        os.system('cls' if os.name == 'nt' else 'clear')


        
        
        





def menu_de_opcoes():
    numeros= [sys.exit, op1, op2,op3,op4,op5,op6]
    opcoes = validated_input(" 1- Novo Pedido\n 2- Cancela Pedido\n 3- Insere Produto \n 4- Cancela Produto\n 5- Valor do Pedido\n 6- Extrato do Pedido\n \n 0-Sair ", 
    validate_opcoes,
    "Erro digite alguma opção ")
    opcoes = int(opcoes)
    return numeros[opcoes]()

    

clientes_txt = ler_txt("clientes.txt", default="")
clientes = []

for cliente in clientes_txt.split("\n"):
    dados_cliente = cliente.split(",")
    if len(dados_cliente) == 3:
        cpf, nome, telefone = dados_cliente
        clientes.append([cpf, nome, telefone])

def encontrar_client(cpf):
    for c in clientes:
        if c[0] == cpf:
            return c
        return None

def salvar_clientes():
    clientes_txt = ""

    for c in clientes:
        clientes_txt += f"{c[0]},{c[1]},{c[2]}\n"
        salvar_txt("clientes.txt", clientes_txt)
    

try:
    CPF = validated_input("Digite o CPF: ", validate_cpf, "CPF deve ter 11 dígitos")
    cliente = encontrar_client(CPF)
    senha = ""

    if cliente is None:
        senha = validated_input("Crie uma senha: ", lambda x: len(x.strip()) > 0, "Senha inválida")
        nome = validated_input("Digite o nome: ", lambda x: len(x.strip()) > 0, "Nome inválido")
        cliente = [CPF, nome, senha]

        clientes.append(cliente)

        salvar_clientes()
    else:
        senha  = validated_input("Digite a senha: ", lambda x: x == cliente[2], "Senha inválida")
except Exception as e :
        print(e)
        salvar_txt("clientes.txt", clientes_txt)
menu_de_opcoes()









#dados=[]  #os foi utilizado para o sistema verificar se o arquivo(pedidos) existe
#if os.access("pedidos.json",mode=1): # a extensão json foi utilizada para armazenar os dados dentro de uma lista e poder utilizar depois
    #dados=json.load(open("pedidos.json")) # carregando os dados do arquivo em uma variável


#def menu_opcoes():
    #bemvindo=input("Você já fez o seu pedido??(sim/não)")
    #lista=["sim","não"]
    #while not bemvindo in lista:   
       #print("ERRO! Digite sim ou não")
        #bemvindo=input("Você já fez o seu pedido??(sim/não) ")
    #if bemvindo=="sim":
        #print("O seu pedido já foi feito!")
        #resposta=int(input(" 1- Novo Pedido\n 2- Cancela Pedido\n 3- Insere Produto \n 4- Cancela Produto\n 5- Valor do Pedido\n 6- Extrato do Pedido\n \n 0-Sair "))
    #else: 
        #print("Seja bem-vindo(a) à Burguer FEI!!")
        #resposta=int(input(" 1- Novo Pedido\n 2- Cancela Pedido\n 3- Insere Produto \n 4- Cancela Produto\n 5- Valor do Pedido\n 6- Extrato do Pedido\n \n 0-Sair "))
        
        
        #if resposta==1:
            #def opção1():
                #with open("pedidos.txt","a") as pedidos:    #with: trata todos os métodos de abrir e fechar o arquivo(automaticamente)
                    #nome=input("Nome: \n")
                    #while nome.strip() == "":
                        #print("Esse campo é obrigatório!")
                        #nome=input("Nome: \n")
                    #CPF=input("CPF: \n")
                    #while CPF.strip() == "":
                        #print("Esse campo é obrigatório!")
                        #CPF=input("CPF: \n")
                    #senha=input("Senha: \n")
                    #while senha.strip() == "":
                        #print("Esse campo é obrigatório!")
                        #senha=input("senha: \n")
                    #pedidos.write(f"nome: {nome}\nCPF: {CPF}\nsenha: {senha}\n\n")
            #opção1()

        
        #elif resposta==2:
            
            #def opção2():
                #menu_do_pedido=[" X-salada","X-Burguer","Cachorro Quente","Misto Quente","Salada de Frutas","Refrigerante","Suco Natural"]
                #preços=[10.00,10.00,7.50,8.00 ,5.50 ,4.50 ,6.25]
                #a=0
    
        #for pedido in menu_do_pedido:
            #print(f"{a+1} {pedido} {preços[a]}\n")
            #a+=1
        #usuario_código=input("Digite o código do produto: ")   
        #usuario_quantidade=int(input("Digite a quantidade do produto: "))


        #with open("pedidos.txt","r") as pedidos:
            #CPF=input("Digite o seu CPF: ")
            #senha= input("Digite a sua senha: ")
            #print(pedidos) #if CPF and senha == pedidos:
                        # #print("Pedido Cancelado!!")

            
            
            
            
            
            
            
            #opção2()               


            #menu_do_pedido=["" X-salada","X-Burguer","Cachorro Quente","Misto Quente","Salada de Frutas","Refrigerante","Suco Natural"]
    #preços=[10.00,10.00,7.50,8.00 ,5.50 ,4.50 ,6.25]
    #a=0
    
    #for pedido in menu_do_pedido:
        #print(f"{a+1} {pedido} {preços[a]}\n")
        #a+=1
    #usuario_código=input("Digite o código do produto: ")   
    #usuario_quantidade=int(input("Digite a quantidade do produto: "))


#menu_opcoes()


#isvalid=all(map(lambda x: x.isdigit(),usuario_código))

#menu_do_pedido=["","X-salada","X-Burguer","Cachorro Quente","Misto Quente","Salada de Frutas","Refrigerante","Suco Natural"]
        #preços=[0,10.00,10.00,7.50,8.00 ,5.50 ,4.50 ,6.25]
        #a=0
        
        #for pedido in menu_do_pedido:
            #print(f"{a+1} {pedido} R$ {preços[a]}\n")
            #a+=1 