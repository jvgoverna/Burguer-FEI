- main.py
- opcoes (cada arquivo tem a função pra lidar com a seleção de uma opção)
  - criar_pedido.py
  - verificar_pedido.py
  - sair.py
  - ...etc
- pedidos.json (esse arquivo não existe antes de termos pedidos pra armazenar)
- utils.py (aqui temos funções que podemos usar em todos os arquivos, utilidades de formatação, validação, leitura de arquivos etc)


No pedidos.json, a estrutura será a seguinte

```json
{
    "1111111111": {
        "CPF": "11111111111",
        "Nome": "João",
        "Senha":"123",
    },
    "22222222222": {
        "CPF": "22222222222",
        "Nome": "Cleber",
        "Senha":"456",
    }
}
```

para cada cliente, temos um dicionário com as informações do cliente indexado pelo CPF.

deve ser acessado no código pelo CPF, da seguinte forma:

```python
# utils.py
import os
import json

def ler_json(arquivo, default=None):
    data = default

    if os.access(arquivo, mode=1):
        with open(arquivo, 'r') as f:
            data = json.load(f)
    return data

def salvar_json(arquivo, data):
    with open(arquivo, 'w+') as f:
        json.dump(data, f,indent=2)  #salvar arquivos json

def validated_input(prompt, validator, error_msg):
    while True:
        value = input(prompt)
        if validator(value):
            return value
        else:
            print(error_msg)
def validate_cpf(cpf):
    if len(cpf) != 11:
        return False
    else:
        return all(map(lambda x: x.isdigit(), cpf.strip())) # map percorre o interável chamando a função para cada item e retorna os resultados em um interável novo
                                                            # lambda cria uma função em uma linha
# main.py
from utils import ler_json, salvar_json, validated_input, validate_cpf

pedidos = utils.ler_json("pedidos.json", default={})	
try:

    CPF = validated_input("Digite o CPF: ", validate_cpf, "CPF deve ter 11 dígitos")

    cliente = pedidos.get(CPF, None)
    senha = ""

    if cliente is None:
        senha = validated_input("Crie uma senha: ", lambda x: len(x.strip()) > 0, "Senha inválida")
        nome = validated_input("Digite o nome: ", lambda x: len(x.strip()) > 0, "Nome inválido")
        cliente = {
            "CPF": CPF,
            "Nome": nome,
            "Senha": senha
        }

        pedidos[CPF] = cliente

        utils.salvar_json("pedidos.json", pedidos)

    else:
        senha  = validated_input("Digite a senha: ", lambda x: x == cliente["Senha"], "Senha inválida")
except e:
    print(e)
    utils.salvar_json("pedidos.json", pedidos)
```