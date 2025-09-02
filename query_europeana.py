#Script per cercare opere o info su Europeana dato il nome di una persona.

import os
import re
import requests
from argparse import ArgumentParser
from dotenv import load_dotenv

BASE_URL = "https://api.europeana.eu/record/v2/search.json"

#Funzioni di supporto

def pulisci_testo(testo: str | None) -> str:
    """toglie spazi e a capo in più"""
    return re.sub(r"\s+", " ", (testo or "")).strip()

def prendi_stringa(val):
    """Europeana a volte manda liste, a volte stringhe: qui la normalizzo"""
    if isinstance(val, list) and val:
        return str(val[0]).strip()
    if isinstance(val, str):
        return val.strip()
    return ""

def scegli_descrizione(opera) -> str:
    """Cerco di restituire un testo leggibile per l'opera:
       1)Se c'è una descrizione in inglese, la uso.
       2)Se non c'è in inglese, prendo una descrizione in un'altra lingua se disponibile.
       3)Se non ci sono descrizioni in nessuna lingua, uso il titolo dell'opera come ultima risorsa.
       """
    descr = opera.get("dcDescriptionLangAware") or {}
    if isinstance(descr, dict):
        if "en" in descr and descr["en"]:
            return pulisci_testo(" ".join(descr["en"]))
        for v in descr.values():
            if v:
                return pulisci_testo(" ".join(v))
    titoli = opera.get("title") or []
    return pulisci_testo(" ".join(titoli)) if titoli else ""

def cerca_europeana(api_key: str, nome: str, quanti: int = 10):
    """fa la richiesta a Europeana filtrando per 'who' cioè persone"""
    params = {
        "wskey": api_key,
        "query": nome,
        "qf": f'who:"{nome}"',
        "rows": quanti,
        "profile": "standard",
    }
    r = requests.get(BASE_URL, params=params, timeout=20)
    r.raise_for_status()
    dati = r.json() or {}
    return dati.get("items", []) or []



def main():
    #Carico la chiave dal .env
    load_dotenv()
    chiave = os.getenv("EUROPEANA_API_KEY")
    if not chiave:
        raise RuntimeError("Metti EUROPEANA_API_KEY nel file .env")

    #Prendo il nome dalla riga di comando, di default Caravaggio
    parser = ArgumentParser(description="Cerca su Europeana per persona (who).")
    parser.add_argument("nome", nargs="*", default=["caravaggio"], help="es. 'Artemisia Gentileschi'")
    parser.add_argument("--rows", type=int, default=10, help="quanti risultati vuoi (default 10)")
    args = parser.parse_args()
    nome = " ".join(args.nome)

    #Chiamata all'API
    risultati = cerca_europeana(chiave, nome, quanti=args.rows)
    if not risultati:
        print(f"Nessun risultato per: {nome}")
        return

    #Stampo i primi 5
    print(f"Risultati per: {nome}\n")
    for i, opera in enumerate(risultati[:5], start=1):
        titolo = " / ".join(opera.get("title", [])[:2]) if isinstance(opera.get("title", []), list) else ""
        anno   = " / ".join(opera.get("year", [])[:2])  if isinstance(opera.get("year", []), list)  else ""
        descr  = scegli_descrizione(opera)
        link   = prendi_stringa(opera.get("edmIsShownAt")) or prendi_stringa(opera.get("guid"))

        print(f"{i}. Titolo: {titolo or '(s.n.)'}")
        if anno:
            print(f"   Anno: {anno}")
        if descr:
            print(f"   Descrizione: {descr[:300]}{'…' if len(descr) > 300 else ''}")
        if link:
            print(f"   URL: {link}")
        print()

if __name__ == "__main__":
    main()
