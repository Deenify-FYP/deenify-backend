from fastapi import Request,HTTPException
from transformers import RobertaForTokenClassification, AutoTokenizer

label2diacritic = {0: 'ّ', # SHADDA
                   1: 'َ', # FATHA
                   2: 'ِ', # KASRA
                   3: 'ُ', # DAMMA
                   4: 'ْ'} # SUKKUN


def arabic_diacritize(request:Request,text:str):
    model:RobertaForTokenClassification = request.app.state.diacritizer_model
    tokenizer:AutoTokenizer = request.app.state.diacritizer_tokenizer

    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Diacritizer Model not loaded yet")

    tokens = tokenizer(text, return_tensors="pt")
    preds = (model(**tokens).logits.sigmoid() > 0.5)[0][1:-1]
    new_text = []
    for p, c in zip(preds, text):
        new_text.append(c)
        for i in range(1, 5):
            if p[i]:
                new_text.append(label2diacritic[i])
        if p[0]:
            new_text.append(label2diacritic[0])
        
    new_text = "".join(new_text)
    return new_text

