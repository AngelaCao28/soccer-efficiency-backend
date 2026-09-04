# Soccer Match Efficiency Analysis Backend

The analytical backend of an interactive visual analytics system for the in-depth analysis of soccer match efficiency.

This repository contains the Python implementation for processing team and match data, estimating the influence of performance indicators, and serving analytical results to the [React frontend](https://github.com/AngelaCao28/soccer-efficiency-system).

## Overview

Match efficiency characterizes how effectively a team creates or defends goal chances during a match. The backend analyzes three complementary dimensions:

- **Offensive efficiency:** The number of shots on target produced by a team per unit of its possession time. A higher value indicates more effective offense.
- **Defensive efficiency:** The number of shots on target produced by the opponent per unit of the opponent's possession time. A lower value indicates more effective defense.
- **Net efficiency:** The difference between offensive and defensive efficiency.

For a selected team, the backend trains separate random-forest regression models to predict offensive, defensive, and net efficiency from team performance indicators and the opponent's match efficiency. The feature importance values are used as weights to characterize how individual factors influence each dimension of match efficiency.

The backend also returns team summaries and match-level efficiency records for interactive exploration in the frontend.

## Main Components

| File | Description |
| --- | --- |
| `server.py` | Defines the Flask application and API endpoints. |
| `impact_factor.py` | Trains the regression models and calculates the influence of team indicators and opponent efficiency. |
| `team_detail.py` | Collects match-level efficiency records for selected teams. |
| `league_info.py` | Processes league-level team information. |
| `impact_factor_evaluation.py` | Evaluates the fitted indicator models across teams. |
| `utilities.py` | Provides shared data-loading and lookup functions. |
| `frontend-data/` | Contains the preprocessed JSON data used by the backend and frontend. |

## Technology Stack

- Python
- Flask and Flask-CORS
- NumPy and pandas
- scikit-learn

## Getting Started

### Prerequisites

- Python 3 (tested with 3.12.13)
- pip

### Installation

```bash
git clone https://github.com/AngelaCao28/soccer-efficiency-backend.git
cd soccer-efficiency-backend

python -m venv .venv
source .venv/bin/activate
pip install flask flask-cors numpy pandas scikit-learn
```

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\activate
```

### Running the Server

```bash
python server.py
```

The Flask service will run at [http://localhost:5050](http://localhost:5050).

Both API endpoints were tested successfully with Python 3.12. The optional evaluation script `impact_factor_evaluation.py` additionally requires `openpyxl` for Excel output.

## API Endpoints

### `POST /indicatorInfo`

Returns team information and the estimated influence of performance indicators and opponent match efficiency.

Example request:

```json
{
  "LeagueName": "england",
  "TeamName": "Manchester City",
  "TeamId": 1625
}
```

The response contains:

- a summary of the selected team's playing style and match results;
- average performance-indicator values and their influence on offensive, defensive, and net efficiency; and
- the estimated influence of the opponent's match efficiency.

### `POST /detailInfo`

Returns match-level offensive, defensive, and net efficiency records for a selected team.

Example request:

```json
{
  "LeagueName": "england",
  "TeamName": "Manchester City",
  "TeamId": 1625
}
```

## Data

The main data covers the five major European soccer leagues in the 2017/18 season:

- English Premier League
- Spanish La Liga
- German Bundesliga
- Italian Serie A
- French Ligue 1

The repository also includes preprocessed data for UEFA Euro 2020.

## Related Repository

- [soccer-efficiency-system](https://github.com/AngelaCao28/soccer-efficiency-system): React frontend for interactive match efficiency analysis.

## Author

[Anqi Cao](https://angelacao28.github.io/)
