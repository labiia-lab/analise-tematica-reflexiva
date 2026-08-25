# IA em Análise Temática Reflexiva

## Sumário

1. Estatuto da integração
2. Riscos centrais
3. Controles operacionais
4. Relato
5. Evidência e limites

## 1. Estatuto da integração

A IA pode executar F0–F6, inclusive sem participação humana durante o fluxo. Isso constitui uma rota metodológica e técnica deliberada, não prova de equivalência com um pesquisador humano.

Separar:

- capacidade de produzir todos os artefatos;
- cobertura efetiva do corpus;
- integridade das evidências;
- qualidade interpretativa;
- contestação;
- validação humana posterior.

A literatura comparativa usada na construção desta skill é predominantemente híbrida e costuma manter autoridade humana final. Os estudos standalone são menos numerosos e apresentam resultados frágeis para ATR aberta. Esse quadro justifica controles fortes, mas não obriga esta skill a abandonar a experimentação autônoma.

## 2. Riscos centrais

### Sycophancy

Tendência de acomodar a análise à hipótese, teoria ou preferência já apresentada. Controlar com leitura principal antes da contestação, rival material e registro de mudanças.

### Fabricação ou polimento de citações

Texto plausível pode ser inventado, fundido ou melhorado. Usar busca exata, localizador e `scripts/verificar_citacoes.py`. Nunca tratar similaridade semântica como literalidade.

### Ilusão de significados

Prosa coerente pode simular profundidade sem conceito organizador, genealogia ou evidência. Exigir a frase “este tema argumenta que...”, fontes localizadas e uma rival capaz de alterar o mapa.

### Apagamento experiencial

Abstrações podem suprimir hesitação, ambivalência, marcas culturais, metáforas materiais e experiências raras. O risco pode ser silencioso e mais difícil de detectar que uma alucinação explícita.

### Human Experiential Content — HEC

Usar HEC como lente de atenção a conteúdo vivido, culturalmente situado ou corporal que a modelagem textual tende a tornar genérico. Não atribuir à IA a experiência que ela apenas descreve.

### Reflexive Uncertainty Framework — RUF

Tratar zonas de ambiguidade ou instabilidade como sinais epistêmicos a investigar, não como simples ruído. Registrar a incerteza e seu efeito no passaporte do tema.

### Triangulação de superfície

Convergência entre modelos ou passes pode refletir treinamento, prompt ou vocabulário compartilhado. Não chamar isso de triangulação humana nem de validação.

### Confusão entre níveis

Modelos podem misturar excerto, código, categoria e tema. Preservar a hierarquia e exigir conceito organizador para temas.

## 3. Controles operacionais

### Delegação explícita

Registrar nível 0–3 por fase, função, modelo, fontes e verificação. Não usar “a IA ajudou” como descrição suficiente.

### Sweet spot operacional

Usar busca de contraexemplos, rastreamento, reorganização e crítica como operações fortes. Submeter abstrações temáticas a contestação e conservação experiencial antes da integração.

### Responsabilidade algorítmica

Registrar condições técnicas que afetaram a análise: modelo, versão, parâmetros expostos, janela de contexto, lotes, repetição, pós-processamento e falhas.

### Correflexão

Documentar como instruções humanas, material anterior e processamento algorítmico influenciaram decisões. Na rota sem humanos, registrar explicitamente “não houve intervenção humana” e preservar a reflexividade operacional da IA.

### Segurança e consentimento

Minimizar dados, registrar processamento local/remoto quando conhecido e não inventar autorização. Incerteza ética limita alegações; não transforma automaticamente a interpretação em inexistente.

## 4. Relato

Um relato inspirado em TROUT-AI, COREQ e SRQR deve incluir, quando aplicável:

- modelo, versão, data e ambiente;
- parâmetros expostos;
- rota e delegação por fase;
- prompts ou versões sanitizadas;
- corpus realmente processado;
- métodos de verificação;
- intervenções humanas;
- mudanças após contestação;
- limitações técnicas, culturais e epistemológicas;
- arquivos produzidos.

Não registrar raciocínio interno nem dados sensíveis apenas para aumentar a aparência de transparência.

## 5. Evidência e limites

Achados usados como âncoras:

- Naeem et al. (2025): decomposição passo a passo melhora estrutura, mas não elimina dependência interpretativa.
- Nguyen-Trung (2025): prompts detalhados ajudam e ainda deixam confusões conceituais.
- Jowsey et al. (2025), Wachinger et al. (2025) e Vikan et al. (2026): citações fabricadas e profundidade desigual exigem conferência literal.
- Sakaguchi et al. (2025): temas culturalmente situados foram mais difíceis que temas descritivos.
- Pretorius e Pretorius (2025): diálogo pode reconfigurar a leitura, sem virar requisito para toda rota.
- Kempny et al. (2026): relato de modelos e parâmetros é frequentemente incompleto.
- Costa e Bem-Haja (2025): incerteza pode ser preservada como sinal epistêmico.

HEC, sycophancy, ilusão de significados, sweet spot, TROUT-AI, responsabilidade algorítmica e correflexão funcionam aqui como conceitos sensibilizadores e controles. Antes de citá-los em manuscrito acadêmico, verificar a referência primária correspondente. A skill não transforma esses conceitos em escalas validadas.
