"""Explicit, narrow correction for a previously observed coin/die ambiguity."""
BAD = 'uma moeda (ou de um dado, caso tenham em casa) e verifiquem se a frequência da face escolhida se aproxima de 50%'
GOOD = 'uma moeda equilibrada e comparem a frequência de uma face escolhida com 50%; se utilizarem um dado equilibrado de seis faces, observem o evento “obter um número par”, cuja probabilidade é 3/6 = 50% (uma face específica tem probabilidade 1/6)'


def correct_known_probability_example(response):
    """Keep raw_content intact and mark every change; not a general fact checker."""
    if BAD in response.content:
        return response.model_copy(update={
            'content':response.content.replace(BAD, GOOD),
            'warnings':[*response.warnings, 'probability_coin_die_example_corrected_v1'],
        })
    return response
