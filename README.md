## Dyenamic 
### DOI: 10.5281/zenodo.4264592

The Dyenamic is an open-software designed to investigate gravity currents generated in laboratory tanks, providing a set of tools to estimate many physical parameters as time-series data, including gravity current speed, Froude number, mixing length, and many others. Users also can work with erodible beds, in which, based on gray-scale values, the software distinguishes the gravity current from the sediment particles, and can compute many variables to analyze the dynamic of sediment caused by gravity currents.
The Dynamic provides a powerful and easily accessible analysis of gravity currents through a simple recorded video, which can be used by students and researchers.

### Atual version: Beta 

### scientific paper (unpublished):
DE CARVALHO BUENO, Rafael; DINIZ, André Luís, DA SILVA; Nathan Streisky; BLENINGER, Tobias Bernward. **Gravity current analyzer for lock-release experiments**. Subimitted to Revista Brasileira de Recursos Hídricos.


### How to run:

To run the Dyenamic’s scripts in a Python interpreter, the system must have:

* Python interpreter;

* Python packages: OpenCV, OpenPIV, Numpy, Scipy, Nitime, Matplotlib, and Tkinter;

The steps below describes the installation instruction for Anaconda’s users, which is the simplest way to run
the Dyenamic’s codes. We recommend the use of Anaconda distribution since it will automatically
install almost all required additional Python packages. Interwave Analyzer also can be ran through other
Python interpreters, but additional packages installations is required.


To run the Dyenamic’s scripts directly in Anaconda interpreter, first download the Anaconda distribution
for Python 3.x.

1) Go to Anaconda website (https://www.anaconda.com/) and find the option for Anaconda distribution;
2) Choose the Python 3.x graphical installer version (note that there are three options for operating system:
Windows, macOS, and Linux);
3) Install the Anaconda interpreter;
4) After the installation, open the Anaconda Prompt (as administrator) and install the following packages
that are used by Interwave Analyzer and are not available in Anaconda:

* OpenCV (4.4.0 or compatible): conda install -c conda-forge opencv
* OpenPIV (0.22.3 or compatible): conda install -c conda-forge openpiv
* Nitime (0.7 or compatible): conda install -c conda-forge nitime

**Attention:** If you already have anaconda installed in your computer, make sure that the above packages
are installed and the anaconda version has Python 3.X. If you use another interpreter, make sure that the
following packages are installed in the your python interpreter: OpenCV 4.4.0, OpenPIV 0.22.3, Numpy 1.16.3, Scipy 1.2.1, Nitime 0.7, Matplotlib 3.1.0, and tk (tkinter) 8.6.8, or compatibles versions.

5) After the installation, download all files .py available to download, including the raster-graphics file-format 0interwave.png which is the logo used by the Interwave Analyzer’s report and the icon interwave icon, which is used as Interwave Analyzer icon on the GUI;
6) Put everything in the same folder and run the script called grase_gui.py;
8) A graphical user interface (GUI) should be launched in seconds;
9) We recommend you to download the example files available at Dyenamic’s website on Download
example. For a detailed tutorial using these files, see section User's Manual.

**Attention:** For more information (user manual, how to obtain the pre-compiled version, FAQ, team, etc), please visit: https://sites.google.com/view/dyenamic/dyenamic
