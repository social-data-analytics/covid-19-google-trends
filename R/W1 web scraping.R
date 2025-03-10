library(RSelenium)
setwd(dirname(rstudioapi::getSourceEditorContext()$path))
# remDr <- remoteDriver(
#   port = 4445L,
#   browserName = "firefox"
# )
library('stringr')
u_lower <- 2
u_upper <- 5
rep <- 9
start_day_vec <- seq(from=as.POSIXct("2020-01-01"), by=as.difftime(89, units="days"), to=as.POSIXct("2023-12-31"))
end_day_vec <- start_day_vec + as.difftime(88, units="days")
end_day_vec[length(end_day_vec)] <- as.POSIXct("2023-12-31")

keyword_vec <- c("Long%20COVID",
  "Clouding%20of%20consciousness",
  "Fatigue",
  "Myalgia",
  "Chest%20pain",
  "Mental%20health",
  "Anxiety",
  "Hypochondriasis",
  "Lightheadedness",
  "Hip%20pain",
  "Aching%20Muscle%20Pain",
  "Insomnia",
  "Palpitations",
  "Shortness%20of%20breath",
  "Dizziness",
  "Headache",
  "Ageusia",
  "Chest%20Tightness",
  "Major%20depressive disorder",
  "Sleep%20disorder",
  "Anosmia"
  )



start.time <- Sys.time()

fail_case <- c()
fail_i <- c()
fail_k <- c()

n_day <- length(start_day_vec)
n_keyword <- length(keyword_vec)

for(ss in 1:10){

all_case <- data.frame(i=rep(1:n_day,each=n_keyword),k=rep(1:n_keyword,n_day))
all_case <- all_case[sample(1:nrow(all_case)),]


# for(i in 1:length(start_day_vec)){
#   for(k in 1:length(keyword_vec)){
for(l in 1:nrow(all_case)){
    i <- all_case[l,"i"]
    k <- all_case[l,"k"]
    
    if(!file.exists(paste0("RSV_kw_",k,"_t_",i,"_rep_",rep,".csv"))){
    
    print(paste0("Trial: keyword:",k,", time ",i,", rep ",rep,".csv"))
    retry <- TRUE
    tried_cnt <- 0
    while(retry){
      
    an_trial <- tryCatch({
#Start for loops

start_day <- as.character(start_day_vec[i])
end_day <- as.character(end_day_vec[i])
keyword <- keyword_vec[k]

#Start scraping -------------------------------------------------------------------------------

rD <- rsDriver(browser="firefox", port=4711L, verbose=F, chromever = NULL)
remDr <- rD[["client"]]
# remDr$open()
# remDr$getStatus()
remDr$navigate("https://trends.google.com/")
Sys.sleep(runif(1,u_lower,u_upper))

# action_rand<-runif(1,0,1)
action_rand <- 0.7

if(action_rand<0.5){
  rand_place <- sample(c("HK","IE","JP","CN"),1)
  web_link <- paste0("https://trends.google.com/trends/explore?date=",start_day,"%20",end_day,"&geo=",rand_place,"&q=",keyword,"&hl=en-US")
  remDr$navigate(web_link)
  Sys.sleep(runif(1,u_lower,u_upper))*1.5
  }else{
    click_bar <- remDr$findElement(using = 'xpath', value = '/html/body/c-wiz/div/div[2]/div[4]/div[1]/c-wiz[1]/div/div[1]/div[3]/div/div[1]')
    click_bar$clickElement()
    Sys.sleep(runif(1,u_lower,u_upper))
    
    address_element <- remDr$findElement(using = 'id', value = 'i7')
    for(sub_s in 1:sample(1:4,1)){
      address_element$sendKeysToElement(list(key="backspace"))
      Sys.sleep(runif(1,0.3,0.5))
    }
    Sys.sleep(runif(1,u_lower,u_upper))*2
    string_to_send <- strsplit(list(str_replace_all(keyword,"%20"," "))[[1]],split="")[[1]]
    
    for(sub_s in 1:length(string_to_send)){
      address_element$sendKeysToElement(list(string_to_send[sub_s]))
      Sys.sleep(runif(1,0.3,0.5))
    }
    
    Sys.sleep(runif(1,u_lower,u_upper))
    address_element$sendKeysToElement(list(key="enter")) 
    Sys.sleep(runif(1,10,13))
}

location_button <- remDr$findElement(using = 'xpath', value = '/html/body/div[3]/div[2]/div/header/div/div[3]/ng-transclude/div[2]/div/div/hierarchy-picker[1]/ng-include/div[1]')
Sys.sleep(runif(1,u_lower,u_upper))
location_button$clickElement()
Sys.sleep(runif(1,u_lower,u_upper))
location_area <-  remDr$findElement(using = 'xpath', value = '//*[@id="input-8"]')
#Add randomness at typing
location_area$sendKeysToElement(list("W"))
Sys.sleep(runif(1,0.3,0.5))
location_area$sendKeysToElement(list("o"))
Sys.sleep(runif(1,0.3,0.5))
location_area$sendKeysToElement(list("r"))
Sys.sleep(runif(1,0.3,0.5))
location_area$sendKeysToElement(list("l"))
Sys.sleep(runif(1,0.3,0.5))
location_area$sendKeysToElement(list("d"))
Sys.sleep(runif(1,0.3,0.5))
location_area$sendKeysToElement(list("w"))
Sys.sleep(runif(1,0.3,0.5))
location_area$sendKeysToElement(list("i"))
Sys.sleep(runif(1,0.3,0.5))
location_area$sendKeysToElement(list("d"))
Sys.sleep(runif(1,0.3,0.5))
location_area$sendKeysToElement(list("e"))
#
Sys.sleep(runif(1,u_lower,u_upper))
location_button$clickElement()
Sys.sleep(runif(1,u_lower,u_upper))
location_area$sendKeysToElement(list(key="down_arrow"))
Sys.sleep(runif(1,u_lower,u_upper))
location_area$sendKeysToElement(list(key="enter"))
Sys.sleep(runif(1,u_lower,u_upper))


  # if(action_rand>0.5){
  #Try to choose day first
tryCatch(
{
past_day <- remDr$findElement(using = 'xpath', value = '//*[@id="select_value_label_9"]/span[2]')
past_day$clickElement()
Sys.sleep(runif(1,u_lower,u_upper))
custom_range <- remDr$findElement(using = 'css selector', value = '#select_option_23 > div:nth-child(1)')
custom_range$clickElement()
Sys.sleep(runif(1,u_lower,u_upper))
From <- remDr$findElement(using = 'css selector', value = 'md-datepicker.ng-pristine > div:nth-child(2) > input:nth-child(1)')
Sys.sleep(runif(1,u_lower,u_upper))
for(i in 1:10){
  From$sendKeysToElement(list(key="backspace"))
  Sys.sleep(runif(1,0.3,0.5))
}

#Enter start day one by one
From$sendKeysToElement(list(start_day))
Sys.sleep(runif(1,0.3,0.5))
From$sendKeysToElement(list(key="tab"))
Sys.sleep(runif(1,0.3,0.5))
arrow_next_to_from <- remDr$findElement(using = 'css selector', value = 'md-datepicker.ng-dirty > div:nth-child(2) > button:nth-child(2)')
arrow_next_to_from$sendKeysToElement(list(key="tab"))
##
Sys.sleep(runif(1,u_lower,u_upper))
To <- remDr$findElement(using = 'css selector', value = 'md-datepicker.ng-pristine > div:nth-child(2) > input:nth-child(1)')
for(i in 1:10){
  To$sendKeysToElement(list(key="backspace"))
  Sys.sleep(runif(1,0.3,0.5))
}
To$sendKeysToElement(list(end_day))
Sys.sleep(runif(1,u_lower,u_upper))
OK <- remDr$findElement(using = 'css selector', value = 'button.custom-date-picker-dialog-button:nth-child(3)')
OK$clickElement()
Sys.sleep(runif(1,8,12))
},error=function(e){
  Sys.sleep(runif(1,3,5))
    web_link <- paste0("https://trends.google.com/trends/explore?date=",start_day,"%20",end_day,"&q=",keyword,"&hl=en-US")
    remDr$navigate(web_link)
    Sys.sleep(runif(1,8,12))
}
)
  # }
if(remDr$getCurrentUrl()[[1]] != 
   paste0("https://trends.google.com/trends/explore?date=",start_day,"%20",end_day,"&q=",keyword,"&hl=en-US")){
  web_link <- paste0("https://trends.google.com/trends/explore?date=",start_day,"%20",end_day,"&q=",keyword,"&hl=en-US")
  remDr$navigate(web_link)
  Sys.sleep(runif(1,8,12))
}



# remDr$navigate("https://trends.google.com/")
  
  found_download <- FALSE
  
  for(try_finding in 1:sample(4:6,1)){
      found_download <- tryCatch({
    Download <- remDr$findElement(using = 'xpath', value = '/html/body/div[3]/div[2]/div/md-content/div/div/div[1]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]/i');TRUE
    },error=function(ee) {remDr$refresh();Sys.sleep(runif(1,8,12));FALSE})
      
  }
  
  
  Download$clickElement()

1

    },error=function(e) print("retry")
  )
    tried_cnt <- tried_cnt + 1
  if(an_trial==1 || tried_cnt >=5) retry <- FALSE
    if(tried_cnt >=5){
      fail_case <- c(fail_case,paste0("RSV_kw_",k,"_t_",i,"_rep_",rep,".csv"))
      fail_i <- c(fail_i,i)
      fail_k <- c(fail_k,k)
    }
    
  tryCatch({rD[["server"]]$stop()},error=function(e) print("Cannot close the server."))
}


rD[["server"]]$stop()

#Rename the downloaded file
y <- tryCatch({
  file.rename("multiTimeline.csv",paste0("RSV_kw_",k,"_t_",i,"_rep_",rep,".csv"))
},error=function(e) print("Unable to rename."))
  print(paste0("Success: ",l,"/",nrow(all_case)))
  print(Sys.time()-start.time)
  
    }else{
      print(paste0("RSV_kw_",k,"_t_",i,"_rep_",rep,".csv exists. Skip."))
      print(paste0("Skip: ",l,"/",nrow(all_case)))
      print(Sys.time()-start.time)
    }
  
}


}


