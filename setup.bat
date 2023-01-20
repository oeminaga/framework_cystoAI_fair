ECHO ********************************************************************
ECHO *          This script prepares container for a new study          *
ECHO ********************************************************************
ECHO Please name the study -Please do not provide empty space-
set /p varname=Study name:
ECHO Installing required python packages
ECHO PLEASE ENSURE THAT PYTHON 3.9 IS INSTALLED BEFORE YOU CAN CONTINUE!
python -m pip install -r requirements.txt

ECHO Creating the organization folders

mkdir ../%varname%
mkdir ../%varname%/Data
mkdir ../%varname%/Data/Complete
mkdir ../%varname%/Data/UnderReview
mkdir ../%varname%/Data/InformedConsents
mkdir ../%varname%/Data/RequireApproval
mkdir ../%varname%/Data/Complete_NoPathology
mkdir ../%varname%/Data/InComplete_NoScreenShots
mkdir ../%varname%/Data/InComplete_NotLabelled
mkdir ../%varname%/Data/InComplete_IncompleteLabels
mkdir ../%varname%/Data/OfficeCystoscopy
mkdir ../%varname%/Data/Others
mkdir ../%varname%/CaseSummaries
mkdir ../%varname%/Scripts
mkdir ../%varname%/CaseSummaries
mkdir ../%varname%/BladderMap

ECHO Generating configuration and custom scripts
ECHO "Complete" >> ../%varname%/Data/GetSummaryFromTheseFolders.cfg

ECHO python3 Calculate.py >> ../%varname%/Scripts/UpdateData.sh
ECHO python3 Summarize.py >> ../%varname%/Scripts/UpdateData.sh

ECHO python Calculate.py >> ../%varname%/Scripts/UpdateData.bat
ECHO python Summarize.py >> ../%varname%/Scripts/UpdateData.bat

ECHO python3 LabelingManager.py --source ../Data --script LabelTheImages.py --prefix Images >> ../%varname%/Scripts/RunLabeling.sh
ECHO python LabelingManager.py --source ../Data --script LabelTheImages.py --prefix Images >> ../%varname%/Scripts/RunLabeling.bat

copy Calculate.py ../%varname%/Scripts/Calculate.py
copy CaseEntry.py ../%varname%/Scripts/CaseEntry.py
copy CheckFiles.py ../%varname%/Scripts/CheckFiles.py
copy Database_Script_Protocol.docx ../%varname%/Scripts/Database_Script_Protocol.docx
copy Databases.Rproj ../%varname%/%varname%.Rproj
copy DataSharing.py ../%varname%/Scripts/DataSharing.py
copy DataSummarization.Rmd ../%varname%/DataSummarization.Rmd
copy GeneratePPTCase.py ../%varname%/Scripts/GeneratePPTCase.py

ECHO python GeneratePPTCase.py --csv ../Data/SummaryReportImages.csv  --dst ../CaseSummaries >> ../%varname%/Scripts/GeneratePPTForCases.bat
ECHO python3 GeneratePPTCase.py --csv ../Data/SummaryReportImages.csv  --dst ../CaseSummaries >> ../%varname%/Scripts/GeneratePPTForCases.sh

copy GenerateReportFromcMDX.py ../%varname%/Scripts/GenerateReportFromcMDX.py
copy GenerateValidationReport.bat ../%varname%/Scripts/GenerateValidationReport.bat
copy GenerateValidationReport.sh ../%varname%/Scripts/GenerateValidationReport.sh
copy LabelingManager.py ../%varname%/Scripts/LabelingManager.py
copy LabelTheImages.py ../%varname%/Scripts/LabelTheImages.py
copy main_win.py ../%varname%/Scripts/main_win.py
copy main.bat ../%varname%/Scripts/main.bat
copy main.py ../%varname%/Scripts/main.py
copy main.sh ../%varname%/Scripts/main.sh
copy MergeReports.py ../%varname%/Scripts/MergeReports.py
copy ReadTextFromImage.py ../%varname%/Scripts/ReadTextFromImage.py
copy RemovePHI.py ../%varname%/Scripts/RemovePHI.py

copy SortedData.R ../%varname%/Scripts/SortedData.R
copy Summarize.py ../%varname%/Scripts/Summarize.py

copy utils.py ../%varname%/Scripts/utils.py
copy validation.json ../%varname%/Scripts/validation.json
copy Validation.py ../%varname%/Scripts/Validation.py
copy ExtractData.py ../%varname%/Scripts/ExtractData.py
