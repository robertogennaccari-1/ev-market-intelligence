# EV Market Intelligence - Architettura con Persistenza

## Analisi Situazione Attuale

### Componenti Esistenti
✅ **Repository GitHub**: `robertogennaccari-1/ev-market-intelligence`
✅ **Script Python**: 
- `ev_news_collector.py` (mock data)
- `create_corrected_rankings.py`
- `calculate_rankings_delta.py`
✅ **Script Shell**: `ev_intelligence_update.sh`
✅ **Struttura dati**: JSON files in `data/` e `history/`

### Componenti Mancanti
❌ **Dashboard React**: Directory non presente
❌ **Raccolta notizie reale**: Attualmente usa dati mock
❌ **Deployment automatico**: Dashboard non configurato
❌ **Storage persistente**: Nessun backup su S3 o storage esterno
❌ **Bootstrap script**: Nessuno script per setup iniziale

## Problema Fondamentale

Il sandbox è **effimero**: i file creati durante una sessione non persistono automaticamente tra esecuzioni diverse. Per un task schedulato bisettimanale, questo è critico.

## Soluzione Architetturale

### 1. Persistenza Multi-Livello

```
┌─────────────────────────────────────────────────────────┐
│                    TASK SCHEDULATO                       │
│              (Martedì e Venerdì, 9:00 CET)              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              BOOTSTRAP SCRIPT                            │
│  1. Clone repository da GitHub                          │
│  2. Setup ambiente Python                               │
│  3. Recupera dati storici (se necessario)               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│           ESECUZIONE AGGIORNAMENTO                       │
│  1. Raccolta notizie (API/scraping reale)              │
│  2. Aggiornamento rankings                              │
│  3. Calcolo delta                                       │
│  4. Generazione report                                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              PERSISTENZA DATI                            │
│  1. Commit e push su GitHub                             │
│  2. Deploy dashboard (GitHub Pages o Vercel)            │
│  3. Backup opzionale su S3                              │
└─────────────────────────────────────────────────────────┘
```

### 2. Componenti da Implementare/Migliorare

#### A. Script di Raccolta Notizie Reale
**File**: `scripts/ev_news_collector.py`
- Sostituire mock data con ricerca reale
- Utilizzare search API per raccogliere notizie recenti
- Filtrare per rilevanza e data (ultimi 3-4 giorni)
- Categorizzare per regione e produttore

#### B. Dashboard React
**Directory**: `dashboard/`
- Creare con `webdev_init_project` (web-static)
- Componenti:
  - News feed per regione
  - Tabelle rankings BEV/PHEV
  - Grafici trend storici
  - Indicatori di cambiamento
- Deploy su GitHub Pages o Vercel

#### C. Bootstrap Script
**File**: `bootstrap.sh`
```bash
#!/bin/bash
# 1. Clone repository
# 2. Setup Python environment
# 3. Install dependencies
# 4. Run update script
# 5. Deploy dashboard
```

#### D. Sistema di Deployment
**Opzioni**:
1. **GitHub Pages** (preferito per semplicità)
   - Build statico del dashboard
   - Deploy automatico via GitHub Actions
   
2. **Vercel** (alternativa)
   - Deploy automatico da GitHub
   - Preview per ogni commit

### 3. Flusso di Esecuzione Schedulata

```bash
# Cron job esegue:
0 0 9 * * 2,5 /usr/local/bin/ev_market_intelligence_runner.sh

# Runner script:
#!/bin/bash
cd /tmp
git clone https://github.com/robertogennaccari-1/ev-market-intelligence.git
cd ev-market-intelligence
./bootstrap.sh
```

### 4. Gestione Credenziali

**Variabili d'ambiente necessarie**:
- `GITHUB_TOKEN`: Per push automatico
- `OPENAI_API_KEY`: Già disponibile per ricerche
- Opzionale: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` per S3

**Storage**:
- Credenziali salvate in `.env` file (gitignored)
- O passate come variabili d'ambiente al task schedulato

### 5. Backup e Recovery

**Strategia**:
1. **Primary**: GitHub repository (codice + dati)
2. **Secondary**: GitHub Pages (dashboard pubblico)
3. **Tertiary** (opzionale): S3 bucket per dati storici

**Recovery**:
- Ogni esecuzione parte da clone fresco del repository
- Dati storici sempre disponibili in `history/`
- Dashboard sempre accessibile via URL pubblico

## Implementazione Step-by-Step

### Fase 1: Migliorare Script Esistenti
1. ✅ Analizzare script esistenti
2. 🔄 Implementare raccolta notizie reale
3. 🔄 Verificare/migliorare script rankings
4. 🔄 Testare script delta

### Fase 2: Creare Dashboard
1. 🔄 Init progetto React con webdev_init_project
2. 🔄 Implementare componenti UI
3. 🔄 Integrare dati JSON
4. 🔄 Build e test locale

### Fase 3: Setup Deployment
1. 🔄 Configurare GitHub Pages o Vercel
2. 🔄 Creare workflow CI/CD
3. 🔄 Test deployment

### Fase 4: Bootstrap e Scheduling
1. 🔄 Creare bootstrap script
2. 🔄 Configurare task schedulato
3. 🔄 Test esecuzione completa

### Fase 5: Documentazione
1. 🔄 Aggiornare README
2. 🔄 Creare guida operativa
3. 🔄 Documentare troubleshooting

## Metriche di Successo

- ✅ Repository GitHub contiene tutto il codice
- ✅ Dashboard accessibile pubblicamente
- ✅ Esecuzione schedulata funziona senza intervento manuale
- ✅ Dati persistono tra esecuzioni
- ✅ Sistema recupera automaticamente da errori
- ✅ Documentazione completa e chiara

## Timeline Stimata

- **Fase 1**: 30 minuti
- **Fase 2**: 45 minuti
- **Fase 3**: 30 minuti
- **Fase 4**: 20 minuti
- **Fase 5**: 15 minuti

**Totale**: ~2.5 ore

## Note Importanti

1. **Sandbox Lifecycle**: Il sandbox hiberna e riprende, ma i file non persistono indefinitamente
2. **GitHub come Source of Truth**: Tutto deve essere committato e pushato
3. **Idempotenza**: Gli script devono essere eseguibili multiple volte senza effetti collaterali
4. **Error Handling**: Gestire gracefully fallimenti di rete, API, etc.
5. **Logging**: Mantenere log dettagliati per debugging
