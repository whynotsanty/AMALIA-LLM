# Guião de Apresentação: Avaliação da Quantização do AMALIA-9B

## 1. Introdução: O Problema e a Ideia
**Pessoa 1:** 
"Queríamos apresentar-lhe os resultados do nosso projeto de avaliação de LLMs em Português de Portugal. 
A nossa ideia surgiu de um problema duplo na literatura atual: primeiro, a maioria dos *benchmarks* avalia o inglês ou o Português do Brasil, ignorando as nuances do nosso idioma nativo. Segundo, para correr modelos localmente, temos de usar técnicas de compressão (*quantização*), mas ninguém sabe ao certo como é que essa "perda de memória" afeta o raciocínio e a fidelidade cultural de um modelo treinado em pt-PT."

**Pessoa 2:**
"Exato. Para resolver isto, pegámos no modelo **AMALIA-9B** e aplicámos seis níveis de quantização: desde a versão base (BF16), descendo para formatos como o Q8_0, Q5_K_M e Q4_K_M, até aos limites extremos de compressão: o Q3_K_M e o Q2_K. 
O nosso objetivo era claro: encontrar a **Fronteira de Pareto**, ou seja, descobrir até onde podemos comprimir o modelo para o tornar rápido e leve, antes de ele sofrer um colapso linguístico e cognitivo."

## 2. A Metodologia: As Três Dimensões de Teste
**Pessoa 1:**
"Para que a nossa avaliação fosse blindada e rigorosa, dividimos os testes em 3 dimensões diferentes:
*   **Dimensão 1 (Métricas de Hardware e Perda Passiva):** Avaliámos a velocidade de inferência (*Throughput* de *prefill* e *decode*) e calculámos a Perplexidade (PPL) pura usando o dataset `PorTEXTO`, isento de instruções complexas.
*   **Dimensão 2 (Métricas Fechadas):** Avaliámos os Testes D, E e F (Exames de Escolha Múltipla) utilizando a métrica corretiva **NPM (Normalized Preferred Metric)**, que penaliza o acerto ao acaso, e avaliámos métricas de N-Gramas (BERTScore, ROUGE) nos testes generativos."

**Pessoa 2:**
"E finalmente chegamos ao nosso maior desafio: a **Dimensão 3 (Avaliação Qualitativa)**. Como não podíamos avaliar centenas de respostas à mão, criámos um *Pipeline* de **LLM-as-a-Judge**. 
Utilizámos o *Gemini 3 Flash Preview* via API, com a Temperatura a zero e o *Thinking Level* no máximo ('High') para garantir determinismo. Avaliámos os modelos em três tarefas críticas: Teste A (Conversação), Teste B (Tradução) e Teste C (Reescrita)."

## 3. Validação: A Abordagem Human-in-the-Loop (HITL)
**Pessoa 1:** *(Aconselho a mostrar o gráfico `judge_human_correlation.png` aqui)*
"Claro que a primeira pergunta seria: 'Como sabemos que o juiz LLM é de confiança?'
Para provar a robustez do nosso juiz, criámos um ficheiro de validação `HITL.csv` onde avaliámos manualmente várias respostas. Os resultados foram excelentes:
*   Conseguimos uma **Correlação de Pearson de 0.76**, o que indica um alinhamento forte com a avaliação humana.
*   O nosso Erro Médio Absoluto (MAE) foi de apenas **0.61** numa escala de 1 a 5.

**Pessoa 2:**
"O único 'problema' que detetámos nesta validação foi um ligeiro **viés de complexidade** por parte do juiz. Por exemplo, quando o utilizador agradecia e o AMALIA respondia apenas com um natural 'De nada!', nós (humanos) dávamos nota 5 pela concisão social. Mas o juiz LLM penalizava o modelo com notas 1 ou 2, por achar que a resposta era demasiado curta e não tinha 'raciocínio gerado'. Tendo isto em conta, validámos que o juiz é extremamente rigoroso para tarefas difíceis."

## 4. Análise dos Resultados: O "Sweet Spot" e o Colapso
**Pessoa 1:**
"Passando aos resultados da quantização, os dados revelam uma história muito interessante:
A 'Zona de Segurança' vai desde o BF16 até ao formato **Q4_K_M**. Com 4-bits, o tamanho do modelo desce de 17 GB para apenas 5.2 GB, e a velocidade de geração salta de 45 para quase 107 *tokens* por segundo. Linguisticamente, o modelo mantém-se perfeito nestes níveis: respeita o pt-PT, usa vocabulário como 'pequeno-almoço' e 'telemóvel', e até usa corretamente a norma europeia na colocação pronominal."

**Pessoa 2:**
"Mas a magia do *benchmark* acontece quando descemos abaixo dos 4 bits. 
No nível **Q3_K_M** (3-bits), o modelo atinge um ponto de inflexão. Ele começa a esquecer-se de parónimos na tradução: por exemplo, traduziu *dispute* por 'diferimento' (adiamento) em vez de 'diferendo', e alucinou ao traduzir 'beep' por 'alfaia'. Nos testes de reescrita, o modelo começou a entrar em *loops* semânticos, repetindo exaustivamente os cabeçalhos de sistema."

**Pessoa 1:**
"O **colapso catastrófico** e a **crise de identidade** ocorrem na quantização extrema de 2-bits (**Q2_K**). O modelo esquece o alinhamento cultural imposto pelo *fine-tuning* local.
Descobrimos três patologias principais:
1. **Intrusão Dialetal:** Cai para o pt-BR (padrão da internet), recomendando receitas com 'pães de sal' em vez de carcaças, e falhando completamente na sintaxe.
2. **Alucinações Factuais Graves:** Movimentou o Deserto de 'Sonara' para a Austrália, e inventou uma analogia onde tubarões brancos são ameaçados por *baleias que afundam navios*. E numa tradução do Teste B, cometeu um erro que poderia ser fatal, traduzindo *moral damage* (danos morais) por 'danos mortais'.
3. **Colapso Morfológico:** Em tarefas de reescrita, a sintaxe partiu-se completamente originando *gibberish*, produzindo lixo textual infinito como 'CAMPÂÂÂÂNÂÂ'."

## 5. Conclusão da Reunião
**Pessoa 2:**
"Em suma, professor, o nosso projeto conclui de forma empírica que os 4 bits (Q4_K_M) oferecem o compromisso perfeito para correr o AMALIA-9B em máquinas locais em Portugal. Mais importante ainda, provámos que avaliar a degradação de LLMs não se pode limitar à perda de perplexidade (matemática): a compressão agressiva ataca diretamente o conhecimento cultural e a matriz de alinhamento sintático da variante portuguesa. A nossa arquitetura de LLM-Juiz provou ser uma ferramenta escalável para resolver a lacuna dos testes em pt-PT."

