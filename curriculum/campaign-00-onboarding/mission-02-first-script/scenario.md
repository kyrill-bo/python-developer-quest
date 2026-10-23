## Mission: First Contact

**Rank:** Python Initiate
**Difficulty:** 1/5
**Estimated time:** 15 Minuten
**XP reward:** 10

### Prerequisites
- Environment Recon abgeschlossen.

### Scenario
Jedes Projekt beginnt mit einem lauffaehigen Skript. Du schreibst eine
Funktion, die einen Namen entgegennimmt und eine Begruessung zurueckgibt --
und ein kleines CLI-Script, das diese Funktion nutzt.

### Objectives
- Eine Funktion mit Parameter und Rueckgabewert schreiben.
- Command-line Argumente lesen (Pendant zu `args` in einer Kotlin/Java `main`-Funktion).
- Ein Skript direkt ausfuehrbar machen.

### Requirements
Erstelle `workspace/hello.py` mit:

1. Einer Funktion `greet(name: str) -> str`, die
   `"Hello, {name}! Welcome to Python Developer Quest."` zurueckgibt.
2. Einem ausfuehrbaren Teil, der:
   - ohne Argumente `greet("World")` ausgibt,
   - mit einem Argument (`python3 hello.py Alice`) `greet("Alice")` ausgibt.

### Restrictions
- Keine Interaktion via `input()` -- der Name kommt ausschliesslich ueber
  Command-line-Argumente.
- Kein Exit mit Fehlercode bei fehlendem Argument -- der Default greift.

### Acceptance Criteria
- `python3 workspace/hello.py` gibt eine Zeile mit "Hello" und "World" aus.
- `python3 workspace/hello.py Alice` gibt eine Zeile mit "Hello" und "Alice" aus.
- Exit-Code ist in beiden Faellen 0.

### Submission
`workspace/hello.py`

### Evaluation
`python -m quest check campaign-00-onboarding/mission-02-first-script`
