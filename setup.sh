#!/bin/bash
echo ********************************************************************
echo *          This script prepares container for a new study          *
echo ********************************************************************
echo Please name the study -Please do not provide empty space-
read varname
echo Installing required python packages
python3 -m pip install -r requirements.txt

echo Creating the organization folders

mkdir ../$varname
mkdir ../$varname/Data
mkdir ../$varname/Data/Complete
mkdir ../$varname/Data/UnderReview
mkdir ../$varname/Data/InformedConsents
mkdir ../$varname/Data/RequireApproval
mkdir ../$varname/Data/Complete_NoPathology
mkdir ../$varname/Data/InComplete_NoScreenShots
mkdir ../$varname/Data/InComplete_NotLabelled
mkdir ../$varname/Data/InComplete_IncompleteLabels
mkdir ../$varname/Data/OfficeCystoscopy
mkdir ../$varname/Data/Others
mkdir ../$varname/CaseSummaries
mkdir ../$varname/Scripts
mkdir ../$varname/CaseSummaries
mkdir ../$varname/BladderMap

echo Generating configuration and custom scripts
printf "Complete" >> ../$varname/Data/GetSummaryFromTheseFolders.cfg

echo python3 Calculate.py >> ../$varname/Scripts/UpdateData.sh
echo python3 Summarize.py >> ../$varname/Scripts/UpdateData.sh

echo python Calculate.py >> ../$varname/Scripts/UpdateData.bat
echo python Summarize.py >> ../$varname/Scripts/UpdateData.bat

echo python3 LabelingManager.py --source ../Data --script LabelTheImages.py --prefix Images >> ../$varname/Scripts/RunLabeling.sh
echo python LabelingManager.py --source ../Data --script LabelTheImages.py --prefix Images >> ../$varname/Scripts/RunLabeling.bat

cp Calculate.py ../$varname/Scripts/Calculate.py
cp CaseEntry.py ../$varname/Scripts/CaseEntry.py
cp CheckFiles.py ../$varname/Scripts/CheckFiles.py
cp Database_Script_Protocol.docx ../$varname/Scripts/Database_Script_Protocol.docx
cp Databases.Rproj ../$varname/$varname.Rproj
cp DataSharing.py ../$varname/Scripts/DataSharing.py
cp DataSummarization.Rmd ../$varname/DataSummarization.Rmd
cp GeneratePPTCase.py ../$varname/Scripts/GeneratePPTCase.py

echo python GeneratePPTCase.py --csv ../Data/SummaryReportImages.csv  --dst ../CaseSummaries >> ../$varname/Scripts/GeneratePPTForCases.bat
echo python3 GeneratePPTCase.py --csv ../Data/SummaryReportImages.csv  --dst ../CaseSummaries >> ../$varname/Scripts/GeneratePPTForCases.sh

cp GenerateReportFromcMDX.py ../$varname/Scripts/GenerateReportFromcMDX.py
cp GenerateValidationReport.bat ../$varname/Scripts/GenerateValidationReport.bat
cp GenerateValidationReport.sh ../$varname/Scripts/GenerateValidationReport.sh
cp LabelingManager.py ../$varname/Scripts/LabelingManager.py
cp LabelTheImages.py ../$varname/Scripts/LabelTheImages.py
cp main_win.py ../$varname/Scripts/main_win.py
cp main.bat ../$varname/Scripts/main.bat
cp main.py ../$varname/Scripts/main.py
cp main.sh ../$varname/Scripts/main.sh
cp MergeReports.py ../$varname/Scripts/MergeReports.py
cp ReadTextFromImage.py ../$varname/Scripts/ReadTextFromImage.py
cp RemovePHI.py ../$varname/Scripts/RemovePHI.py

cp SortedData.R ../$varname/Scripts/SortedData.R
cp Summarize.py ../$varname/Scripts/Summarize.py

cp utils.py ../$varname/Scripts/utils.py
cp validation.json ../$varname/Scripts/validation.json
cp Validation.py ../$varname/Scripts/Validation.py
cp ExtractData.py ../$varname/Scripts/ExtractData.py