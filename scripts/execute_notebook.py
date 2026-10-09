"""Execute the untouched uploaded notebook in a separate output directory."""
from pathlib import Path
import os
import sys
import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parents[1]
output = root / "outputs" / "notebook"
output.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", "/tmp/polaris-matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/polaris-cache")
os.environ.setdefault("IPYTHONDIR", "/tmp/polaris-ipython")
os.environ.setdefault("JUPYTER_RUNTIME_DIR", "/tmp/polaris-jupyter-runtime")
notebook = nbformat.read(root / "notebooks" / "POLARIS-X_Colab_Simulation_VERIFIED.ipynb", as_version=4)
client = NotebookClient(notebook, timeout=180, kernel_name="python3", resources={"metadata": {"path": str(output)}})
# Run the kernel with this environment's exact interpreter; no global kernel registration.
client.create_kernel_manager()
client.km.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
client.execute()
nbformat.write(notebook, output / "POLARIS-X_executed.ipynb")
for cell in notebook.cells:
    for result in cell.get("outputs", []):
        if result.output_type == "stream":
            print(result.text, end="")
print(f"Executed notebook and figures: {output}")
