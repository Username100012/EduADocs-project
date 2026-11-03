**Plano de Aula: Consultas SQL com SELECT e WHERE em uma tabela**

---

### **1. Dados Gerais**

- **Tópico:** Consultas SQL com SELECT e WHERE em uma tabela
- **Nível educacional:** Graduação em Ciência da Computação – formação introdutória
- **Duração:** 50 minutos
- **Metodologia:** Resolução colaborativa de problemas
- **Materiais e recursos:** Quadro, folha com tabela de produtos (contendo código, nome e preço), projetor (opcional), computadores com acesso a ambiente SQL (opcional)
- **Estratégia de avaliação:** Escrever duas consultas com SELECT e WHERE, uma com igualdade e outra com comparação numérica, e indicar os resultados esperados

---

### **2. Objetivos de Aprendizagem**

- Identificar e utilizar cláusulas SELECT e WHERE em consultas SQL.
- Escrever consultas que retornem linhas específicas de uma tabela com base em condições de igualdade e comparação numérica.
- Entender como as condições afetam o resultado de uma consulta SQL.

---

### **3. Estrutura do Plano de Aula**

#### **I. Introdução (5 minutos)**

- Apresentar o tema e o objetivo da aula.
- Explicar brevemente o que é uma consulta SQL e a importância das cláusulas SELECT e WHERE.
- Introduzir a tabela de produtos com exemplos de dados.
- Mostrar a estrutura básica de uma consulta SQL: `SELECT [campos] FROM [tabela] WHERE [condição]`.

#### **II. Explicação Teórica (10 minutos)**

- Explicar a sintaxe do comando SELECT com WHERE:
  ```
  SELECT * FROM produtos WHERE [condição];
  ```
- Explicar as condições de igualdade: `=`, `==`, `LIKE`, `IN`, etc.
- Explicar as condições de comparação numérica: `>`, `<`, `>=`, `<=`, `BETWEEN`, etc.
- Exemplificar com exemplos simples:
  - `WHERE preco = 100`
  - `WHERE preco > 50 AND preco < 200`

#### **III. Atividade Prática (25 minutos)**

**1. Atividade 1: Consulta com igualdade (10 minutos)**

- Distribuir a folha com a tabela de produtos (exemplo):
  | Código | Nome         | Preço |
  |--------|--------------|-------|
  | 1      | Notebook     | 1200  |
  | 2      | Celular      | 800   |
  | 3      | Mouse        | 100   |
  | 4      | Teclado      | 150   |
  | 5      | Monitor      | 600   |

- Instruir os alunos a criar uma consulta que retorne produtos com preço igual a 100.
- Compartilhar as respostas e discutir os resultados.

**2. Atividade 2: Consulta com comparação numérica (15 minutos)**

- Instruir os alunos a criar uma consulta que retorne produtos com preço entre 100 e 200.
- Compartilhar as respostas e discutir os resultados.
- Comparar os resultados das duas consultas e discutir a diferença entre `=`, `>`, `<`, etc.

#### **IV. Avaliação (5 minutos)**

- Os alunos devem escrever duas consultas SQL no quadro:
  1. Uma com `WHERE preco = 100`
  2. Uma com `WHERE preco > 100 AND preco < 200`
- Indicar os resultados esperados com base na tabela fornecida.
- Os alunos devem apresentar as consultas e discutir os resultados em grupo.

---

### **4. Conclusão (5 minutos)**

- Resumir o conteúdo principal: cláusulas SELECT e WHERE, condições de igualdade e comparação numérica.
- Destacar a importância de entender as condições para filtrar dados corretamente.
- Oferecer sugestões para aprofundamento (ex.: uso de operadores lógicos, funções de agregação, etc.).
- Encerrar a aula com uma pergunta de reflexão: "Como você usaria estas consultas em um sistema de gestão de uma loja?"

---

### **5. Recursos Complementares (Opcionais)**

- Ambiente online de execução de SQL (como SQLFiddle, DB Fiddle, ou o próprio banco de dados do curso).
- Exercícios adicionais para casa (opcional).

---

### **6. Aprendizagem Esperada**

- Os alunos serão capazes de escrever consultas SQL simples com SELECT e WHERE.
- Compreender como as condições afetam o resultado de uma consulta.
- Identificar e aplicar corretamente as condições de igualdade e comparação numérica.

--- 

**Fim do plano de aula.**