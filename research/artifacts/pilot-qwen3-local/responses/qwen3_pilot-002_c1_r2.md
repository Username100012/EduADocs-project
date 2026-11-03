**Plano de Aula: Consultas SQL com SELECT e WHERE**

---

**Disciplina:** Informática / Banco de Dados  
**Nível:** Graduação em Ciência da Computação  
**Formação:** Introdutória  
**Duração:** 50 minutos  
**Objetivo de Aprendizagem:**  
Escrever consultas SQL com `SELECT` e `WHERE` em uma tabela de produtos e determinar as linhas retornadas por condições de igualdade e comparação numérica.

---

### **1. Introdução (5 minutos)**

**Objetivo:** Estabelecer o contexto e a relevância das consultas SQL para extração de dados em bancos de dados.

- Apresentar a importância de manipular dados em tabelas de produtos.
- Introduzir os conceitos de `SELECT` e `WHERE` como ferramentas essenciais para filtrar resultados.
- Mostrar a estrutura básica de uma consulta SQL:
  ```sql
  SELECT [campos] FROM [tabela] WHERE [condições];
  ```

---

### **2. Revisão de Conceitos (5 minutos)**

**Objetivo:** Reforçar o entendimento dos conceitos de igualdade e comparação numérica.

- **Igualdade:** `=`, `==`, `=` (em SQL, apenas `=` é válido)
- **Comparação numérica:** `>`, `<`, `>=`, `<=`, `!=`, `<>`

- Exemplo:
  ```sql
  SELECT * FROM produtos WHERE preco = 100;
  ```
  ```sql
  SELECT * FROM produtos WHERE preco > 50;
  ```

---

### **3. Apresentação dos Materiais (5 minutos)**

**Objetivo:** Familiarizar os alunos com a tabela de produtos que será utilizada durante a aula.

- **Material 1:** Quadro com a tabela de produtos (código, nome, preço)
- **Material 2:** Folha com a tabela de produtos (código, nome, preço)

**Exemplo da Tabela de Produtos:**

| Código | Nome         | Preço |
|--------|--------------|-------|
| 1      | Caneta       | 2.50  |
| 2      | Lapis        | 3.00  |
| 3      | Caderno      | 15.00 |
| 4      | Borracha     | 1.00  |
| 5      | Lapiseira    | 4.50  |

---

### **4. Atividade Colaborativa: Resolução de Problemas (25 minutos)**

**Objetivo:** Os alunos trabalham em grupos para resolver duas consultas com `SELECT` e `WHERE`, uma com igualdade e outra com comparação numérica.

**Instruções:**

1. Dividir os alunos em grupos de 3 a 4 pessoas.
2. Cada grupo recebe o quadro e a folha com a tabela de produtos.
3. Cada grupo deve resolver as duas consultas:
   - **Consulta 1 (Igualdade):** Encontre todos os produtos cujo preço é igual a 3.00.
   - **Consulta 2 (Comparação numérica):** Encontre todos os produtos cujo preço é maior que 5.00.
4. Os grupos devem escrever as consultas SQL e mostrar os resultados esperados.

**Exemplo de Consultas:**

- Consulta 1 (Igualdade):
  ```sql
  SELECT * FROM produtos WHERE preco = 3.00;
  ```
  **Resultado esperado:**
  ```
  Código | Nome     | Preço
  2      | Lapis    | 3.00
  ```

- Consulta 2 (Comparação numérica):
  ```sql
  SELECT * FROM produtos WHERE preco > 5.00;
  ```
  **Resultado esperado:**
  ```
  Código | Nome     | Preço
  3      | Caderno  | 15.00
  ```

---

### **5. Apresentação dos Resultados (5 minutos)**

**Objetivo:** Os grupos apresentam suas consultas e resultados, com a participação de todos os alunos.

- Cada grupo apresenta a consulta SQL e o resultado esperado.
- O professor corrigi e complementa as respostas, destacando a importância da sintaxe correta e da interpretação das condições.

---

### **6. Conclusão e Avaliação (5 minutos)**

**Objetivo:** Reforçar o conteúdo e avaliar o entendimento dos alunos.

- O professor ressalta a importância de usar `WHERE` para filtrar dados.
- A avaliação será feita com base na capacidade dos alunos de escrever consultas corretas com `SELECT` e `WHERE`.
- O professor pode realizar uma pequena avaliação escrita (em folha de rosto) para verificar o entendimento de alguns conceitos.

---

### **7. Recursos Utilizados**

- Quadro com tabela de produtos
- Folha com tabela de produtos
- Lápis, caneta, papel
- Tela com ambiente SQL (opcional)

---

### **8. Extensão (opcional, 5 minutos)**

- Introduzir a possibilidade de usar múltiplas condições com `AND` e `OR`.
- Exemplo:
  ```sql
  SELECT * FROM produtos WHERE preco = 3.00 OR preco = 4.50;
  ```

---

**Aulas Recomendadas:**  
- Revisão de SQL (introdutório)
- Consultas com `WHERE` e `ORDER BY`
- Operadores lógicos e comparação de strings

--- 

**Nota:** Este plano de aula pode ser adaptado com base no nível de domínio dos alunos.