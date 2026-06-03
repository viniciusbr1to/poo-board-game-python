# Jogos de Tabuleiro
Projeto desenvolvido para a disciplina de Programação Orientada a Objetos.

## Integrantes
- Vinicius Lavraldo de Brito

## Descrição da arquitetura
O projeto foi construído com uma arquitetura orientada a objetos extensível, separada em duas camadas:

- `src/core/`: classes genéricas e reutilizáveis que formam a base para qualquer jogo de tabuleiro.
- `src/jogos/`: implementações concretas de jogos que herdam da base.

A classe central é `JogoTabuleiro`, uma classe abstrata que define o contrato que todo jogo deve seguir. Para adicionar um novo jogo, basta criar uma subclasse e implementar três métodos: `validar_jogada`, `aplicar_jogada` e `verificar_fim`.

## Classes principais
### `JogoTabuleiro` (abstrata)
Classe base de todos os jogos. Define o fluxo geral de uma partida, inicializar, jogar, alternar turnos e encerrar,e exige que as subclasses implementem as regras específicas de cada jogo.

### `Tabuleiro`
Representa a grade do jogo. Armazena as peças em uma matriz e oferece métodos para obter, definir e verificar posições. É genérico: funciona para qualquer tamanho de grade.

### `Jogador`
Representa um jogador com nome, símbolo e pontuação acumulada entre partidas.

### `Peca`
Representa uma peça no tabuleiro, com símbolo e referência ao jogador dono.

### `Jogada`
Representa uma jogada, contendo linha, coluna e o jogador que a realizou.

### `Turno`
Controla a alternância entre jogadores durante a partida.

### `JogoDaVelha`
Implementação concreta do Jogo da Velha. Herda de `JogoTabuleiro` e implementa as regras específicas: tabuleiro 3×3, verificação de vitória em linhas, colunas e diagonais, e detecção de empate.

### Instalação
```bash
pip install pytest
```
### Rodar o jogo
```bash
python main.py
```

### Rodar os testes
```bash
python -m pytest tests/
```

## Jogos implementados
- **Jogo da Velha**: dois jogadores disputam em um tabuleiro 3×3. Vence quem completar uma linha, coluna ou diagonal com seu símbolo.

## Decisões de projeto
- A classe `JogoTabuleiro` foi definida como abstrata para garantir que toda subclasse implemente obrigatoriamente `validar_jogada`, `aplicar_jogada` e `verificar_fim`, evitando erros em tempo de execução.
- O encapsulamento foi aplicado em todas as classes com atributos privados e acesso via `@property`, protegendo o estado interno dos objetos.
- A classe `Tabuleiro` foi mantida genérica, sem nenhuma lógica de jogo, para que possa ser reutilizada por qualquer jogo com qualquer tamanho de grade.
- `Turno` e `Jogada` foram separados em classes próprias para deixar as responsabilidades bem definidas e facilitar extensões futuras.

## Limitações e melhorias futuras
- O projeto conta com apenas um jogo implementado. A arquitetura permite adicionar novos jogos como Lig-4, Damas ou Xadrez simplificado com impacto mínimo no código existente.
- A interface atual é apenas via terminal. Uma melhoria futura seria adicionar uma interface gráfica com `pygame` ou semelhantes.
