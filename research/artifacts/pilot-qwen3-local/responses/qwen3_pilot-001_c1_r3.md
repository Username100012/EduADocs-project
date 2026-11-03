**Plano de Aula: Busca Linear em Vetores**

**Nível:** Graduação em Ciência da Computação  
**Formação:** Introductory  
**Duração:** 50 minutos  
**Objetivo de Aprendizagem:**  
- Implementar pseudocódigo para a busca linear em um vetor de inteiros.  
- Retornar a posição do elemento ou indicar sua ausência.  
- Testar casos de presença e ausência de elementos.  
- Aplicar a metodologia de resolução colaborativa de problemas.  
- Utilizar o quadro e folha com vetores de inteiros para testes de mesa.  
- Produzir pseudocódigo e realizar testes de mesa, justificando os resultados.  

---

### **1. Introdução (5 minutos)**

**Objetivo:** Contextualizar a busca linear como uma técnica básica de busca em estruturas de dados.

- **Definição:** A busca linear é um algoritmo que percorre cada elemento de um vetor sequencialmente até encontrar o elemento desejado.
- **Aplicação:** Usada em vetores não ordenados, onde não há necessidade de ordenamento prévio.
- **Duração:** O algoritmo tem complexidade O(n), onde n é o tamanho do vetor.
- **Aprendizagem esperada:** Entender a lógica de percorrer um vetor e verificar se um elemento está presente.

**Material necessário:**  
- Quadro de quadriculação para anotações.  
- Folhas de papel com vetores de inteiros para testes.  
- Pincel e caneta.  
- Pizzaria ou caneta para escrita.  

---

### **2. Explicação Teórica (10 minutos)**

**Objetivo:** Explicar a lógica do algoritmo de busca linear e apresentar o pseudocódigo.

- **Algoritmo de busca linear:**
  - Iniciar com um índice inicial (0) e um índice final (n-1).
  - Percorrer cada posição do vetor, comparando com o elemento buscado.
  - Se encontrar, retornar a posição.
  - Se não encontrar, retornar -1 ou indicar ausência.

**Pseudocódigo:**

```
Função buscaLinear(vetor, elemento):
    para i de 0 até tamanho(vetor) - 1:
        se vetor[i] == elemento:
            retornar i
    retornar -1
```

**Explicação:**  
- `vetor` é o vetor de inteiros.  
- `elemento` é o valor que queremos buscar.  
- `i` é o índice atual.  
- O algoritmo retorna a posição do elemento se encontrado, caso contrário, retorna -1.

**Material necessário:**  
- Quadro com pseudocódigo escrito.  
- Folhas com exemplos de vetores.  

---

### **3. Resolução Colaborativa (20 minutos)**

**Objetivo:** Os alunos trabalham em grupos para implementar e testar o pseudocódigo.

**Dividir os alunos em grupos de 3 a 4 pessoas.**

**Passos do grupo:**

1. **Definir o vetor de teste:**  
   - Cada grupo recebe um vetor de inteiros pré-definido (ex: [5, 3, 8, 1, 9, 2, 7]).  
   - Cada grupo deve anotar o vetor no quadro.

2. **Implementar o pseudocódigo:**  
   - Cada grupo deve escrever o pseudocódigo de busca linear no quadro, adaptando-o para seu vetor.  
   - Alguém do grupo deve liderar a escrita do pseudocódigo.

3. **Testar casos de presença e ausência:**  
   - Cada grupo deve testar dois casos:
     - **Casos de presença:** (ex: buscar 8 ou 9)
     - **Casos de ausência:** (ex: buscar 10 ou 4)
   - Os grupos devem realizar os testes de mesa e anotar os resultados.

4. **Justificar resultados:**  
   - Cada grupo deve explicar o resultado obtido, mostrando os passos da execução do algoritmo.

**Material necessário:**  
- Folhas com vetores de inteiros.  
- Quadro para anotações.  
- Caneta e pincel para escrita.  

---

### **4. Discussão e Avaliação (10 minutos)**

**Objetivo:** Validar a compreensão dos alunos e reforçar o conteúdo.

- **Perguntas para a turma:**
  - O que acontece se o elemento estiver no final do vetor?
  - O que acontece se o elemento estiver no início do vetor?
  - Como o algoritmo se comporta se o elemento não estiver no vetor?
  - Por que a busca linear é mais lenta que a busca binária?

- **Avaliação:**  
  - **Testes de mesa:** Os alunos devem apresentar os resultados obtidos com base no pseudocódigo.  
  - **Justificativa:** Cada grupo deve justificar o resultado com base no algoritmo.  
  - **Participação:** Os alunos devem participar ativamente do processo de resolução colaborativa.

**Material necessário:**  
- Perguntas escritas no quadro.  
- Folhas com respostas esperadas.  

---

### **5. Conclusão (5 minutos)**

**Objetivo:** Reforçar o conteúdo e preparar os alunos para a próxima aula.

- **Resumo:**  
  - A busca linear é simples, mas pode ser lenta para grandes vetores.  
  - O algoritmo é útil para vetores não ordenados.  
  - O pseudocódigo é claro e fácil de implementar.

- **Próxima aula:**  
  - Introdução à busca binária.  
  - Comparação entre busca linear e busca binária.  

**Material necessário:**  
- Quadro com resumo da aula.  
- Folhas com resumo para os alunos.  

---

### **Anexos:**

1. **Exemplo de vetor de teste:**  
   - [5, 3, 8, 1, 9, 2, 7]

2. **Exemplo de pseudocódigo com comentários:**  
   ```
   Função buscaLinear(vetor, elemento):
       para i de 0 até tamanho(vetor) - 1:
           se vetor[i] == elemento:
               retornar i
       retornar -1
   ```

3. **Exemplo de teste de mesa (caso de presença):**  
   - Vetor: [5, 3, 8, 1, 9, 2, 7]  
   - Elemento buscado: 8  
   - Resultado: posição 2

4. **Exemplo de teste de mesa (caso de ausência):**  
   - Vetor: [5, 3, 8, 1, 9, 2, 7]  
   - Elemento buscado: 10  
   - Resultado: -1 (não encontrado)

---

**Nota:** Este plano de aula foi elaborado com base na metodologia de **resolução colaborativa de problemas**, que estimula a participação ativa, a comunicação e a aplicação prática dos conceitos teóricos.