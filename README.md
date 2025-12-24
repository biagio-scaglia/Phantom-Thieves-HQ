# 🃏 Phantom Thieves HQ

**Persona 5–inspired Productivity & Insight System**

Un sistema di produttività gamificato che trasforma le tue attività quotidiane in missioni stile Persona 5. Completa task, aumenta le tue statistiche e conquista i Palace degli obiettivi più grandi.

---

## 🎯 Concept

Ogni attività della vita reale diventa una **missione**. Completandole, aumenti le tue **stats** come in Persona 5:

| Stat        | Significato                    |
| ----------- | ------------------------------ |
| Knowledge   | Studio, lettura, corsi         |
| Guts        | Task difficili o fuori comfort |
| Proficiency | Skill tecniche                 |
| Kindness    | Attività social                |
| Charm       | Presentazioni, networking      |

---

## ✨ Features

### ✅ Task System
- Aggiunta task con difficoltà, categoria e deadline
- Ogni task completata aumenta una stat, dà EXP e sblocca achievement

### 🏯 Palace System
- Ogni obiettivo grande è un Palace (es. "Imparare Python", "Costruire portfolio")
- Percentuale di infiltrazione
- Boss finale (milestone)
- Countdown stile "giorni rimasti"

### 📊 Dashboard
- Stats in tempo reale
- Grafici di progresso (matplotlib)
- Cronologia progressi
- "Persona affinities" (bonus se segui certe routine)

### 🧬 Save System
- SQLite per persistenza dati
- Supporto multi-profilo utente
- Backup automatico

---

## 🛠️ Stack Tecnologico

- **Python 3.12+**
- **SQLAlchemy** - ORM per database
- **Rich** - UI terminale avanzata
- **Matplotlib** - Visualizzazione dati
- **Pydantic** - Validazione dati
- **Architettura MVC** - Separazione concerns

---

## 📦 Installazione

```bash
# Clona il repository
git clone <your-repo-url>
cd phantom_thieves_hq

# Installa le dipendenze
pip install -r requirements.txt

# Avvia l'applicazione
python app.py
```

---

## 🚀 Utilizzo

1. **Crea un profilo** - Inizia la tua avventura come Phantom Thief
2. **Aggiungi task** - Trasforma le tue attività in missioni
3. **Completa missioni** - Guadagna EXP e aumenta le stats
4. **Crea Palace** - Definisci obiettivi grandi da conquistare
5. **Monitora progressi** - Visualizza dashboard e grafici

---

## 📁 Struttura Progetto

```
phantom_thieves_hq/
├── app.py                 # Entry point
├── core/
│   ├── game_loop.py      # Main game loop
│   ├── stats_engine.py   # Gestione statistiche
│   └── palace_engine.py  # Sistema Palace
├── models/
│   ├── user.py           # Modello utente
│   ├── task.py           # Modello task
│   └── palace.py         # Modello Palace
├── db/
│   ├── database.py       # Configurazione DB
│   └── schema.sql        # Schema database
├── ui/
│   ├── dashboard.py      # Dashboard principale
│   └── menus.py          # Menu navigazione
├── analytics/
│   └── charts.py         # Generazione grafici
├── assets/
│   └── ascii_art.py      # Arte ASCII
└── README.md
```

---

## 🎮 Esempi

### Aggiungere una Task
```
Categoria: Knowledge
Difficoltà: Medium
Descrizione: Studiare SQLAlchemy
Deadline: 2024-12-31
```

### Creare un Palace
```
Nome: Master Python
Descrizione: Diventare esperto in Python
Milestone: 10 progetti completati
Scadenza: 2025-06-30
```

---

## 🔮 Roadmap Futura

- [ ] Export dati in CSV
- [ ] Modalità "Hard" (penalità se salti task)
- [ ] Notifiche desktop
- [ ] AI assistant per suggerire task
- [ ] GUI con Tkinter o web con Flask
- [ ] Sistema di achievement avanzato
- [ ] Multiplayer/leaderboard

---

## 📝 License

MIT License - Senti libero di usare questo progetto per il tuo CV!

---

## 👤 Autore

Creato con ❤️ ispirato da Persona 5

**"Take Your Heart"** 🃏

