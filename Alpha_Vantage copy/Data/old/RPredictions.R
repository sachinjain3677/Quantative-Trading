library(fUnitRoots)
library(forecast)
library(rugarch)

rm(list=ls())   #Clear the memory
setwd("/Users/doof/Desktop/dataFetchProject/Alpha_Vantage/Data/Nifty50")
for(one in 0:1){
  print(one)
  print("Reading file...")
  read_file = paste(c(one, ".csv"), collapse="")
  data=read.csv(read_file, header=F)
  
  print("Calculating ret1...")
  ret1=diff(log(data[,2]))
  
  # "ct" for a regression with an intercept (constant) and a time trend. 
  # The default is "c".
  #a = adfTest(ret1,lags=10,type=c("ct"))

  #Box.test(ret1,lag=20,type="Ljung")
  my_models <- list("sGARCH", "gjrGARCH", "eGARCH")
  my_dists <- list("norm", "std", "ged", "snorm", "sstd", "sged")
  for(two in 1:3){
    my_model <- toString(my_models[two])
    print("Running")
    print(my_model)
    for(three in 1:6){
      my_dist <- toString(my_dists[three])
      print("Running distribution")
      print(my_dist)
      l=length(ret1)
      l1=l-26
      pred1=0
      pred2=0
      for(i in 1:(l-l1+1)){
        spec2=ugarchspec(variance.model = list(model = my_model, garchOrder = c(1, 1)),
                         mean.model = list(armaOrder = c(10, 0), include.mean = TRUE),distribution.model = my_dist)
        garch_fit_3 = ugarchfit(spec = spec2, data = ret1[i:(l1+i-1)])
        forc_2 = ugarchforecast(garch_fit_3, n.ahead=1)
        pred1[i]=forc_2@forecast$seriesFor[[1]]
        pred2[i]=forc_2@forecast$sigmaFor[[1]]
      }
      pred_all=cbind(pred1,pred2)
      path <- "./GarchPred/"
      path <- paste(c(path, one), collapse="")
      path <- paste(c(path, my_model), collapse="/")
      
      file_name <- paste(c(my_model, my_dist), collapse="_")
      file_name <- paste(c(file_name, ".csv"), collapse="")
      
      path <- paste(c(path, file_name), collapse="/")
      print(path)
      write.csv(pred_all,path)
    }
  }
}
