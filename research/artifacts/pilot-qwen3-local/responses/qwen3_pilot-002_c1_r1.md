**Plano de Aula: Consultas SQL com SELECT e WHERE**

---

**Disciplina:** Informática / Banco de Dados  
**Nível:** Graduação em Ciência da Computação  
**Formação:** Introductory (Introdutória)  
**Duração da aula:** 50 minutos  
**Objetivo de Aprendizagem:**  
- Escrever consultas SQL com `SELECT` e `WHERE` em uma tabela de produtos.  
- Determinar as linhas retornadas por condições de **igualdade** e **comparação numérica**.  
- Desenvolver habilidades de **resolução colaborativa de problemas**.

---

### **1. Introdução (5 minutos)**

- **Objetivo:** Introduzir o conceito de consultas SQL, destacando a importância do `SELECT` e do `WHERE` para filtrar dados.
- **Conteúdo:**
  - Breve explicação sobre o que é um banco de dados e como as consultas SQL ajudam a extrair informações.
  - Introdução ao conceito de tabelas (como código, nome, preço).
  - Objetivo da aula: usar `SELECT` e `WHERE` para filtrar dados de uma tabela de produtos.

---

### **2. Materiais e Recursos (2 minutos)**

- **Quadro:** Com a tabela de produtos (código, nome, preço).
- **Folha com tabela de produtos** (com dados fictícios, como:  
  | Código | Nome           | Preço |
  |--------|----------------|-------|
  | 1      | Notebook       | 2500  |
  | 2      | Mouse          | 150   |
  | 3      | Teclado        | 300   |
  | 4      | Monitor        | 1500  |
  | 5      | Pen Drive      | 80    |
  | 6      | Câmera         | 2000  |
  | 7      | Smartphone     | 1500  |

- **Ferramentas:**  
  - Folhas de papel para anotações.  
  - Pincel para escrever no quadro.  
  - Cartões com instruções para as tarefas.

---

### **3. Atividade de Introdução (5 minutos)**

- **Tarefa:**  
  - Peça aos alunos que observem a tabela de produtos no quadro e respondam:  
    - Qual é o preço mais caro?  
    - Qual é o nome do produto com código 3?  
    - Qual é o produto com preço menor que 1000?  
  - Este é um momento para estimular a reflexão e a observação.

---

### **4. Explicação da Lógica (10 minutos)**

- **Conteúdo:**
  - Explicar o comando `SELECT` e `WHERE` com exemplos.
  - Exemplo 1: `SELECT * FROM produtos WHERE codigo = 3;`  
    - **Condição de igualdade**.
  - Exemplo 2: `SELECT * FROM produtos WHERE preco < 1000;`  
    - **Comparação numérica**.
  - Explicar como a sintaxe funciona e o que cada parte representa.

---

### **5. Atividade Colaborativa (20 minutos)**

- **Tarefa 1:**  
  - **Condição de igualdade:**  
    - Escrever uma consulta SQL que retorne o produto com código **5**.  
    - **Resposta esperada:** Câmera, preço 2000.

- **Tarefa 2:**  
  - **Comparação numérica:**  
    - Escrever uma consulta SQL que retorne os produtos com preço **menor que 1000**.  
    - **Resposta esperada:** Mouse (150), Teclado (300), Pen Drive (80).

- **Metodologia:**  
  - Dividir a turma em grupos de 2 a 3 alunos.  
  - Cada grupo recebe uma tarefa.  
  - Os grupos devem escrever a consulta SQL e identificar os dados retornados.  
  - Após a escrita, os grupos apresentam suas respostas à turma.  
  - O professor corrige e explica eventuais dúvidas.

---

### **6. Avaliação (5 minutos)**

- **Estratégia de Avaliação:**  
  - Os alunos devem escrever **duas consultas SQL** com `SELECT` e `WHERE`:  
    1. Uma com **igualdade** (ex: `WHERE codigo = 5`).  
    2. Uma com **comparação numérica** (ex: `WHERE preco < 1000`).  
  - Os alunos devem **indicar os resultados esperados** para cada consulta.  
  - **Criterios de Avaliação:**  
    - Correto uso da sintaxe SQL.  
    - Correto entendimento das condições.  
    - Identificação correta dos dados retornados.

---

### **7. Conclusão e Encerramento (3 minutos)**

- **Resumo da aula:**  
  - Revisar os conceitos de `SELECT` e `WHERE`.  
  - Destacar a importância da lógica de filtros em consultas SQL.  
  - Incentivar a prática e a aplicação em projetos futuros.

- **Pergunta para reflexão:**  
  - "Por que é importante usar a cláusula WHERE em uma consulta SQL?"

---

### **8. Recomendações para a Próxima Aula**

- Introduzir a cláusula `ORDER BY` para ordenar resultados.  
- Explorar `AND`, `OR` e `NOT` como operadores lógicos.  
- Praticar com outras tabelas (ex: clientes, fornecedores).

---

**Notas Finais:**  
Este plano de aula tem como objetivo **introduzir os conceitos básicos de SQL** de forma prática e colaborativa, com ênfase em consultas simples com `SELECT` e `WHERE`. A metodologia de resolução colaborativa ajuda a desenvolver habilidades de trabalho em grupo e pensamento crítico.