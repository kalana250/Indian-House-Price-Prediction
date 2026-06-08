# Capstone Proj 1 — Notebook-Only Activity Guide (IDET Assessment)

Purpose: Provide a sequenced set of notebook tasks for contributors who may only edit `NOTEBOOK/indian-house-price-prediction.ipynb`. Each task is self-contained in the notebook and demonstrates an end-to-end pipeline understanding without changing repo production code.

Audience & Constraints
- Audience: IDET students/assessees who can only edit the notebook.
- Constraint: Do not modify files outside `NOTEBOOK/`. Use existing artifacts in the repository (`artifacts/`, `artifact/`, `city_locality.npy`) for inputs and demonstrations.

How to submit
- Deliverable: updated `NOTEBOOK/indian-house-price-prediction.ipynb` containing completed tasks, output screenshots saved in the notebook, and a final markdown summary cell.
- Optionally include a short (<=3 min) screencast showing the notebook run and results.

Assessment workflow (ordered tasks)
1. Setup & quick run (5–10 min)
   - Add a top-level markdown cell describing purpose and environment.
   - Add a code cell that lists key repository files and verifies availability of required artifacts, e.g., check `artifacts/preprocessor.pkl` and `artifacts/model.pkl`.
   - Run a quick prediction using `src.pipeline.predict_pipeline.CustomData` and `PredictRecommendPipeline` and show the output.

2. Exploratory Data Analysis (20–40 min)
   - Load `artifact/Dataset.csv` (or `artifacts/recommend_data.csv`) and produce: data shape, missing-value table, 3 key univariate plots, and 1 small cross-tab or pairwise relation relevant to price.
   - Add short markdown interpretation for each figure (1–2 sentences).

3. Preprocessing demonstration (20–30 min)
   - Recreate the preprocessing transformations used in `src/` as small, re-implemented notebook cells (do not import or edit `src/` unless reading). Example: simple encodings for `propertyType`, `furnishing`, `city`, and numeric casts for `bedrooms`/`bathrooms`.
   - Show transformed example rows and confirm shape matches what `artifacts/preprocessor.pkl` expects (a sanity check).

4. Train a small baseline model (30–60 min)
   - On a small subset (e.g., 5–10% or a sampled subset) of the dataset, train a compact model (e.g., scikit-learn `RandomForestRegressor` or `XGBRegressor` with few trees). Keep training quick so CI-like checks aren't required.
   - Evaluate with RMSE and R^2 on a holdout split. Present metrics in a table.
   - Save model to a temporary in-notebook file (e.g., `./tmp_notebook_model.pkl`) — do not add files to repository permanently.

5. Model integration & prediction parity (15–30 min)
   - Use the trained baseline model to produce a prediction for the same input used in Task 1 and compare to the production model's prediction (from `PredictRecommendPipeline`). Report differences and a short explanation.

6. Recommendation demo (15–20 min)
   - Call `PredictRecommendPipeline().recommend()` with an example input and show the recommended rows (use `artifacts/recommend_data.csv`).
   - Add a markdown cell interpreting the `distances` or similarity measure.

7. Robustness checks & edge cases (15–30 min)
   - Demonstrate 3 edge cases: missing locality, unknown city, extreme bedrooms count. Show predictions or graceful failures and write short notes on expected behavior.

8. Final summary & reflection (10–15 min)
   - One markdown cell summarizing work done, key metrics, limitations, and next steps (if you had push access to `src/`).

Checkpoint deliverables
- Submit the updated notebook that includes the completed tasks and outputs for each numbered task above.
- Required visible outputs: at least 3 plots, a metrics table, prediction comparison (baseline vs production), recommendation sample, and robustness examples.

Grading rubric (suggested)
- Completed quick run & prediction: 10 pts
- EDA clarity and interpretation: 20 pts
- Preprocessing demonstration correctness: 15 pts
- Baseline training and evaluation: 20 pts
- Integration comparison with production model: 15 pts
- Recommendation demo & interpretation: 10 pts
- Robustness checks and final summary: 10 pts

Notes & tips
- Keep code cells small and focused; each task should be runnable independently (use small sample sizes for training to keep runs fast).
- Do not modify any `src/` files, tests, or `Dockerfile`. If a cell needs a package not in `requirements.txt`, document it in the submission and include a short justification.
- If any required artifact from `artifacts/` is missing, document the exact missing file and how you would proceed; show partial results using local sampling instead.

Estimated total time: 3–6 hours depending on sampling and plotting choices.

Extensions (optional, not required)
- Add a lightweight visualization dashboard inside the notebook (plotly) to show prediction vs actual distributions.
- Add a short reproducible script cell that replays all analysis end-to-end using a single `run_all()` function.
From notebook analysis to a complete E2E project (notebook-only workflow)
- Purpose: Some contributors only have permission to edit the notebook but are expected to deliver a complete end-to-end project that matches the repository's strict structure. This section explains how to do that without writing to repository files directly.

- Key rule: Do not modify repository files outside `NOTEBOOK/`. Instead, produce a self-contained *submission package* inside the notebook (a local directory `submission_package/` or a downloadable `.zip`) that contains the full E2E project files mirroring the canonical layout. The instructor or maintainer will extract and integrate the package into the repo.

- Required steps inside the notebook:
  1. Analysis first — mandatory
     - Thoroughly analyze `artifact/Dataset.csv` (or `artifacts/recommend_data.csv`) and the notebook itself to understand inputs, preprocessing, and model expectations. Document findings in a clear markdown cell.
     - Confirm which artifact files are required (list file names and sizes) and whether any expected artifact is missing.

  2. Design mapping — mandatory
     - Create a mapping table (markdown or DataFrame) that lists every file the final project will contain, its path in the canonical layout, and a short description (purpose, dependencies). Example row: `src/pipeline/train_pipeline.py | training orchestration script | reads artifacts/processed_data.csv`.

  3. Implement generation cells — mandatory
     - Add code cells that programmatically write the content of every required source file into a `submission_package/` directory when executed. Each generated file should contain the exact code (or a clear runnable stub) required to reproduce the project behavior.
     - For large binary artifacts (models, preprocessor pickles), if you cannot recreate them in-notebook, include placeholder steps and scripts that show how to re-run preprocessing and training to reconstruct them. Provide a small sample model trained on a subset saved into `submission_package/artifacts/` for demonstration only.
     - Ensure all generated files use the canonical file paths inside `submission_package/` (mirror the repo root structure).

  4. Package & deliver — mandatory
     - Add a final cell that zips `submission_package/` into `submission_package.zip` and displays its size and top-level contents.
     - Include a top-level `INSTRUCTIONS.md` inside the package with clear steps for the maintainer to integrate the package into the repository (where to copy files, how to run a smoke test, and which artifacts are placeholders).

  5. Dockerfile as final packaging step — mandatory
     - The `Dockerfile` must be included inside the package at root level and should match the canonical `Dockerfile` behavior described in `CAPSTONE_PROJ_1_GUIDELINES.md` (EXPOSE 5000 and start the app). The `Dockerfile` must be the last file in the package creation order and a short validation cell should attempt a local `docker build` command (optional — only if Docker is available in the environment).

  6. Validation & smoke run — recommended
     - Provide a smoke-run script (inside `submission_package/ci/` or as `run_smoke.sh`) that performs quick checks: install `requirements.txt` in a venv, run `python app.py` for a few seconds and call `/api/city_arr` and `/` routes to confirm basic functionality.

Checklist for submission package
- `submission_package/README.md` — integration steps and assumptions
- full `src/` directory mirroring production code
- `artifacts/` with either real small artifacts or rebuild scripts
- `Dockerfile` at package root (final item)
- `INSTRUCTIONS.md` for maintainers
- `submission_package.zip` created by the notebook

Grading adjustments for package workflow
- Analysis & design mapping: 25 pts
- Correct file mapping and completeness of package: 25 pts
- Generated code correctness and runnable stubs: 20 pts
- Dockerfile included and correct: 15 pts
- Packaging & clear integration instructions: 15 pts

---
Follow these steps when you must deliver a full E2E project from the notebook only. If you want, I can add a starter notebook cell template that: (a) checks artifact availability, (b) creates `submission_package/` and writes one example file (`submission_package/README.md`) so you can see the pattern. Want me to add that starter cell? 

Quick Action Plan — Analyze dataset and create E2E package
1. Verify artifacts and notebook
   - In a top cell run: list files `!ls -al ../artifacts ../artifact city_locality.npy` and import `src.pipeline.predict_pipeline` to confirm runtime imports work.
2. Reproduce a prediction (smoke run)
   - Use `CustomData` + `PredictRecommendPipeline()` to call `.predict()` and `.recommend()` on one example; capture outputs and logs.
3. Rapid EDA (15–30 min)
   - Load `artifact/Dataset.csv` or `artifacts/recommend_data.csv`; show `df.shape`, `df.info()`, missing-value counts, and 3 small plots (histogram of price, counts of `propertyType`, boxplot bedrooms vs price).
4. Minimal preprocessing stub
   - Implement a small transform cell that encodes categorical columns and casts numeric columns; run it on a few rows and show the result.
5. Small baseline model (demo)
   - Train a tiny `RandomForestRegressor(n_estimators=10)` on a sampled subset; evaluate RMSE on a holdout; save to `submission_package/artifacts/sample_model.pkl`.
6. Build submission package files programmatically
   - In notebook cells, create `submission_package/` and write: `README.md`, `INSTRUCTIONS.md`, `src/` stubs (train script, predict pipeline), `artifacts/` (sample model, sample preprocessor), and `Dockerfile`.
7. Zip and report
   - Zip `submission_package/` to `submission_package.zip`, print size and tree, and include a short integration checklist in `INSTRUCTIONS.md`.
8. Optional smoke validation
   - If environment allows, run the smoke script that starts `python submission_package/app.py` and calls `/api/city_arr` to validate basic runtime.

Use this plan as a compact checklist — follow each step inside `NOTEBOOK/indian-house-price-prediction.ipynb` with self-contained cells. Say "Add starter cell" if you want me to insert the top verification + package-creation example cell into the notebook.

Instruction to contributors — analyze notebook and build full E2E project (no notebook edits required)
- Primary requirement: Analyze the existing notebook and dataset, then independently produce a complete end-to-end project that matches the canonical repository layout. You are NOT required to edit `NOTEBOOK/indian-house-price-prediction.ipynb` — make changes there only if you choose to, but it is not mandatory.
- Deliverable options (choose one):
   1. A `submission_package.zip` created locally that mirrors the canonical layout and contains all source files, artifacts (or rebuild scripts), `Dockerfile`, and `INSTRUCTIONS.md` for maintainers; OR
   2. A public Git branch/PR (preferred when possible) that adds the full E2E project files to a fork of the repository following the canonical layout.
- Required contents: working `src/` code (train/predict/recommender), `artifacts/` or rebuild instructions, `requirements.txt`, `Dockerfile` configured to run the app, and `INSTRUCTIONS.md` describing how to run a smoke test.
- Keep the notebook as a reference but do not depend on it: the maintainer should be able to run your package or PR and reproduce the basic app behavior (`/api/city_arr`, `/` homepage) using the included artifacts or rebuild steps.
- If you choose to provide a `submission_package.zip`, include a small sample model (trained on a subset) so reviewers can run a smoke test without retraining full models.

This instruction is the canonical ask: analyze the notebook and dataset, then produce a standalone, runnable E2E project package or PR — no changes to the original notebook are necessary.

---
Follow this activity guide as the assessment checklist. If you want, I can add a starter top cell to the notebook that implements Task 1 (quick run & verification). Tell me if you want that starter cell added.
