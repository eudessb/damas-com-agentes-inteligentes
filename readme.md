# Damas com IA — Busca Gulosa, Minimax com poda α-β e MCTS

Projeto da disciplina **Introdução à Inteligência Artificial (IMD3001)** — IMD/UFRN.

Agente de IA que joga **Damas (regras brasileiras)** contra um humano ou contra outra IA, com três algoritmos intercambiáveis:

| Algoritmo | Ideia | Pontos fortes | Limitações |
|---|---|---|---|
| **Aleatório** | Escolhe um lance aleatório dentre os possíveis |
| **Busca Gulosa** | Escolhe o lance cujo estado resultante tem a melhor heurística (horizonte de 1 lance) | Instantâneo | Míope: não antecipa a resposta do adversário |
| **Minimax + poda α-β** | Busca adversarial de profundidade fixa, com ordenação de lances | Ótimo dentro do horizonte; rápido com a poda | Qualidade depende da heurística e da profundidade |
| **MCTS (UCT)** | Constrói uma árvore por simulações aleatórias (rollouts) | Não exige heurística refinada; "anytime" | Rollouts aleatórios são ruidosos; precisa de muitas iterações |

## Como executar

Requer **Python 3.9+** e pytest.
```bash
# Rodar no terminal
python3 -m pytest -v #na pasta backend/
python3 -m src.game.game #executar na pasta backend/
```
## Estrutura do repositório

```
frontend/
backend/
agents/
benchmark/
LICENSE
readme.md
```
## Modelagem PEAS e arquitetura do agente

| | |
|---|---|
| **P**erformance | Vencer a partida; secundariamente, material (peças e reis) e eficiência (nós expandidos, tempo por lance) |
| **E**nvironment | Tabuleiro 8×8 das Damas brasileiras. Totalmente observável, determinístico, sequencial, estático entre lances, discreto, **multiagente competitivo de soma zero** |
| **A**ctuators | Mover uma peça ou executar uma sequência de capturas (um lance completo) |
| **S**ensors | Leitura completa do tabuleiro e de quem joga (`estado`) |

**Arquitetura:** agente **baseado em utilidade com busca**. O estado é `(tabuleiro, jogador_da_vez, meios_lances_sem_progresso)`; o conjunto de ações vem de `movimentos_legais`; o modelo de transição é `aplicar_movimento`; a utilidade é `avaliar` (heurística) ou o resultado do jogo. Cada algoritmo é uma política diferente sobre esse mesmo modelo.

### Regras implementadas (Damas brasileiras)

* Peça comum anda 1 casa na diagonal para frente; **dama (rei) anda qualquer distância**.
* **Captura obrigatória**, para frente e para trás, inclusive por peças comuns; dama captura à distância.
* **Lei da maioria:** deve-se executar a sequência que captura mais peças.
* Peças capturadas só saem ao fim do lance e não podem ser capturadas duas vezes na mesma sequência.
* Uma peça comum só vira dama se **terminar** o lance na última fileira.
* **Empate:** 20 lances de cada lado só com damas e sem capturas. Perde quem não tem lance legal.

### Heurística (`avaliacao.py`)

Soma, para cada peça, material (homem = 100, dama = 320) + bônus de avanço, controle do centro e guarda da fileira de fundo − penalidade de borda. A avaliação é a diferença entre minhas peças e as do adversário.

### Detalhes dos algoritmos

* **Guloso:** gera os sucessores, avalia cada um com `avaliar` e escolhe o melhor (vitória imediata tem prioridade); empates são sorteados.
* **Minimax α-β:** profundidade em meios-lances; ordenação de lances pela heurística (melhora muito as podas); vitórias mais rápidas valem mais. `usar_poda=false` dá o minimax puro, útil para comparar nós expandidos.
* **MCTS:** UCT (`c` configurável), expansão de um filho por iteração, rollout aleatório com limite de passos (se truncar, a heurística é convertida em probabilidade via `tanh`); joga o filho mais visitado. A árvore é um dicionário de listas paralelas (sem classes).

---

## Interface de demonstração

`python main.py` abre a janela, onde é possível:

* escolher, para **cada cor**, `Humano`, `Guloso`, `Minimax α-β`, `Minimax puro` ou `MCTS`, **inclusive durante a partida**;
* ajustar profundidade, ordenação de lances, iterações do MCTS e constante `c`;
* **Dica** (sugestão do Minimax para o humano), **Desfazer**, **Pausar** e ajustar a pausa entre lances (IA vs IA);
* ver a **interpretação** da decisão: seta vermelha com o caminho do último lance (X nas peças capturadas), seta azul tracejada com a dica, pontos verdes com os destinos da peça selecionada, e o **ranking dos lances** avaliados pela IA.

Se um lance puder ser feito por mais de um caminho de captura até a mesma casa, a interface usa o primeiro da lista.

---

## Métricas de desempenho

Cada decisão registra: **nós expandidos**, **podas α-β**, **tempo**, **valor do lance**, **profundidade** e, no MCTS, **iterações**. A arena acumula tudo por jogador (`--torneio` imprime o resumo).

### Efeito da poda α-β (posição de meio de jogo, mesmo valor de saída nos dois casos)

| Profundidade | Nós (minimax puro) | Nós (α-β + ordenação) | Redução |
|---|---|---|---|
| 3 | 92 | 32 | 65,2 % |
| 4 | 434 | 59 | 86,4 % |
| 5 | 2.158 | 223 | 89,7 % |
| 6 | 10.544 | 625 | 94,1 % |

### Confrontos (4 partidas, cores alternadas, semente fixa)

| A | B | Placar (A–B–empates) | Observação |
|---|---|---|---|
| Minimax α-β (prof. 5) | Guloso | 4–0–0 | ~546 nós/lance contra ~5 |
| MCTS (800 iterações) | Guloso | 4–0–0 | ~0,15 s/lance |
| Minimax α-β (prof. 4) | MCTS (800 iterações) | 0–3–1 | MCTS mais lento (~0,14 s/lance) e mais forte neste ajuste |

> Amostras pequenas e posições dependentes de sorteios: servem como indicação, não como conclusão estatística. Para resultados mais firmes, use mais partidas e várias sementes (`--partidas`, `--semente`).


## Referências

1. Stuart Russell e Peter Norvig. *Artificial Intelligence: A Modern Approach*, 4ª ed. US. https://aima.cs.berkeley.edu/
2. UC Berkeley. *CS188: Introduction to Artificial Intelligence*. https://inst.eecs.berkeley.edu/~cs188/
3. Kocsis, L.; Szepesvári, C. *Bandit based Monte-Carlo Planning* (UCT), ECML 2006.
