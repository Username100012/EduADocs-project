# Auditoria local do fluxo da julgadora — 15/10/2026

Foi implementado `src/experiment/judge_audit.py` para integrar os componentes existentes
com respostas simuladas. A rotina não importa clientes de provedores nem executa APIs.

## Constatações e correções

O registro anterior não ligava cada tentativa ao manifesto e não verificava se o
resultado validado correspondia ao texto bruto. O envelope versionado
`AuditedJudgeAttempt` acrescenta hash do manifesto e número da tentativa sem modificar
o esquema legado. Antes da gravação, a rotina reconstrói o prompt e refaz o parsing da
resposta bruta, comparando os resultados com o registro recebido.

A rotina verifica o selo canônico do manifesto, os seis arquivos congelados e a
igualdade entre a configuração selecionada e a configuração do manifesto. Sob bloqueio,
verifica duplicidade, ordem das tentativas e preservação dos dados da primeira tentativa.
Permite a segunda tentativa apenas após erro elegível. Os limites são três repetições
e duas tentativas por repetição. Linhas incompletas ou inválidas interrompem a gravação.

O log da auditoria usa um envelope próprio e deve ficar em arquivo separado do JSONL
legado de `JudgeRecordLogger`. Os testes usam diretórios temporários; não foram criados
resultados experimentais em `data/`.

## Verificação reproduzível

```bash
python3 -m unittest tests.test_judge_offline_audit tests.test_llm_judge_manifest -v
```

Os casos cobrem sucesso, falha seguida de sucesso, duplicidade concorrente, adulteração
da resposta bruta e do manifesto, salto de tentativa, repetição excedente, alteração de
entrada durante nova tentativa e preservação de log incompleto.

## Limites

O cegamento estrutural significa que condição, identificador da geração e nome do
modelo não são inseridos pelo sistema no prompt. Não garante que o próprio texto
candidato não contenha pistas de origem nem que o julgador seja imparcial.

O manifesto existente permanece intacto. Seus seis hashes não cobrem este novo código
de integração: antes da coleta real será necessário registrar a revisão do código ou
criar uma nova versão de manifesto que também identifique a implementação executada.
O selo SHA-256 detecta divergência em relação ao selo preservado; não é assinatura
digital nem proteção contra edição simultânea do manifesto e do próprio selo.

Os testes demonstram integridade do fluxo local. Não demonstram confiabilidade semântica
do julgador, disponibilidade do snapshot, compatibilidade real dos parâmetros com a API
ou validade da rubrica. A próxima etapa é preparar os casos metamórficos congelados e
seu critério de análise, antes de executar um piloto com o modelo.
