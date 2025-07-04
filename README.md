# IA_2023_Homework – Artificial Intelligence Projects Collection

This repository contains multiple AI-focused projects developed during an Artificial Intelligence course. Each subfolder demonstrates a different AI concept or algorithm, ranging from neural networks to reinforcement learning and game-solving agents.

---

## 🗂️ Project Structure

```
IA_2023_Homework-main/
├── MatrixSorterIA/       # C# application for intelligent matrix ordering
├── NumberScrabble/       # Python game agent (rule-based or search-based)
├── RLIA/                 # Q-learning based reinforcement learning agent
├── ReteaNeuronalaIA/     # Neural network trained on a seed classification dataset
├── SudokuIA/             # C# Sudoku solver, possibly using CSP or backtracking
```

---

## 🧠 Projects Overview

### ✅ MatrixSorterIA
- **Language**: C#
- **Files**: `.sln` and `.csproj` solution files
- Implements intelligent sorting logic for matrix data (likely using heuristics or rule systems)
- Built in Visual Studio environment

### ✅ NumberScrabble
- **Language**: Python
- **main.py**: Likely simulates the "Number Scrabble" game (a numerical variant of Tic-Tac-Toe)
- May use basic adversarial search or decision trees

### ✅ RLIA
- **Language**: Python
- **QLearn.py**: Core Q-learning algorithm
- **Environment.py**: Custom environment for training the agent
- **main.py**: Entry point for training/testing

### ✅ ReteaNeuronalaIA (Neural Network on Seeds Dataset)
- **Language**: Python
- **Core Files**:
  - `datasetExtractor.py`, `instance.py`: Handle dataset preparation
  - `neuralNetworkUtils.py`, `trainingNeuralNetwork.py`: Manual neural net training implementation
- **Dataset**: `seeds_dataset.txt` – likely based on UCI Seeds Dataset (classification task)
- No external libraries used (built from scratch)

### ✅ SudokuIA
- **Language**: C#
- **Files**: Visual Studio solution
- Likely implements backtracking or constraint propagation to solve Sudoku puzzles

---

## 🛠️ Tech Stack

- **Python 3**
  - Manual ML & RL implementations
  - No TensorFlow or PyTorch used
- **C# (.NET / Visual Studio)**
  - Used for GUI-based or logic-heavy applications (MatrixSorter & Sudoku)

---

## ▶️ Running Instructions

### Python Projects
Navigate to the respective folder and run `main.py`:

```bash
cd RLIA
python3 main.py
```

### C# Projects
Open the `.sln` file in **Visual Studio** and run the project.

---

## 🎯 Educational Value

This project collection is ideal for students and educators looking to explore:
- Manual implementation of AI algorithms
- Classic problem-solving techniques (search, backtracking, heuristics)
- Reinforcement learning logic from scratch
- Neural networks without external frameworks
