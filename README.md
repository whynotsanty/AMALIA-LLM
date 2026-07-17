# Metodologia e Datasets: Avaliação do AMALIA-9B Quantizado

Este documento resume a infraestrutura de testes desenvolvida para avaliar o impacto da Quantização Pós-Treino (PTQ) no modelo fundacional português AMALIA-9B. A avaliação está dividida em duas dimensões complementares.

## Dimensão I: Engenharia e Hardware (Análise Técnica)

Esta dimensão foca-se no impacto "físico" e matemático da compressão dos pesos do modelo (do formato original BF16 até ao extremo Q2_K).

**O que é analisado?**
* **Perplexidade (PPL):** A degradação matemática da capacidade do modelo prever a próxima palavra.
* **Consumo de Recursos:** Alocação de memória RAM e VRAM necessária para carregar o modelo.
* **Velocidade de Inferência:** Medição em *tokens por segundo* nas fases de *prefill* e *decode*.
* **Redução:** A percentagem de compressão e poupança de espaço obtida no tamanho do modelo quando comparado com a versão original em precisão total (BF16, que serve de baseline com 0.0% de redução).
* **AvgLoss:** A perda média de desempenho associada à quantização face ao baseline de referência.

**Dataset Utilizado:**
* **`PorTEXTO`**: Um *corpus* massivo de textos nativos de Portugal. É utilizado de forma passiva (leitura contínua) para calcular a perplexidade isolando a estrutura do PT-PT, sem introduzir ruído de tarefas complexas.


## Dimensão II: Capacidades Linguísticas e Culturais (Análise Prática)

Esta dimensão avalia as quantização, mapeando o ponto de rutura onde o modelo perde a sua capacidade de seguir ordens, raciocinar e lembrar-se da cultura portuguesa.

### Subdimensão II - A (Competência Linguistica e Semãntica Gerativa)
* **Teste A (`amalia-smoltalk2_everyday_conv_pt`):** Mede a naturalidade e a fluidez das respostas numa interação contínua, simulando a coesão exigida a um assistente virtual no dia a dia.
* **Teste B (`amalia-PTradutor`):** Avalia a tradução (EN -> PT). O foco é verificar se a quantização destrói a resiliência do modelo em manter o PT-PT, cedendo ao viés estatístico de gerar vocabulário ou gerúndios em PT-BR.
* **Teste C (`smol-rewrite-PT`):** Avalia a reescrita e adaptação de tom, medindo a capacidade do modelo adaptar o texto para um tom pedido, preservando o seu significado principal.

### Subdimensão II - B (Integridade Cognitiva, Conhecimento Factual e Cultura)
* **Teste D (`pt_exams`):** Avalia a Lógica e Raciocínio. Utiliza perguntas reais dos exames nacionais do sistema de ensino português para testar a degradação da inferência sob compressão. O dataset pt_exams apresenta 6 subjects diferentes.
* **Teste E (`alba_mcq`):** Avalia o conhecimento linguístico endémico. Testa provérbios, expressões idiomáticas e usos semânticos exclusivos de Portugal.
* **Teste F (`cultura-viva-pt-mcq`):** Avalia a Memória Factual. Testa o conhecimento sobre história, geografia e personalidades de Portugal, identificando o nível de quantização em que o modelo começa a gerar alucinações de forma confiante.