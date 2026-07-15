import os
import re
import glob

def processar_no_proprio_ficheiro(caminho_ficheiro):
    print(f"A processar (in-place): {caminho_ficheiro}")
    
    # 1. Ler o conteúdo original como texto bruto
    with open(caminho_ficheiro, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # --- REGRA 1: Substituir \n por \\n (quebra de linha real por string "\n") ---
    conteudo_processado = conteudo.replace('\n', '\\n')

    # --- REGRA 2: Reverter para quebra de linha real APENAS no início de registos ---
    padrao_registo_csv = r'\\n\s*(\d+;)'
    conteudo_processado = re.sub(padrao_registo_csv, r'\n\1', conteudo_processado)

    # --- REGRA 3: Alterar \n \n (ou \n\n) literais para apenas um \n literal ---
    padrao_duplo_n = r'\\n\s*\\n'
    conteudo_processado = re.sub(padrao_duplo_n, r'\\n', conteudo_processado)

    # --- REGRA 4: Substituir ;1; por A, ;2; por B, ;3; por C, ;4; por D ---
    # Criamos um mapeamento dos números para as respetivas letras
    mapeamento = {'1': 'A', '2': 'B', '3': 'C', '4': 'D'}
    
    # A função determina o que colocar com base no número capturado no Grupo 1
    def substituir_por_letra(match):
        numero = match.group(1)
        return mapeamento[numero]

    # Procuramos o padrão ;[1-4]; e aplicamos a substituição
    padrao_letras = r';([1-4]);'
    conteudo_processado = re.sub(padrao_letras, substituir_por_letra, conteudo_processado)

    # 2. Gravar de volta no próprio ficheiro, substituindo o conteúdo anterior
    with open(caminho_ficheiro, 'w', encoding='utf-8', newline='') as f:
        f.write(conteudo_processado)
        
    print(f"Ficheiro {os.path.basename(caminho_ficheiro)} atualizado com sucesso!\n")

def processar_pasta(pasta):
    ficheiros_csv = glob.glob(os.path.join(pasta, "*.csv"))
    
    if not ficheiros_csv:
        print(f"Alerta: Nenhum ficheiro .csv encontrado na pasta: {pasta}")
        return

    for ficheiro in ficheiros_csv:
        processar_no_proprio_ficheiro(ficheiro)

# --- EXECUÇÃO ---
if __name__ == "__main__":
    pasta_alvo = "./" 
    processar_pasta(pasta_alvo)