# Avaliação Automatizada da Quantização do Modelo AMALIA-9B em Português Europeu: Validação de um Pipeline *Human-in-the-Loop* com *LLM-as-a-Judge*

## Resumo 
A implantação de Grandes Modelos de Linguagem (LLMs) em ambientes com recursos computacionais limitados (*edge computing*) exige o recurso a técnicas de compressão, nomeadamente a quantização dos pesos neuronais. Contudo, a quantização agressiva tende a induzir uma degradação severa nas capacidades de raciocínio lógico e na fidelidade linguística, um problema particularmente premente em variantes com menor representação analítica, como o Português Europeu (pt-PT). O presente artigo documenta o *benchmarking* do modelo AMALIA-9B ao longo de seis resoluções de quantização, validando um sistema de avaliação automática (*LLM-as-a-Judge*) calibrado através de um rigoroso protocolo *Human-in-the-Loop* (HITL). A análise estatística comprova um alinhamento forte (Correlação de Pearson = 0.7590; Kappa = 0.6102) entre o julgamento automático e a anotação do especialista humano, atestando a fiabilidade metodológica para a avaliação em larga escala de tarefas de geração, tradução e reescrita de texto.



## 1. Introdução

A adoção generalizada de Grandes Modelos de Linguagem (LLMs) revolucionou o Processamento de Linguagem Natural, contudo, a sua colossal escala de parâmetros (frequentemente na ordem das dezenas de milhares de milhões) impõe constrangimentos proibitivos de armazenamento e latência de inferência. Para viabilizar a execução de modelos como o AMALIA-9B em ambientes locais ou servidores de capacidade intermédia, a indústria tem adotado técnicas de compressão por quantização pós-treino (PTQ). Este processo converte os pesos de elevada precisão (como o ponto flutuante de 32 ou 16 bits - FP32/BF16) em formatos discretos de menor resolução matemática (ex: INT8, formatos "K-quant" como Q5_K_M, Q4_K_M ou Q2_K). Num modelo com biliões de parâmetros, esta compressão permite uma redução drástica na pegada de memória, frequentemente diminuindo os requisitos de ~36 GB para menos de 9 GB, salvaguardando a latência da inferência a troco de uma potencial erosão nas capacidades generativas.

No contexto do Português Europeu, o impacto desta erosão carece de referenciais de teste rigorosos. Uma vasta porção dos *benchmarks* atuais assenta em traduções automatizadas a partir do Inglês ou padece de um forte viés para a norma do Português do Brasil (pt-BR). O ecossistema concebido para o projeto AMALIA-9B endereça esta lacuna através de uma bateria abrangente: os Testes de Geração Escrita (A a C, cobrindo conversação, tradução e reescrita) e os Testes de Escolha Múltipla (D a F). Cada ficheiro avalia um espectro de 6 níveis de quantização aplicados a 49 interações.

O problema central de investigação reside no gargalo da validação. Avaliar manualmente milhares de respostas requer um esforço hercúleo. A delegação desta tarefa num avaliador automatizado (*LLM-as-a-Judge*, à semelhança do testado no *benchmark* recente ALBA para pt-PT) levanta o desafio da sua própria fiabilidade. Torna-se imperativo validar se o Juiz automático é estatisticamente robusto e se está solidamente alinhado com o escrutínio de um especialista humano nativo em pt-PT, de forma a validar integralmente o *pipeline* de avaliação das quantizações do modelo.



## 2. Metodologia e Protocolo de Validação (HITL)

Para aferir a eficácia do modelo AMALIA-9B e a degradação introduzida por cada quantização, arquitetou-se um avaliador generativo (um LLM avançado em modo *High Thinking* e Temperatura zero) encarregado de classificar as respostas.

### 2.1. Arquitetura do Juiz
O *prompt* do Juiz LLM foi estruturado sob a matriz de uma escala de Likert de 1 a 5, escrutinando a resposta gerada com base na Solução de Referência e no Problema Original. O sistema foi calibrado para observar rigorosamente três eixos:
1. **Precisão:** Deteção de coesão lógica, adequação dos factos e ausência de alucinações empíricas.
2. **Qualidade Linguística:** Adesão estrita à norma europeia (pt-PT). O juiz foi explicitamente instruído a penalizar a presença de gerúndios desnecessários, traduções literais em inglês e sintaxe ou vocabulário intrinsecamente brasileiros (ex: penalizar "a gente se move" ou "café da manhã").
3. **Completude:** O grau com que o modelo cumpriu todas as diretrizes da instrução original.

### 2.2. Protocolo *Human-in-the-Loop* (HITL)
Por forma a estabelecer uma base de verdade (*ground truth*), implementou-se um protocolo de validação por humanos, materializado no *dataset* `HITL.csv`. 
Aplicou-se uma Amostragem Estratificada (*Stratified Sampling*), garantindo a cobertura dos testes de escrita (A, B e C) através de várias quantizações (como BF16, Q8_0, Q5_K_M e Q2_K) para obter diversidade nas classes de erro. Adicionalmente, estabeleceu-se um protocolo de Anotação Duplo-Cego (*Double-Blind Annotation*) quando possível para mitigar o viés de confirmação, e procedeu-se à validação exaustiva de todas as respostas inerentes à quantização destrutiva Q2_K no Teste A. O perito humano assinalou uma nota final e documentou qualitativamente as suas avaliações numa grelha de observações (*obs*).

### 2.3. Validação Estatística do Acordo Inter-Anotador
O rigor científico do alinhamento entre o humano e o juiz automático foi medido por um conjunto de métricas não apenas de escala linear, mas de natureza ordinal:
* **Erro Médio Absoluto (MAE):** Avalia o desvio médio na escala de 1 a 5 pontos.
* **Correlação de Pearson (\\(r\\)):** Mede a associação linear forte entre as séries de classificações.
* **Correlação de Spearman (\\(\rho\\)):** Mede a dependência monotónica, fundamental por se tratar de notas ordinais que não possuem distâncias perfeitamente proporcionais.
* **Linear Weighted Cohen's Kappa (\\(k\\)):** Considerado o padrão-ouro na linguística computacional para medir a concordância entre os avaliadores enquanto elimina a probabilidade de concordância fruto do acaso.



## 3. Resultados e Benchmarking do Modelo

O cruzamento dos julgamentos do especialista (extraídos do log HITL) com as pontuações independentes do *LLM-as-a-Judge* resultou no referencial empírico central desta investigação.

### 3.1. Métricas da Validação Automática
Numa amostragem validada (N = 18 amostras cruzadas) do "Relatório de Validação HITL", os dados extraídos comprovaram um grau de fiabilidade e precisão notáveis:

| Métrica de Alinhamento | Valor Obtido | Grau de Confiança / P-value | Significado Estatístico |
| :--- | :---: | :---: | :--- |
| **Erro Médio Absoluto (MAE)** | 0.6111 | N/A | Excelente precisão num espetro de 1 a 5. |
| **Correlação de Pearson (r)** | 0.7590 | 2.60e-04 (Muito Forte) | Relação linear indiscutível (sem margem para o acaso). |
| **Correlação de Spearman (ρ)** | 0.7343 | 5.21e-04 (Muito Forte) | Ordens de magnitude hierarquizadas quase em perfeito acordo. |
| **Linear Weighted Cohen's Kappa (k)** | 0.6102 | Forte / Substancial | Excelente concordância inter-avaliadores mitigando o acaso. |

### 3.2. Análise do Trade-off de Quantização (Eficiência vs. Acurácia)
O *benchmarking* quantitativo aplicado ao AMALIA-9B confirma os princípios elementares da compressão. Os testes de avaliação automática evidenciaram que nos regimes próximos da precisão de base (como a resolução Q8_0 e Q5_K_M), a métrica semântica sobrevive sem erosão documentada. Observa-se que níveis de quantização como o formato **Q4_K_M** atingem o ponto ideal da fronteira de Pareto: compressão na ordem dos 4-bits proporciona poupança crítica em tempo de inferência e capacidade (VRAM) reduzindo os tamanhos para cerca de ~5 GB, ao passo que as notas se mantêm predominantemente na ordem dos 4 a 5 pontos. Pelo contrário, à medida que se desce até à redução limite (Q2_K a ~2.7 bits), assiste-se ao colapso total da rede neuronal na coerência sintática, na exatidão e na retenção do registo local.



## 4. Discussão e Análise Crítica de Erros (*Error Analysis*)

A robustez da matriz estatística não iliba o sistema de fricções avaliativas. A dissecção aprofundada do ficheiro empírico `HITL.csv`, com especial atenção à coluna qualitativa `obs`, revelou anomalias altamente ilustrativas sobre a perceção ontológica do juiz LLM versus o especialista humano.

### 4.1. O "Viés de Complexidade" nas Interações Sociais
Verifica-se sistematicamente um "viés de complexidade" (ou foco excessivo no erro estrutural) por parte do Juiz Automático. O fenómeno manifestou-se repetidamente em interações fáceis de cariz social e cortesias. Por exemplo, em entradas onde o modelo base AMALIA respondeu unicamente "De nada!" a perguntas que terminavam em construtos como "Muito obrigado pelas dicas!" (visível nos índices A_Q2_8, A_Q2_14 ou no A_BF_33), o especialista humano atribuiu notas máximas (5) com a observação *"foi muito conciso"*. Para o anotador nativo, a adequação social, a concisão e a fluidez pragmática representam uma resposta irrepreensível em conversação. 

Em contrapartida, o LLM a atuar como juiz detém um viés implícito por formulações longas, analíticas e textualmente expansivas. Em consequência, frequentemente categorizou interações simples de agradecimento como falhas em desenvolver um "raciocínio gerado", atribuindo-lhes notas severas na ordem do 1 ou 2. É este subconjunto desbalanceado e restrito (em que perguntas terminavam com agradecimentos induzindo o "de nada" sistémico do gerador) que motivou divergências matemáticas agudas que se manifestaram inflando ligeiramente a taxa de erro para o **MAE de 0.6111**.

### 4.2. Colapso Cultural e Alucinações Graves no Modelo Q2_K
Se a métrica divergiu nas saudações, o `HITL.csv` demonstra que, nos testes críticos e com densidade de conhecimento, as notações em pt-PT convergiram perfeitamente. O nível de compressão extrema Q2_K evidenciou falências morfológicas e geográficas destrutivas que tanto humano como juiz sancionaram ativamente:
* **Intrusão do Português do Brasil:** No índice A_Q2_40 (receita de *strata*), o humano aponta o erro: *"paes de sal é pt-br"* (o termo local é carcaça ou papo seco). No índice A_Q2_19 o humano castiga o termo "se move" por desvio da sintaxe europeia, juntamente com o barbarismo *"empurhar"*.
* **Alucinações Factuais e Lógicas:** A degradação destruiu o conhecimento espacial do modelo, culminando no erro flagrante do índice A_Q2_18, com a observação *"sonara não existe | confundiu com sanara nos EUA. Anulou quase td a resposta"*. De igual modo, no índice A_Q2_6 documentam-se falhas basilares na escala do tempo da Terra (*"hadeano não é o mais curto | paleo não é o mais longo"*), ou respostas totalmente bizarras de interações ecológicas, como *"o tubarão branco [...] pode ser ameaçado por baleias [...] que afundam navios"* (A_Q2_11).

### 4.3. Opinião Científica e Robustez do Avaliador
Esta análise permite inferir um juízo firme e seguro. O facto de o juiz LLM atritar nas avaliações puramente curtas não obscurece de forma alguma o rigor das suas notações complexas. O Índice Linear Weighted Cohen's Kappa (\\(k\\)) calculado de **0.6102** atua como fiel de balança. Este valor é considerado academicamente como um "acordo substancial/forte", sendo capaz de filtrar flutuações e viés ocasional. Tal facto credibiliza indiscutivelmente a validade estatística e sintática deste *pipeline* avaliativo no mapeamento das subtilezas exigidas na avaliação dos Testes de Tradução (Teste B) e Testes de Reescrita de Tom (Teste C).


## 5. Conclusão

O presente *benchmarking* contribui de forma decisiva para desbravar a barreira existente na avaliação dos Modelos de Linguagem para o Português de Portugal. Confirma-se empiricamente que o modelo AMALIA-9B, quando submetido a níveis de quantização equilibrada de média densidade (tais como o Q4_K_M), apresenta um *trade-off* excecionalmente positivo, salvaguardando quer a sua estrutura lógica quer as nuances sintáticas cruciais do panorama lusitano em Portugal continental sem necessitar do peso estático de 16-bits. 

No que tange ao esforço de validação sistemática, a integração do escrutínio especialista *Human-in-the-Loop* consolidou categoricamente que o uso ponderado de um *LLM-as-a-Judge*, sujeito aos devidos constrangimentos no *prompt*, emula com fiabilidade de coeficiente forte (\\(k = 0.61\\)) a capacidade humana de detetar idiomatismos intrusos (pt-BR) ou lapsos conceptuais catastróficos perante dados com degradação (como em Q2_K). Com as limitações de ruído social de curtas mensagens de saudação devidamente reconhecidas e isoladas, conclui-se que o presente protocolo avaliativo é metodologicamente seguro, célere e rigoroso para aplicações de modelagem à escala na variante do Português Europeu.