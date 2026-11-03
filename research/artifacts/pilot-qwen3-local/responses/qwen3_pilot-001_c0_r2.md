Claro! A seguir está um **plano de aula** sobre o tema **"Busca linear em vetores"**, adequado para alunos do ensino médio ou início do ensino superior, com base em conceitos de programação e estruturas de dados.

---

## **Plano de Aula: Busca Linear em Vetores**

### **1. Dados do curso / disciplina:**
- **Disciplina:** Algoritmos e Estruturas de Dados  
- **Carga horária:** 2 aulas (45 minutos cada)  
- **Nível:** Ensino Médio / Início do Ensino Superior  
- **Objetivos:**  
  - Entender o conceito de vetor e suas operações.  
  - Compreender o funcionamento da busca linear em vetores.  
  - Implementar um algoritmo de busca linear em um vetor.  
  - Analisar a eficiência da busca linear em diferentes cenários.  

---

### **2. Conteúdo da aula:**

#### **Aula 1: Introdução a Vetores e Busca Linear**

**Objetivos:**
- Definir o que é um vetor.  
- Explicar a estrutura de dados de vetor.  
- Introduzir o conceito de busca linear.  
- Apresentar o algoritmo de busca linear.  

**Conteúdo:**
- **Vetor:** Estrutura de dados que armazena elementos em ordem.  
  - Exemplo: `vetor = [10, 20, 30, 40, 50]`  
- **Busca linear:** Algoritmo que percorre cada elemento do vetor, comparando com o valor buscado.  
- **Passos do algoritmo de busca linear:**
  1. Iniciar um índice `i` com 0.  
  2. Enquanto `i < tamanho do vetor`:  
     - Se `vetor[i] == valor_busca`, retornar `i`.  
     - Senão, incrementar `i` em 1.  
  3. Se não encontrado, retornar -1.  

**Exemplo prático:**
- Vetor: `[10, 20, 30, 40, 50]`  
- Valor a buscar: `30`  
- Resultado: `2` (índice do elemento).  

**Atividade:**
- Pedir aos alunos que criem um vetor de números e realizem uma busca linear manualmente.  
- Discutir a eficiência do algoritmo.  

---

#### **Aula 2: Implementação e Análise da Busca Linear**

**Objetivos:**
- Implementar o algoritmo de busca linear em uma linguagem de programação.  
- Analisar a complexidade do algoritmo.  
- Discutir as vantagens e desvantagens da busca linear.  

**Conteúdo:**
- **Implementação em Python:**
  ```python
  def busca_linear(vetor, valor_busca):
      for i in range(len(vetor)):
          if vetor[i] == valor_busca:
              return i
      return -1

  # Exemplo de uso
  vetor = [10, 20, 30, 40, 50]
  valor_busca = 30
  resultado = busca_linear(vetor, valor_busca)
  print("Índice encontrado:", resultado)
  ```

- **Complexidade de tempo:**  
  - Pior caso: **O(n)**  
  - Melhor caso: **O(1)**  
  - Caso médio: **O(n/2)**  
- **Vantagens:**  
  - Simples e fácil de implementar.  
  - Funciona com vetores desordenados.  
- **Desvantagens:**  
  - Não eficiente para grandes vetores.  
  - Não é ótimo para buscas repetidas.  

**Atividade:**
- Pedir aos alunos que implementem o algoritmo em outro idioma (como C, Java, ou JavaScript).  
- Comparar a eficiência do algoritmo em vetores de diferentes tamanhos.  

---

### **3. Avaliação:**

- **Avaliação formativa:**  
  - Participação nas atividades práticas.  
  - Entendimento do conceito de busca linear.  
- **Avaliação sumativa:**  
  - Trabalho em grupo: Implementar e testar um algoritmo de busca linear.  
  - Perguntas de fixação:  
    - O que é uma busca linear?  
    - Qual é a complexidade de tempo da busca linear?  
    - Em que casos a busca linear é mais adequada?  

---

### **4. Recursos:**
- Computadores com acesso a Python ou outro linguagem de programação.  
- Projetor de vídeo ou tela para demonstração.  
- Fichas de atividade e exemplos.  

---

### **5. Referências:**
- **Livros:**
  - *Algoritmos* – Robert Sedgewick e Kevin Wayne  
  - *Introdução à Programação com Python* – Nilo M. Duarte  
- **Sites:**
  - [GeeksforGeeks - Busca Linear](https://www.geeksforgeeks.org/linear-search/)  
  - [Wikipedia - Linear search](https://en.wikipedia.org/wiki/Linear_search)  

---

Se quiser, posso adaptar o plano para um nível específico (como ensino médio ou ensino superior) ou incluir exemplos com linguagem de programação específica.