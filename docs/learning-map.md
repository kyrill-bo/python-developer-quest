# Learning Map

Uebersicht aller 15 Campaigns. Details, Topics und Boss-Fight-
Beschreibungen stehen in `curriculum/campaign-XX/campaign.json` bzw. per
`python -m quest campaign <id>`.

| # | Campaign | Status | Haupt-Skill-Tracks |
|---|---|---|---|
| 0 | Developer Onboarding | **Implementiert** (7 Missionen) | Python Core, Testing |
| 1 | Python Fundamentals | **Implementiert** (10 Missionen + Projekt + Boss) | Python Core |
| 2 | Advanced Python | Geplant | Python Advanced |
| 3 | REST API Engineer (FastAPI) | Geplant | FastAPI, Testing |
| 4 | Database Engineer | Geplant | Databases, Testing |
| 5 | Django & DRF | Geplant | Django, Databases |
| 6 | Asynchronous Python | Geplant | Async |
| 7 | Microservices Architect | Geplant | Microservices, FastAPI |
| 8 | Message Brokers (RabbitMQ/Kafka) | Geplant, benoetigt Docker | Messaging |
| 9 | Data Pipelines / Data Engineering | Geplant | Data Engineering, Databases |
| 10 | Testing & Software Quality | Geplant | Testing |
| 11 | Docker, Kubernetes, CI/CD | Geplant, benoetigt Docker | Containers |
| 12 | Security & Production Reliability | Geplant | Security, Observability |
| 13 | System Design & Senior Engineering | Geplant | System Design |
| 14 | Capstone: Fleet Analytics Platform | Geplant | System Design, Data Eng., Microservices |

## Einordnung (essenziell vs. spezialisiert)

- **Essenziell fuer jede Python-Backend-Rolle:** Campaigns 0-4, 10 (Testing
  zieht sich durch alle Campaigns).
- **Senior-Level-Engineering:** Campaign 2 (Advanced), 7, 12, 13.
- **Data-Engineering-Schwerpunkt** (fuer deine Zielrolle besonders
  relevant): Campaign 9, 14.
- **Infrastruktur/Plattform:** Campaign 11 (Docker/K8s/CI-CD).
- **Framework-spezifisch:** Campaign 3 (FastAPI) vs. Campaign 5 (Django/DRF)
  -- beide werden behandelt, FastAPI zuerst, Django als zweite Perspektive.
- **Spezialisierung/optional je nach Zielrolle:** Campaign 8 (Messaging,
  RabbitMQ *und* Kafka im Vergleich).

## Reihenfolge und Abhaengigkeiten

Siehe `prerequisite_campaigns` in jeder `campaign.json`. Grob:

```
0 -> 1 -> 2 -> {3, 4} -> {5, 6} -> 7 -> {8, 9, 10} -> 11 -> 12 -> 13 -> 14
```

Campaigns ohne erfuellte Voraussetzungen erscheinen in `quest map` als
GESPERRT, auch wenn sie bereits "geplant" (inhaltlich vorbereitet) sind.
