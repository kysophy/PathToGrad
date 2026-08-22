# Curriculum data

Canonical inputs for the demo database. **Do not hand-edit the CSV files.** Change the generator and re-run it.

| File | Role |
|---|---|
| `Courses.csv` | Normalized curriculum (GEN + specializations) |
| `offerings.csv` | Synthetic timetable for demo term `2026.1` (`term_type = Semester2`; covers GEN semesters 2, 5 and SE semester 8 — see C-01 in `DECISIONS.md`) |
| `prepare_curriculum.py` | Builds `Courses.csv` from `Materials and Notes/Courses.raw.csv` (that raw dump is local, not in git) |
| `generate_offerings.py` | Builds `offerings.csv` from `Courses.csv` |

```powershell
# from this folder, after Courses.raw.csv is in place
python prepare_curriculum.py
python generate_offerings.py
```

Then load into MySQL from `src/backend`:

```powershell
python -m app.scripts.import_courses
```

Modelling rules these files encode (mandatory `CSC*`/`MTH*`, required credits 138, half-open meeting times, and so on) are in [`docs/DECISIONS.md`](../docs/DECISIONS.md).
