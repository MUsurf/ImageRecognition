# Miniconda Overview
## What is Miniconda? [^1]
- A minimal "Anaconda" Python distro, the necessary components to run Python and manage packages
	- CLI tool to simplify installation and management of software dependencies
### Virtual Environments
- Isolated environments that allow separate installs of Python and packages for different projects
- This avoids conflicts in versions of packages and ensures easier project setup
## Installation
- [Miniconda — Anaconda documentation](https://docs.anaconda.com/miniconda/)
- To verify installation run `conda --version`
## Use
### Create a New Virtual Environment (venv)
- `conda create --name myenv`
	- `conda create -n myenv python=3.9` for a specific python version
- After creating a venv you next need to activate it to use it
	- Windows: `conda activate myenv`, macOS and Linux: `source activate myenv`
- To return to global python you must deactivate
	- Windows: `conda deactivate`, macOS and Linux: `source deactivate`
### Packages
- Packages can be installed to the activated venv
	- e.g., `conda install numpy` or `pip install pandas`
- Update will update the packages in an environment and removes unneeded dependencies
	- `conda env update --file environment.yml --prune`
### Reproducibility
#### Built-In (Platform Dependent)
- `conda list --explicit` produces a spec list of all the environment facts
- `conda list -e > requirements-conda.txt` outputs this two a text file
	- `conda create --name myenv --file requirements-conda.txt` can be used to create an environment from that text file
	- `conda install --name myenv --file requirements-conda-txt` alternatively installs the packages to myenv
- `pip freeze > requirements.txt` creates a text file listing all installed packages
  - `pip install -r requirements.txt` installs the listed packages
- <mark style="background: #FF5582A6;">This only works between the same platform</mark>
#### Stack Overflow (Platform Independent)[^2]
- `conda env export --from-history > environment.yaml` produces a less dependent list
	- <mark style="background: #FF5582A6;">Some code specific packages or pip installed packages may have issues</mark>
### VS Code [^4]
- Set the Python Interpreter
  - Ctrl/Cmd + Shift + P: "Python: Select Interpreter", Select `Python #.#.# ('name') ~\miniconda`
  - Select Python Interpreter on Status Bar

---
# References
[^1]: [A Comprehensive Tutorial on Miniconda: Creating Virtual Environments and Setting Up with VS Code | by Amina Saeed | Medium](https://medium.com/@aminasaeed223/a-comprehensive-tutorial-on-miniconda-creating-virtual-environments-and-setting-up-with-vs-code-f98d22fac8e2)
[^2]: [build - Managing conda env in cross platform environment - Stack Overflow](https://stackoverflow.com/questions/58009732/managing-conda-env-in-cross-platform-environment)
[^3]: [Managing environments — conda 24.7.2.dev75 documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
[^4]: [How to activate conda environment in VS code](https://medium.com/@udiyosovzon/how-to-activate-conda-environment-in-vs-code-ce599497f20d)