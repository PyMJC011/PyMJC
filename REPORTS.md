# 1º Relatóio: Etapa AI-a (Analisador Léxico e Sintático)

1. Qual é o nome do relator?

    > Luis Fernando Bastos Rego

2. A etapa foi completamente ou parcialmente concluída?

    > A etapa foi completamente concluída.

3. No caso de parcialmente concluída, o que não foi concluído?

    > Não se aplica.

4. O programa passa nos testes automatizados?
    
    > Não, pois acredito que existe um possível erro nos testes (Erro na contagem dos tokens)

5. Algum erro de execução foi encontrado para alguma das entradas? Quais?
    
    > Não.

6. Quais as dificuldades encontradas para realização da etapa do projeto?
    
    > A dificuldade foi de:
    resolver cada parte de expressão regular na gramática do MiniJava, e também suas ambiguidades; 
    o Python não permitiu colocar um novo método para a classe MJParser para contagem de colunas (Diversos erros foram mostrados);
    por conta do motivo anterior, não foi possível printar o número da coluna do token que o Parser não conseguiu tratar;
    conflito de shift/reduce que surgiu com a regra de gramática para tratar dos seguintes constructos:  ( VarDeclaration )* e ( Type Identifier ( "," Type Identifier )* )?

7. Qual a participação de cada membro da equipe na etapa de execução?
    
    > Ambos os membros fizeram os analisadores em conjunto, exceto por apenas algumas partes de implementação que foram feitas após o planejamento executado pela equipe, por exemplo:
    A implementação da gramática após ela ser reconstruída para não ter expressões regulares e nem ambiguidades foi feita por Samuel;
    A adaptação do lexer para se adequar ao modelo encontrado no repositório foi feito por Luis.


# 2º Relatóio: Etapa AI-b (Árvores Sintática Abstrata e Análise Semântica)

1. Qual é o nome do relator?

    > Samuel Vieira de Paula Farias

2. A etapa foi completamente ou parcialmente concluída?

    > Parcialmente concluída.

3. No caso de parcialmente concluída, o que não foi concluído?

    > Não temos certeza sobre integridade dos Visitors.

4. O programa passa nos testes automatizados?
    
    > Os testes automatizados não foram feitos, apenas pequenos testes feitos isoladamente.

5. Algum erro de execução foi encontrado para alguma das entradas? Quais?
    
    > ...

6. Quais as dificuldades encontradas para realização da etapa do projeto?
    
    > Compreender os pontos exatos para realizar a checagem da tabela de símbolos e a checagem de tipos nos visitors.

7. Qual a participação de cada membro da equipe na etapa de execução?
    
    > Ambos fizeram o trabalho em conjunto.


# 3º Relatóio: Etapa AI-c (Tradução para o Código Intermediário)

1. Qual é o nome do relator?

    > Luis Fernando Bastos Rego

2. A etapa foi completamente ou parcialmente concluída?

    > Parcialmente concluída
    > 2º entrega: Completamente concluída

3. No caso de parcialmente concluída, o que não foi concluído?

    > Não foi concluída a implementação dos seguintes visitors: array_assign, new_array, if, while, print, identifier, identifier_exp
    > 2º entrega: não se aplica.

4. O programa passa nos testes automatizados?
    
    > Não se aplica.

5. Algum erro de execução foi encontrado para alguma das entradas? Quais?
    
    > Não se aplica.

6. Quais as dificuldades encontradas para realização da etapa do projeto?
    
    > As dificuldades foram em conseguir utilizar o framework do projeto, pois as implementações diferem das aulas do Prof. Heron e das implementações já existentes nos livros e site da Cambridge, além de que as implementações do Prof. Heron também são diferentes que essas outras implementações.
    > 2º entrega: com as novas implementações do framework, ficou mais fácil de reproduzir as implementações dos visitors, logo a dificuldade foi entender visit_call e visit_new_object, pois estas diferem muito nos livros e nas aulas, logo foi consumido muito tempo para saber se esses dois visitors estavam implementados parcialmente ou não.  
    
7. Qual a participação de cada membro da equipe na etapa de execução?
    
    > Ambos fizeram o trabalho em conjunto.


# 4º Relatóio: Etapa AI-d (Seleção de Instruções)

1. Qual é o nome do relator?

    > Samuel Vieira de Paula Farias

2. A etapa foi completamente ou parcialmente concluída?

    > Parcialmente concluída.

3. No caso de parcialmente concluída, o que não foi concluído?

    > Resta escrever os demais métodos para cores fora AssignColors; não foram feito os métodos de Simplify, Coalesce, Freeze e Spill e relacionados;

4. O programa passa nos testes automatizados?
    
    > ...

5. Algum erro de execução foi encontrado para alguma das entradas? Quais?
    
    > ...

6. Quais as dificuldades encontradas para realização da etapa do projeto?
    
    > Faltou tempo para implementar os métodos do arquivo .java, pois muitos deles utilizaram estratégias diferentes das utilizadas pelo framework, além de muitas implementações eram para ser feitas do zero (apesar de existirem no .java como base). Além disso, um dos membros adoeceu.

7. Qual a participação de cada membro da equipe na etapa de execução?
    
    > Ambos fizeram o trabalho em conjunto.


# 5º Relatóio: Etapa AI-e (Alocação de Registradores)

1. Qual é o nome do relator?

    > Escreva sua resposta aqui

2. A etapa foi completamente ou parcialmente concluída?

    > Escreva sua resposta aqui

3. No caso de parcialmente concluída, o que não foi concluído?

    > Escreva sua resposta aqui

4. O programa passa nos testes automatizados?
    
    > Escreva sua resposta aqui

5. Algum erro de execução foi encontrado para alguma das entradas? Quais?
    
    > Escreva sua resposta aqui

6. Quais as dificuldades encontradas para realização da etapa do projeto?
    
    > Escreva sua resposta aqui

7. Qual a participação de cada membro da equipe na etapa de execução?
    
    > Escreva sua resposta aqui


# 6º Relatóio: Etapa AI-f (Integração e Geração do Código Final)

1. Qual é o nome do relator?

    > Escreva sua resposta aqui

2. A etapa foi completamente ou parcialmente concluída?

    > Escreva sua resposta aqui

3. No caso de parcialmente concluída, o que não foi concluído?

    > Escreva sua resposta aqui

4. O programa passa nos testes automatizados?
    
    > Escreva sua resposta aqui

5. Algum erro de execução foi encontrado para alguma das entradas? Quais?
    
    > Escreva sua resposta aqui

6. Quais as dificuldades encontradas para realização da etapa do projeto?
    
    > Escreva sua resposta aqui

7. Qual a participação de cada membro da equipe na etapa de execução?
    
    > Escreva sua resposta aqui
