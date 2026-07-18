# Avaliação Multidimensional da Quantização do Modelo AMALIA-9B para Português de Portugal

## 1. Resumo

Este artigo apresenta uma investigação técnica sobre o impacto da compressão por quantização no modelo AMALIA-9B, otimizado para a variante linguística do Português de Portugal (PT-PT). Através de uma metodologia rigorosa que integra LLM-as-a-Judge e Human-in-the-Loop (HiTL), avaliou-se a preservação da integridade semântica e sintática face à redução de precisão numérica. Os resultados quantitativos revelam um Erro Médio Absoluto (Mean Absolute Error - MAE) de 0,6111. Este valor, embora demonstre a robustez da arquitetura original, exige uma análise qualitativa profunda para garantir que nuances críticas da norma europeia do português não sejam obscurecidas por métricas de desempenho global.

## 2. Introdução

Contextualização A trajetória dos Modelos de Linguagem de Larga Escala (LLMs) revela uma expansão sem precedentes, escalando de 1 bilião de parâmetros em 2018 para arquiteturas que ultrapassam os 100 biliões em 2024. Segundo documentado na framework COMPRESS AND COMPARE, esta escalabilidade acarreta custos computacionais e financeiros que tornam a implementação em infraestruturas locais ou dispositivos de utilizador final um desafio de engenharia significativo.

O Desafio da Compressão A quantização surge como uma técnica imperativa para viabilizar a execução on-device do AMALIA-9B, visando reduzir a latência e a ocupação de recursos sem degradar a precisão linguística. Para o Português de Portugal, o desafio é particularmente acutilante: o processo de compressão não deve neutralizar especificidades como a colocação pronominal (ênclise e mesóclise) ou o léxico lusitano, sob risco de convergência para variantes com maior disponibilidade de recursos, como o Português do Brasil.

Objetivo do Estudo O presente estudo avalia o equilíbrio entre a eficiência técnica e a preservação da qualidade semântica, procurando determinar se o modelo comprimido mantém a identidade linguística exigida para aplicações críticas em Portugal.

## 3. Fundamentação Teórica: Técnicas de Quantização e Benchmarking

Mecânicas de Quantização Com base na framework PQ Bench, a quantização é definida pela conversão de pesos e ativações de formatos de alta precisão (tipicamente FP32) para tipos de menor precisão, como INT8 ou FP16. Este mapeamento permite reduzir a complexidade aritmética e otimizar o processamento em hardware especializado.

Vantagens Competitivas Dados do PQ Bench sustentam que a quantização geralmente supera o pruning (poda de parâmetros) na preservação da acurácia e na redução da pegada de memória (memory footprint). Enquanto o pruning não estruturado pode gerar padrões de esparsidade ineficientes, a quantização mantém a topologia do modelo, facilitando ganhos previsíveis em hardware compatível.

Desafios Técnicos (C1 a C4) Identificamos quatro desafios fundamentais no design de modelos comprimidos:

* C1: A estratégia ideal é inerentemente específica para a tarefa e o modelo; não existe uma solução universal.
* C2: A compressão exige compromissos humanos entre métricas de memória, tempo e precisão diagnóstica.
* C3: As métricas de topo (como acurácia global) podem ocultar mudanças comportamentais subtis, especialmente em subgrupos linguísticos raros.
* C4: A compressão pode introduzir efeitos indesejados nas camadas internas, dificultando o diagnóstico sem ferramentas de inspeção avançadas.

##  4. Metodologia de Avaliação

Implementou-se uma abordagem híbrida multidimensional:

1. LLM-as-a-Judge: Utilização de modelos de escala superior para auditar a coerência lógica e a fluidez das respostas.
2. Human-in-the-Loop (HiTL): Intervenção de especialistas para validar a manutenção de normas gramaticais de PT-PT que métricas automatizadas tendem a ignorar.
3. Métricas de Desempenho: Utilização do Mean Absolute Error (MAE) como indicador primário da divergência entre as distribuições de probabilidade do modelo original e do quantizado.
4. Visual Analytics: Utilização da ferramenta COMPRESS AND COMPARE, especificamente o Model Map, para identificar a estrutura de ramificação das receitas de compressão, e a vista de Selection Details para isolar as variáveis que explicam as diferenças de desempenho. A análise da Curva de Pareto foi central para filtrar as variantes do AMALIA-9B que melhor satisfazem os orçamentos de latência e memória.

##  5. Resultados e Análise de Benchmarking

O desempenho geral do AMALIA-9B quantizado fixou-se num MAE de 0,6111.

Interpretação Estatística

* Aceitabilidade: O erro de 0,6111 é considerado aceitável para aplicações de produção, indicando uma divergência controlada na confiança do modelo.
* Robustez: O valor sugere que o modelo original possui redundância paramétrica suficiente para suportar a redução de precisão sem colapso semântico.


### Trade-offs Eficiência-Acurácia

| Métrica | Modelo Original (FP32) | AMALIA-9B Quantizado (INT8) | Impacto / Observação |
| :--- | :---: | :---: | :--- |
| **Precisão (MAE)** | 0.0000 (Base) | 0.6111 | Divergência Marginal |
| **Pegada de Memória** | ~36 GB | ~9 GB | Redução de 4x (75%) |
| **Latência** | Elevada | Baixa (Otimizada)* | Viabilização técnica em edge |

*Nota de Cautela: De acordo com as evidências do PQ Bench, a redução da latência em INT8 depende criticamente do suporte de hardware (ex: Tensor Cores NVIDIA Ampere ou superior). Em hardware sem suporte nativo para operações de inteiros, a quantização pode, paradoxalmente, aumentar o tempo de inferência devido a conversões de tipos de dados dispendiosas (costly data type conversions).

## 6. Discussão: Artefactos e Comportamentos Indesejados

Análise de Erros e Viés Linguístico Embora o MAE de 0,6111 seja reduzido, o desafio C3 alerta-nos de que métricas globais podem mascarar degradações em subgrupos. Em estudos análogos (CelebA/ResNet), observou-se que a compressão pode aumentar o erro em atributos sub-representados em mais de 100% (chegando a ~145%), mesmo mantendo a acurácia global estável. Transpondo para o AMALIA-9B, existe o risco de o modelo "esquecer" construções raras do Português de Portugal ou tornar-se excessivamente confiante em respostas gramaticalmente incorretas. A validação HiTL é, portanto, indispensável para garantir que a "colocação pronominal" e outras especificidades lusitanas não foram degradadas.

Influência da Arquitetura e Sensibilidade das Camadas A análise via Layers tab demonstrou que a compressão não afeta o modelo uniformemente. Tal como no caso de estudo do T5-Large, as camadas de normalização mostraram-se críticas: embora representem uma fração minúscula do total de pesos do modelo, a sua compressão agressiva é responsável por uma parcela desproporcional do erro de geração. No AMALIA-9B, a preservação da precisão nestas camadas foi vital para manter a estabilidade das ativações.

Especificidade PT-PT A viabilização técnica do modelo em dispositivos finais não deve ser feita à custa da "neutralização" regional. O MAE obtido demonstra que o AMALIA-9B é robusto, mas a inspeção visual do comportamento das camadas revela que a calibração pós-quantização deve focar-se nos módulos de atenção que processam dependências sintáticas longas, típicas da prosa literária e técnica portuguesa.

## 7. Conclusão

O AMALIA-9B quantizado demonstra uma viabilidade técnica notável, equilibrando uma redução de 75% na ocupação de memória com uma preservação substantiva da qualidade (MAE 0,6111). A robustez evidenciada permite a sua implementação em cenários de computação de fronteira (edge computing), desde que o hardware suporte eficientemente aritmética de inteiros.

Trabalhos futuros deverão focar-se no ajuste fino pós-quantização (post-quantization calibration) utilizando datasets exclusivamente lusitanos, visando mitigar os artefactos identificados nas camadas de normalização e assegurar que o viés linguístico não penalize as formas mais sofisticadas do Português de Portugal.
