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
echo Generating configuration and custom scripts
printf "Complete" >> ../$varname/Data/GetSummaryFromTheseFolders.cfg

echo python GeneratePPTCase.py --csv ../Data/SummaryReportImages.csv  --dst ../CaseSummaries >> ../$varname/Scripts/GeneratePPTForCases.bat
echo python3 GeneratePPTCase.py --csv ../Data/SummaryReportImages.csv  --dst ../CaseSummaries >> ../$varname/Scripts/GeneratePPTForCases.sh

echo python3 Calculate.py >> ../$varname/Scripts/UpdateData.sh
echo python3 Summarize.py >> ../$varname/Scripts/UpdateData.sh

echo python Calculate.py >> ../$varname/Scripts/UpdateData.bat
echo python Summarize.py >> ../$varname/Scripts/UpdateData.bat

echo python3 LabelingManager.py --source ../Data --script LabelTheImages.py --prefix Images >> ../$varname/Scripts/RunLabeling.sh
echo python LabelingManager.py --source ../Data --script LabelTheImages.py --prefix Images >> ../$varname/Scripts/RunLabeling.bat


cp Calculate.py ../$varname/Scripts/Calculate.py
cp Summarize.py ../$varname/Scripts/Summarize.py
cp LabelingManager.py ../$varname/Scripts/LabelingManager.py
cp GeneratePPTCase.py ../$varname/Scripts/GeneratePPTCase.py
cp Validation.py ../$varname/Scripts/Validation.py
cp GenerateValidationReport.sh ../$varname/Scripts/GenerateValidationReport.sh
cp GenerateValidationReport.bat ../$varname/Scripts/GenerateValidationReport.bat
cp LabelTheImages.py ../$varname/Scripts/LabelTheImages.py
cp RemovePHI.py ../$varname/Scripts/RemovePHI.py
cp ExtractData.py ../$varname/Scripts/ExtractData.py
cp DataSummarization.Rmd ../$varname/DataSummarization.Rmd
cp Databases.Rproj ../$varname/$varname.Rproj