# +++++++++++++++++++++++++++++++++++++++++ #
# --- UNOS INTERVIEW PRESENTATION --- #
# --- JULIA E. BARNHART --- #
# --- JUNE 7, 2017 --- #
# --- EXAMPLE POISSON REGRESSION MODEL --- #
# +++++++++++++++++++++++++++++++++++++++++ #
# Note: This is just a snippet of code outlining some backbone techniques
# and code used in predictive modeling. This does not reflect the
# scope of a real predictive modeling project.
# ----------
# LIBRARIES
# ----------
library(ggplot2)
library(mice)
library(caTools)
library(leaps)
# ------------------------------
# SECTION 1: WINE DATASET INPUT
# ------------------------------
tbl <- read.csv("C:/Users/Julia/Desktop/UNOS_Presentation/wine.csv", header = T)
# -------------------------------------
# SECTION 2: EXPLORATORY DATA ANALYSIS
# -------------------------------------
# Display all variables in dataset
str(tbl)
# Display a few first and last observations
head(tbl)
tail(tbl)
# Descriptive Statistics
summary(tbl)
# Create function for displaying histograms of numeric variables
# Histograms available in PNG format on file system
NumVarHist <- function(dataF,noBins,fpath){
# Get type of input data frame columns
col.type <- data.frame("varType"=sapply(dataF, function (x) class(x)))
# Convert rownames/variable names to a data frame column
col.type$varName <- rownames(col.type)
# Set row names of data frame to null
rownames(col.type) <- NULL
nCol <- nrow(col.type)
for(i in 1:nCol){
if(col.type[i,1]=="numeric"){
# path and name of image
fileN=paste(col.type[i,2],"png",sep=".")
png(file=paste(fpath,fileN,sep="\\"))
hist(dataF[,col.type[i,2]],
breaks=noBins,
main=paste(" Histogram for ",col.type[i,2],sep=""),
xlab=paste(" Variable : ",col.type[i,2],sep=""),
ylab="Count",
col="grey",
border="black"
)
# close the graphic device
dev.off()
}
}
}
# Run function
NumVarHist(tbl, 10, "C:/Users/Julia/Desktop/UNOS_Presentation")
# ------------------------------------
# SECTION 3: MISSING-VALUE IMPUTATION
# ------------------------------------
# Using R's mice() package for multiple imputation
# Exclude variables TARGET and INDEX
imp <- mice(tbl, pred=quickpred(tbl, mincor = 0.3, minpuc = 0, include = "", exclude = "'INDEX','TARGET'", method =
"pearson"), print=F)
# Take a look at what methods were used for imputation
imp$meth
# Change method to "cart" for all non-Null values
for (i in 1:length(imp$meth)) {
if (imp$meth[i] != "") { # if it is an empty string
imp$meth[i] <- "cart"
}
}
# Check methods again
nmethod = imp$method
# Re-run imputation with "cart" method
imp2 <- mice(tbl, meth = nmethod, print=F)
# create final imputed dataset
imp_final = complete(imp2,'long')
# ----------------------------------------------
# SECTION 4: SPLITTING DATASET 70/30 TRAIN/TEST
# ----------------------------------------------
require(caTools)
# set pseudo-random number generator
set.seed(123)
# create a new vector of TRUE and FALSE
spl <- sample.split(imp_final, SplitRatio = 2/3)
# Create training and test datasets using vector
imp_train = subset(imp_final, spl==TRUE)
imp_test = subset(imp_final, spl == FALSE)
# ----------------------------------------
# SECTION 5: AUTOMATED VARIABLE SELECTION
# ----------------------------------------
require(leaps)
# forward selection
pred_set = regsubsets(TARGET ~ AcidIndex + Alcohol + Chlorides + CitricAcid + Density + FixedAcidity +
FreeSulfurDioxide + LabelAppeal + pH +
ResidualSugar + STARS + Sulphates + TotalSulfurDioxide + VolatileAcidity,
data = imp_train, method = "forward")
# ouput of selection method
summary(pred_set)
# preliminary winners: AcidIndex, Alcohol, Chlorides, FreeSulfurDioxide, LabelAppeal, STARS, TotalSulfurDioxide,
VolatileAcidity
# -------------------------
# SECTION 6: BUILD MODELS
# -------------------------
p_model_1 = glm(TARGET ~ AcidIndex + Alcohol + Chlorides + FreeSulfurDioxide + LabelAppeal + STARS +
TotalSulfurDioxide + VolatileAcidity,
family=poisson(link="log"), data=imp_train)
# output of regression model
summary(p_model_1)
# --------------------------------------
# SECTION 7: TEST MODEL ON TEST DATASET
# --------------------------------------
test_results = predict.glm(p_model_1, imp_test)
summary(test_results)
# Create function to calculate Average Squared Error for test
