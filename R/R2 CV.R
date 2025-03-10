library("MBESS")

CV_df <- data.frame(array(dim=c(0,3)))
colnames(CV_df) <- c("Related topic","Before improvement","After improvement")

#Before

for(k in 1:n_keyword){
    X <- RSV_list[[k]][rownames(RSV_list[[k]])<="2021-12-31",1]
    before_CV <- ci.cv(data=X, conf.level=.95)
    
    #After
    X <- RSV_list[[k]][rownames(RSV_list[[k]])>"2021-12-31",1]
    after_CV <- ci.cv(data=X, conf.level=.95)
    
    
    CV_df[k,1] <- keyword_vec[k]
    
      CV_df[k,2] <-  paste0(round(before_CV$C.of.V,3)," (",
           round(before_CV$Lower.Limit.CofV,3),",",
                 round(before_CV$Upper.Limit.CofV,3),")")
    
    CV_df[k,3] <-  paste0(round(after_CV$C.of.V,3)," (",
                          round(after_CV$Lower.Limit.CofV,3),",",
                          round(after_CV$Upper.Limit.CofV,3),")")
}


write.csv(CV_df,"result/CV_df.csv")
