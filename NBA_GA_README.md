# NBA Team Optimization — Genetic Algorithm

A genetic algorithm simulation that evolves NBA team statistics over 200 generations to converge toward playoff-level performance benchmarks.

---

## Project Overview

This project applies a genetic algorithm to optimize NBA team statistics against historical playoff averages. Each generation selects the highest-performing teams based on a fitness function, then applies crossover and mutation operators to evolve the population toward an optimal solution.

---

## How It Works

### Fitness Function
Each team is scored by comparing its statistics against target playoff averages across 6 categories. The closer a team's stats are to the playoff benchmarks, the higher its fitness score. The score is computed as:

```
fitness = 1 / (1 + total_difference)
```

Where `total_difference` is the sum of absolute differences between the team's stats and the playoff averages. A perfect match yields a fitness score approaching 1.

### Playoff Benchmark Targets

| Stat | Playoff Average |
|---|---|
| PPG (Points Per Game) | 116.6 |
| APG (Assists Per Game) | 26.8 |
| OREB (Offensive Rebounds) | 10.4 |
| BLKS (Blocks) | 4.7 |
| STLS (Steals) | 7.3 |
| DREB (Defensive Rebounds) | 33.6 |

### Selection
Each generation selects the top 8 teams by fitness score to serve as parents for the next generation.

### Crossover
Random pairs of selected teams swap a randomly chosen stat, simulating genetic recombination.

### Mutation
One team per generation has a single stat modified by a small random amount drawn from a normal distribution (mean=0, std=1). Stats are clamped to a minimum of 0.

### Simulation
The algorithm runs for 200 generations. Average fitness per generation is tracked and plotted. The top 3 final generations are printed to the console.

---

## Data Source

Team statistics are loaded from a **Google Sheets** spreadsheet named `NBAGA` via the `pygsheets` library using a Google service account.

### Required Sheet Structure

The spreadsheet must contain the following columns:

| Column | Description |
|---|---|
| Team | Team name |
| PPG | Points per game |
| APG | Assists per game |
| OREB | Offensive rebounds |
| BLKS | Blocks |
| STLS | Steals |
| DREB | Defensive rebounds |

---

## Setup

### 1. Install Dependencies

```bash
pip install pygsheets pandas numpy matplotlib
```

### 2. Google Sheets Authentication

This project uses a **Google service account** for authentication.

- Create a project in [Google Cloud Console](https://console.cloud.google.com/)
- Enable the **Google Sheets API** and **Google Drive API**
- Create a service account and download the JSON credentials file
- Share your `NBAGA` Google Sheet with the service account email

### 3. Configure Credentials Path

Update the path to your service account JSON file in the script:

```python
gc = pygsheets.authorize(service_file='path/to/your/credentials.json')
```

> **Note:** Never commit your credentials JSON file to version control. Add it to `.gitignore`.

---

## Usage

```bash
python genetic_algorithm.py
```

The script will:
1. Load team data from Google Sheets
2. Run 200 generations of selection, crossover, and mutation
3. Print the top teams from the final 3 generations
4. Display a plot of average fitness score per generation

---

## Output

**Console:** Top 8 teams by fitness score for generations 198, 199, and 200.

**Plot:** Line chart showing average fitness score across all 200 generations — a rising curve indicates the population is converging toward playoff-level performance.

---

## Dependencies

| Library | Purpose |
|---|---|
| pygsheets | Google Sheets API integration |
| pandas | Data loading and manipulation |
| numpy | Numerical operations and mutation sampling |
| matplotlib | Fitness score visualization |
| random | Selection and crossover randomization |

---

## Author

**Malik Freeman**  
M.S. Software Engineering — Mercer University
