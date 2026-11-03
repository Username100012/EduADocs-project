# Orçamento Gemini — estudo principal

Somente geração Gemini. Julgamentos OpenAI têm saldo separado. Nenhuma geração de coleta foi executada.

36 prompts únicos contados pelo provedor, reutilizados nas três repetições; 108 chamadas planejadas.

| Condição | Chamadas | Tokens de entrada | Entrada mínima–máxima/chamada | Teto de saída | Custo USD no teto |
|---|---:|---:|---:|---:|---:|
| C0 | 36 | 831 | 19–27 | 147456 | 0.55358325 |
| C1 | 36 | 4944 | 123–155 | 147456 | 0.556668 |
| C2 | 36 | 6888 | 177–209 | 147456 | 0.558126 |

Entrada total: 12663 tokens. Saída máxima total: 442368 tokens, incluindo raciocínio.

Preços Standard: US$ 0,75 por milhão de tokens de entrada e US$ 3,75 por milhão de tokens de saída, incluindo raciocínio, até 31/12/2026. Sem desconto de cache, Batch ou Flex.

PTAX venda de referência em 23/10/2026: R$ 5,0377/US$. Para planejamento, usa-se R$ 6,00/US$ e reserva adicional de 25%, escolhas conservadoras dos autores. A reserva não autoriza novas chamadas ou retries.

| Cenário | Custo em reais |
|---|---:|
| Todas as saídas no limite de 4096, câmbio de planejamento | R$ 10.02 |
| Mesmo teto + reserva de 25% | R$ 12.52 |
| Preços duplicados + mesmo teto e reserva | R$ 25.03 |

Saldo informado: R$ 30.00. Margem após estimativa conservadora: R$ 17.48. Decisão: Keep 12 tasks, three conditions and three repetitions per generator; no reduction required.

O usuário aceita ultrapassar R$ 30: esse valor é uma referência, não um limite obrigatório. O desenho completo foi mantido.

Não é garantia de gasto: diferenças de conversão, tributos, alterações de preços ou uso por outras aplicações podem consumir a margem. O cálculo não altera a configuração nem congela o protocolo.

[Preços oficiais](https://ai.google.dev/gemini-api/docs/pricing#gemini-3.8-flash) · [PTAX oficial](https://ptax.bcb.gov.br/ptax_internet/consultarUltimaCotacaoDolar.do) · [Teto incluindo raciocínio](https://ai.google.dev/gemini-api/docs/generate-content/thinking)
