import os
import re
import glob
import pandas as pd

def extrair_resposta_final(caminho_ficheiro):
    print(f"A limpar raciocínios em: {caminho_ficheiro}")
    
    # 1. Carregar o CSV garantindo o separador correto e tratando strings textuais
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
            # Devolve no formato ;Letra; que queres para o teu mapeamento final
            return f";{letra};"
        
        # Se não encontrar a tag, mantém o original para saberes que houve falha no modelo
        return texto

    # Apply a limpeza a toda a coluna
    df[coluna_alvo] = df[coluna_alvo].apply(limpar_linha)

    # 2. Gravar de volta mantendo o formato original com ponto e vírgula
    df.to_csv(caminho_ficheiro, sep=';', index=False, encoding='utf-8')
    print(f"✓ Ficheiro {os.path.basename(caminho_ficheiro)} limpo com sucesso!\n")

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