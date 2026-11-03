**Plano de Aula: Busca Linear em Vetores**

**Nível:** Graduação em Ciência da Computação  
**Formação:** Introdutória  
**Duração:** 50 minutos  
**Metodologia:** Resolução colaborativa de problemas  
**Objetivo de Aprendizagem:**  
- Implementar a busca linear em pseudocódigo sobre um vetor de inteiros, retornando a posição do elemento ou indicando ausência.  
- Testar casos de presença e ausência de elementos no vetor.  
- Justificar os resultados obtidos como estratégia de avaliação.  

---

### **1. Introdução (5 minutos)**

- **Contextualização:**  
  A busca linear é uma técnica simples e eficaz para localizar um elemento em um vetor. É útil quando o vetor não está ordenado ou quando o número de elementos é pequeno.  
  - **Definição:** Percorrer cada elemento do vetor sequencialmente até encontrar o elemento desejado ou verificar que ele não existe.  

- **Objetivo da aula:**  
  - Entender o conceito de busca linear.  
  - Implementar o algoritmo em pseudocódigo.  
  - Testar o algoritmo com exemplos.  

---

### **2. Aprendizagem Direta (10 minutos)**

- **Explicação do Algoritmo de Busca Linear:**
  - Passo a passo:
    1. Iniciar um índice `i` em 0.
    2. Enquanto `i < tamanho do vetor`:
        - Comparar o elemento no índice `i` com o elemento buscado.
        - Se encontrarmos, retornar o índice.
        - Senão, incrementar `i`.
    3. Se o laço terminar sem encontrar, retornar -1 ou "não encontrado".

- **Exemplo de pseudocódigo:**

```pseudocódigo
funcao buscaLinear(vetor, elemento):
    i = 0
    enquanto i < tamanho(vetor):
        se vetor[i] == elemento:
            retornar i
        senão:
            i = i + 1
    retornar -1
```

- **Explicação de cada parte do pseudocódigo.**

---

### **3. Atividade Colaborativa (25 minutos)**

**Materiais necessários:**
- Quadro para anotações.
- Folhas com vetores de inteiros para testes de mesa.
- Canetas e lápis.

**Passo a passo da atividade:**

1. **Dividir a turma em grupos de 3 a 4 alunos.**
2. **Distribuir a cada grupo um vetor de inteiros e um elemento para buscar.**
3. **Cada grupo deve:**
   - Implementar o pseudocódigo de busca linear.
   - Realizar testes de mesa com o vetor fornecido.
   - Anotar a posição do elemento encontrado ou a mensagem de ausência.
   - Justificar o resultado com base no algoritmo.

**Exemplo de vetor para teste:**

```plaintext
vetor = [5, 10, 3, 7, 15, 2]
elemento = 7
```

**Resultado esperado:** posição 3

**Outro exemplo:**

```plaintext
vetor = [1, 3, 5, 7, 9]
elemento = 10
```

**Resultado esperado:** ausência

---

### **4. Apresentação e Discussão (10 minutos)**

- **Cada grupo apresenta o pseudocódigo e os resultados de testes de mesa.**
- **Discutir:**
  - Como o algoritmo funciona.
  - O que acontece quando o elemento está no início, no meio ou no final do vetor.
  - Como identificar a ausência do elemento.
  - Dificuldades encontradas durante a implementação.

---

### **5. Avaliação (10 minutos)**

- **Avaliação por meio de testes de mesa realizados pelos grupos.**
- **Critérios de avaliação:**
  - Correção do pseudocódigo.
  - Correção dos testes de mesa.
  - Justificativa clara dos resultados.
  - Participação ativa na resolução colaborativa.

---

### **6. Encerramento (5 minutos)**

- **Resumo da aula:**
  - A busca linear é uma técnica simples, mas eficaz para vetores não ordenados.
  - O pseudocódigo foi implementado com base em lógica sequencial.
  - Testes de mesa ajudam a validar a corretude do algoritmo.

- **Questões para reflexão:**
  - Qual é a complexidade do algoritmo de busca linear?
  - Em que situações é mais vantajoso usar a busca linear?
  - Como seria a busca linear em um vetor ordenado?

- **Próxima aula:** Introdução à busca binária.

---

### **Recursos Utilizados:**
- Quadro de anotações
- Folhas com vetores de inteiros
- Canetas e lápis
- Pseudocódigo como base para implementação

---

**Nota:** Este plano de aula é adaptado para uma aula prática, com ênfase em resolução colaborativa e testes de mesa, para reforçar a compreensão teórica de algoritmos básicos em estruturas de dados.