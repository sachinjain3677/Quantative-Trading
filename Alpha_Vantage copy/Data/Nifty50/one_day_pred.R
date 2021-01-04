library(fUnitRoots)
library(forecast)
library(rugarch)

setwd("/Users/doof/Desktop/Personal/dataFetchProject/Alpha_Vantage/Data/Nifty50")
rm(list=ls())   #Clear the memory

best_model_path = "./GarchPred/best_models.csv"
models_data = read.csv(best_model_path, header=1)

pred_date="2021-1-5"

for(one in 0:25){
  print(one)
  print("Reading file...")
  read_file = paste(c(one, ".csv"), collapse="")
  data=read.csv(read_file, header=F)
  
  print("Calculating ret1...")
  ret1=diff(log(data[,2]))
  
  best_model = models_data[which(models_data$Company.Name==one),"Best.Model"]
  best_dist = models_data[which(models_data$Company.Name==one),"Best.Distribution"]
  print("Running model...")
  print(best_model)
  print("Running Dist...")
  print(best_dist)
  
  spec1=ugarchspec(variance.model = list(model = best_model, garchOrder = c(1, 1)),
                   mean.model = list(armaOrder = c(10, 0), include.mean = TRUE),distribution.model = best_dist)
  garch_fit_1 = ugarchfit(spec = spec1, data = ret1)
  garch_fit_1
  std_res_1=as.numeric(residuals(garch_fit_1,standardize=TRUE))
  ugarchforecast(garch_fit_1,n.ahead = 1) -> prediction

  print(paste(c("Prediction for ", one), collapse=""))
  print(prediction)
  
  pred1 <- prediction@forecast$seriesFor[[1]]
  pred2 <- prediction@forecast$sigmaFor[[1]]
  
  pred <- cbind(pred1, pred2)

  path <- paste(c("./GarchPred/",one), collapse="")
  path <- paste(c(path, "predictions.csv"), collapse="/")
  
  write.table(pred, path, 
              append=TRUE, 
              sep=",", 
              col.names = FALSE, 
              row.names = pred_date)
}
