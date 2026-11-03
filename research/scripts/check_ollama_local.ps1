# Local feasibility probe. Does not run the experimental pilot.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$base = 'http://localhost:11434'
$model = 'llama3:latest'
$version = Invoke-RestMethod "$base/api/version"
$tags = Invoke-RestMethod "$base/api/tags"
$entry = $tags.models | Where-Object { $_.name -eq $model } | Select-Object -First 1
if (-not $entry) { throw 'Required installed model was not found.' }
$show = Invoke-RestMethod "$base/api/show" -Method Post -ContentType 'application/json' -Body (@{model=$model} | ConvertTo-Json)
$config = Get-Content (Join-Path $root 'experiments/pilot_config.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$p = $config.tasks[0].payload
$prompt = "Elabore um plano de aula sobre $($p.topic) para estudantes do nível $($p.grade_level), com duração de $($p.duration_minutes) minutos. O objetivo de aprendizagem é $($p.learning_objectives). Utilize $($p.methodology) como metodologia, considerando $($p.materials) como materiais e recursos disponíveis e $($p.assessment_strategy) como estratégia de avaliação."
$options = @{temperature=0.7; seed=42; num_ctx=4096; num_predict=512}
$samples = @()
$responses = @()
foreach ($phase in @('initial_load','warm')) {
    $body = @{model=$model; prompt=$prompt; stream=$false; keep_alive='10m'; options=$options} | ConvertTo-Json -Depth 5
    $watch = [Diagnostics.Stopwatch]::StartNew()
    $r = Invoke-RestMethod "$base/api/generate" -Method Post -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($body)) -TimeoutSec 300
    $watch.Stop()
    $loaded = Invoke-RestMethod "$base/api/ps"
    $gpu = & "$env:WINDIR\System32\nvidia-smi.exe" --query-gpu=name,memory.total,memory.used,memory.free --format=csv,noheader,nounits
    $processes = @(Get-Process | Where-Object { $_.ProcessName -like '*ollama*' } | Select-Object ProcessName,WorkingSet64,PrivateMemorySize64)
    $samples += [pscustomobject]@{
        phase=$phase; wall_ms=$watch.Elapsed.TotalMilliseconds
        total_duration_ns=$r.total_duration; load_duration_ns=$r.load_duration
        prompt_eval_count=$r.prompt_eval_count; prompt_eval_duration_ns=$r.prompt_eval_duration
        eval_count=$r.eval_count; eval_duration_ns=$r.eval_duration
        output_tokens_per_second=$(if ($r.eval_duration -gt 0) { $r.eval_count * 1e9 / $r.eval_duration } else { $null })
        done=$r.done; done_reason=$r.done_reason
        loaded_models=$loaded.models; gpu_snapshot_after_call=$gpu
        ollama_process_memory_after_call=$processes
    }
    $responses += [pscustomobject]@{phase=$phase; text=$r.response}
}
$report = [pscustomobject]@{
    experimental_data=$false; purpose='Local feasibility only; two observations, not a benchmark'
    checked_at=(Get-Date).ToUniversalTime().ToString('o'); ollama_version=$version.version
    model=$model; model_digest=$entry.digest; details=$show.details; options=$options
    prompt=$prompt; measurements=$samples; responses=$responses
    memory_measurement='Snapshots after each call; not peak memory. Process RAM includes shared/mapped pages and must not be summed as unique usage.'
}
$directory = Join-Path $root 'artifacts'
New-Item -ItemType Directory -Force $directory | Out-Null
$path = Join-Path $directory 'ollama_local_feasibility.json'
$report | ConvertTo-Json -Depth 12 | Set-Content $path -Encoding UTF8
$samples | Select-Object phase,wall_ms,eval_count,output_tokens_per_second,done_reason | ConvertTo-Json
