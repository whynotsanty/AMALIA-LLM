# Guião de Apresentação: Avaliação da Quantização do AMALIA-9B

## 1. Introdução: o problema e a ideia
**Gonçalo**
Gostaria de apresentar o trabalho que desenvolvemos sobre a quantização do modelo AMALIA-9B. O nosso estudo incidiu sobre seis níveis de quantização: BF16, Q8_0, Q5_K_M, Q4_K_M, Q3_K_M e Q2_K.

A motivação para este projeto surgiu de uma questão prática: como fazer com que modelos grandes consigam correr em ambientes locais, com recursos limitados, sem comprometer aspetos essenciais, como o raciocínio, a fluidez linguística e a fidelidade cultural.

O nosso objetivo foi perceber até que ponto é possível comprimir o modelo sem o fazer entrar em degradação evidente. Em termos mais simples, procurámos encontrar a fronteira de Pareto entre eficiência computacional e qualidade de resposta. Pretendemos, assim, identificar o ponto em que o modelo fica mais leve e mais rápido, sem perder de forma crítica a sua capacidade de responder de maneira robusta e natural em português europeu.

Importa referir que achamos o estudo particularmente relevante dado que o projeto AMALIA é bastante recente. 

## 2. Objetivo do estudo e Metodologia
**Eduarda**
A pergunta central do nosso projeto foi a seguinte: até que ponto a quantização afeta o desempenho do AMALIA-9B em tarefas de linguagem, raciocínio e fidelidade cultural em português europeu?

Para responder a esta pergunta, estruturámos a avaliação em três dimensões distintas: uma dimensão de desempenho computacional, uma dimensão de métricas fechadas e uma dimensão de avaliação qualitativa.

### 2.1. Dimensão I: métricas de hardware e perda passiva
Na primeira dimensão, avaliámos o modelo em termos de eficiência computacional e degradação estrutural básica.

Utilizámos o dataset PorTEXTO e testámos quatro janelas de contexto diferentes: 512, 1024, 2048 e 4096 tokens. Medimos métricas como:
- pico de memória VRAM e RAM;
- throughput de prefill e decode;
- perplexidade (PPL);
- Avg Loss.

Estas métricas permitem compreender o impacto da quantização na capacidade do modelo de processar informação e na sua estabilidade preditiva. São importantes porque mostram o custo computacional da compressão e ajudam a identificar o ponto em que a eficiência começa a ser obtida à custa de uma perda significativa de qualidade.

### 2.2. Dimensão II: métricas fechadas
A segunda dimensão foi dividida em duas subdimensões.

#### Subdimensão A: geração e transformação de texto
Utilizámos datasets como:
- amalia-smoltalk2_everyday_conv_pt para conversação quotidiana;
- amalia-PTradutor para tradução;
- smol-rewrite-PT para reescrita de texto.

Para analisar estes resultados, recorremos a métricas como BLEU, ROUGE-L, Levenshtein Normalization e BERTScore F1.

Estas métricas permitem avaliar aspetos diferentes da geração textual:
- BLEU e ROUGE-L medem semelhança lexical com a referência;
- Levenshtein Normalization mede a distância entre sequências;
- BERTScore F1 avalia a semântica contextual, mesmo quando as palavras não coincidem exatamente.

#### Subdimensão B: questões de escolha múltipla
Na segunda subdimensão, avaliámos o modelo em tarefas de exame e conhecimento cultural com datasets como:
- pt_exams para questões de exame em diferentes domínios;
- cultura-viva-pt para questões diversas de cultura geral;
- alba_mcq para provérbios e expressões portuguesas.

Em vez de usar apenas accuracy, recorremos à métrica NPM, ou Normalized Preferred Metric. Esta métrica é mais robusta porque remove o efeito de acerto ao acaso, sobretudo em testes com várias opções. Assim, conseguimos comparar modelos de forma mais justa e mais realista.

### 2.3. Dimensão III: avaliação qualitativa
A terceira dimensão foi essencial porque muitos problemas surgem na qualidade da resposta e não apenas nos resultados numéricos.

Como não seria viável avaliar centenas de respostas manualmente, criámos um pipeline de LLM-as-a-Judge. Para isso, recorremos ao Gemini 3 Flash Preview via API, com temperatura 0 e Thinking Level em High, de modo a garantir um comportamento mais rigoroso e determinista.

O juiz foi instruído a avaliar as respostas com base em três critérios:
1. Precisão: se a resposta está correta, coerente e livre de alucinações;
2. Qualidade linguística: se a resposta está fluente, gramaticalmente correta e fiel ao português de Portugal;
3. Completude: se a resposta responde de forma integral ao que foi pedido.

Esta abordagem foi delineada e com base na leitura dos artigos ALBA e MMLU-ProX, pensada para dar especial atenção à variante europeia do português e para penalizar claramente desvios para o português do Brasil ou erros de cultura local.

## 3. Validação: a abordagem Human-in-the-Loop
**Gonçalo**
Uma questão natural é a seguinte: como sabemos que este juiz automático é confiável?

Para responder a isso, construímos um conjunto de validação, avaliando manualmente várias respostas e comparando-as com as notas atribuídas pelo juiz.

Os resultados foram muito positivos:
- Correlação de Pearson de 0.76;
- Erro Médio Absoluto (MAE) de 0.61 numa escala de 1 a 5.

Estes valores sugerem que o juiz possui um alinhamento forte com a avaliação humana, sobretudo em tarefas complexas e em contextos em que a qualidade linguística e cultural é crítica.

Claro que há também uma limitação importante. Detetámos um ligeiro viés de complexidade no juiz. Em respostas muito curtas e pragmáticas, como um simples “De nada!”, o avaliador humano podia dar uma nota elevada pela adequação social da interação, enquanto o juiz automático tendia a penalizar a resposta por a considerar demasiado curta.

Mesmo assim, esta limitação não invalida o método. Pelo contrário, demonstra que o juiz é particularmente útil para identificar problemas reais de precisão, morfologia, sintaxe e fidelidade cultural em tarefas mais exigentes.

## 4. Análise dos resultados: o “sweet spot” e o colapso
**Eduarda**
Os resultados mostram uma história muito clara. Existe uma zona de segurança entre BF16 e Q4_K_M. Nesta faixa, o modelo consegue reduzir bastante o tamanho e ganhar velocidade sem sofrer uma degradação severa da qualidade.

Por exemplo, ao passar de BF16 para Q4_K_M, o modelo reduz de cerca de 17 GB para 5.2 GB e o throughput de decode aumenta consideravelmente, enquanto a degradação em termos de perda permanece relativamente moderada. Isto sugere que os 4 bits constituem um bom compromisso entre eficiência e robustez.

No entanto, quando descemos para Q3_K_M e sobretudo para Q2_K, começam a surgir sinais claros de desestabilização. No nível Q3_K_M, o modelo já mostra problemas de consistência, como loops semânticos, erros de tradução e perda de controlo sobre a estrutura das respostas.

Na quantização extrema de 2 bits, o colapso é muito mais severo. Observámos três patologias principais:
1. Intrusão dialetal: o modelo começa a cair para o português do Brasil e a perder a fidelidade à norma europeia.
2. Alucinações factuais: aparecem erros geográficos, semânticos e lógicos, com respostas claramente inventadas.
3. Colapso morfológico e sintático: a resposta perde estrutura, fluidez e coerência, passando a incluir repetições, gibberish ou erros graves de construção.

## 5. Análise crítica global dos resultados
**Gonçalo**
Uma das observações mais interessantes do estudo é que a degradação não é uniforme em todos os testes. Alguns domínios são mais sensíveis do que outros.

Em particular, os resultados dos testes E e F mostram que tarefas ligadas a provérbios, expressões idiomáticas e cultura geral são muito exigentes. Mesmo o BF16, que é o melhor modelo da nossa comparação, não atinge um desempenho tão forte quanto esperávamos nestas áreas.

Isto sugere que a fidelidade cultural e o conhecimento específico da língua portuguesa não são garantidos apenas pelo uso de um modelo mais pesado. Mesmo modelos “melhores” podem ter fragilidades importantes em domínios culturais e linguísticos específicos.

Uma observação particularmente marcante é a seguinte: no Teste D, a quantização Q3_K_M, que é uma das mais fracas da nossa comparação, obteve um NPM_Score de 52.0. Esse valor é igual ou superior ao NPM_Score do BF16 nos Testes E e F. Em outras palavras, numa tarefa específica, uma versão mais comprimida pode parecer competitiva, enquanto noutras dimensões o mesmo modelo já mostra sinais claros de fragilidade.

Esta constatação reforça uma ideia central do projeto: a avaliação de LLMs não deve depender de uma única métrica. É preciso olhar para a qualidade linguística, para a cultura, para a robustez e para a consistência do comportamento do modelo, e não apenas para perdas matemáticas ou métricas de hardware.

### 5.1. Observações qualitativas e mais pessoais extraídas dos CSVs
Para além das pontuações, os ficheiros de resultados revelam uma mudança de comportamento muito interessante no modelo à medida que a quantização aumenta. O que mais nos chamou a atenção não foi apenas a queda de desempenho, mas a forma como o modelo começa a perder a sua identidade como assistente.

Até níveis moderados de compressão, o AMALIA-9B continua a parecer um modelo estável, útil e culturalmente sensível. As respostas mantêm um tom natural, respeitam a norma do português europeu e conseguem lidar com instruções complexas sem parecer forçadas. No entanto, à medida que descemos para Q3_K_M e sobretudo Q2_K, começa a surgir algo mais inquietante: o modelo deixa de parecer apenas menos preciso e passa a parecer menos controlado.

Há vários sinais disso. Em tarefas de tradução, começam a aparecer erros que não são simples deslizes linguísticos, mas falhas de semântica contextual. Exemplos como a tradução de "beep" para "alfaia" ou de "moral damage" para "danos mortais" mostram que o modelo não só perde qualidade, mas também perde segurança na interpretação do sentido. Em tarefas de reescrita, o problema é ainda mais visível: o modelo começa a repetir blocos, a perder a noção da estrutura da resposta e a entrar em ciclos de auto-referência. Isso não é um erro de vocabulário; é uma perda de controlo sobre o processo de geração.

Outro ponto importante é que a degradação não afeta apenas a precisão factual. Ela atinge também a dimensão cultural. O modelo começa a parecer menos “português” e mais genérico, como se o alinhamento local fosse uma camada frágil que a compressão consegue remover. Isto é particularmente relevante nos testes mais culturais, como os de provérbios, expressões idiomáticas e cultura geral. Nesses cenários, o modelo não só erra mais; parece menos seguro de si, menos natural e menos ancorado à realidade linguística e social que pretendia representar.

Em termos mais pessoais, o que mais nos marcou foi o contraste entre a sensação de confiança de uma resposta de alta qualidade e a sensação de estranheza de uma resposta degradada. Um modelo quantizado a níveis mais baixos pode continuar a parecer plausível à primeira vista, mas, quando se olha com mais atenção, percebemos que está a “fingir” compreensão. Esse efeito é talvez o mais preocupante, porque é precisamente o tipo de erro que pode passar despercebido num uso prático.

Estas observações tornam a discussão mais rica do que uma simples comparação de métricas. Elas mostram que a quantização não atua apenas sobre o desempenho matemático do modelo, mas também sobre a sua forma de pensar, de escrever e de existir como assistente linguístico.

## 6. Conclusão e proposta para a reunião
**Eduarda**
Em suma, o nosso trabalho mostra que a quantização pode ser uma estratégia muito útil para tornar modelos como o AMALIA-9B mais leves e mais rápidos, mas também mostra que esta vantagem tem limites. Os 4 bits parecem oferecer um bom compromisso, enquanto os níveis mais agressivos comprometem de forma visível a fidelidade linguística, o raciocínio e a identidade cultural do modelo.

Mais importante ainda, este estudo demonstra que a avaliação de LLMs não pode reduzir-se à perplexidade ou ao throughput. A qualidade de uma resposta depende também de fatores como precisão, fluidez, adequação cultural e consistência semântica.

Para esta reunião, gostaríamos de ouvir a sua opinião sobre três pontos principais:
1. O valor deste estudo como contributo para o projeto AMALIA e para a comunidade de investigação;
2. A pertinência de transformar este trabalho numa publicação, relatório técnico ou extensão do benchmark já existente;
3. Que direções adicionais poderíamos seguir para fortalecer a validação, por exemplo criar uma Leaderboard de Modelos Quantizados em pt-PT, ter mais testes humanos, mais datasets culturais ou novas métricas de avaliação.

Em conjunto, o nosso objetivo é mostrar que este projeto não é apenas um estudo de eficiência computacional, mas também uma contribuição importante para compreender como a compressão afeta a qualidade e a identidade linguística de modelos em português europeu.
