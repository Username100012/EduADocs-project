"""Estimate the Gemini-only collection cost; countTokens never generates plans."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal, ROUND_CEILING
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from experiment.pilot_runner import build_plan, _hash
from google_credentials import read_google_key

PRICES = {'checked_on':'2026-10-25','valid_through':'2026-12-31',
          'input_usd_per_million':0.75,'output_usd_per_million':3.75,
          'url':'https://ai.google.dev/gemini-api/docs/pricing#gemini-3.8-flash'}


def estimate(config, counts, *, exchange='6.00', reserve='0.25', available='30.00', price_multiplier='1'):
    jobs=[j for j in build_plan(config) if j['generator_id']=='gemini']
    limit=config['generators']['gemini']['generation_config']['max_output_tokens']
    rate=Decimal(exchange);buffer=Decimal(reserve);balance=Decimal(available);multiple=Decimal(price_multiplier)
    if rate<=0 or buffer<0 or balance<0 or multiple<=0:
        raise ValueError('invalid budget assumptions')
    groups=[]
    for condition in sorted({j['condition'] for j in jobs}):
        selected=[j for j in jobs if j['condition']==condition]
        values=[]
        for job in selected:
            key=sha256(job['prompt']['text'].encode()).hexdigest()
            n=counts.get(key)
            if type(n) is not int or n<=0:
                raise ValueError('missing or invalid measured token count')
            values.append(n)
        input_total=sum(values);output_total=len(selected)*limit
        usd=(Decimal(input_total)*Decimal(str(PRICES['input_usd_per_million']))+
             Decimal(output_total)*Decimal(str(PRICES['output_usd_per_million'])))*multiple/Decimal(1_000_000)
        groups.append({'condition':condition,'calls':len(selected),'input_tokens':input_total,
                       'input_tokens_min_per_call':min(values),'input_tokens_max_per_call':max(values),
                       'output_tokens_cap':output_total,'usd_at_output_cap':str(usd)})
    total=sum(Decimal(g['usd_at_output_cap']) for g in groups)
    base=total*rate;conservative=base*(1+buffer)
    money=lambda n:str(n.quantize(Decimal('.01'),rounding=ROUND_CEILING))
    return {'calls':len(jobs),'by_condition':groups,'input_tokens_total':sum(g['input_tokens'] for g in groups),
        'output_tokens_total_cap':sum(g['output_tokens_cap'] for g in groups),'output_tokens_per_call_cap':limit,
        'price_multiplier':str(multiple),'usd_at_output_cap':str(total),'planning_usd_brl':str(rate),
        'brl_at_output_cap':money(base),'reserve_fraction':str(buffer),'conservative_brl':money(conservative),
        'available_brl':money(balance),'remaining_brl_after_reserve':str((balance-Decimal(money(conservative))).quantize(Decimal('.01'))),
        'fits_budget':conservative<=balance}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--count-live',action='store_true',help='Count the unique inputs through the provider, without inference.')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts/gemini-main-budget-2026-10-25')
    args=parser.parse_args()
    config=json.loads((ROOT/'experiments/main_config.json').read_text(encoding='utf-8'))
    generator=config['generators']['gemini']
    if generator['model']!='gemini-3.8-flash' or generator['tools_enabled'] or generator['conversation_history'] or generator['system_instruction'] or generator['response_schema']:
        raise ValueError('budget assumptions do not cover this generator configuration')
    jobs=[j for j in build_plan(config) if j['generator_id']=='gemini']
    unique={sha256(j['prompt']['text'].encode()).hexdigest():j['prompt']['text'] for j in jobs}
    args.output.mkdir(parents=True,exist_ok=True)
    cache=args.output/'input_token_counts.json'
    if args.count_live:
        if cache.exists():
            raise ValueError('counts already saved; omit --count-live to reuse them')
        from google import genai
        from google.genai import types
        key,_=read_google_key()
        if not key:
            raise ValueError('Google credential absent')
        options=types.HttpOptions(timeout=60000,retry_options=types.HttpRetryOptions(attempts=1))
        def count(item):
            digest,text=item
            with genai.Client(api_key=key,http_options=options) as client:
                result=client.models.count_tokens(model=generator['model'],contents=text)
            if type(result.total_tokens) is not int or result.total_tokens<=0:
                raise ValueError('invalid countTokens response')
            return digest,result.total_tokens
        # Four independent counting requests at most; no generation endpoint used.
        with ThreadPoolExecutor(max_workers=4) as pool:
            measured=dict(pool.map(count,sorted(unique.items())))
        token_report={'model':generator['model'],'configuration_hash':_hash(config),'count_tokens_calls':len(unique),
                      'generate_content_calls':0,'counts':dict(sorted(measured.items()))}
        cache.write_text(json.dumps(token_report,indent=2)+'\n',encoding='utf-8')
    else:
        token_report=json.loads(cache.read_text(encoding='utf-8'))
    if token_report['model']!=generator['model'] or set(token_report['counts'])!=set(unique):
        raise ValueError('token counts do not match the current plan')
    regular=estimate(config,token_report['counts'])
    doubled=estimate(config,token_report['counts'],price_multiplier='2')
    report={'checked_on':'2026-10-25','scope':'Gemini generation only; OpenAI judging balance and local electricity excluded.',
        'configuration_hash':_hash(config),'input_counts_sha256':sha256(cache.read_bytes()).hexdigest(),
        'model':generator['model'],'pricing':PRICES,
        'budget_policy':'R$30 is a reference balance, not a strict cap: user explicitly accepts overruns. No reduction solely to meet this amount.',
        'exchange_reference':{'date':'2026-10-23','ptax_usd_brl_sell':5.0377,
            'source':'https://ptax.bcb.gov.br/ptax_internet/consultarUltimaCotacaoDolar.do',
            'planning_rate':6.0,'interpretation':'Authorial conservative conversion, not the actual Google billing exchange rate.'},
        'current_price_output_cap':regular,'double_price_stress_test':doubled,
        'decision':'Keep 12 tasks, three conditions and three repetitions per generator; no reduction required.' if regular['fits_budget'] else 'Reduce prospectively before protocol freeze; keep condition balance.',
        'limits':['Assumes a single candidate, no tools, no paid cache storage, no conversation history and no automatic retries.',
                  '4096 includes thinking and visible output; do not add the thinking budget a second time.',
                  'No cache discounts or free-tier allowances assumed. No collection calls made.',
                  'Reserve and exchange buffer are planning assumptions, not a guarantee or an invoice; other project usage can consume balance.',
                  'Recheck pricing after 2026-12-31 or any change of provider configuration.']}
    (args.output/'budget.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Orçamento Gemini — estudo principal','',
        'Somente geração Gemini. Julgamentos OpenAI têm saldo separado. Nenhuma geração de coleta foi executada.','',
        f"{len(unique)} prompts únicos contados pelo provedor, reutilizados nas três repetições; {regular['calls']} chamadas planejadas.",'',
        '| Condição | Chamadas | Tokens de entrada | Entrada mínima–máxima/chamada | Teto de saída | Custo USD no teto |',
        '|---|---:|---:|---:|---:|---:|']
    for g in regular['by_condition']:
        lines.append(f"| {g['condition'].upper()} | {g['calls']} | {g['input_tokens']} | {g['input_tokens_min_per_call']}–{g['input_tokens_max_per_call']} | {g['output_tokens_cap']} | {g['usd_at_output_cap']} |")
    lines+=['',f"Entrada total: {regular['input_tokens_total']} tokens. Saída máxima total: {regular['output_tokens_total_cap']} tokens, incluindo raciocínio.",'',
        'Preços Standard: US$ 0,75 por milhão de tokens de entrada e US$ 3,75 por milhão de tokens de saída, incluindo raciocínio, até 31/12/2026. Sem desconto de cache, Batch ou Flex.','',
        'PTAX venda de referência em 23/10/2026: R$ 5,0377/US$. Para planejamento, usa-se R$ 6,00/US$ e reserva adicional de 25%, escolhas conservadoras dos autores. A reserva não autoriza novas chamadas ou retries.','',
        '| Cenário | Custo em reais |','|---|---:|',
        f"| Todas as saídas no limite de 4096, câmbio de planejamento | R$ {regular['brl_at_output_cap']} |",
        f"| Mesmo teto + reserva de 25% | R$ {regular['conservative_brl']} |",
        f"| Preços duplicados + mesmo teto e reserva | R$ {doubled['conservative_brl']} |",'',
        f"Saldo informado: R$ {regular['available_brl']}. Margem após estimativa conservadora: R$ {regular['remaining_brl_after_reserve']}. Decisão: {report['decision']}",'',
        'O usuário aceita ultrapassar R$ 30: esse valor é uma referência, não um limite obrigatório. O desenho completo foi mantido.','',
        'Não é garantia de gasto: diferenças de conversão, tributos, alterações de preços ou uso por outras aplicações podem consumir a margem. O cálculo não altera a configuração nem congela o protocolo.','',
        '[Preços oficiais](https://ai.google.dev/gemini-api/docs/pricing#gemini-3.8-flash) · [PTAX oficial](https://ptax.bcb.gov.br/ptax_internet/consultarUltimaCotacaoDolar.do) · [Teto incluindo raciocínio](https://ai.google.dev/gemini-api/docs/generate-content/thinking)']
    (args.output/'BUDGET.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'current':regular,'stress':doubled,'decision':report['decision']},ensure_ascii=False))


if __name__=='__main__':
    try:
        main()
    except Exception as error:
        # Provider exceptions can contain request credentials; never print them.
        code=getattr(error,'code',None)
        print(json.dumps({'status':'budget_failed','error_type':type(error).__name__,
                          'code':code if isinstance(code,(str,int)) else None}))
        raise SystemExit(1)
