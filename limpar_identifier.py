import os

def deletar_arquivos_com_extensao(caminho_pasta, extensao):
    for pasta_atual, subpastas, arquivos in os.walk(caminho_pasta):
        for arquivo in arquivos:
            if arquivo.endswith(extensao):
                caminho_arquivo = os.path.join(pasta_atual, arquivo)
                try:
                    os.remove(caminho_arquivo)
                    print(f"Arquivo excluído: {caminho_arquivo}")
                except Exception as e:
                    print(f"Erro ao excluir {caminho_arquivo}: {str(e)}")

# Substitua 'caminho_da_sua_pasta' pelo caminho da pasta que você deseja percorrer
# e '.Identifier' pela extensão do arquivo que deseja excluir
deletar_arquivos_com_extensao('.', '.Identifier')
