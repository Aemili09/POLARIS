from io import StringIO
import json
import numpy as np
import pytest
from numpy.testing import assert_allclose
from polaris.mechanics import kirsch
from polaris.data import stress_csv, read_stress_csv
from polaris.cli import main


def test_csv_roundtrip_and_invalid_grid():
    field = kirsch(nx=31, ny=21)
    csv = stress_csv(field)
    restored = read_stress_csv(StringIO(csv))
    assert_allclose(restored.delta_sigma_mpa, field.delta_sigma_mpa, atol=1e-12)
    assert_allclose(restored.outside, field.outside)
    with pytest.raises(ValueError):
        read_stress_csv(StringIO('\n'.join(csv.splitlines()[:-1])))
    with pytest.raises(ValueError):
        read_stress_csv(StringIO(csv+csv.splitlines()[1]+'\n'))


def test_csv_nonuniform_grid_rejected():
    import pandas as pd
    df = pd.read_csv(StringIO(stress_csv(kirsch(nx=5, ny=5))))
    df.loc[df.x_mm == 25, "x_mm"] = 24
    with pytest.raises(ValueError, match="uniformly spaced"):
        read_stress_csv(StringIO(df.to_csv(index=False)))


def test_cli_artifacts_and_import(tmp_path):
    output = tmp_path / "demo"
    main(["simulate", "--nx", "41", "--ny", "21", "--output", str(output)])
    for name in ("POLARIS_X_Main_Results.png", "POLARIS_X_Analyzer_Sweep.png", "simulation.npz", "stress_field.csv", "summary.json"):
        assert (output/name).stat().st_size > 100
    with np.load(output/"simulation.npz", allow_pickle=False) as archive:
        assert archive["rgb_linear"].shape == (21, 41, 3)
        assert json.loads(str(archive["metadata_json"]))["analyzer_deg"] == 90
    main(["simulate", "--model", "csv", "--input", str(output/"stress_field.csv"), "--output", str(tmp_path/"import")])
    main(["reconstruct", str(output/"simulation.npz"), "--output", str(tmp_path/"inverse.npz")])
    with np.load(tmp_path/"inverse.npz") as inverse:
        assert inverse["valid"].any()
