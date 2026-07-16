import os
import re
import glob
import pandas as pd

def extrair_resposta_final(caminho_ficheiro):
    print(f"A limpar raciocínios em: {caminho_ficheiro}")
    
    # 1. Carregar o CSV garantindo o separador correto
    try:
        df = pd.read_csv(caminho_ficheiro, sep=';', on_bad_lines='skip')
    except Exception as e:
        print(f"Erro ao ler o ficheiro {caminho_ficheiro}: {e}")
        return

    coluna_alvo = 'Raciocinio_Gerado_Pelo_Modelo'
    
    # Verificar se a coluna existe no ficheiro atual
    if coluna_alvo not in df.columns:
        print(f"Aviso: Coluna '{coluna_alvo}' não encontrada em {os.path.basename(caminho_ficheiro)}. A saltar...")
        return

    # Expressão regular para apanhar o que está dentro das tags <resposta>X</resposta>
    padrao_tag = r'<resposta>\s*([A-D])\s*</resposta>'

    def limpar_linha(texto):
        if pd.isna(texto):
            return texto
        
        texto_str = str(texto)
        match = re.search(padrao_tag, texto_str, re.IGNORECASE)
        
        if match:
            letra = match.group(1).upper()
            # Colocamos a estrutura base da letra
            return f";{letra};{letra}"
        
        return texto

    # Aplica a limpeza a toda a coluna
    df[coluna_alvo] = df[coluna_alvo].apply(limpar_linha)

    # 2. Gravar temporariamente com o pandas (ele vai meter aspas por causa dos ponto e vírgula)
    df.to_csv(caminho_ficheiro, sep=';', index=False, encoding='utf-8')

    # 3. Pós-processamento de Texto Bruto: Remove as aspas geradas automaticamente pelo Pandas
    with open(caminho_ficheiro, 'r', encoding='utf-8') as f:
        conteudo_limpo = f.read()

    # Procura padrões como ";C;C" ou C;C;" e limpa as aspas indesejadas
    conteudo_limpo = re.sub(r'(";([A-D]);([A-D])")', r';\2;\3', conteudo_limpo)
    conteudo_limpo = re.sub(r'";([A-D]);";([A-D]);"', r';\1;\2', conteudo_limpo)
    
    # Remove aspas literais duplas remanescentes que fiquem coladas às letras das respostas
    conteudo_limpo = re.sub(r'"?([A-D])"?;"?([A-D])"?', r'\1;\2', conteudo_limpo)

    # 4. Grava o ficheiro final sem aspas na coluna de resposta
    with open(caminho_ficheiro, 'w', encoding='utf-8', newline='') as f:
        f.write(conteudo_limpo)

    print(f"✓ Ficheiro {os.path.basename(caminho_ficheiro)} limpo e formatado como ;C;C com sucesso!\n")

def processar_pasta(pasta):
    ficheiros_csv = glob.glob(os.path.join(pasta, "*.csv"))
    
    if not ficheiros_csv:
        print(f"Alerta: Nenhum ficheiro .csv encontrado na pasta: {pasta}")
        return

    for ficheiro in ficheiros_csv:
        extrair_resposta_final(ficheiro)

# --- EXECUÇÃO ---
if __name__ == "__main__":
    # Executa na pasta atual
    pasta_alvo = "./" 
    processar_pasta(pasta_alvo)