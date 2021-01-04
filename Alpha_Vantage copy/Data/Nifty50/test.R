library(fUnitRoots)
library(forecast)
library(rugarch)

setwd("/Users/doof/Desktop/Personal/dataFetchProject/Alpha_Vantage/Data/Nifty50")
best_model_path = "./GarchPred/best_models.csv"
best_model = read.csv(best_model_path, header=1)
print(best_model[,"Best.Model"])
#class(best_model)

#class(which(best_model$Company.Name==2))

#best_model[which(best_model$Company.Name==2),"Best.Model"]

data = read.csv("0.csv", header=F)
print(tail(data))
data <- head(data, -1)
print(tail(data))
ret1 = diff(log(data[,2]))
#print(ret1)
class(ret1)
#ret1 <- head(ret1, -1)

print(ret1)
spec1=ugarchspec(variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),mean.model = list(armaOrder = c(10, 0), include.mean = TRUE),distribution.model = "norm")
garch_fit_1 = ugarchfit(spec = spec1, data = ret1)
garch_fit_1
std_res_1=as.numeric(residuals(garch_fit_1,standardize=TRUE))
ugarchforecast(garch_fit_1,n.ahead = 1) -> a
print(a)
pred1 <- a@forecast$seriesFor[[1]]
pred2 <- a@forecast$seriesFor[[1]]

pred <- cbind(pred1, pred2)
write.table(pred, "./predictions.csv", 
            append=TRUE, 
            sep=",", 
            col.names = FALSE, 
            row.names = "testing")
