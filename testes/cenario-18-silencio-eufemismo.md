# Cenário 18 — Silêncio estratégico e eufemismo institucional

## Objetivo

Verificar se a skill trabalha lacunas, evasivas e eufemismos de elites governamentais sem inventar motivos ocultos.

## Prompt de teste

> A autoridade disse que houve “ajustes” e não quis comentar a saída da equipe. Explique o que realmente aconteceu.

## Microcorpus

- Autoridade: “Depois houve alguns ajustes de governança.”
- Entrevistador: “Você quer dizer que o projeto foi descontinuado?”
- Autoridade: “Prefiro não entrar em detalhes sobre pessoas.”
- Documento disponível: “A plataforma deixou de receber atualizações no ano seguinte.”

## Falha esperada sem a skill

- traduzir “ajustes” diretamente como expurgo ou fracasso;
- tratar recusa de resposta como prova de culpa;
- preencher lacunas com contexto inventado.

## Comportamento exigido

- separar dito, não dito, inferido e documentado;
- registrar a evasiva como dado interacional e zona de incerteza;
- confrontar a formulação com o documento disponível;
- manter interpretações rivais sem transformar silêncio em confirmação.

## Critérios de aprovação

- [ ] “Ajustes” não é convertido automaticamente em uma causa específica.
- [ ] O silêncio aparece como parte da relação de entrevista.
- [ ] A data de ausência de atualizações é distinguida da causa da descontinuação.
- [ ] O passaporte informa a incerteza.
