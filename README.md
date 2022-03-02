# optoDroplet image analysis 

**Purpose**: 

Analysis of confocal images of cells expressing optoDroplet construct to extract pixel intensities before and after activation.

**Cell Types tested**: 

- Neuro-2a 

**Instrument/techniques**:

- Confocal microscopy datasets at 63X zoom obtained using Leica SP5 confocal microscope

**Data produced:** 

- LIF files extracted to TIFF stacks using auxillary ImageJ scripts (LIF_to_TIFF.ijm file in analysis_scripts folder)
- From TIFF stacks, outline cells and optionally nuclei, then assign pixels for individual cells and their xy coordinates.
- Export this is pandas dataframe/csv for further processing

**Analysis:** 

- Downstream applications include:
  - Determine diffuse/concentrated phase pixels in different model proteins of interest in collaboration with Kiersten Ruff (Washington State)

**Getting started:**

- All dependancies can be found in the ```environment.yml``` file. To install these automatically into a new conda environment:

```conda env create -f environment.yml```

- After installation, don't forget to activate your new environment (```conda activate cellpose```)
- You can then check out the example notebooks to see the scripts in action

**References/Resources:** 

- CellPose [homepage](http://www.cellpose.org/), [documentation](https://cellpose.readthedocs.io/en/latest/) and [repository](https://github.com/MouseLand/cellpose)

- Napari [repository](https://github.com/napari/napari), [documentation](https://napari.org/docs/) and [tutorials](https://napari.org/tutorials/)