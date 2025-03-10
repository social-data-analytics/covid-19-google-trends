setwd(dirname(rstudioapi::getSourceEditorContext()$path))

temp_rds <- readRDS("all_pvalues_media_coverage.rds")
H1_pvalue_tGCL <- temp_rds[[1]]
H2_pvalue_tGCL <- temp_rds[[2]]
H3_pvalue_tGCL <- temp_rds[[3]]
H4_pvalue_tGCL <- temp_rds[[4]]
H1_pvalue_AUC <- temp_rds[[5]]
H2_pvalue_AUC <- temp_rds[[6]]
H3_pvalue_AUC <- temp_rds[[7]]
H4_pvalue_AUC <- temp_rds[[8]]
H1_pvalue_BIC <- temp_rds[[9]]
H2_pvalue_BIC <- temp_rds[[10]]
H3_pvalue_BIC <- temp_rds[[11]]
H4_pvalue_BIC <- temp_rds[[12]]
H1_pvalue_HQC <- temp_rds[[13]]
H2_pvalue_HQC <- temp_rds[[14]]
H3_pvalue_HQC <- temp_rds[[15]]
H4_pvalue_HQC <- temp_rds[[16]]





#1. For each test, determine the best p

H1_best_lag <- array(dim=c(20,20))
H2_best_lag <- array(dim=c(20,20))
H3_best_lag <- array(dim=c(20,20))
H4_best_lag <- array(dim=c(20,20))
rownames(H1_best_lag) <- RT_no_long_covid_no_dot
rownames(H2_best_lag) <- RT_no_long_covid_no_dot
rownames(H3_best_lag) <- RT_no_long_covid_no_dot
rownames(H4_best_lag) <- RT_no_long_covid_no_dot


for(symi_1 in 1:20){
  for(symi_2 in 1:20){

    
    H1_best_lag[symi_1,symi_2] <- which.min(sapply(H4_pvalue_HQC[1:60],function(x) x[symi_1,symi_2]))
    H2_best_lag[symi_1,symi_2] <- which.min(sapply(H4_pvalue_HQC[1:60],function(x) x[symi_1,symi_2]))
    H3_best_lag[symi_1,symi_2] <- which.min(sapply(H4_pvalue_HQC[1:60],function(x) x[symi_1,symi_2]))
    H4_best_lag[symi_1,symi_2] <- which.min(sapply(H4_pvalue_HQC[1:60],function(x) x[symi_1,symi_2]))
    

  }
}

H1_pvalue_best <- array(dim=c(20,20))
H2_pvalue_best <- array(dim=c(20,20))
H3_pvalue_best <- array(dim=c(20,20))
H4_pvalue_best <- array(dim=c(20,20))

rownames(H1_pvalue_best) <- RT_no_long_covid_no_dot
rownames(H2_pvalue_best) <- RT_no_long_covid_no_dot
rownames(H3_pvalue_best) <- RT_no_long_covid_no_dot
rownames(H4_pvalue_best) <- RT_no_long_covid_no_dot

# RT_no_long_covid_no_dot <- c("Local communication policies","Non-pharmacological interventions",
#                        "Health system policies","Vaccine policies")
colnames(H1_pvalue_best) <- RT_no_long_covid_no_dot
colnames(H2_pvalue_best) <- RT_no_long_covid_no_dot
colnames(H3_pvalue_best) <- RT_no_long_covid_no_dot
colnames(H4_pvalue_best) <- RT_no_long_covid_no_dot


for(symi_1 in 1:20){
  for(symi_2 in 1:20){
    
    H1_pvalue_best[symi_1,symi_2] <- H1_pvalue_tGCL[[H1_best_lag[symi_1,symi_2]]][symi_1,symi_2]
    H2_pvalue_best[symi_1,symi_2] <- H2_pvalue_tGCL[[H2_best_lag[symi_1,symi_2]]][symi_1,symi_2]
    H3_pvalue_best[symi_1,symi_2] <- H3_pvalue_tGCL[[H3_best_lag[symi_1,symi_2]]][symi_1,symi_2]
    H4_pvalue_best[symi_1,symi_2] <- H4_pvalue_tGCL[[H4_best_lag[symi_1,symi_2]]][symi_1,symi_2]
  
  }
}


H1_sig <- H1_pvalue_best < 0.05
H2_sig <- H2_pvalue_best < 0.05
H3_sig <- H3_pvalue_best < 0.05
H4_sig <- H4_pvalue_best < 0.05

colSums(H1_sig)/nrow(H1_sig)
colSums(H2_sig)/nrow(H2_sig)

#Reject H1, Cannot reject H3 => confounders



confounding_sym_GC_LC <- H1_sig & !H3_sig
confounding_LC_GC_sym <- H2_sig & !H4_sig

colSums(confounding_sym_GC_LC)/nrow(confounding_sym_GC_LC)
colSums(confounding_LC_GC_sym)/nrow(confounding_LC_GC_sym)

ifelse(confounding_sym_GC_LC,"C","")
ifelse(confounding_LC_GC_sym,"C","")

significant_columns <- RT_no_long_covid_no_dot[order(RT_no_long_covid_no_dot)]
significant_columns <- significant_columns[c(2,3,5,7,9,10,11,12,13,14,18,20)]




write.csv(ifelse(H1_sig[significant_columns,significant_columns],"G",""),"result/H1_sig_media.csv")
write.csv(ifelse(H2_sig[significant_columns,significant_columns],"G",""),"result/H2_sig_media.csv")

write.csv(ifelse(confounding_sym_GC_LC[significant_columns,significant_columns],"C",""),"result/confounding_sym_GC_LC_media.csv")
write.csv(ifelse(confounding_LC_GC_sym[significant_columns,significant_columns],"C",""),"result/confounding_LC_GC_sym_media.csv")

media_coverage_original <- readRDS("news_freq_ts.rds")

plot(media_coverage_original$Ageusia) #Not good
plot(media_coverage_original$Anosmia) #Not good
plot(media_coverage_original$`Chest pain`) #Not good

plot(media_coverage_original$`Clouding of consciousness`)
plot(media_coverage_original$Fatigue)
plot(media_coverage_original$Headache)
plot(media_coverage_original$`Hip pain`) #Not good
plot(media_coverage_original$Hypochondriasis)
plot(media_coverage_original$Insomnia) #Not good
plot(media_coverage_original$Lightheadedness)
plot(media_coverage_original$Palpitations) #Not good
plot(media_coverage_original$`Sleep disorder`) #Not good

colMeans(media_coverage_original)[significant_columns]


