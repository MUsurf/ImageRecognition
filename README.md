# ImageRecognition
Repository to hold code working on image recognition tasks

- `./classes` python files of classes to be used in files
  - `compass.py` is a pygame module to draw a compass when passed an angle
  - `helper.py` is a module to add helper functions like combining a mask and frame
- `./docs` documentation
  - `Miniconda.md` basic miniconda write up
- `./orange_oblong_detection` directory of programs related to bounding orange shapes
  - `orange_oblong_detection.py` derives movements from orange shape
  - `orange_oblong_line_draw.py` derives a direction as line to draw on top
  - `Convexity.py` derives an angle from a shape (UNFINISHED)
- `./test_images` images for testing the scripts
  - `mask.png` is a quick example of continuous oblong
  - `maskBent.png` is a quick example of bent oblong
- `cameraCheck.py` script to ensure pygame can access camera
- `README.md` this file
- `requirements-conda.txt` conda environment installed with `conda create --name opencv3.12 --file requirements-conda.txt` 
- `requirements.txt` python pip packages to install with `pip install -r requirements.txt`

## Todo
- [ ] Separate Detection into its own class
- [ ] Support Contour Detection for bent sticks [Docs](https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html)
  - [ ] Finish `Convexity.py`
- [ ] Thorough Documentation
- [ ] Ensure Compatibility with Sub Controls
- [ ] StandArdiZe capitalIZATIOn

## Docs
- [Miniconda](./docs/Miniconda.md)
- 
### TL;DR SURF Setup
- `git clone https://github.com/MUsurf/ImageRecognition` to download files
- `cd ImageRecognition` to go into ImageRecognition folder
- `conda init` (If first use of Conda)
- `conda create --name myenvname python=3.12` to create anaconda environment
- `conda activate myenvname` to enter the virtual environment
- `pip install -r requirements.txt` install required libraries
- **WHEN FINISHED** `conda deactivate` to exit the virtual environment
  - Run `conda activate myenvname` to "re-enter" the virtual environment with relevant modules