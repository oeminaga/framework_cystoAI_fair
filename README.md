# Conceptual Framework and Documentation Standards of Cystoscopic Media Content for Artificial Intelligence based on FAIR principles.

General requirements:</br>
- Visual Studio Code
- Python 3.9
- R studio
- Cloud/Network/Local drive

Please place the setup folder in the cloud/network/local drive where you want to store the cystoscopy media content.

If you want to setup a new data container, please use the setup.sh or setup.bat in the setup folder and follow the instruction given on the screen.
 
Please use the terminal to run the setup file.

After installation, you can run main.sh for Linux and Mac and main.bat for Windows to get to the main window.

If you want to extract textual informations from image copies of pathology and surgery reports, please first install tesseract (MacOS: brew install tesseract; Windows: https://codetoprosper.com/tesseract-ocr-for-windows; Ubuntu: https://tesseract-ocr.github.io/tessdoc/Installation.html) and then run ReadTextFromImage.py.It is important to tag these image copies with "path", "op", "path2","path1", "op1", "op2" or "op3" so that they can be recognized by the framework.

If you want to generate a powerpoint presentation using the image material for each case, please run GeneratePPTForCases.bat on Windows or GeneratePPTForCases.sh on Linux or Mac.

Please be aware this framework covers only the backend solution. You can easily build a front-end solution upon this using meta-data that facilitates FAIR principles.

Should you have issues, please open a thread in the issue section.

For citation, please use:</br>
Eminaga, O., Jiyong Lee, T., Ge, J., Shkolyar, E., Laurie, M., Long, J., Graham Hockman, L., & Liao, J. C. (2023). Conceptual Framework and Documentation Standards of Cystoscopic Media Content for Artificial Intelligence. Journal of Biomedical Informatics, 104369. https://doi.org/10.1016/j.jbi.2023.104369
