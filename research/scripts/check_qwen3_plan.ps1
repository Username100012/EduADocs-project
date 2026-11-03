# Preflight only. The request file is built with the canonical Python prompt builder.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$directory = Join-Path $root 'artifacts/qwen3-preflight'
$requestPath = Join-Path $directory 'request.json'
$body = Get-Content $requestPath -Raw -Encoding UTF8
$request = $body | ConvertFrom-Json
$base = 'http://localhost:11434'
$version = Invoke-RestMethod "$base/api/version"
$tags = Invoke-RestMethod "$base/api/tags"
$entry = $tags.models | Where-Object { $_.name -eq $request.model } | Select-Object -First 1
if (-not $entry) { throw 'Model not installed.' }
$show = Invoke-RestMethod "$base/api/show" -Method Post -ContentType 'application/json' -Body (@{model=$request.model} | ConvertTo-Json)
$before = Invoke-RestMethod "$base/api/ps"
$watch = [Diagnostics.Stopwatch]::StartNew()
$response = Invoke-RestMethod "$base/api/generate" -Method Post -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($body)) -TimeoutSec 600
$watch.Stop()
$loaded = Invoke-RestMethod "$base/api/ps"
$gpu = & "$env:WINDIR\System32\nvidia-smi.exe" --query-gpu=name,memory.total,memory.used,memory.free --format=csv,noheader,nounits
$report = [pscustomobject]@{
    experimental_data=$false; checked_at=(Get-Date).ToUniversalTime().ToString('o')
    purpose='One complete Portuguese lesson-plan preflight, not an experimental sample'
    ollama_version=$version.version; model=$request.model; digest=$entry.digest
    details=$show.details; capabilities=$show.capabilities; request=$request
    wall_ms=$watch.Elapsed.TotalMilliseconds; raw_response=$response
    output_tokens_per_second=$(if ($response.eval_duration -gt 0) { $response.eval_count * 1e9 / $response.eval_duration } else { $null })
    models_before=$before.models; models_after=$loaded.models
    gpu_memory_snapshot_after=$gpu
    ollama_process_memory_after=@(Get-Process | Where-Object { $_.ProcessName -like '*ollama*' } | Select-Object ProcessName,WorkingSet64,PrivateMemorySize64)
    memory_note='Post-call snapshots, not peak usage; RAM process counters include mapped/shared memory.'
}
$report | ConvertTo-Json -Depth 14 | Set-Content (Join-Path $directory 'report.json') -Encoding UTF8
$response.response | Set-Content (Join-Path $directory 'plano_de_aula.md') -Encoding UTF8
[pscustomobject]@{model=$entry.name; digest=$entry.digest; done_reason=$response.done_reason; tokens=$response.eval_count; seconds=$watch.Elapsed.TotalSeconds; tokens_per_second=$report.output_tokens_per_second} | ConvertTo-Json
