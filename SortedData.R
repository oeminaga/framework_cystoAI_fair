library(stringr)
SummaryReportImagesWithTextForPathOPAndcMDX$YEAR = str_sub(SummaryReportImagesWithTextForPathOPAndcMDX$DATE, -4,-1)
SummaryReportImagesWithTextForPathOPAndcMDX$DAY = as.numeric(str_sub(SummaryReportImagesWithTextForPathOPAndcMDX$DATE, -6,-5))
SummaryReportImagesWithTextForPathOPAndcMDX$MONTH = str_pad(str_sub(SummaryReportImagesWithTextForPathOPAndcMDX$DATE, 0,-7),2,pad="0")
SummaryReportImagesWithTextForPathOPAndcMDX$YEARMONTH=as.numeric(paste0(SummaryReportImagesWithTextForPathOPAndcMDX$YEAR,SummaryReportImagesWithTextForPathOPAndcMDX$MONTH))
unique(SummaryReportImagesWithTextForPathOPAndcMDX$ImageModality)
SummaryReportImagesWithTextForPathOPAndcMDX$IMG_MOD="NA"
SummaryReportImagesWithTextForPathOPAndcMDX$IMG_MOD[SummaryReportImagesWithTextForPathOPAndcMDX$ImageModality=="WLC"]="WLC"
SummaryReportImagesWithTextForPathOPAndcMDX$IMG_MOD[SummaryReportImagesWithTextForPathOPAndcMDX$ImageModality=="BLC"]="BLC"
SummaryReportImagesWithTextForPathOPAndcMDX$IMG_MOD[str_sub(SummaryReportImagesWithTextForPathOPAndcMDX$ImageModality,0,1)=="H"]="H"
SummaryReportImagesWithTextForPathOPAndcMDX$IMG_MOD=factor(SummaryReportImagesWithTextForPathOPAndcMDX$IMG_MOD, levels = c("WLC", "BLC","H", "NA"))
data=SummaryReportImagesWithTextForPathOPAndcMDX[order(SummaryReportImagesWithTextForPathOPAndcMDX$ID,-SummaryReportImagesWithTextForPathOPAndcMDX$YEARMONTH, SummaryReportImagesWithTextForPathOPAndcMDX$IDENTIFICATION, SummaryReportImagesWithTextForPathOPAndcMDX$IMG_MOD),]
write.csv(data,"Data/SummaryReportImagesWithTextForPathOPAndcMDX_sorted.csv")
