# SmartCalc Pro

SmartCalc Pro is a desktop scientific calculator built with Python and Tkinter. It combines a traditional calculator with a local math assistant powered by SymPy.

## Features

- Arithmetic, parentheses, powers, percentages, factorials, square roots, logarithms, and trigonometry
- DEG/RAD angle modes
- Calculator memory and previous-answer support
- Calculation history
- Natural-language percentage and square-root questions
- Basic one-variable equation solving, such as `2*x + 3 = 7`
- Average/mean queries and common length, mass, and temperature conversions

## Run

Use Python 3.10 or newer:

```powershell
python -m pip install -r requirements.txt
python src\main.py
```

Run the regression tests with:

```powershell
python -m unittest discover -s tests -v
```

## Next development milestones

1. Move the calculation engine out of the Tkinter window into a tested service.
2. Replace string-based factorial handling with a tokenized expression parser.
3. Add persistent history and memory using a small JSON or SQLite store.
4. Add assistant intents for unit conversion, statistics, finance, and step-by-step explanations.
5. Add accessibility improvements, responsive sizing, and a clear error/status model.
