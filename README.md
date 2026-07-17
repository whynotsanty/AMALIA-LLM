# Metodologia e Datasets: Avaliação do AMALIA-9B Quantizado

Este repositório reúne a infraestrutura de testes, os conjuntos de dados e o pipeline de avaliação desenvolvidos para mapear o impacto da **Quantização Pós-Treino (PTQ)** no modelo fundacional português **AMALIA-9B** (Llama-3.1-8B-Instruct + DPO). 

A nossa avaliação adota um paradigma bidimensional, dividindo-se entre a análise de infraestrutura técnica de sistemas (Dimensão I) e as capacidades cognitivo-linguísticas práticas (Dimensão II).

---

## 🔧 Dimensão I: Engenharia e Hardware (Análise Técnica)

Esta dimensão foca-se no impacto físico, infraestrutural e matemático da compressão dos pesos do modelo (desde a precisão original `BF16` de 16-bits até ao formato de compressão extrema de 2-bits `Q2_K`).

### 📊 Métricas Analisadas
* **Perplexidade (PPL):** Mede a degradação matemática da capacidade do modelo prever a próxima palavra, avaliada de forma contínua.
* **Consumo de Recursos (VRAM/RAM):** Registo do pico de alocação de memória necessário para carregar o modelo durante a inferência.
* **Velocidade de Inferência (Throughput):** Medição do rendimento de geração em *tokens por segundo* (t/s) distinguindo as fases de **Prefill** (processamento do prompt com $pp=512$) e **Decode** (geração cumulativa com $tg=128$).
* **Redução de Tamanho (%):** A percentagem de compressão física obtida no tamanho do ficheiro do modelo em relação ao baseline `BF16` (17.05 GB).
* **AvgLoss (%):** A taxa de perda média acumulada nas tarefas de processamento de linguagem natural face ao baseline de precisão nativa.

### 💾 Dataset Utilizado
* **`PorTEXTO`**: Um *corpus* de referência contendo textos nativos do português de Portugal (pt-PT). É utilizado de forma passiva (leitura de blocos de contexto contínuo de 512, 1024, 2048 e 4096 tokens) para calcular a perplexidade de forma pura, isolando os padrões sintáticos e lexicais europeus de qualquer ruído de tarefas externas.

---

## 🧠 Dimensão II: Capacidades Linguísticas e Culturais (Análise Prática)

Esta dimensão mapeia o ponto de rutura cognitivo do AMALIA-9B, avaliando em que nível de bits o modelo perde a capacidade de seguir instruções complexas, raciocinar logicamente e preservar a autenticidade linguística portuguesa.

### 📝 Subdimensão II - A (Competência Linguística e Semântica Gerativa)
Esta subdimensão foca-se em tarefas de geração aberta de texto, onde as respostas do modelo são avaliadas de forma qualitativa por um avaliador automático:
* **Teste A (`amalia-smoltalk2_everyday_conv_pt`):** Avalia a fluidez e a naturalidade numa interação conversacional contínua, simulando a coesão exigida a um assistente virtual no dia a dia.
* **Teste B (`amalia-PTradutor`):** Avalia a tradução de inglês para português (EN $\rightarrow$ PT), verificando se a quantização destrói a resiliência do modelo em manter o pt-PT, cedendo ao viés estatístico de gerar gerúndios ou vocabulário em pt-BR.
* **Teste C (`smol-rewrite-PT`):** Avalia a reescrita e adaptação de registo, medindo a capacidade do modelo para reescrever um texto mantendo o seu núcleo informativo, mas alterando o tom para uma variante formal, amigável ou concisa.

### 🎯 Subdimensão II - B (Integridade Cognitiva, Conhecimento Factual e Cultura)
Esta subdimensão foca-se em tarefas de escolha múltipla (MCQs) determinísticas:
* **Teste D (`pt_exams`):** Avalia a lógica e o raciocínio formal utilizando perguntas reais dos Exames Nacionais oficiais do sistema de ensino de Portugal (cobrindo 6 disciplinas diferentes). Os resultados são pontuados através da métrica **NPM (Normalized Preferred Metric)** para expurgar o efeito de acerto ao acaso.
* **Teste E (`alba_mcq`):** Avalia o conhecimento linguístico e semântico profundo, testando o domínio de provérbios, expressões idiomáticas e usos semânticos exclusivos de Portugal.
* **Teste F (`cultura-viva-pt-mcq`):** Avalia a memória factual e cultural, testando o conhecimento sobre história, geografia, literatura e personalidades portuguesas, identificando o nível de compressão a partir do qual o modelo começa a alucinar.

---

## ⚖️ Metodologia LLM-as-a-Judge

Para avaliar as tarefas de geração aberta da **Subdimensão II-A** (onde métricas como BLEU ou ROUGE-L falham ao não capturar nuances de adequação dialetal ou coesão estilística), foi estabelecido um pipeline de avaliação automática por **LLM-as-a-Judge** seguindo as melhores práticas do benchmark científico **ALBA**.

### 1. Evitar o *Confounding Variable* (Viés do Juiz Quantizado)
Como este estudo avalia os efeitos da quantização pós-treino (PTQ), **o modelo juiz não pode sofrer de qualquer compressão de pesos**. Utilizar um juiz quantizado (como formatos AWQ ou GGUF de 4 bits) introduziria ruídos de dequantização e falhas de atenção no próprio processo de avaliação. Por esse motivo, o pipeline corre via **API Cloud em precisão total de ponto flutuante (FP16/FP32)**, garantindo que o avaliador opera sem limitações matemáticas.

### 2. Configuração do Ambiente de Julgamento
* **Modelo Utilizado:** `Gemini 3 Flash Preview` (disponibilizado via Google AI Studio API).
* **Temperatura ($\tau$):** `0.0` (Obrigatório para remover comportamento estocástico, garantindo que as avaliações são determinísticas e reprodutíveis cientificamente).
* **Thinking Budget (Raciocínio Profundo):** Configurado em `High` (mínimo de `1024 tokens` de espaço de raciocínio). Isto obriga o juiz a gerar primeiro uma cadeia de raciocínio (*Chain-of-Thought*) detalhada onde analisa criticamente as nuances da resposta antes de emitir a nota final.

### 3. Estratégia de Calibração: 3-Shot "Length-Diverse"
Seguindo o padrão validado na literatura do ALBA (que reduz o Erro Médio Absoluto para apenas **$MAE=0.475$** em comparação com linguistas humanos nativos), as **System Instructions** do juiz incluem três exemplos pouca-aprendizagem (*few-shot*) com tamanhos de resposta intencionalmente discrepantes para calibrar os extremos da escala Likert de 1 a 5:
* **Exemplo de Nota 1 (Resposta Curta):** Resposta em que o modelo colapsa linguisticamente para o português do Brasil (pt-BR), introduzindo termos como *"cara"*, *"rolê"* ou *"misto quente"* (o equivalente europeu é *"tosta mista"*).
* **Exemplo de Nota 3 (Resposta Média):** Resposta gramaticalmente correta em pt-PT, mas que falha por completo ao interpretar de forma puramente literal uma expressão idiomática cultural portuguesa (ex: interpretar "dar graxa" como polir sapatos real, em vez de bajular/adular).
* **Exemplo de Nota 5 (Resposta Longa):** Resposta impecável, fluida, que cumpre integralmente a instrução e exibe uma rica variedade sintática e vocabulário elegante da norma padrão de Portugal.

---

### 📝 Template de Prompt Utilizado (System Instructions)

O prompt de sistema abaixo foi carregado na infraestrutura do Google AI Studio para automatizar as avaliações:

```markdown
Atuas como um avaliador linguístico especialista em Português de Portugal (pt-PT). A tua tarefa é avaliar a qualidade da resposta gerada por um assistente de Inteligência Artificial com base numa pergunta/instrução e, opcionalmente, num texto de referência.

Avalia a resposta numa escala Likert de 1 (Muito Má) a 5 (Excelente) com base em três eixos rigorosos:
1. Precisão (Se a resposta está factualmente correta, logicamente coesa e sem alucinações).
2. Qualidade Linguística (Fluidez, gramática correta e fidelidade estrita à variedade do Português de Portugal, penalizando severamente gerúndios desnecessários, sintaxe ou vocabulário exclusivo do português do Brasil, como "a gente", "cara", "café da manhã", etc.).
3. Completude (Se cumpre integralmente o que foi pedido na instrução).

[Instruções de Formato]
Deves gerar primeiro uma breve justificação passo a passo (Chain-of-Thought) detalhando os pontos fortes e as falhas de precisão, variedade linguística e completude da resposta. 
Termina sempre a tua avaliação com uma linha final no formato estrito: "Nota Final: [X]" (onde X é um número inteiro de 1 a 5).

[Exemplos Few-Shot de Calibração (Length-Diverse)]

### EXEMPLO 1 (Nota: 1 - Resposta Curta com Viés de pt-BR)
- Pergunta: "Olá! Como estás hoje? Tens alguma sugestão de passeio por Lisboa?"
- Resposta Gerada pelo Modelo: "Olá, cara! Eu estou bem. A gente pode dar um rolê pelo bondinho ou comer um misto quente à tarde na calçada."
- Texto de Referência: "Olá! Estou ótimo, obrigado. Sugiro uma caminhada pelo bairro de Alfama, uma visita ao Castelo de São Jorge e, no final da tarde, degustar um pastel de nata na zona de Belém."
- Justificação da Avaliação: A resposta cumpre a instrução de forma muito superficial, mas apresenta falhas graves na dimensão de qualidade e variedade linguística. Introduz vocabulário e expressões informais exclusivas do português do Brasil (pt-BR), tais como "cara", "a gente", "dar um rolê" e "misto quente" (o termo correto em pt-PT é "tosta mista"). Adicionalmente, refere-se ao elétrico de Lisboa como "bondinho", o que é factual e culturalmente incorreto para o contexto de Portugal.
Nota Final: 1

### EXEMPLO 2 (Nota: 3 - Resposta Média com Interpretação Literal)
- Pergunta: "O que significa a expressão idiomática portuguesa 'dar graxa'?"
- Resposta Gerada pelo Modelo: "Significa limpar e polir os sapatos de alguém utilizando graxa preta ou castanha para que fiquem brilhantes."
- Texto de Referência: "A expressão 'dar graxa' é uma expressão idiomática que significa adular, lisonjear ou bajular alguém com o objetivo de obter algum favor ou benefício pessoal."
- Justificação da Avaliação: A resposta está gramaticalmente correta em português de Portugal (pt-PT) e é fluida. No entanto, falha por completo na dimensão semântica e cultural. O modelo interpretou a expressão de forma puramente literal (polir sapatos com graxa real), falhando em identificar o verdadeiro significado figurativo e idiomático da expressão ("bajular/adular"), que é de conhecimento comum em Portugal.
Nota Final: 3

### EXEMPLO 3 (Nota: 5 - Resposta Longa, Excelente em pt-PT)
- Pergunta: "Olá! Como estás hoje? Tens alguma sugestão de passeio por Lisboa?"
- Resposta Gerada pelo Modelo: "Olá! Estou excelente, muito obrigado por perguntar. Para um dia agradável em Lisboa, sugiro começar com uma caminhada pelas ruelas históricas de Alfama, seguida de uma visita ao imponente Castelo de São Jorge para desfrutar da vista sobre a cidade. No final da tarde, recomendo vivamente ir até Belém para saborear um pastel de nata quentinho, mesmo ao lado do Mosteiro dos Jerónimos."
- Texto de Referência: "Olá! Estou ótimo, obrigado. Sugiro uma caminhada pelo bairro de Alfama, uma visita ao Castelo de São Jorge e, no final da tarde, degustar um pastel de nata na zona de Belém."
- Justificação da Avaliação: A resposta é excecional. Cumpre perfeitamente a instrução, expandindo-a de forma natural e precisa. A linguagem utilizada é 100% autêntica em português de Portugal (pt-PT), com construções sintáticas elegantes ("recomendo vivamente", "ruelas históricas", "saborear") e total ausência de qualquer influência ou termos da variante brasileira.
Nota Final: 5

[Caso para Avaliar]
Pergunta: {instruction}
Resposta Gerada pelo Modelo: {model_output}
Texto de Referência (Se aplicável): {reference_text}

Justificação da Avaliação:
```

---

## 📈 Sumário do Comportamento de Degradação (Resultados)

A avaliação conjunta das duas dimensões de teste revelou um perfil de degradação muito consistente entre a integridade matemática dos pesos e o comportamento qualitativo:

*   **BF16 / Q8_0 / Q5_K_M (Nota do Juiz: 5 - Excelente):** Perfeita preservação do português europeu (pt-PT). Utilização correta de vocabulário nacional (*"pequeno-almoço"*, *"comboio"*, *"telemóvel"*) e domínio sintático impecável (construção *"estou a [verbo]"*).
*   **Q4_K_M (Nota do Juiz: 5/4 - Muito Bom):** O modelo preserva de forma notável a integridade sintática e regional, sendo o **sweet-spot absoluto** (redução de 69,50% em tamanho e velocidade acrescida em relação ao BF16). Registam-se apenas pequenos desvios terminológicos residuais (como traduzir *"anchilosed"* mantendo o radical inglês em vez do correto português *"anquilosado"*).
*   **Q3_K_M (Nota do Juiz: 4/3 - Médio/Razoável):** Ocorre uma simplificação evidente na estrutura sintática. Surgem as primeiras falhas de gestão de output decorrentes da compressão (loops repetitivos que geram múltiplas versões da reescrita dentro da mesma resposta e confusão de contextos simples como traduzir *"beep"* como *"alfaia"*).
*   **Q2_K (Nota do Juiz: 2/1 - Insuficiente/Colapso):** Colapso linguístico e comportamental severo.
    *   **Fratura Dialetal:** O modelo perde as ligações refinadas do pt-PT e colapsa (*defaults*) de volta para a norma dominante no pré-treino (pt-BR), gerando *"pães de sal"* em vez de *"carcaças"*.
    *   **Loops Infinitos:** Entrada em ciclos repetitivos de caracteres sem sentido (*"CAMPÂÂÂÂNÂÂ"*).
    *   **Erros Semânticos Graves:** Tradução errada de conceitos vitais, como converter o termo jurídico *"moral damage"* (danos morais) para *"danos mortais"*.

