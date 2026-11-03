# Compatibilidade Google antes da coleta

Em 15/10/2026, o adaptador foi ajustado para enviar, no modelo `gemini-3.8-flash`,
somente limite de saída, nível de raciocínio baixo e MIME de texto definidos no piloto.
Temperatura não é enviada nesse caminho. Outros modelos mantêm o comportamento anterior.

O adaptador agora registra versão retornada, versão do SDK, motivo de término, tokens
de entrada, saída, raciocínio, cache e total quando fornecidos. Valores não fornecidos
permanecem nulos. O cliente é fechado após a chamada. Nenhuma credencial é persistida.

O SDK 1.50.1 rejeitou `thinking_level` localmente. A configuração foi aceita com 1.56.0,
agora fixada em requirements.txt. Também foram ajustadas google-auth e distro, exigidas
por essa versão. O SDK foi instalado em diretório temporário no Linux; o ambiente
Windows não foi atualizado por esta operação.

Houve uma tentativa com falha de conexão no ambiente restrito e uma execução autorizada
fora da restrição. A chamada bem-sucedida retornou `COMPATIBILIDADE_OK`, término `STOP`,
13 tokens de entrada e 7 tokens de saída. Raciocínio e cache não foram informados.
O relatório é `artifacts/google_pilot_compatibility.json`. O script guarda a última
verificação; não é o log experimental append-only. Nenhuma tarefa curricular foi gerada.

Para repetir a validação local:

```powershell
python scripts/check_google_pilot.py
```

Para executar uma chamada técnica (consome API):

```powershell
python scripts/check_google_pilot.py --live
```

A credencial é lida do ambiente ou das entradas GOOGLE_API_KEY/GEMINI_API_KEY no .env,
sem imprimir valores. O script informa erros por tipo/código sem expor mensagens brutas.

A compatibilidade demonstra acesso e aceitação dos parâmetros; não valida o conteúdo
de planos completos, tamanho suficiente para todas as tarefas, custo final ou qualidade
da julgadora. O identificador retornado permaneceu `gemini-3.8-flash`, sem snapshot datado.
