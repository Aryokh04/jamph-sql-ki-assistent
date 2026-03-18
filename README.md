# JAMPH-sql-ki-assistent

Dette er ment som en installasjonsmappe. Vår assistent er komponenbasert.

Bruker en AI modell og arkitektur til å skrive BigQuery spørringer. Forenkler prosessen med å skrive personlig statstikker.

## Komme i gang

Filen README_install.MD inneholder instruksjoner for å sette opp miljøet.

## Henvendelser

Enten:
Spørsmål knyttet til koden eller repositoryet kan stilles som issues her på GitHub

Eller:
Spørsmål knyttet til koden eller repositoryet kan stilles til teamalias@nav.no (som evt må opprettes av noen™ Windows-mennesker) eller som issues her på GitHub (stryk det som ikke passer).

## Endringslogg

### 2026-03-18 — Tjenestekommunikasjon koblet opp mot NAIS-miljø

Tidligere hardkodet alle tjenester mot `localhost`. Nå brukes miljøvariabler og NAIS-konfigurasjon:

- **Frontend** bruker `VITE_RAG_API_URL` (satt i `.env` / `.env.production`) i stedet for hardkodet `localhost:8004`
- **RAG API** får `OLLAMA_BASE_URL=http://jamph-ollama` via NAIS env, slik at den snakker med Ollama internt i clusteret
- **NAIS accessPolicy** er oppdatert med `outbound`-regler fra RAG → Ollama i begge miljøer
- **Ollama prod**-applikasjonen er omdøpt fra `reops-ollama` til `jamph-ollama` for å samsvare med dev og øvrige referanser

### For Nav-ansatte

Interne henvendelser kan sendes via Slack i kanalen #teamkanal.(teamreasarchobs)