**Plano de Aula: Consultas SQL com SELECT e WHERE em uma tabela**

---

### **1. Dados Gerais**

- **Tópico:** Consultas SQL com SELECT e WHERE em uma tabela
- **Nível educacional:** Graduação em Ciência da Computação – formação introdutória
- **Duração:** 50 minutos
- **Metodologia:** Resolução colaborativa de problemas
- **Materiais e recursos:** Quadro, folha com tabela de produtos (contendo código, nome e preço), projetor (opcional), laptop com ambiente de SQL (ex: MySQL Workbench ou SQL Server Management Studio)
- **Estratégia de avaliação:** Escrever duas consultas com SELECT e WHERE, uma com igualdade e outra com comparação numérica, e indicar os resultados esperados

---

### **2. Objetivos de Aprendizagem**

- Entender a estrutura básica de uma consulta SQL com SELECT e WHERE
- Utilizar operadores de comparação (igualdade e numérica) para filtrar registros
- Identificar e escrever consultas que retornam apenas as linhas que atendem a uma condição específica
- Desenvolver habilidades práticas de consulta em uma tabela de produtos

---

### **3. Conteúdo Programático**

- Introdução à linguagem SQL
- Estrutura de uma consulta SELECT
- Operadores de comparação: =, >, <, >=, <=, !=
- Aplicação em uma tabela de produtos
- Resolução colaborativa de exercícios práticos

---

### **4. Cronograma da Aula**

| Tempo | Atividade |
|-------|-----------|
| 0–5 min | Apresentação do tema e objetivo da aula |
| 5–10 min | Introdução à linguagem SQL e estrutura da consulta SELECT |
| 10–20 min | Explicação dos operadores de comparação e exemplos |
| 20–35 min | Resolução colaborativa de duas consultas práticas |
| 35–45 min | Discussão dos resultados esperados e resolução de dúvidas |
| 45–50 min | Avaliação individual: escrita de duas consultas com SELECT e WHERE |
| 50 min | Encerramento e revisão dos pontos principais |

---

### **5. Desenvolvimento da Aula**

#### **5.1. Introdução (0–5 min)**

- Apresentar o tema e o objetivo da aula.
- Explicar que a aula tem como objetivo ensinar os alunos a escrever consultas SQL básicas com SELECT e WHERE, com foco em condições de igualdade e comparação numérica.
- Introduzir a tabela de produtos (cod, nome, preço) como exemplo prático.

#### **5.2. Estrutura da Consulta SQL (5–10 min)**

- Explicar a estrutura básica de uma consulta SQL:
  ```
  SELECT [colunas] FROM [tabela] WHERE [condição];
  ```
- Apresentar os operadores de comparação: =, >, <, >=, <=, !=.

#### **5.3. Operadores de Comparações (10–20 min)**

- Explicar os operadores de comparação com exemplos:
  - **Igualdade:** `WHERE cod = 101`
  - **Comparação numérica:** `WHERE preco > 50`
- Mostrar como aplicar esses operadores em uma tabela de produtos.
- Fazer uma demonstração com a tabela fornecida (cod, nome, preço).

#### **5.4. Resolução Colaborativa (20–35 min)**

- Dividir a turma em pequenos grupos.
- Distribuir uma tabela de produtos (exemplo):
  | cod | nome         | preco |
  |-----|--------------|-------|
  | 101 | Notebook     | 2500  |
  | 102 | Celular      | 1500  |
  | 103 | Tablet       | 1200  |
  | 104 | Monitor      | 800   |
  | 105 | Mouse        | 100   |

- Cada grupo deve escrever duas consultas:
  1. Uma com **igualdade** (ex: `SELECT * FROM produtos WHERE cod = 101`)
  2. Uma com **comparação numérica** (ex: `SELECT * FROM produtos WHERE preco > 1000`)

- Cada grupo apresenta suas consultas e os resultados esperados.

#### **5.5. Discussão e Resolução de Dúvidas (35–45 min)**

- Discutir as consultas apresentadas pelos grupos.
- Revisar os resultados esperados com base na tabela de produtos.
- Corrigir erros e esclarecer dúvidas.

#### **5.6. Avaliação Individual (45–50 min)**

- Cada aluno deve escrever **duas consultas** com SELECT e WHERE, uma com igualdade e outra com comparação numérica, com base na tabela fornecida.
- Indicar os resultados esperados para cada consulta.
- Recolher as respostas e revisar posteriormente.

---

### **6. Avaliação**

- **Critérios de avaliação:**
  - Correção da consulta com SELECT e WHERE
  - Uso correto dos operadores de igualdade e comparação
  - Indicação correta dos resultados esperados
  - Participação ativa na resolução colaborativa

---

### **7. Recursos Complementares**

- Folha com a tabela de produtos
- Póster com a estrutura da consulta SQL
- Ambiente de SQL para execução (opcional)

---

### **8. Encerramento (50 min)**

- Revisar os principais pontos da aula.
- Destacar a importância de usar consultas SQL para filtrar dados.
- Incentivar a prática e o estudo de exemplos mais complexos.

---

### **9. Refletir e Estender**

- Propor que os alunos criem uma tabela própria e façam consultas com base nela.
- Sugere a leitura de exemplos de consultas mais avançadas (como JOINs, filtros múltiplos, etc.).

--- 

**Fim do plano de aula.**