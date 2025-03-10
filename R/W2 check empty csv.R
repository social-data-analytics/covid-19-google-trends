problem_i <- c()
problem_k <- c()

for(i in 1:length(start_day_vec)){
  for(k in 1:length(keyword_vec)){

    if(file.info(paste0("RSV_kw_",k,"_t_",i,"_rep_",rep,".csv"))$size == 0){
      problem_i <- c(problem_i,i)
      problem_k <- c(problem_k,k)
    }
  }
}