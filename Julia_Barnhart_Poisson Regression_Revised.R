# +++++++++++++++++++++++++++++++++++++++++ # 
# --- UNOS INTERVIEW PRESENTATION ---       #
# --- JULIA E. BARNHART ---                 #
# --- JUNE 7, 2017 ---
# --- Revised January 25, 2018 --- 
# --- EXAMPLE POISSON REGRESSION MODEL ---  #
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
library(Hmisc)
library(corrplot)
library(dplyr)

# ------------------------------
# SECTION 1: WINE DATASET INPUT
# ------------------------------

tbl <- read.csv("C:/Users/Julia/Desktop/Wine_Prediction/wine.csv", header = T)

# Rename index column
colnames(tbl)[1] <- "Indicator"

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


# -----------
# Histograms 
# -----------

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

# Generate histograms of target and predictor variables
# Run function
NumVarHist(tbl, 10, "C:/Users/Julia/Desktop/Wine_Prediction")

# -------------------
# Correlation Matrix 
# -------------------

# Generate simple correlation matrix of correlation coefficients
# "NA" appears for those cells where there are missing values unless "use"
# is used 
# # Numbers are slightly off from SAS because "use" deletes case-wise 
corr <- cor(tbl, use= "complete.obs")
round(corr, 4)

# Generate correlation matrix with significance levels
corr2 <- rcorr(as.matrix(tbl))

# Create function for flattening correlation matrix
# cormat : matrix of the correlation coefficients
# pmat : matrix of the correlation p-values
flattenCorrMatrix <- function(cormat, pmat) {
  ut <- upper.tri(cormat)
  data.frame(
    row = rownames(cormat)[row(cormat)[ut]],
    column = rownames(cormat)[col(cormat)[ut]],
    cor  =(cormat)[ut],
    p = pmat[ut]
  )
}

fcorr2 <- flattenCorrMatrix(corr2$r, corr2$P)

# Visualization of simple correlation matrix using correlogram 
corrplot(corr, type = "upper", order = "hclust", 
         tl.col = "black", tl.srt = 45)

# ------------------------------------
# SECTION 3: MISSING-VALUE IMPUTATION
# ------------------------------------

# Using R's mice() package for multiple imputation

# Exclude variables TARGET and INDEX
imp <- mice(tbl, pred=quickpred(tbl, mincor = 0.3, minpuc = 0, include = "", exclude = "'INDEX','TARGET'", method = "pearson"), print=F)

# Take a look at what methods were used for imputation
imp$meth

# Change method to "cart" for all non-Null values
for (i in 1:length(imp$meth)) {
  if (imp$meth[i] != "") {   # if it is an empty string
    imp$meth[i] <- "cart"
  }
}

# Check methods again
nmethod = imp$method

# Re-run imputation with "cart" method
imp2 <- mice(tbl, meth = nmethod, print=F)

# Create final imputed dataset
imp_final = complete(imp2,'long')


# Renaming imputed columns for differentiation from original columns 
colnames(imp_final) <- paste("Imp", colnames(imp_final), sep = "_")

# Drop unnecessary columns that get confusing with merging later on
imp_final <- subset(imp_final, select = -Imp_.imp)
imp_final <- subset(imp_final, select = -Imp_.id)


# Merge both original and imputated dataset
compldata <- merge(x=tbl, y=imp_final, by.x='Indicator', by.y='Imp_Indicator')


# --------------------------------------
# SECTION 4: DATA MANIPULATION- BINNING
# --------------------------------------





# ----------------------------------------------
# SECTION 5: SPLITTING DATASET 70/30 TRAIN/TEST
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
# SECTION 6: AUTOMATED VARIABLE SELECTION
# ----------------------------------------

require(leaps)

# forward selection
pred_set = regsubsets(TARGET ~ AcidIndex + Alcohol + Chlorides + CitricAcid + Density + FixedAcidity + FreeSulfurDioxide + LabelAppeal + pH +
           ResidualSugar + STARS + Sulphates + TotalSulfurDioxide + VolatileAcidity,
           data = imp_train, method = "forward")

# ouput of selection method
summary(pred_set)

# preliminary winners: AcidIndex, Alcohol, Chlorides, FreeSulfurDioxide, LabelAppeal, STARS, TotalSulfurDioxide, VolatileAcidity

# -------------------------
# SECTION 7: BUILD MODELS
# -------------------------


p_model_1 = glm(Imp_TARGET ~ Imp_AcidIndex + Imp_Alcohol + Imp_Chlorides + Imp_FreeSulfurDioxide + Imp_LabelAppeal + Imp_STARS + Imp_TotalSulfurDioxide + Imp_VolatileAcidity,
                family=poisson(link="log"), data=imp_train)

# output of regression model
summary(p_model_1)

# --------------------------------------
# SECTION 8: TEST MODEL ON TEST DATASET
# --------------------------------------

# UNFINISHED BUSINESS

test_results = data.frame(predict.glm(p_model_1, imp_test))
colnames(test_results) <- c("pred_target")

summary(test_results)

# Compare original target variable to predicted target variable 
# Create column for original target
test_results$target <-NA
# convert rownames into a true dataframe column
test_results <-cbind(rowidx = rownames(test_results), test_results)
imp_final <-cbind(rowidx = rownames(imp_final), imp_final)
# merge both dataframes on rowidx
comparison <- merge(test_results, imp_final, by="rowidx") 
comparison <- select(comparison, Imp_TARGET, pred_target)

# Create loss function by calculating MSE 
# Create new column first 

attach(comparison)
# calculate squared error for each observation
comparison <- comparison %>% mutate(SE = rowMeans(comparison[,c("")])

comparison


