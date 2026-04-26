# 2D Plane streess/Plain strain Finite Element Analysis (FEA) Solver

An interactive, Python-based Finite Element Analysis (FEA) solver with a Streamlit graphical interface. This application solves 2D solid mechanics problems under Plane Stress and Plane Strain conditions using 3-node Constant Strain Triangles (CST).

**Live Demo:** [https://www.youtube.com/watch?v=doo5pnxTVNY](<https://civl-537-fea-solver-omarceentayyab.streamlit.app/>)

## 🚀 Features

* **Cantilever Beam Simulation:** Validates FEA displacements against analytical Timoshenko beam theory. Includes automated mesh convergence studies (log-log plotting).
* **Plate with a Circular Hole:** Simulates stress concentrations and validates against Kirsch analytical equations. Uses transfinite interpolation for quarter-symmetry mesh generation.
* **Interactive Visualizations:** Powered by Plotly. View node/element meshes, deformed shapes, and detailed stress distribution plots along specific boundaries.
* **Volumetric Locking Analysis:** Demonstrates numerical breakdown limits of CST elements as materials approach incompressibility ($\nu \to 0.5$).
* **Data Export:** One-click export of global nodal coordinates, displacements, and calculated stresses to CSV.

## 🛠️ Installation & Running

This application can be run locally using standard Python or via a containerized Docker environment.

### Option 1: Running with Docker (Recommended)
Ensure Docker Desktop is installed and running on your machine.

1. Open Bash Terminal.. Ensure you have the correct directory loaded. If uncertain use, the following command. 
    cd "C://user//...///.... //.. My project folder"
2. Write docker compose up.
3. Ensure the requirements.txt file is upto date and added to the  path.
4. Go to http://localhost:8501/ to see your containirzed local app hosted on your PC.
5. Hit Ctrl + C and type up docker compose up to have changes reflect in your local host. 

### Option 2: Expert only (No explanation needed)

# Running TESTS:
There are three stages or milestones for which tests are made available.. 

1) Elements - Once module is ready, run docker compose run fea-solver pytest tests/test_elements.py -v
2) Assembly, - Once module is ready, run docker compose run fea-solver pytest tests/test_assembly.py -v
3) Solver, - Once module is ready, run docker compose run fea-solver pytest tests/test_solver.py -v