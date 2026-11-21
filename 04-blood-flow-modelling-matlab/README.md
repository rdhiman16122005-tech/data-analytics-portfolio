# Blood Flow Modelling in Stenosed Arteries (MATLAB)

Numerical study of how a narrowing (stenosis) changes wall shear stress, velocity profiles and
pressure gradient when blood is modelled as a **non-Newtonian (shear-thinning) power-law fluid**.

## Model
Steady, axisymmetric, fully developed flow in a slowly varying tube. Blood: `tau = K (du/dr)^n`.
Stenosis: cosine-shaped narrowing with severity `delta` (fraction of radius lost).
The script solves for the local pressure gradient and wall shear stress along the artery and
checks the solution by recovering the flow rate `Q` numerically.

## What the script produces (`./outputs`)
- Geometry, wall shear stress and pressure-gradient plots (power-law vs Newtonian)
- Velocity profiles at the throat vs a healthy section
- Sensitivity analysis over stenosis severity and viscosity (`sensitivity_results.csv`)

## Run it
Open `stenosis_powerlaw_flow.m` in MATLAB (R2016b or later) and press **Run**.

## Notes
- This is a simplified reference model. Add your own governing equations, boundary conditions
  and results from your research project, and cite the source papers you used.
- Manuscript source (LaTeX) can live in a `/paper` folder.
