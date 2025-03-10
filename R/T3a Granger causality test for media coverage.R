library(lmtest)
library(FIAR)
library(dynlm)
RT_no_long_covid_no_dot <- gsub("\\."," ",RT_no_long_covid)
media_coverage <- readRDS("news_freq_ts.rds")

#Stablize the media coverage
for(RT_i in RT_no_long_covid_no_dot){
  #Start for loop
  temp_ts <- ts(media_coverage[,RT_i])
  temp_adf <- adf.test(temp_ts)
  diff_order[RT_i] <- 0
  if(all(temp_ts==0)){
    
  }else{
  while(temp_adf$p.value > 0.05){
    diff_order[RT_i] <- diff_order[RT_i] + 1
    temp_ts <- diff(temp_ts)
    temp_adf <- adf.test(temp_ts)
  }
  }
  p_values[RT_i] <- temp_adf$p.value
  media_coverage[,RT_i] <- NA
  media_coverage[(diff_order[RT_i]+1):nrow(media_coverage),RT_i] <- temp_ts
}


#Use to store p-values
H1_pvalue_tGCL <- list()
H2_pvalue_tGCL <- list()
H3_pvalue_tGCL <- list()
H4_pvalue_tGCL <- list()
H1_pvalue_AUC <- list()
H2_pvalue_AUC <- list()
H3_pvalue_AUC <- list()
H4_pvalue_AUC <- list()
H1_pvalue_BIC <- list()
H2_pvalue_BIC <- list()
H3_pvalue_BIC <- list()
H4_pvalue_BIC <- list()

H1_pvalue_HQC <- list()
H2_pvalue_HQC <- list()
H3_pvalue_HQC  <- list()
H4_pvalue_HQC  <- list()
ind <- 1
for(p in 1:60){
  H1_pvalue_tGCL[[p]] <- array(dim=c(20,20))
  H2_pvalue_tGCL[[p]] <- array(dim=c(20,20))
  H3_pvalue_tGCL[[p]] <- array(dim=c(20,20))
  H4_pvalue_tGCL[[p]] <- array(dim=c(20,20))
  
  H1_pvalue_AUC[[p]] <- array(dim=c(20,20))
  H2_pvalue_AUC[[p]] <- array(dim=c(20,20))
  H3_pvalue_AUC[[p]] <- array(dim=c(20,20))
  H4_pvalue_AUC[[p]] <- array(dim=c(20,20))
  
  H1_pvalue_BIC[[p]] <- array(dim=c(20,20))
  H2_pvalue_BIC[[p]] <- array(dim=c(20,20))
  H3_pvalue_BIC[[p]] <- array(dim=c(20,20))
  H4_pvalue_BIC[[p]] <- array(dim=c(20,20))
  
  H1_pvalue_HQC[[p]] <- array(dim=c(20,20))
  H2_pvalue_HQC[[p]] <- array(dim=c(20,20))
  H3_pvalue_HQC[[p]] <- array(dim=c(20,20))
  H4_pvalue_HQC[[p]] <- array(dim=c(20,20))
  
  rownames(H1_pvalue_tGCL[[p]]) <- RT_no_long_covid
  rownames(H2_pvalue_tGCL[[p]]) <- RT_no_long_covid
  rownames(H3_pvalue_tGCL[[p]]) <- RT_no_long_covid
  rownames(H4_pvalue_tGCL[[p]]) <- RT_no_long_covid
  rownames(H1_pvalue_AUC[[p]]) <- RT_no_long_covid
  rownames(H2_pvalue_AUC[[p]]) <- RT_no_long_covid
  rownames(H3_pvalue_AUC[[p]]) <- RT_no_long_covid
  rownames(H4_pvalue_AUC[[p]]) <- RT_no_long_covid
  rownames(H1_pvalue_BIC[[p]]) <- RT_no_long_covid
  rownames(H2_pvalue_BIC[[p]]) <- RT_no_long_covid
  rownames(H3_pvalue_BIC[[p]]) <- RT_no_long_covid
  rownames(H4_pvalue_BIC[[p]]) <- RT_no_long_covid
  rownames(H1_pvalue_HQC[[p]]) <- RT_no_long_covid
  rownames(H2_pvalue_HQC[[p]]) <- RT_no_long_covid
  rownames(H3_pvalue_HQC[[p]]) <- RT_no_long_covid
  rownames(H4_pvalue_HQC[[p]]) <- RT_no_long_covid
  
  # for(ind in 1:4){
    

    for(symi_1 in 1:20){
      for(symi_2 in 1:20){
      CF_ts <- media_coverage[2:nrow(media_coverage),RT_no_long_covid_no_dot[symi_2]]
      LongCOVID_ts <-  MSV_stationary[2:nrow(MSV_stationary),"Long.Covid"] #This is the MSV of the symptom.
      
      #We should choose the best p! Calculate the AUC
      
      Symi_ts <-  MSV_stationary[2:nrow(MSV_stationary),RT_no_long_covid[symi_1]] #This is the media coverage of the symptom
      # MSV
      # LongCOVID_ts <- MSV$Long.Covid[2:nrow(OxCGRT_agg)]
      # Symi_ts <- MSV$Ageusia[2:nrow(OxCGRT_agg)]
      
      #test 1: Symi_ts G-causes Long COVID? ------------------------------------------------
      #Granger causality test 1: x=Symi_ts G-causes y=Long COVID?
      
      # H1_null_AR <- dynlm(ts(LongCOVID_ts)~L(ts(LongCOVID_ts),1:p))
      H1_alt_AR <- dynlm(ts(LongCOVID_ts)~L(ts(LongCOVID_ts),1:p)+L(ts(Symi_ts),1:p))
      # H1_F_test <- anova(H1_null_AR,H1_alt_AR)
      H1_pvalue_AUC[[p]][symi_1,symi_2] <- AIC(H1_alt_AR)
      T <- length(LongCOVID_ts) - p
      num_par <- 3*p + 2
      H1_pvalue_HQC[[p]][symi_1,symi_2] <-  -2* as.numeric(logLik(H1_alt_AR)) + 2*num_par*log(log(T))
      H1_pvalue_BIC[[p]][symi_1,symi_2] <- BIC(H1_alt_AR)
      
      
      temp_gc_test <- grangertest(Symi_ts,LongCOVID_ts,order=p)
      #p-value<0.1 means significant G-causality.
      
      
      H1_pvalue_tGCL[[p]][symi_1,symi_2] <-  temp_gc_test$`Pr(>F)`[2]
      
      #Conditional Granger causality test 1: Symi_ts G-causes Long COVID?
      # H3_null_AR <- dynlm(ts(LongCOVID_ts)~L(ts(LongCOVID_ts),1:p)+L(ts(CF_ts),1:p))
      H3_alt_AR <- dynlm(ts(LongCOVID_ts)~L(ts(LongCOVID_ts),1:p)+L(ts(Symi_ts),1:p)+L(ts(CF_ts),1:p))
      # H3_F_test <- anova(H3_null_AR,H3_alt_AR)
      H3_pvalue_AUC[[p]][symi_1,symi_2] <- AIC(H3_alt_AR)
      T <- length(LongCOVID_ts) - p
      num_par <- 3*p + 2
      H3_pvalue_HQC[[p]][symi_1,symi_2] <-  -2* as.numeric(logLik(H3_alt_AR)) + 2*num_par*log(log(T))
      H3_pvalue_BIC[[p]][symi_1,symi_2] <- BIC(H3_alt_AR)
      
      
      temp_df <- data.frame(Symi_ts,LongCOVID_ts,CF_ts)
      temp_cgc_test <- condGranger(temp_df,order=p)
      #p-value: p>0.1 means CF is a confounding factor
      H3_pvalue_tGCL[[p]][symi_1,symi_2] <- temp_cgc_test$prob
      
      #test 2: Symi_ts G-caused by Long COVID? ------------------------------------------------
      #Granger causality test 2: x=Symi_ts G-caused by y=Long COVID?
      # H2_null_AR <- dynlm(ts(Symi_ts)~L(ts(Symi_ts),1:p))
      H2_alt_AR <- dynlm(ts(Symi_ts)~L(ts(LongCOVID_ts),1:p)+L(ts(Symi_ts),1:p))
      # H2_F_test <- anova(H2_null_AR,H2_alt_AR)
      H2_pvalue_AUC[[p]][symi_1,symi_2] <- AIC(H2_alt_AR)
      T <- length(LongCOVID_ts) - p
      num_par <- 3*p + 2
      H2_pvalue_HQC[[p]][symi_1,symi_2] <-  -2* as.numeric(logLik(H2_alt_AR)) + 2*num_par*log(log(T))
      H2_pvalue_BIC[[p]][symi_1,symi_2] <- BIC(H2_alt_AR)
      temp_gc_test <- grangertest(LongCOVID_ts,Symi_ts,order=p)
      #p-value<0.1 means significant G-causality.
      H2_pvalue_tGCL[[p]][symi_1,symi_2] <- temp_gc_test$`Pr(>F)`[2]
      
      #Conditional Granger causality test 2: Symi_ts G-causes Long COVID?
      # H4_null_AR <- dynlm(ts(Symi_ts)~L(ts(Symi_ts),1:p)+L(ts(CF_ts),1:p))
      H4_alt_AR <- dynlm(ts(Symi_ts)~L(ts(LongCOVID_ts),1:p)+L(ts(Symi_ts),1:p)+L(ts(CF_ts),1:p))
      # H4_F_test <- anova(H4_null_AR,H4_alt_AR)
      H4_pvalue_AUC[[p]][symi_1,symi_2] <- AIC(H4_alt_AR)
      
      
      T <- length(LongCOVID_ts) - p
      num_par <- 3*p + 2
      H4_pvalue_HQC[[p]][symi_1,symi_2] <-  -2* as.numeric(logLik(H4_alt_AR)) + 2*num_par*log(log(T))
      H4_pvalue_BIC[[p]][symi_1,symi_2] <- BIC(H4_alt_AR)
      
      temp_df <- data.frame(LongCOVID_ts,Symi_ts,CF_ts)
      temp_cgc_test <- condGranger(temp_df,order=p)
      #p-value: p>0.1 means CF is a confounding factor
      H4_pvalue_tGCL[[p]][symi_1,symi_2] <- temp_cgc_test$prob
      print(paste0("p=",p,"; symi_1=",symi_1,"; symi_2=",symi_2))
      }
    }
    
  # }
  # par(mfrow=c(1,1))
  # plot(LongCOVID_ts)
  # lines(Symi_ts)
  
}

saveRDS(list(
  H1_pvalue_tGCL,
  H2_pvalue_tGCL,
  H3_pvalue_tGCL ,
  H4_pvalue_tGCL ,
  H1_pvalue_AUC ,
  H2_pvalue_AUC ,
  H3_pvalue_AUC,
  H4_pvalue_AUC ,
  H1_pvalue_BIC ,
  H2_pvalue_BIC ,
  H3_pvalue_BIC ,
  H4_pvalue_BIC,H1_pvalue_HQC,H2_pvalue_HQC,H3_pvalue_HQC,H4_pvalue_HQC ),"all_pvalues_media_coverage.rds")




