# Teste de aptidão do modelo

Microtarefa de três partes, feita antes de F0, para saber se o modelo que vai
executar a análise sustenta o mínimo que a skill exige: citar literalmente,
distinguir tema de tópico e perceber uma citação alterada.

O corpus é ficcional e está em `microcorpus.txt`, uma fala por linha. Responder
sem abrir `scripts/auditar_analise.py`: o gabarito está lá e a consulta anula o
teste.

## Parte 1 — Citação literal

Escolher três trechos diferentes do microcorpus, cada um com seis palavras ou
mais, copiados caractere por caractere, e informar a linha de cada um.

## Parte 2 — Tema ou tópico

Classificar cada formulação como `tema` (padrão de significado com uma
afirmação) ou `topico` (assunto sobre o qual se fala):

- A. Opiniões sobre a horta
- B. Cuidar da horta como forma de voltar a contar com os vizinhos
- C. Vantagens e desvantagens do mutirão
- D. A regra só vale quando quem cobra também põe a mão na terra
- E. Dificuldades enfrentadas
- F. Colher sem ter plantado ameaça o pertencimento, não só a colheita

## Parte 3 — Citação alterada

Indicar quais destas “citações” não estão literalmente no microcorpus:

- X1. “cada um passou a avisar o vizinho do lado”
- X2. “A horta nos devolveu o sentido de comunidade que o bairro tinha perdido”
- X3. “sei quem aparece no mutirão e quem só aparece na colheita”
- X4. “Quem cobra regras de mim precisa estar com a mão na terra também”
- X5. “Eu parei de ir porque me senti julgada pelos outros moradores”

## Formato da resposta

Gravar `respostas-aptidao.json` fora da pasta da skill:

```json
{
  "citacoes": [{"texto": "...", "linha": 1}, {"texto": "...", "linha": 2}, {"texto": "...", "linha": 3}],
  "classificacao": {"A": "topico", "B": "tema", "C": "...", "D": "...", "E": "...", "F": "..."},
  "nao_literais": ["X0"]
}
```

Os valores acima mostram só o formato. Corrigir com:

```text
python "<PASTA_DA_SKILL>/scripts/auditar_analise.py" aptidao --respostas respostas-aptidao.json --output aptidao.json
```

## Leitura do resultado

- `apto`: seguir com o perfil que o ambiente permitir.
- `parcial`: seguir com o andaime reforçado e registrar a parte que falhou.
- `inapto`: avisar o usuário antes de F0. Se ele mandar continuar, usar o
  andaime reforçado e declarar o resultado no estatuto final.

O teste mede um piso, não a qualidade da análise que virá.
