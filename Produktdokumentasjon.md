# Produktdokumentasjon – JAMPH SQL KI-assistent

---

## Forord

Denne produktdokumentasjonen er beregnet på teknisk personell med ansvar for installasjon, drift og vedlikehold av JAMPH SQL KI-assistent-løsningen. Leseren forutsettes å ha kjennskap til følgende teknologier og konsepter:

- **Docker** og containerorkestrering (Kubernetes/NAIS)
- **Java/Kotlin** og bygging med Maven
- **Node.js** og pakkehåndtering med pnpm
- **REST API**-integrasjon og HTTP-protokoll
- **Google BigQuery** og grunnleggende SQL
- Grunnleggende kjennskap til store språkmodeller (LLM) og konseptet RAG *(Retrieval-Augmented Generation)*

Dokumentasjonen er også ment som underlag for sensor og veileder ved evaluering av bacheloroppgaven. Den gir en helhetlig oversikt over systemets egenskaper, virkemåte og gjennomført testing.

---

## Innholdsfortegnelse

- [Forord](#forord)
- [1. Beskrivelse av programmet](#1-beskrivelse-av-programmet)
  - [1.1 Hensikt](#11-hensikt)
  - [1.2 Hva systemet gjør – prinsipielt](#12-hva-systemet-gjør--prinsipielt)
- [2. Samsvar mellom kravspesifikasjon og produkt](#2-samsvar-mellom-kravspesifikasjon-og-produkt)
- [3. Sentrale datastrukturer](#3-sentrale-datastrukturer)
  - [3.1 BigQuery-datamodell](#31-bigquery-datamodell)
  - [3.2 Interne datastrukturer – Kotlin API](#32-interne-datastrukturer--kotlin-api)
  - [3.3 Frontend-datastrukturer (TypeScript)](#33-frontend-datastrukturer-typescript)
- [4. Programmets oppbygging og virkemåte](#4-programmets-oppbygging-og-virkemåte)
  - [4.1 Tjeneste 1 – Jamph-Umami-Frontend](#41-tjeneste-1--jamph-umami-frontend)
  - [4.2 Tjeneste 2 – Reops-Jamph-Rag-Api-Umami](#42-tjeneste-2--reops-jamph-rag-api-umami)
  - [4.3 Tjeneste 3 – Reops-Jamph-Ollama](#43-tjeneste-3--reops-jamph-ollama)
- [5. Hovedprogram og underprogrammer](#5-hovedprogram-og-underprogrammer)
  - **Backend – Reops-Jamph-Rag-Api-Umami**
  - [5.1 RagV2 SQL-genereringspipeline](#51-ragv2-sql-genereringspipeline)
  - [5.2 Forhåndsbygde SQL-maler (PrebuiltSchemas)](#52-forhåndsbygde-sql-maler-prebuiltschemas-backend)
  - [5.3 URL-til-nettsted-oppslag](#53-url-til-nettsted-oppslag-bigqueryurltositeidandurlpath-backend)
  - [5.4 OllamaClient](#54-ollamaclient-backend)
  - [5.6 BigQuerySchemaService](#56-bigqueryschemaservice--skjemaoppslag-og-helsestatus-backend)
  - **Frontend – Jamph-Umami-Frontend**
  - [5.5 Frontendkomponenter – detaljert oversikt](#55-frontendkomponenter--detaljert-oversikt)
  - [5.7 Batchet datahenting](#57-batchet-datahenting-batcheddashboardfetcherts-frontend)
- [6. Funksjonelt grensesnitt (maskin- og programvare)](#6-funksjonelt-grensesnitt-maskin--og-programvare)
  - [6.1 Maskinvarekrav](#61-maskinvarekrav)
  - [6.2 Programvarekrav](#62-programvarekrav)
  - [6.3 Miljøvariabler](#63-miljøvariabler)
  - [6.4 Operativsystemstøtte](#64-operativsystemstøtte)
  - [6.5 NAIS-plattform](#65-nais-plattform)
- [7. Installasjon og drift](#7-installasjon-og-drift)
  - [7.1 Lokal utvikling (uten Docker)](#71-lokal-utvikling-uten-docker)
  - [7.2 Docker Compose (anbefalt for lokal testing)](#72-docker-compose-anbefalt-for-lokal-testing)
  - [7.3 Produksjonsutrulling (NAIS)](#73-produksjonsutrulling-nais)
- [8. Feilsøking](#8-feilsøking)
- [9. Testdokumentasjon](#9-testdokumentasjon)
  - [9.1 Teststrategi og overordnet mål](#91-teststrategioversikt)
  - [9.2 SQL-korrekthetstesting (LlmSqlLogic)](#92-sql-korrekthetstesting-llmsqllogic)
  - [9.3 Dialekt- og semantisk testing](#93-dialekt--og-semantisk-testing-dialectvalidetallmtosql)
  - [9.4 SQL-syntaksvalidering (ValidateSqlQuery)](#94-sql-syntaksvalidering-validatesqlquery)
  - [9.5 Ytelsesmåling](#95-ytelsesmåling-tokenspeedmeasurer-endtoendtimer)
  - [9.6 Resultatformat – ModelBenchmarkResult](#96-resultatformat--modelbenchmarkresult)
- [10. Sikkerhets- og personvernhensyn](#10-sikkerhets--og-personvernhensyn)
- [Figurliste](#figurliste)
- [Tabellliste](#tabellliste)

---

## 1. Beskrivelse av programmet

### 1.1 Hensikt

JAMPH SQL KI-assistent er en webapplikasjon som lar analytikere og andre ikke-tekniske brukere stille spørsmål på naturlig språk (norsk og engelsk) mot nettanalysedata innsamlet via Umami Analytics og lagret i Google BigQuery. Systemet oversetter brukerens spørsmål til BigQuery-SQL ved hjelp av en lokal stor språkmodell (LLM), kjører spørringen, og presenterer resultatet som interaktive grafer og tabeller.

**Kjerneproblemet systemet løser:** Nettanalysedata (sidevisninger, brukerreiser, hendelser, søk) er rike og verdifulle, men tradisjonelt utilgjengelige for ikke-tekniske brukere som ikke kan skrive SQL. JAMPH SQL KI-assistent fjerner dette tekniske barrieret.

### 1.2 Hva systemet gjør – prinsipielt

1. Brukeren velger et nettsted og skriver et spørsmål på naturlig språk, f.eks.:  
   *«Vis daglige sidevisninger for siste 30 dager»*
2. Systemet klassifiserer spørsmålstypen og genererer en BigQuery-SQL-spørring via en lokal LLM (Ollama med modellen `qwen2.5-coder:7b`).
3. SQL-spørringen kjøres mot Google BigQuery-datalageret.
4. Resultatet visualiseres som linjediagram, søylediagram, sektordiagram, tabell eller statistikkort direkte i dashbordet.

Systemet tilbyr i tillegg en manuell grafbygger, SQL-editor, brukerreise-analyse, trafikkanalyse, retensjonsanalyse og en benchmarking-funksjon for å sammenligne LLM-modeller.

---

## 2. Samsvar mellom kravspesifikasjon og produkt

| # | Krav | Status | Merknad |
|---|------|--------|---------|
| **Funksjonelle krav** | | | |
| K1 | Naturlig-språk til SQL-konvertering | ✅ Implementert | RagV2-pipeline med 4 steg |
| K2 | Dialekt-støtte og engelsk inndata | ✅ Implementert | LLM håndterer norske dialekter og engelsk; bekreftet i `DialectValidetaLlmToSql` |
| K3 | Visualisering av analyseresultater | ✅ Implementert | 11 widgettyper (linje, søyle, sektor, tabell, osv.) |
| K4 | Kompatibelt med BigQuery-dialekt | ✅ Implementert | Genererer BigQuery-SQL; validert med JSQLParser + `BigQueryQueryService` |
| K6 | Dashbord med lagring av widgets | ✅ Implementert | `EndeligKI.tsx`, `defaultWidgets.json` |
| K7 | Kostnadsestimat for BigQuery-spørringer | ✅ Implementert | Dry-run via `/api/bigquery/estimate` |
| K10 | LLM-modellbenchmarking | ✅ Implementert | `ModellBenchmarkRunner2.kt`, `/api/benchmark` |
| K11 | Flerbruker-websitestøtte | ✅ Implementert | Nettsteder hentes fra `public_website`-tabellen |
| K13 | Integrasjon med NAV sitt verktøy (Start Umami) | ✅ Implementert | Leser Umami Analytics-data fra BigQuery (`umami_student`); opprinnelig planlagt med Metabase, endret til Start Umami |
| K14 | Korrekt mottak og tolkning av forespørsler | ✅ Implementert | 87 % SQL-nøyaktighet i benchmark (`LlmSqlLogic`); semantisk validering mot fasit i `DialectValidetaLlmToSql` |
| K15 | Forståelig feilmelding ved SQL-generering | ✅ Implementert | Feilkoder 10000–10003 med beskrivende meldinger; vises i frontend via `error`-tilstand i `EndeligKI.tsx` |
| **Ikke-funksjonelle krav** | | | |
| K5 | Lokal LLM-kjøring (personvern) | ✅ Implementert | Ollama på NAIS, ingen data sendes ut av plattformen |
| K8 | Autentisering mot grensesnitt | ✅ Implementert | Basic Auth i `server.js` |
| K9 | Containerisert utrulling | ✅ Implementert | Docker-bilder for alle tre tjenester |
| K12 | Sikkerhet: kun lesende SQL | ✅ Implementert | `ValidateSqlQuery.kt` blokkerer DML/DDL |
| K16 | Responstid | ✅ Implementert | Flere BigQuery-spørringer kombineres til én (`batchedDashboardFetcher.ts`); GPU-akselerasjon reduserer LLM-responstid fra ~60s til ~3–8s; `TokenSpeedMeasurer` måler tokens/sek per modell |
| K17 | Komponentbasert arkitektur | ✅ Implementert | Frontend er bygget som gjenbrukbare React-komponenter (`DashboardWidget`, `DashboardLayout`, `FilterBar`, `AiByggerPanel` m.fl.) på toppen av NAV Designsystem (`@navikt/ds-react`); Kotlin-backend følger samme prinsipp med separate tjenesteklasser |

---

## 3. Sentrale datastrukturer

### 3.1 BigQuery-datamodell

Systemet leser data fra Google BigQuery-prosjektet `fagtorsdag-prod-81a6`, dataset `umami_student`. De sentrale tabellene er:

#### Tabell: `public_website`
Inneholder oversikt over alle nettsteder som spores.

| Kolonne | Type | Beskrivelse |
|---------|------|-------------|
| `website_id` | STRING | Unik UUID for nettstedet |
| `name` | STRING | Visningsnavn (f.eks. «Aksel») |
| `domain` | STRING | Domenenavn (f.eks. `aksel.nav.no`) |

#### Tabell: `event`
Alle web-hendelser – sidevisninger og tilpassede hendelser.

| Kolonne | Type | Beskrivelse |
|---------|------|-------------|
| `event_id` | STRING | Unik hendelse-ID |
| `session_id` | STRING | Kobling til besøksøkt |
| `visit_id` | STRING | Unikt besøk innen en økt |
| `website_id` | STRING | Hvilket nettsted hendelsen tilhører |
| `url_path` | STRING | URL-sti (f.eks. `/komponenter/ikoner`) |
| `url_query` | STRING | URL-spørringsstreng |
| `referrer_domain` | STRING | Henviningsdomene |
| `page_title` | STRING | Sidetittel |
| `event_type` | INT64 | `1` = sidevisning, `2` = tilpasset hendelse |
| `event_name` | STRING | Navn på hendelse (kun ved `event_type = 2`) |
| `created_at` | TIMESTAMP | Tidspunkt |
| `utm_source/medium/campaign` | STRING | Markedsføringssporing |

**Kjente hendelsenavn** (`event_name`): `navigere`, `sok`, `sidebar-subnav`, `accordion åpnet/lukket`, `skjema fullfort`, `client-error`, `404`, `last ned`

#### Tabell: `session`
Besøksøkter med teknisk og geografisk kontekst.

| Kolonne | Type | Beskrivelse |
|---------|------|-------------|
| `session_id` | STRING | Unik økt-ID |
| `website_id` | STRING | Nettsted |
| `browser` | STRING | Nettleser (`chrome`, `safari`, `firefox`, osv.) |
| `os` | STRING | Operativsystem |
| `device` | STRING | Enhetstype (mobil, laptop, osv.) |
| `screen` | STRING | Skjermoppløsning |
| `language` | STRING | Nettleserspråk |
| `country` | STRING | Land |
| `created_at` | TIMESTAMP | Starttidspunkt for økt |
| `session_parameters` | ARRAY\<STRUCT\> | Egendefinerte parametere (unnestes med `CROSS JOIN UNNEST`) |

---

### 3.2 Interne datastrukturer – Kotlin API

#### `Website`
```kotlin
data class Website(
    val websiteId: String,
    val name: String,
    val domain: String?
)
```

#### `SiteIdAndPath`
Resultat av URL-oppslagslogikken (se avsnitt 5.3).
```kotlin
data class SiteIdAndPath(
    val siteId: String,
    val urlPath: String   // Tomt = hele nettstedet, «/sti%» = starts-with
)
```

#### `QueryTypeResult`
Klassifiseringsresultat fra steg 1 i RagV2-pipeline.
```kotlin
data class QueryTypeResult(
    val queryType: String,     // "linear"|"rankings"|"search"|"journey"|"cards"|"default"
    val siteId: String,
    val urlPath: String,
    val userPrompt: String,
    val rawLlmResponse: String?
)
```

#### `SQLRequest`
HTTP-forespørsel til `POST /api/sql`. Definert i `Application.kt`.
```kotlin
data class SQLRequest(
    val query: String,
    val url: String? = null,
    val model: String? = null,
    val pathOperator: String? = null,  // "starts-with" | "exact" | null
    val debug: Boolean? = null
)
```

#### `SQLResponse`
HTTP-svar fra `POST /api/sql`. Definert i `Application.kt`.
```kotlin
data class SQLResponse(
    val sql: String,
    val debugInfo: Map<String, String?>? = null
    // debugInfo-nøkler: queryType, siteId, urlPath,
    //                   extractedVariables, rawClassificationResponse
)
```

#### `ErrorResponse`
Feilsvar fra API-et. Definert i `Application.kt`.
```kotlin
data class ErrorResponse(val error: String)
```

#### `BenchmarkRequest`
HTTP-forespørsel til `POST /api/benchmark`. Definert i `Application.kt`.
```kotlin
data class BenchmarkRequest(
    val model: String? = null,
    val ollamaBaseUrl: String? = null
)
```

#### `SqlGenerationResult`
Fullstendig utdata fra RagV2-pipeline.
```kotlin
data class SqlGenerationResult(
    val sql: String,
    val queryType: String,
    val siteId: String,
    val urlPath: String,
    val extractedVariables: String?,
    val rawClassificationResponse: String?
)
```

#### `ModelBenchmarkResult`
Benchmarkingsresultat per LLM-modell. Definert i `ModellBenchmarkRunner2.kt`.
```kotlin
data class ModelBenchmarkResult(
    val model: String,
    val timestamp: String,
    val sqlAccuracy: Double,        // 0.0–1.0
    val dialectAccuracy: Double,    // 0.0–1.0
    val averageCostMB: Double,
    val endToEndMs: Long,
    val longPromptMs: Long,
    val shortPromptMs: Long,
    val tokensPerSecond: Double,
    val promptTokens: Int,
    val responseTokens: Int,
    val evalDurationMs: Long
)
```

---

### 3.3 Frontend-datastrukturer (TypeScript)

#### `DashboardWidgetType`, `DashboardWidgetSize`, `DashboardWidgetDefinition`
Definert i `src/components/dashboardjson/model/widgetType.ts`.
```typescript
export type DashboardWidgetType =
    | 'table' | 'regresjon' | 'linechart' | 'areachart' | 'barchart'
    | 'piechart' | 'statcards' | 'stegvisning' | 'kiforklaring'
    | 'pageflow' | 'metrics';

export interface DashboardWidgetSize {
    cols: number;
    rows: number;
}

export interface DashboardWidgetDefinition {
    id: string;
    title: string;
    chartType: string;          // løst typet; valideres til DashboardWidgetType ved kjøring
    sql: string;
    aiPrompt?: string;
    size: DashboardWidgetSize;
}

// Utvidet versjon med faktisk resultat (returnert av useDashboardWidgetResolver):
export interface DashboardWidgetResolved extends DashboardWidgetDefinition {
    chartType: DashboardWidgetType;
    result: { success: boolean; data: unknown[]; rowCount: number };
}
```

---

## 4. Programmets oppbygging og virkemåte

Systemet er delt inn i tre hovedtjenester som kjører som separate containere og kommuniserer over HTTP. Figur 1 viser den overordnede arkitekturen med alle tre tjenester og deres kommunikasjonsflyt.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          BRUKER (nettleser)                                  │
│               Analytiker / ikke-teknisk bruker / driftsansvarlig             │
└──────────────────────────────────┬───────────────────────────────────────────┘
                                   │  HTTPS (port 443)
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                  TJENESTE 1 – Jamph-Umami-Frontend                           │
│                                                                              │
│  ┌─────────────────────────────────┐  ┌──────────────────────────────────┐   │
│  │          React SPA              │  │    Node.js / Express BFF         │   │
│  │  Vite · TypeScript · Tailwind   │  │          server.js               │   │
│  │  @navikt/ds-react               │  │                                  │   │
│  │                                 │  │  ● Serverer statiske filer       │   │
│  │  ● KiBygger / EndeligKI         │  │  ● Basic Auth-tilgangskontroll   │   │
│  │  ● Dashboard-widgets (11 typer) │  │  ● Audit-logging (NAV-ident)     │   │
│  │  ● Grafbygger / SQL-editor      │  │                                  │   │
│  │  ● Brukerreise / Trafikkanalyse │  │  POST /api/bigquery              │   │
│  │  ● Funnel / Retensjon / Profiler│  │  POST /api/bigquery/estimate     │   │
│  └─────────────────────────────────┘  └─────────────────┬────────────────┘   │
└───────────────────────┬──────────────────────────────── │ ──────────────────┘
                        │                                 │
             POST /api/sql                    SQL + service account
           (naturlig språk +                              │
            url + pathOperator)                           ▼
                        │              ┌───────────────────────────────────────┐
                        │              │           Google BigQuery             │
                        │              │   Prosjekt: fagtorsdag-prod-81a6      │
                        │              │   Datasett:  umami_student            │
                        │              │   Region:    europe-north1            │
                        │              │                                       │
                        │              │   Tabeller:                           │
                        │              │   ● event          (sidevisninger)    │
                        │              │   ● session        (besøksøkter)      │
                        │              │   ● public_website (nettsteder)       │
                        │              └───────────────────────────────────────┘
                        ▼
┌───────────────────────────────────────────────────────────────────────────┐
│              TJENESTE 2 – Reops-Jamph-Rag-Api-Umami                       │
│                   Kotlin / Ktor / Netty – Port 8004                       │
│                                                                           │
│  Inngangsdata: { query, url, pathOperator, model?, debug? }               │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                       RagV2 SQL-pipeline                            │  │
│  │  Steg 1 → Klassifiser spørsmålstype via Ollama (temp. 0.0)         │  │
│  │  Steg 2 → Ekstraher variabler som JSON (Ollama)                    │  │
│  │  Steg 3 → Konstruer SQL fra forhåndsbygd mal                       │  │
│  │           ─── eller (ved type = default) ───                       │  │
│  │  Steg 4 → Fri SQL-generering med fullt skjema (Ollama)             │  │
│  └────────────────────────────┬────────────────────────────────────────┘  │
│                               │  POST /api/generate                       │
└───────────────────────────────┼───────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────────────┐
              │   TJENESTE 3 – Reops-Jamph-Ollama       │
              │       Ollama LLM – Port 11434           │
              │                                         │
              │   Modell: qwen2.5-coder:7b (7B par.)    │
              │   Kjører lokalt på NAIS / Kubernetes     │
              │   Ingen brukerdata forlater             │
              │   plattformen (personvern ivaretatt)    │
              └─────────────────────────────────────────┘
```

*Figur 1: Overordnet systemarkitektur med tre tjenester, datakommunikasjon og BigQuery-tilkobling.*

---

### 4.1 Tjeneste 1 – Jamph-Umami-Frontend

Frontenden er en enkeltsideapplikasjon (SPA) bygget med React 19, TypeScript og Vite, og bruker NAVs designsystem (`@navikt/ds-react`). Den kjøres i to parallelle prosesser under utvikling:

- **Vite devserver** – hot-reload for React-koden
- **Express-server (`server.js`)** – betjener BigQuery-kall og Basic Auth-beskyttelse

I produksjon bygges Vite-appen til statiske filer som Express-serveren serverer direkte.

#### Ruting

Applikasjonen benytter React Router v7. Alle ruter er definert i `src/routes.tsx`. Se Tabell 1 for fullstendig ruteoversikt.

*Tabell 1: Ruteoversikt i Jamph-Umami-Frontend (alle ruter definert i `src/routes.tsx`)*

| Sti | Komponent | Formål |
|-----|-----------|--------|
| `/` | `Home` | Forside |
| `/endelig-ki` | `EndeligKI` | Hoved-KI-dashbord (nåværende produksjonsversjon) |
| `/ki-bygger` | `KiBygger` | Alternativ KI-bygger |
| `/endelig-prototype` | `EndeligPrototype` | Endelig prototype (forgjenger) |
| `/grafbygger` | `Charts` | Manuell grafbygger |
| `/sql` | `SqlEditor` | Direkte SQL-editor |
| `/ai-bygger` | `AiBygger` | AI-bygger (bare layout) |
| `/prototype3` | `Prototype3` | Prototype 3 |
| `/dashboards` | `DashboardOverview` | Dashbordoversikt |
| `/dashboard` | `Dashboard` | Enkelt dashbord |
| `/grafdeling` | `Grafdeling` | Del graf/widget |
| `/widget` | `WidgetVisning` | Innebyggbar widget (bare layout) |
| `/brukerreiser` | `UserJourney` | Brukerreiseanalyse |
| `/hendelsesreiser` | `EventJourney` | Hendelsesreiser |
| `/trafikkanalyse` | `TrafficAnalysis` | Trafikkanalyse |
| `/markedsanalyse` | `MarketingAnalysis` | Markedsanalyse |
| `/brukerlojalitet` | `Retention` | Retensjonsanalyse |
| `/brukersammensetning` | `UserComposition` | Brukersammensetning |
| `/brukerprofiler` | `UserProfiles` | Brukerprofiler |
| `/utforsk-hendelser` | `EventExplorer` | Hendelsesutforsker |
| `/datastruktur` | `EventExplorer` | Alias for `/utforsk-hendelser` |
| `/trakt` | `Funnel` | Traktanalyse |
| `/personvernssjekk` | `PrivacyCheck` | Personvernsjekk |
| `/diagnose` | `Diagnosis` | Systemdiagnose |
| `/profil` | `UserProfile` | Brukerprofil |
| `/testmodell` | `TestModell` | Testmodell-side |
| `/komigang` | `Komigang` | Kom-i-gang-guide |
| `/oppsett` | `Oppsett` | Oppsettsveiledning |
| `/personvern` | `Personvern` | Personvernerklæring |
| `/tilgjengelighet` | `Tilgjengelighet` | Tilgjengelighetserklæring |
| `/taksonomi` | `Taksonomi` | Taksonomiartikkel |
| `/metabase` | `MetabaseGuide` | Metabase-guide |

#### Layoutsystem

`App.tsx` implementerer tre layoutvarianter:
- **Bare** (`/ai-bygger`, `/widget`): Ingen header/footer, full skjermbredde
- **Hjemside** (`/`): Kun `<main>` uten sidebegrensning
- **Standard**: `Page.Block` med `xl`-bredde og header/footer fra NAV Designsystem

#### Formål
Tjeneste 1 er det eneste kontaktpunktet for sluttbrukeren. Den samler alle analyseflater i étt grensesnitt og håndterer autentisering, BigQuery-kommunikasjon og visualisering.

#### Subrutiner og nøkkelmoduler

| Modul | Sti | Ansvar |
|-------|-----|--------|
| `App.tsx` | `src/App.tsx` | Rotkomponent, layoutvalg, React Router-integrasjon |
| `routes.tsx` | `src/routes.tsx` | Ruteregistrering for alle 35+ sidekomponenter |
| `server.js` | `server.js` | Express BFF: BigQuery-proxy, Basic Auth, audit-logging |
| `aiSqlApi.ts` | `src/components/dashboardjson/api/aiSqlApi.ts` | Kaller Kotlin API `/api/sql` med naturlig-språkspørsmål |
| `bigQueryApi.ts` | `src/components/dashboardjson/api/bigQueryApi.ts` | Kaller `/api/bigquery` via server.js |
| `batchedDashboardFetcher.ts` | `src/lib/batchedDashboardFetcher.ts` | Batcher økt-metrics til én BigQuery-skanning |

#### Særlige forhold
- **BFF-mønster (Backend-for-Frontend):** All BigQuery-kommunikasjon går via `server.js` for å unngå CORS-problemer og holde service account-credentials på server-siden – de eksponeres aldri til nettleseren.
- **Audit-trail:** `addAuditLogging()` i `server.js` tagger alle BigQuery-spørringer med NAV-ident som label og SQL-kommentar, noe som gir full sporbarhet i BigQuery-loggene.
- **Ingen server-side state:** Alle widgets og dashbordtilstander lagres i nettleserens `localStorage` – det finnes ingen dedikert database for frontend-tilstand.

---

### 4.2 Tjeneste 2 – Reops-Jamph-Rag-Api-Umami

Backend-API-et er skrevet i Kotlin med Ktor-rammeverket og Netty som HTTP-server. Det bygges med Maven til en fett JAR (`api-1.0-SNAPSHOT-jar-with-dependencies.jar`) og kjøres med Java 21.

#### API-endepunkter

*Tabell 2: REST-endepunkter i Rag-Api-Umami*

| Metode | Sti | Beskrivelse |
|--------|-----|-------------|
| GET | `/` | Statusmelding – bekreftelse på at API kjører |
| GET | `/health` | Helsesjekk – returnerer BigQuery-status |
| GET | `/api/bigquery/websites` | Henter alle nettsteder fra BigQuery |
| GET | `/api/bigquery/schema` | Returnerer skjemakontekst som tekststreng |
| GET | `/api/bigquery/tables/{tableName}` | Returnerer kolonnemetadata for én tabell |
| POST | `/api/sql` | Naturlig språk → SQL (RagV2-pipeline, inkl. debug-info i svar) |
| POST | `/api/chat` | ~~Direktechat~~ – fjernet, returnerer `501 Not Implemented` |
| POST | `/api/benchmark` | Kjør LLM-benchmark (synkront, returnerer ett resultat) |
| POST | `/api/benchmark/stream` | Streaming benchmark via SSE |

**Eksempel – POST `/api/sql`:**
```json
// Forespørsel
{
    "query": "Vis daglige sidevisninger siste 30 dager",
    "url": "https://aksel.nav.no",
    "pathOperator": "starts-with"
}

// Svar
{
    "sql": "SELECT DATE(created_at) AS dag, COUNT(*) AS sidevisninger FROM `fagtorsdag-prod-81a6.umami_student.event` WHERE website_id = 'fb69e1e9-...' AND event_type = 1 AND created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY) GROUP BY dag ORDER BY dag"
}
```

#### Formål
Tjeneste 2 er systemets intelligente kjerne. Den oversetter naturlig språk til BigQuery-SQL ved å orkestrere Ollama-kall gjennom RagV2-pipeline, og eksponerer alle API-operasjoner over HTTP.

#### Subrutiner og nøkkelmoduler

| Klasse / fil | Pakke | Ansvar |
|---|---|---|
| `Application.kt` | `no.jamph.ragumami` | Applikasjonsoppstart, Ktor-konfigurasjon, alle HTTP-endepunkter |
| `Routes.kt` | `no.jamph.ragumami` | Laster `routes.json` – URL-er, BQ-prefix og standardmodell |
| `RagV2SqlService.kt` | `ragV2` | Orkestrerer 4-stegs pipeline |
| `OllamaClient.kt` | `core/llm` | HTTP-klient mot Ollama med retry og timeouts |
| `BigQuerySchemaService.kt` | `bigquery` | Skjemaoppslag og `isHealthy()`-sjekk |
| `BigQueryQueryService.kt` | `bigquery` | Utfører BigQuery-spørringer via Google SDK |
| `BigQueryUrltoSiteIdAndUrlPath.kt` | `bigquery` | URL → (siteId, urlPath) for SQL-filtrering |

#### Særlige forhold
- **Fett JAR-distribusjon:** Maven bygger én enkelt JAR (`api-1.0-SNAPSHOT-jar-with-dependencies.jar`) som inneholder alle avhengigheter, noe som forenkler containerisering og eliminerer runtime-avhengigheter.
- **Mock-modus:** `BigQuerySchemaServiceMock` lar benchmarking og SQL-logikktester kjøres helt uten BigQuery-tilkobling. Den inneholder 31 hardkodede norske nettsteder med statisk skjema.
- **CORS-oppsett:** Konfigurert for `localhost:3000`, `localhost:5173`, `localhost:5174` og produksjons-URL-ene definert i `routes.json`.

---

### 4.3 Tjeneste 3 – Reops-Jamph-Ollama

En containerisert Ollama-tjeneste som kjører en lokal LLM uten å sende data til eksterne tjenester. Tjenesten eksponerer Ollamas standard REST-API på port 11434.

**Standardmodell:** `qwen2.5-coder:7b` – en kodespesialisert 7-milliarders-parametersmodell.

**Entrypoint-logikk (`entrypoint.sh`):**  
I Kubernetes er `/tmp` eneste skrivbare mappe. Modellene bakes inn i Docker-imaget under `/baked-models` ved byggetidspunkt. Ved oppstart kopierer skriptet disse til `/tmp` (Ollamas hjemmemappe), deretter startes `ollama serve`.

#### Formål
Tjeneste 3 tilbyr lokal LLM-inferens uten å sende brukerdata til eksterne tjenester. Dette er avgjørende for systemets personvernprofil – alle spørsmål behandles på NAVs egen infrastruktur (NAIS).

#### Subrutiner og nøkkelmoduler

| Fil | Ansvar |
|-----|--------|
| `Dockerfile` | Bruker ferdigbygd Ollama-binary – rask bygging, men inneholder kjente CVE-er |
| `Dockerfile.build-from-source` | Bygger fra patchet Go 1.24.4; fikser CVE-2025-22871, CVE-2025-47907, CVE-2025-61723 |
| `entrypoint.sh` | Håndterer K8s `/tmp`-begrensning; kopierer modeller og starter `ollama serve` |

#### Særlige forhold
- **K8s `/tmp`-begrensning:** I Kubernetes er kun `/tmp` skrivbart. `entrypoint.sh` setter `HOME`, `OLLAMA_HOME` og `OLLAMA_MODELS` til `/tmp` og kopierer bakte modeller dit ved oppstart for å omgå denne begrensningen.
- **Modell bakt inn i imaget:** `qwen2.5-coder:7b` lastes ned under `docker build` og lagres i `/baked-models`. Dette eliminerer nettverkshenting ved oppstart, men gir et Docker-image på ~6 GB.
- **GPU-akselerasjon:** Ollama oppdager GPU (CUDA/ROCm) automatisk. Med GPU reduseres responstiden fra ~30–60 sekunder til ~3–8 sekunder per SQL-generering.

---

## 5. Hovedprogram og underprogrammer

---

### Backend – Reops-Jamph-Rag-Api-Umami (Kotlin / Ktor)

### 5.1 RagV2 SQL-genereringspipeline

Kjernen i systemet er en 4-stegs pipeline for å konvertere et naturlig-språkspørsmål til en BigQuery-SQL-spørring. Figur 2 viser flyten.

```
  Brukerens spørsmål på naturlig språk
  (f.eks. «Vis daglige sidevisninger siste 30 dager på aksel.nav.no»)
                        │
                        ▼
  ┌───────────────────────────────────────────────────────────────────────┐
  │  STEG 1 – PickASqlQuestionTypeLlm                                     │
  │  Klassifiserer spørsmålet via Ollama (temperatur: 0.0)                │
  │  Inntil 3 forsøk med ulike promptformater ved feil                    │
  │  Feil etter alle forsøk → Error 10000                                 │
  │                                                                       │
  │  Returtyper:                                                          │
  │  linear   – tidsserier og trendanalyse med lineær regresjon           │
  │  rankings – topp-N rangering av URL-stier                             │
  │  search   – søkeordsfrekvens (event_name = 'sok')                     │
  │  journey  – navigasjonsflyt mellom to sider                           │
  │  cards    – nøkkeltallskort med flere metrics parallelt               │
  │  default  – alt annet (faller gjennom til Steg 4)                     │
  └──────────────────────────────┬────────────────────────────────────────┘
                                 │
               ┌─────────────────┴──────────────────┐
               │ type ≠ default                      │ type = default
               ▼                                     ▼
  ┌────────────────────────────┐   ┌──────────────────────────────────────────┐
  │  STEG 2                    │   │  STEG 4 – OtherLlm  (fallback-sti)       │
  │  PickVariableJsonLlm       │   │                                          │
  │                            │   │  Henter BigQuery-skjemakonteksten        │
  │  Sender forenklet SQL-     │   │  fra BigQuerySchemaService               │
  │  utkast + JSON-skjema      │   │                                          │
  │  til Ollama                │   │  Sender fullt skjema + spørsmål          │
  │                            │   │  til Ollama for fri SQL-generering       │
  │  Modellen fyller inn:      │   │                                          │
  │  datoer, metrikker,        │   │  Ekstraherer SQL fra kodeblokk           │
  │  limit, filtre osv.        │   │  eller ved SELECT-nøkkelord              │
  │                            │   │                                          │
  │  Inntil 3 forsøk           │   │  Inntil 3 forsøk                         │
  │  Feil → Error 10001        │   │  Feil → Error 10002                      │
  └────────────┬───────────────┘   └─────────────────────┬────────────────────┘
               │                                         │
               ▼                                         │
  ┌────────────────────────────┐                         │
  │  STEG 3 – ConstructSQL     │                         │
  │                            │                         │
  │  Henter SQL-mal for        │                         │
  │  spørsmålstypen            │                         │
  │                            │                         │
  │  Erstatter plassholdere:   │                         │
  │  [WEBSITE_ID] → UUID       │                         │
  │  [PATH]       → URL-sti    │                         │
  │  [START_DATE] → dato       │                         │
  │  [END_DATE]   → dato       │                         │
  │  [METRIC_SQL] → aggregat   │                         │
  │  [WHERE_FILTERS] → filter  │                         │
  │  prefix.      → BQ-prosjekt│                         │
  │                            │                         │
  │  Rydder dobble backticks   │                         │
  │  og ubrukte plassholdere   │                         │
  │  Feil → Error 10003        │                         │
  └────────────┬───────────────┘                         │
               └─────────────────────────────────────────┘
                                    │
                                    ▼
               ┌────────────────────────────────────────────┐
               │       Ferdig BigQuery SQL-spørring         │
               │  Returneres i SQLResponse { sql, ... }    │
               └────────────────────────────────────────────┘
```

*Figur 2: RagV2 SQL-genereringspipeline med mal-basert sti (Steg 1–3) og fallback-sti (Steg 4).*

#### Steg 1 – Klassifisering (`PickASqlQuestionTypeLlm`)

Sender spørsmålet til Ollama med en klassifiseringsprompt. Modellen skal returnere et JSON-objekt `{"queryType": "<type>"}`. Implementasjonen gjør inntil 3 forsøk med ulike promptformater ved feil.

*Gyldige typer og eksempler:*

| Type | Eksempelspørsmål |
|------|-----------------|
| `linear` | «Gjør en trendanalyse av daglige sidevisninger» |
| `rankings` | «Topp 10 mest besøkte sider i 2025» |
| `search` | «Hvor mange søker etter accessibility?» |
| `journey` | «Hvor mange går fra forsiden til /komponenter?» |
| `cards` | «Vis 4 nøkkeltall: unike besøkende, sidevisninger, hendelser, sesjoner» |
| `default` | Alt annet |

#### Steg 2 – Variabelutrekking (`PickVariableJsonLlm`)

For mal-baserte typer sender dette steget et schema-forenklet SQL-utkast og et JSON-skjema til LLM. Modellen fyller inn verdier i JSON-skjemaet. Implementasjonen prøver inntil 3 ganger.

**Feilkode 10001:** Modellen returnerte ikke gyldig JSON med forventede variabler.

#### Steg 3 – SQL-konstruksjon (`ConstructSQL`)

Henter den forhåndsbygde SQL-malen for gjeldende spørsmålstype og erstatter plassholdere:

| Plassholder | Erstattes med |
|-------------|---------------|
| `[WEBSITE_ID]` | Nettstedets UUID |
| `[PATH]` | URL-sti (f.eks. `/komponenter%`) |
| `prefix.` | Faktisk BigQuery-prefix (`fagtorsdag-prod-81a6.umami_student.`) |
| `[START_DATE]`, `[END_DATE]` | Datoer fra JSON-variabler |
| `[METRIC_SQL]` | Aggregeringsfunksjon |
| `[WHERE_FILTERS]` | Valgfrie filterbetingelser |

Etter erstatning ryddes ubrukte plassholdere og dobble backticks (`\`\``) normaliseres.

**Feilkode 10003:** Mal-konstruksjon feilet.

#### Steg 4 – Fri SQL-generering (`OtherLlm`)

For `default`-typen hentes hele BigQuery-skjemakonteksten fra `BigQuerySchemaService` og sendes sammen med spørsmålet til Ollama. Prøver inntil 3 ganger. Ekstraherer SQL fra kodeblokk-markdown eller søker etter `SELECT`-nøkkelord.

**Feilkode 10002:** Modellen returnerte ikke gyldig SQL.

---

### 5.2 Forhåndsbygde SQL-maler (`PrebuiltSchemas`) *(Backend)*

Hver spørsmålstype har en tilhørende `SchemaTriple` bestående av:
- `bigQuerySchema` – forenklet skjemabeskrivelse for LLM
- `sqlTemplate` – SQL-mal med `[PLACEHOLDER]`-variabler
- `simplifiedSql` – forenklet SQL kun for prompting
- `jsonSchema` – JSON-skjema som LLM skal fylle inn

*Tabell 3: Oversikt over SQL-maltyper*

| Type | SQL-mønster | Eksempel på bruk |
|------|-------------|-----------------|
| `linear` | `WITH base AS (DATE_DIFF...GROUP BY x), ` + lineær regresjon-CTE | Trendanalyse med regresjonslinje |
| `rankings` | `GROUP BY url_path ORDER BY DESC LIMIT [N]` | Topp-N sider |
| `search` | `WHERE event_name = 'sok' AND ... LIKE '%[TERM]%'` | Søkeordsfrekvens |
| `journey` | Doble CTEs for fra-til-navigasjon | Brukerreise mellom to sider |
| `cards` | Flere `COUNT(DISTINCT ...)` som kolonner | Nøkkeltallskort |
| `default` | Fri LLM-generering | Alt annet |

---

### 5.3 URL-til-nettsted-oppslag (`BigQueryUrltoSiteIdAndUrlPath`) *(Backend)*

Konverterer en full URL (f.eks. `https://aksel.nav.no/designsystemet`) til:
- `siteId` – UUID hentet ved domeneoppslag mot `public_website`-tabellen
- `urlPath` – formatert sti for SQL `LIKE`-operator

*Tabell 4: Sti-formatering etter `pathOperator`*

| Operator | Inngangssti | Resultat | SQL-effekt |
|----------|-------------|----------|------------|
| `starts-with` | `/` | `""` | Ingen stifilter (hele nettstedet) |
| `starts-with` | `/designsystemet` | `/designsystemet%` | Undersider inkludert |
| `equals` | `/designsystemet` | `/designsystemet` | Nøyaktig sidetreff |

---

### 5.4 OllamaClient *(Backend)*

HTTP-klient for kommunikasjon med Ollama-tjenesten.

| Egenskap | Verdi |
|----------|-------|
| Forespørselstidsavbrudd | 600 sekunder |
| Tilkoblingstidsavbrudd | 25 sekunder |
| Maks retries (5xx-feil) | 3 forsøk med eksponentiell backoff |
| Temperatur (klassifisering) | 0.0 |
| Temperatur (SQL-generering) | 0.0 |
| `repeat_penalty` | 1.01 |

Klienten tilbyr følgende metoder:
- `generate(prompt)` – standard SQL-generering
- `generateConstrained(prompt, temperature, maxTokens)` – begrenset generering for klassifisering
- `generateRaw(prompt)` – returnerer rå JSON (brukt av `TokenSpeedMeasurer`)
- `fetchDefaultModel(baseUrl)` *(companion object)* – henter første tilgjengelige Ollama-modell automatisk ved oppstart

---

---

### Frontend – Jamph-Umami-Frontend (React / Node.js)

### 5.5 Frontendkomponenter – detaljert oversikt

#### `EndeligKI.tsx` – Hoved-KI-dashbord (produksjonsversjon)

Programmets viktigste brukergrensesnitt, tilgjengelig på ruten `/endelig-ki`. Tilstandsmaskin med følgende hovedelementer:

| Tilstand | Beskrivelse |
|----------|-------------|
| `activeTab` | Aktiv fane: `'grafbygger'` (SQL/KI) eller dashbord-fane |
| `url` | Valgt nettsted-URL fra URL-søksskjema |
| `kiPrompt` | Brukerens naturligspråkspørsmål |
| `kiSuggestion` | SQL-forslag returnert fra RagV2-API |
| `sqlValue` | Gjeldende SQL-spørring (kan redigeres manuelt) |
| `grafTab` | Valgt visualiseringstype (`'linechart'`, `'barchart'`, osv.) |
| `grafTitle` | Grafens visningstittel |
| `previewResult` | Rå resultatdata fra BigQuery |
| `ragLoading` | `true` mens SQL-generering pågår |
| `queryLoading` | `true` mens BigQuery-spørring kjøres |
| `error` | Feilmelding ved mislykkede kall |
| `dashboards` | Liste over lagrede dashbord-navn (localStorage) |
| `selectedDashboard` | Aktivt valgt dashbord |

**Interaksjonsflyt:**
1. Bruker skriver inn URL og velger nettsted
2. Bruker skriver spørsmål på naturlig språk i `kiPrompt`-feltet
3. Klikker «Generer SQL» → RAG-API kalles, `kiSuggestion` populeres
4. SQL vises i redigerbar editor (`sqlValue`), kan justeres manuelt
5. Klikker «Kjør» → BigQuery-spørring sendes via BFF, `previewResult` settes
6. Resultat visualiseres i valgt graftype (`grafTab`)

#### `components/dashboard/` – Chartkomponenter

*Tabell 5: Dashboard-widgets og tilhørende filer*

| Widget | Fil | Beskrivelse |
|--------|-----|-------------|
| `DashboardLineChart` | `DashboardLineChart.tsx` | Linjediagram (tidsserie) |
| `DashboardAreaChart` | `DashboardAreaChart.tsx` | Arealdiagram |
| `DashboardBarChart` | `DashboardBarChart.tsx` | Søylediagram |
| `DashboardPieChart` | `DashboardPieChart.tsx` | Sektordiagram |
| `DashboardTable` | `DashboardTable.tsx` | Datatabell med sortering |
| `DashboardStatCards` | `DashboardStatCards.tsx` | Statistikkort |
| `DashboardJourney` | `DashboardJourney.tsx` | Brukerreise-visualisering |
| `DashboardKIForklaring` | `DashboardKIForklaring.tsx` | KI-generert tekstforklaring |

#### `server.js` – Node.js BFF

Tjener tre formål:
1. Betjener den statiske Vite-bygningen
2. Proxyer BigQuery-kall (unngår CORS og holder credentials på server-siden)
3. Håndterer Basic Auth for tilgangskontroll

`addAuditLogging()` legger til NAV-ident som BigQuery-label og SQL-kommentar slik at alle spørringer er sporbare i BigQuery-loggene.

---

### 5.6 `BigQuerySchemaService` – Skjemaoppslag og helsestatus *(Backend)*

Implementerer `BigQuerySchemaProvider`-grensesnittet med følgende metoder:

| Metode | Beskrivelse |
|--------|-------------|
| `getWebsites()` | Henter alle nettsteder fra `public_website`-tabellen |
| `getTableSchema(tableName)` | Henter kolonnemetadata via BigQuery metadata-API (ingen dataskanning) |
| `listTables()` | Lister alle tabeller i datasetet |
| `getSchemaContext()` | Bygger en tekstlig skjemabeskrivelse for LLM-prompt |
| `isHealthy()` | Kjører en billig testspørring for å verifisere tilkobling |

**`BigQuerySchemaServiceMock`** brukes i testing og benchmarking. Den har 31 hardkodede norske offentlige nettsteder og returnerer et statisk skjema uten BigQuery-tilgang.

---

### 5.7 Batchet datahenting (`batchedDashboardFetcher.ts`) *(Frontend)*

Optimalisering for dashbord med mange widgets: Øktbaserte metrics (land, nettleser, enhet, OS, skjerm, språk) deler samme dataskanning. `batchedDashboardFetcher` henter rådata én gang og beregner alle aggregeringer på klientsiden, noe som reduserer BigQuery-kostnader betraktelig.

---

## 6. Funksjonelt grensesnitt (maskin- og programvare)

### 6.1 Maskinvarekrav

*Tabell 6: Minimumskrav til maskinvare*

| Komponent | Minimum | Anbefalt |
|-----------|---------|---------|
| CPU (Ollama-server) | 4 kjerner | 8+ kjerner |
| RAM (Ollama med qwen2.5-coder:7b) | 8 GB | 16 GB |
| RAM (API + Frontend) | 2 GB | 4 GB |
| Lagringsplass (Docker-image med modell) | 6 GB | 10 GB |
| Nettverkstilgang | BigQuery API (HTTPS/443) | — |

**Merk:** GPU-akselerasjon er støttet av Ollama, men ikke påkrevd. Med GPU reduseres responstiden fra ~30–60 sek til ~3–8 sek.

### 6.2 Programvarekrav

*Tabell 7: Programvarekrav*

| Komponent | Versjon | Formål |
|-----------|---------|--------|
| Java JDK | 21 LTS | Kjøre Kotlin-API |
| Maven | 3.9+ | Bygge Kotlin-API |
| Node.js | 20+ | Kjøre frontend/server |
| pnpm | 9.12.2 | Pakkehåndtering frontend |
| Docker | 20+ | Containerisering |
| Ollama | 0.15.2+ | LLM-kjøring |

### 6.3 Miljøvariabler

*Tabell 8: Miljøvariabler – Kotlin API*

| Variabel | Standard | Beskrivelse |
|----------|---------|-------------|
| `API_PORT` | `8004` | HTTP-port for API |
| `API_HOST` | `0.0.0.0` | Bind-adresse |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama-tjenesteadresse |
| `OLLAMA_MODEL` | Auto-detektert | Modellnavn |
| `BIGQUERY_PROJECT_ID` | `fagtorsdag-prod-81a6` | GCP-prosjekt |
| `BIGQUERY_DATASET` | `umami_student` | BigQuery-datasett |
| `BIGQUERY_LOCATION` | `europe-north1` | Datasettlokasjon |
| `bigquery-credentials` | — | Service account JSON (NAIS-hemmelighet) |
| `GOOGLE_APPLICATION_CREDENTIALS` | — | Sti til nøkkelfil |

*Tabell 9: Miljøvariabler – Frontend/server.js*

| Variabel | Standard | Beskrivelse |
|----------|---------|-------------|
| `VITE_RAG_API_URL` | — | URL til Kotlin API (f.eks. `http://localhost:8004`) |
| `bigquery-credentials` | — | Service account JSON (NAIS-prioritet 1) |
| `GOOGLE_APPLICATION_CREDENTIALS` | — | Sti til nøkkelfil (prioritet 2) |
| `UMAMI_BIGQUERY` | — | Service account JSON som env-var (prioritet 3) |
| `BASIC_AUTH_USERNAME` | — | Brukernavn for Basic Auth |
| `BASIC_AUTH_PASSWORD` | — | Passord for Basic Auth |

### 6.4 Operativsystemstøtte

- **Linux** (Ubuntu 22.04+, Debian 12+): Primær målplattform for produksjon
- **macOS** (12+): Støttet for lokal utvikling
- **Windows**: Støttet via WSL2 eller Docker Desktop

### 6.5 NAIS-plattform

For produksjonsutrulling brukes NAVs Kubernetes-plattform NAIS. Konfigurasjonen ligger i `.nais/`-mappen i hvert repository. Særlige hensyn:

- Ollama-tjenesten kan ikke skrive til `/app` eller rotfilsystemet – all modelldata lagres i `/tmp`
- BigQuery-hemmeligheter injiseres som NAIS-secrets og monteres som miljøvariabler (`bigquery-credentials`)
- Basic Auth-passord injiseres tilsvarende fra NAIS-secrets

---

## 7. Installasjon og drift

### 7.1 Lokal utvikling (uten Docker)

#### Steg 1 – Kotlin API

```bash
cd Reops-Jamph-Rag-Api-Umami
mvn clean package -Dmaven.test.skip=true
java -jar target/api-1.0-SNAPSHOT-jar-with-dependencies.jar
# API tilgjengelig på http://localhost:8004
```

#### Steg 2 – Ollama (separat terminal)

```bash
ollama serve
ollama pull qwen2.5-coder:7b
```

#### Steg 3 – Frontend

```bash
cd Jamph-Umami-Frontend
# Opprett .env med:
# VITE_RAG_API_URL=http://localhost:8004
pnpm install   # første gang
pnpm start     # starter både Vite og Express parallelt
```

Legg filen `fagtorsdag-prod-81a6-52ac69097f46.json` (BigQuery service account) i `Jamph-Umami-Frontend/`-mappen.

### 7.2 Docker Compose (anbefalt for lokal testing)

```bash
# Kotlin API + automatisk tilkobling til lokal Ollama
cd Reops-Jamph-Rag-Api-Umami
docker compose -f docker-compose.dev.yml up
```

Docker Compose-konfigurasjonen bruker `host.docker.internal:11434` for å nå lokal Ollama fra containeren.

### 7.3 Produksjonsutrulling (NAIS)

```bash
# Bygg sikker Ollama-image (med patchet Go)
docker build -f Dockerfile.build-from-source -t jamph-ollama:secure .

# Push og deploy via NAIS GitHub Actions (se .github/workflows/)
```

---

## 8. Feilsøking

*Tabell 10: Vanlige feil og løsninger*

| Symptom | Mulig årsak | Løsning |
|---------|-------------|---------|
| `Error 10000` | Ollama returnerte ikke gyldig JSON etter 3 forsøk | Sjekk Ollama-loggene; forsøk annen modell |
| `Error 10001` | LLM fylte ikke inn variablene korrekt | Sjekk at Ollama er oppe; forenkle spørsmål |
| `Error 10002` | LLM returnerte ikke SQL med SELECT | Sjekk skjema-kontekst; forenkle spørsmål |
| `Error 10003` | SQL-malkonstruksjon feilet | Sjekk at `routes.json` inneholder riktig prefix |
| `BigQuery not configured` | Mangler credentials | Sett `bigquery-credentials` eller `GOOGLE_APPLICATION_CREDENTIALS` |
| `No website found for domain` | URL-domenet finnes ikke i BigQuery | Legg til nettstedet i `public_website`-tabellen |
| Timeout 600s | LLM bruker for lang tid | Vurder raskere modell eller GPU-akselerasjon |
| 401 Unauthorized | Basic Auth aktiv | Bruk riktig brukernavn/passord; se `server.js`-konfigurasjonen |
| Ollama starter ikke | Modell mangler | Kjør `ollama pull qwen2.5-coder:7b` |

**Helsesjekk:**
```bash
curl http://localhost:8004/health
# Svar: {"status":"healthy","bigquery":"connected","service":"rag-umami"}
```

---

## 9. Testdokumentasjon

### 9.1 Teststrategioversikt

#### Overordnet mål for testingen
Testingen av JAMPH SQL KI-assistent har som primærmål å verifisere at den genererte SQL-en er **syntaktisk korrekt** og **semantisk riktig** – dvs. at spørringen faktisk returnerer de dataene brukeren etterspurte. Et sekundært mål er å kvantifisere ytelsesegenskapene (responstid, token-hastighet) for ulike LLM-modeller slik at den best egnede modellen kan velges for produksjon.

#### Omfang og avgrensninger

**Inkludert i testingen:**
- SQL-korrekthet: regelbasert sjekk mot 12 testcase-spørsmål med kjente krav
- SQL-syntaks: statisk validering av all generert SQL med JSQLParser
- Dialektstøtte: norsk og engelsk, inkl. dialekter og skrivefeil
- Ytelse og kostnadsestimering: responstid, token-hastighet og BigQuery-dataskanning per modell

**Ikke inkludert (avgrensning):**
- Brukergrensesnitt-testing (UI): manuelt verifisert – ingen automatisert UI-testpakke er konfigurert
- Last- og skaleringstest av BigQuery-tilkoblingen
- Automatisert akseptansetesting med sluttbrukere
- Frontend-enhetstester: ingen Jest/Vitest-testpakke er satt opp i prosjektet

#### Statisk testing
Statisk testing ble gjennomført ved manuell gjennomgang av:
- SQL-maler i `PrebuiltSchemas.kt` – sjekket for logiske feil, korrekte plassholdere og gyldig BigQuery-syntaks
- Kravspesifikasjonen (K1–K12) – verifisert samsvar med implementasjon (se seksjon 2)
- Regex-regler og JSQLParser-konfigurasjon i `ValidateSqlQuery.kt` – dekker BigQuery-spesifikke konstruksjoner (`QUALIFY`, tidsenhetargumenter)

#### Dynamisk testing – testnivåer

| Testnivå | Implementert av | Beskrivelse |
|----------|----------------|-------------|
| Enhets-/integrasjonstest | `LlmSqlLogic.kt` | 12 spørsmål kjøres mot RagV2-pipeline; regelbaserte krav sjekkes per spørsmål |
| Semantisk test | `DialectValidetaLlmToSql.kt` | SQL kjøres mot BigQuery; resultat sammenlignes med fasit (±5 % toleranse) |
| Syntaksvalidering | `ValidateSqlQuery.kt` | All generert SQL valideres statisk med JSQLParser før retur til klient |
| Ytelsesmåling | `TokenSpeedMeasurer`, `EndToEndTimer` | Tokens/sek og ende-til-ende-tid måles per modell (5 kjøringer, gjennomsnitt) |
| Systemtest / benchmark | `ModellBenchmarkRunner2.kt` | Fullstendig modellbenchmark via `/api/benchmark` og SSE-streaming |

Systemet benytter tre overordnede testlagsnivåer:

1. **Enhets- og integrasjonstesting** – automatiserte SQL-korrekthetstester
2. **Dialekttesting** – semantisk SQL-validering mot kjente fasitsvar
3. **Ytelsesmåling (benchmarking)** – måling av responstid og token-hastighet

### 9.2 SQL-korrekthetstesting (`LlmSqlLogic`)

Automatisert test som kjører et sett av spørsmål mot en modell og sjekker om den genererte SQL-en oppfyller regelbaserte krav. Kjøres via `/api/benchmark`-endepunktet.

*Tabell 11: Eksempel på testcaser i `LlmSqlLogic`*

| Testspørsmål | Sjekker at SQL inneholder |
|--------------|--------------------------|
| «Sidevisninger per dag i 2025» | `fagtorsdag-prod-81a6.umami_student`, website_id, `GROUP BY`, datoekstrahering, `EVENT_TYPE` |
| «Topp 12 mest besøkte undersider i 2025» | `url_path`, `GROUP BY`, `ORDER BY`, `LIMIT 12` |
| «Sidevisninger per måned i 2025» | `EXTRACT(MONTH`, `GROUP BY`, `2025` |
| «Mest brukte søkeord» | `event_name`, `sok`, `GROUP BY`, `ORDER BY` |
| «Brukere fra land» | `country`, `COUNT(DISTINCT session_id)`, `GROUP BY` |

**Returverdi:** Nøyaktighetsrate som desimaltall (0.0–1.0), f.eks. `0.85` = 85 % av reglene bestått.

### 9.3 Dialekt- og semantisk testing (`DialectValidetaLlmToSql`)

Tester at modellen genererer semantisk ekvivalent SQL uavhengig av:
- Skrivefeil og dialekter («kor mange brukarar», «ke mange brukere»)
- Blandede norsk/engelsk formuleringer
- Uformelt språk («folk», «innom»)

Validering gjøres ved å kjøre SQL mot BigQuery og sammenligne resultatet med et kjent fasitsvar (med ±5 % toleranse for tallverdier).

### 9.4 SQL-syntaksvalidering (`ValidateSqlQuery`)

Statisk validering ved hjelp av `JSQLParser`-biblioteket:

1. **Tomsjekk:** Blanke spørringer avvises
2. **DML/DDL-blokkering:** Regulæruttrykk blokkerer `DELETE`, `DROP`, `TRUNCATE`, `UPDATE`, `INSERT`, `ALTER`, `MERGE`, `REPLACE`, `CREATE`, `LOAD`
3. **Syntaksvalidering:** BigQuery-spesifikk syntaks forbehandles (fjerner `QUALIFY`-klausuler, normaliserer tidsenhetargumenter) før JSQLParser validerer syntaksen

### 9.5 Ytelsesmåling (`TokenSpeedMeasurer`, `EndToEndTimer`)

*Tabell 12: Ytelsesmålinger per modell*

`TokenSpeedMeasurer` kjører samme prompt 5 ganger og returnerer gjennomsnittlig:
- Tokens per sekund (`tokensPerSecond`)
- Antall prompttokens (`promptTokens`)
- Antall responstokens (`responseTokens`)
- Total evalueringstid i ms

`EndToEndTimer` måler total tid for hele RagV2-pipeline fra spørsmål til ferdig SQL.

`LongPromptTimer` og `ShortPromptTimer` måler responstid med henholdsvis stort og lite skjema i prompten, noe som hjelper til å identifisere om kontekstlengde er en flaskehals.

`CostValidateLLmEstimator` kjører et sett testspørringer og rapporterer gjennomsnittlig BigQuery-kostnader i MB for den genererte SQL-en.

### 9.6 Resultatformat – `ModelBenchmarkResult`

Alle benchmarkingsresultater returneres som JSON via `/api/benchmark` og skrives til `benchmark_results.csv` for videre analyse:

```json
{
    "model": "qwen2.5-coder:7b",
    "timestamp": "2025-05-14T10:00:00Z",
    "sqlAccuracy": 0.87,
    "dialectAccuracy": 0.79,
    "averageCostMB": 23.4,
    "endToEndMs": 14200,
    "longPromptMs": 18900,
    "shortPromptMs": 4100,
    "tokensPerSecond": 22.7,
    "promptTokens": 1843,
    "responseTokens": 312,
    "evalDurationMs": 13700
}
```

---

## 10. Sikkerhets- og personvernhensyn

| Tiltak | Implementasjon |
|--------|---------------|
| Kun lesende SQL | `ValidateSqlQuery.kt` blokkerer all DML/DDL |
| Lokal LLM | Ingen brukerdata sendes til eksterne tjenester |
| Basic Auth | Tilgangskontroll i `server.js` for hele frontenden |
| BigQuery-sporing | Audit-logging med NAV-ident som label og SQL-kommentar |
| HTTPS | Obligatorisk i NAIS-produksjonsmiljø |
| Ingen SQL-injeksjon | Spørringer genereres av LLM og valideres – brukere skriver ikke direkte SQL |
| Credentials | Håndteres som NAIS-secrets, aldri hardkodet (unntatt fallback-prosjekt-ID) |

---

## Figurliste

- **Figur 1** (avsnitt 4): Overordnet systemarkitektur med tre tjenester, datakommunikasjon og BigQuery-tilkobling
- **Figur 2** (avsnitt 5.1): RagV2 SQL-genereringspipeline med mal-basert sti (Steg 1–3) og fallback-sti (Steg 4)

## Tabellliste

- **Tabell 1** (avsnitt 4.1): Ruteoversikt i Jamph-Umami-Frontend
- **Tabell 2** (avsnitt 4.2): REST-endepunkter i Rag-Api-Umami
- **Tabell 3** (avsnitt 5.2): Oversikt over SQL-maltyper
- **Tabell 4** (avsnitt 5.3): Sti-formatering etter `pathOperator`
- **Tabell 5** (avsnitt 5.5): Dashboard-widgets og tilhørende filer
- **Tabell 6** (avsnitt 6.1): Minimumskrav til maskinvare
- **Tabell 7** (avsnitt 6.2): Programvarekrav
- **Tabell 8** (avsnitt 6.3): Miljøvariabler – Kotlin API
- **Tabell 9** (avsnitt 6.3): Miljøvariabler – Frontend/server.js
- **Tabell 10** (avsnitt 8): Vanlige feil og løsninger
- **Tabell 11** (avsnitt 9.2): Eksempel på testcaser i `LlmSqlLogic`
- **Tabell 12** (avsnitt 9.5): Ytelsesmålinger per modell
