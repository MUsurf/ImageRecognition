# ImageRecognition
Repository to hold code working on image recognition tasks

- `./classes` python files of classes to be used in files
  - `compass.py` is a pygame module to draw a compass when passed an angle
- `./docs` documentation
  - `Miniconda.md` basic miniconda write up
- `./orange_oblong_detection` directory of programs related to bounding orange shapes
  - `orange_oblong_detection.py` derives movements from orange shape
  - `orange_oblong_line_draw.py` derives a direction as line to draw on top
- `./test_images` images for testing the scripts
  - `mask.png` is a quick example of continuous oblong
  - `maskBent.png` is a quick example of bent oblong
- `cameraCheck.py` script to ensure pygame can access camera

## Todo
- [ ] Separate Detection into its own class
- [ ] Support Contour Detection for bent sticks [Docs](https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html)
- [ ] Thorough Documentation
- [ ] Ensure Compatibility with Sub Controls
- [ ] StandArdiZe capitalIZATIOn

## Docs
- [Miniconda](./docs/Miniconda.md)