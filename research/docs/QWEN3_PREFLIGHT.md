# Qwen3 4B — instalação e sondagem de plano completo

Modelo solicitado: `qwen3:4b-q4_K_M`, quantização Q4_K_M. O candidato foi escolhido
por tamanho compatível com a RTX 2060 de 6 GB, família distinta de Gemini e GPT e
suporte multilíngue declarado. Isso não demonstra superioridade pedagógica.

A instalação preserva os modelos existentes. Metadados efetivamente baixados e digest
completo serão registrados pelo teste em `artifacts/qwen3-preflight/report.json`.

## Reproduzir a geração

O arquivo `artifacts/qwen3-preflight/request.json` contém o prompt C2 canônico da tarefa
de busca linear do piloto. Foi construído pelo módulo Python existente, sem instruções
extras de qualidade. Os parâmetros desta sondagem são temperatura 0,7, seed 42,
num_ctx 8192, num_predict 4096 e think=false. O formato de saída não é forçado.

Depois de instalar o modelo, executar no PowerShell:

```powershell
.\scripts\check_qwen3_plan.ps1
```

O script salva o texto em `artifacts/qwen3-preflight/plano_de_aula.md` e os dados
da geração em `report.json`. Os arquivos são de sondagem, não de coleta experimental;
uma repetição do script substitui o relatório corrente. Os dados incluem tempo de
carregamento, contagens de tokens, término, memória após a chamada e versão do Ollama.
Não representam pico de memória nem média de desempenho.

O teste verifica produção de um texto completo em português sob um único prompt.
É necessário inspecionar o texto: término `stop` não comprova completude pedagógica,
fidelidade aos sete requisitos ou ausência de erros. Não extrapolar uma observação para
todos os temas, para C0/C1 ou para o desempenho em inglês.

Nenhuma configuração do piloto é alterada automaticamente por esta sondagem. A inclusão
do modelo requer registrar seu digest e definir os parâmetros para as três condições.

## Resultado observado em 15/10/2026

- Instalação concluída no Ollama 0.17.1, preservando os demais modelos.
- Digest instalado: `2bfd38a7daaf4b1037efe517ccb73d1a3bbd4822cf89f1a82be1569050a114e0`.
- Metadados locais: Qwen3, 4,0B, Q4_K_M.
- Término: `stop`, sem truncamento pelo limite de saída.
- Entrada: 236 tokens; saída: 999 tokens.
- Tempo total observado: 22,59 segundos, incluindo cerca de 4,93 segundos de carregamento.
- Taxa de decodificação: 58,28 tokens/s; não inclui toda a latência.
- `/api/ps`: 4.306.474.112 bytes (aproximadamente 4,01 GiB), com size e size_vram iguais,
  contexto 8192. Indício de residência do modelo na GPU nesta chamada.
- Snapshot da placa inteira após a chamada: 4291 MiB usados, 1676 MiB livres.

Inspeção do texto, sem atribuição de nota experimental: resposta predominantemente em
português, com plano dividido em seções e encerramento explícito. Não houve saída de
raciocínio. A duração declarada é 50 minutos, mas os intervalos do cronograma terminam
em 01:00, totalizando 60 minutos. Há mistura inadequada de inglês (“Formação Introductory”
e “Quadro de whiteboard”) e erros de redação. Os requisitos de algoritmo e testes são
mencionados, o que não comprova qualidade das atividades.

Conclusão limitada: instalação e execução tecnicamente viáveis, com resposta sem corte.
Não declarar aprovação de qualidade ou aderência integral. Preservar a resposta original
e registrar os problemas como motivação para avaliação de duração e adequação linguística.
Não modificar prompts após este exemplo e depois reutilizá-lo como evidência independente.
