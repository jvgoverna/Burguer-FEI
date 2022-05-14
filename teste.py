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




