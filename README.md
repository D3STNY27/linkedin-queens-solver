# LinkedIn Queens Solver

🚀 **LinkedIn Queens Solver** is a Python project that automatically solves "Queens" puzzles by LinkedIn mini-games.  
It places queens on a grid according to the puzzle rules without conflicts.

It combines:
1. Anaytical Solving (Follow the constraints of the puzzle and place queens also removing cells where queen cannot be placed)
2. Backtracking (Although linkedin queens can be solved with analytical solution most of the times, backtracking is added if there is incomplete analytical solution)

Note - Queens-Game is a similar website where queens puzzles are available but they usually contain more than 1 solution where backtracking is required~

---

## 🧩 Project Structure

- `src/` — Core logic and solver implementation and unit-tests
- `.gitignore`
- `README.md`

---

## 📋 Features

- **Automatic Grid Solver**: Efficiently solves Queens puzzles. It can solve 100 grids in around 1 second on average (as per unit-testing)
- **Customizable**: Supports both "Official LinkedIn Queens" & "Queens Game" sources.
- **Lightweight & Fast**: Minimal dependencies, quick execution.
- **Modular Python Code**: Clean and easy to extend.

---

## ⚙️ Setup Instructions

1. **Clone the repository**

    ```bash
    git clone https://github.com/D3STNY27/linkedin-queens-solver.git
    cd linkedin-queens-solver
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Solver**

    ```bash
    cd src/app
    python run.py
    ```

---

## 🧪 Running Unit Tests

Unit tests are available to validate the solver logic:

```bash
cd src
python -m pytest
```