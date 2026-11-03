**Plano de Aula: Busca Linear em Vetores**

**Nível:** Graduação em Ciência da Computação  
**Formação:** Introdutória  
**Duração:** 50 minutos  
**Metodologia:** Resolução colaborativa de problemas  
**Objetivo de Aprendizagem:**  
- Implementar o algoritmo de **busca linear** em pseudocódigo sobre um vetor de inteiros.  
- Retornar a posição do elemento ou indicar sua ausência.  
- Testar casos de **presença** e **ausência** do elemento.  
- Utilizar **quadro e folha com vetores de inteiros** para testes de mesa.  
- Produzir **pseudocódigo** e realizar **testes de mesa**, justificando os resultados como estratégia de avaliação.

---

## **1. Introdução (5 minutos)**

**Objetivo:** Apresentar o conceito de busca linear e sua aplicação em vetores.

**Conteúdo:**

- Definição de vetor: estrutura de dados que armazena elementos sequenciais.
- Busca linear: técnica de busca em que cada elemento do vetor é verificado sequencialmente até encontrar o elemento desejado.
- Aplicação: utilizada quando o vetor não está ordenado ou quando o tamanho do vetor é pequeno.
- Aprendizado esperado: compreender o funcionamento do algoritmo e sua complexidade.

**Atividade:**  
- Professor apresenta o conceito de busca linear com um exemplo simples (ex: vetor [10, 20, 30, 40, 50]) e busca por 30.
- Pergunta: "Como você acharia o elemento 30 no vetor? Como isso seria implementado em pseudocódigo?"

---

## **2. Explicação do Algoritmo (10 minutos)**

**Objetivo:** Explicar o algoritmo de busca linear em pseudocódigo.

**Conteúdo:**

- Pseudocódigo básico de busca linear:
```pseudocódigo
FUNÇÃO buscar_linear(vetor, elemento):
    PARA i DE 0 ATÉ tamanho(vetor) - 1:
        SE vetor[i] == elemento:
            RETORNAR i  // posição do elemento
    RETORNAR -1  // elemento não encontrado
```

- Explicação de cada parte do pseudocódigo:
  - `vetor`: vetor de inteiros.
  - `elemento`: valor a ser buscado.
  - `i`: índice do vetor.
  - `tamanho(vetor)`: número de elementos no vetor.
  - `RETORNAR`: valor da posição ou -1 se não encontrado.

**Atividade:**  
- Professor explica o pseudocódigo com exemplos.
- Pergunta: "Qual seria a saída se buscássemos 60 no vetor [10, 20, 30, 40, 50]?"

---

## **3. Resolução Colaborativa (20 minutos)**

**Objetivo:** Trabalhar em grupo para implementar e testar o algoritmo.

**Materiais:**
- Quadro com vetores de inteiros (ex: [15, 25, 35, 45, 55]).
- Folhas com os mesmos vetores para testes de mesa.
- Páginas de anotações para cada grupo.

**Atividade:**

- Os alunos são divididos em grupos de 3 a 4 pessoas.
- Cada grupo recebe um vetor de inteiros (ex: [15, 25, 35, 45, 55]).
- Cada grupo deve:
  1. Escrever o pseudocódigo da busca linear.
  2. Escolher um elemento para buscar (ex: 35).
  3. Realizar o teste de mesa, mostrando os passos da busca.
  4. Registrar o resultado (posição ou -1).
  5. Justificar o resultado com base no algoritmo.

**Exemplo de teste de mesa:**
- Vetor: [15, 25, 35, 45, 55]
- Buscar 35:
  - Passo 1: i = 0 → 15 ≠ 35 → continuar
  - Passo 2: i = 1 → 25 ≠ 35 → continuar
  - Passo 3: i = 2 → 35 == 35 → retornar 2

**Avaliação:**  
- Cada grupo apresenta o pseudocódigo, o teste de mesa e a justificativa do resultado.
- Professor faz uma correção e oferece feedback.

---

## **4. Discussão e Resumo (10 minutos)**

**Objetivo:** Reforçar o conteúdo e resolver dúvidas.

**Conteúdo:**

- Revisão do pseudocódigo e sua lógica.
- Diferenças entre busca linear e busca binária.
- Aplicação prática da busca linear em situações reais.
- Questões de fixação:
  - Qual é a complexidade de tempo da busca linear?
  - Em que casos é melhor usar a busca linear?

**Atividade:**
- Professor pergunta: "Por que a busca linear não é eficiente em vetores grandes?"
- Alunos respondem e o professor complementa.

---

## **5. Avaliação (5 minutos)**

**Objetivo:** Avaliar o entendimento e a aplicação do algoritmo.

**Critérios de Avaliação:**
- Correto uso do pseudocódigo.
- Correto teste de mesa com justificativa.
- Capacidade de identificar a presença ou ausência do elemento.

**Forma de Avaliação:**
- O professor observa os grupos durante a atividade.
- Cada grupo recebe um “símbolo de aprovação” se completar com sucesso a tarefa.

---

## **Recursos Utilizados:**

- Quadro com vetores de inteiros.
- Folhas com vetores para testes de mesa.
- Páginas de anotações.
- Pseudocódigo em papel.
- Apresentação do professor (opcional, se necessário).

---

## **Próximos Passos:**

- Introduzir a busca binária como alternativa.
- Trabalhar com outros tipos de estruturas de dados.
- Realizar uma atividade prática em linguagem de programação (Python, Java, C, etc.).

---

**Nota:** Este plano de aula pode ser adaptado para diferentes níveis de dificuldade, incluindo o uso de ferramentas digitais (como editores de pseudocódigo online ou simulações de algoritmos).