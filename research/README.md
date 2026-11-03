# EduADocs — pacote de reprodutibilidade experimental

Este diretório preserva a versão experimental original, separada da aplicação atual em `../src`. O estudo é computacional, sem participantes humanos. As correções posteriores da interface e do DOCX não foram retroaplicadas aos resultados.

## O que foi realizado

- 12 tarefas introdutórias de Computação × 3 condições × 2 geradores × 3 repetições: **216 tentativas**, 215 textos e um timeout.
- Geradores: **gemini-3.8-flash** e **qwen3:4b-q4_K_M**, via Ollama. Configuração exata, versões, parâmetros e hashes em `experiments/main_config.json`.
- C0 contém tipo de material e tópico; C1/C2 representam os mesmos sete requisitos em texto livre ou estruturado. C1/C2 é o contraste principal.
- Julgadora **gpt-6.1-sol**, contrato v2, 3 avaliações por texto: **645 tentativas**, 624 válidas, 15 falhas de citação e seis erros de crédito. Os erros não foram repetidos nem receberam zero.
- Frequências nominais mantidas separadas das notas ordinais secundárias. Estas usam 196 trincas completas, com agregação por tarefa.

## Reproduzir a análise sem pagar APIs

Python 3.13 e dependências da versão experimental em `requirements.txt`. Instale em um ambiente separado do aplicativo de produção:

```powershell
# Na raiz do repositório, Windows / PowerShell
py -3.13 -m venv research/.venv
research/.venv/Scripts/python.exe -m pip install -r research/requirements.txt
research/.venv/Scripts/python.exe research/reproduce.py --tests
```

Em Linux/macOS, use `python3.13 -m venv research/.venv` e o executável `research/.venv/bin/python` nos dois comandos seguintes.

A instalação das dependências requer internet; **a reprodução dos resultados não requer chaves**. O executor copia os arquivos para um diretório temporário, bloqueia conexões de rede, verifica o protocolo congelado, recalcula os indicadores e as tabelas da julgadora e compara os JSONs com os publicados. Os logs originais não são sobrescritos. As saídas ficam em `research/reproduced/`; para repetir, escolha uma pasta nova com `--output CAMINHO`.

`verification.json` registra quais resultados foram comparados, os hashes das fontes e se a rede foi bloqueada. A execução com `--tests` roda também a suíte experimental original. Os JSONs de métricas e julgamentos são comparados por conteúdo. O hash de proveniência do arquivo derivado de observações pode diferir por quebras de linha LF/CRLF: cada hash é verificado contra seus próprios bytes e a diferença é documentada, sem editar o resultado ou tolerar diferenças nas métricas. Um resultado igual não prova validade pedagógica nem correção da julgadora.

## Arquivos para conferir a metodologia

| Conteúdo | Local |
|---|---|
| Protocolo e parâmetros congelados | `docs/MAIN_STUDY_PROTOCOL.md`, `experiments/main_config.json` |
| Tarefas e prompts efetivamente enviados | Cabeçalho de `artifacts/main-study-v1/generations.jsonl` |
| Respostas, erros, latência e tokens reportados | `artifacts/main-study-v1/generations.jsonl` |
| Rubrica, prompt e parser v2 | `docs/REQUIREMENT_JUDGE_CONTRACT_V2.md`, `src/experiment/judge_contract_v2.py` |
| Esquema da julgadora | `experiments/judge_response.v2.schema.json` |
| Fila, rótulos separados e julgamentos brutos | `artifacts/main-judgments-v1/{queue,mapping,judgments.v2}.jsonl` |
| Indicadores automáticos e resultados | `artifacts/main-study-v1/AUTOMATIC_METRICS.md`, `artifacts/main-judgments-v1/RESULTS.md` |
| Auditoria exploratória posterior | `artifacts/main-judgments-v1/case-audit/` |
| Sensibilidade pós-coleta com pares completos | `artifacts/main-judgments-v1/paired-complete-sensitivity/` |

Históricos de piloto, diagnósticos e simulações também estão incluídos para rastreabilidade. **Não somar esses registros à coleta principal.** As simulações não são chamadas reais. Manifestações e rubricas v1 não substituem o contrato principal v2.

## Scripts usados

- Geração: `scripts/run_pilot.py` e `src/experiment/pilot_runner.py`. Apesar do nome, o executor também realizou a coleta principal com `main_config.json`.
- Métricas locais: `scripts/observe_saved_requirements.py`, `scripts/summarize_main_observations.py`.
- Julgamentos: `scripts/prepare_requirement_judgments.py`, `scripts/run_requirement_judgments.py`.
- Tabelas: `scripts/report_requirement_results.py`.
- Análises posteriores: `scripts/audit_saved_qwen_cases.py`, `scripts/analyze_paired_complete_cases.py`.

## Nova coleta não é reprodução das tabelas

Os executores históricos permitem chamadas reais somente com `--live`, chaves privadas fornecidas localmente e ambiente compatível com o protocolo. **Não use `--live` para reproduzir os números publicados.** Uma nova coleta pode gerar respostas diferentes e consumir créditos; deve usar diretórios separados. O protocolo não autoriza substituir versões de modelos nem repetir automaticamente IDs com falha. Modelos hospedados podem mudar ou deixar de estar disponíveis.

## Segurança e integridade

Não são incluídos `.env`, secrets do Streamlit, ambiente virtual, configurações de contas ou arquivos de chaves. A revisão incluiu padrões de tokens, campos sensíveis nos JSONs e comparação privada com as chaves locais, sem publicar seus valores. A verificação pode ser repetida sem acesso às chaves:

```powershell
python research/tools/check_publication.py
```

`MANIFEST_SHA256.json` registra os hashes dos 412 arquivos originais preservados. `PUBLICATION_AUDIT.json` documenta a revisão, sem valores de credenciais. Os arquivos de orientação e scripts novos ficam fora desse manifesto histórico. A regra `research/** -text` em `.gitattributes` evita alterações de bytes por conversão automática de finais de linha. Não há garantia de que uma busca por padrões detecte todo tipo de dado sensível.

O código é distribuído sob a licença MIT fornecida neste diretório. A licença do código não substitui os termos dos provedores para os textos gerados; não se faz declaração de exclusividade sobre essas respostas.
