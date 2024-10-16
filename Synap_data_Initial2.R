# Automating Synap Data Analysis for SAT Score Reports
# Higher Ground Learning
# Sept 26 2023

library(dplyr)
library(stringr)
library(ggplot2)
library(gganimate)
library(plotly)
library(viridis)
library(hrbrthemes)
library(reshape2)
library(tidyr)
library(GGally)
library(tibble)
library(tidyr)
library(stringi)
library(vctrs)
library(purrr)

# setwd()

#TODO: remove hard code of filename.
Synap_raw <- read.csv("./sample_data/sat_synap_test.csv", header = FALSE, stringsAsFactors = FALSE)

# Hard coding columns?
Synap_rename <- Synap_raw %>% 
  rename(RW1_1 = 34,RW1_2 = 35,RW1_3 = 36,RW1_4 = 37,RW1_5 = 38,RW1_6 = 39,RW1_7 = 40,RW1_8 = 41,RW1_9 = 42,RW1_10 = 43,RW1_11 = 44,RW1_12 = 45,RW1_13 = 46,RW1_14 = 47,RW1_15 = 48,RW1_16 = 49,RW1_17 = 50, RW1_18 = 51,RW1_19 = 52,RW1_20 = 53,RW1_21 = 54,RW1_22 = 55,RW1_23 = 56,RW1_24 = 57,RW1_25 = 58,RW1_26 = 59,RW1_27 = 60,RW2_1 = 61,RW2_2 = 62,RW2_3 = 63,RW2_4 = 64,RW2_5 = 65,RW2_6 = 66,RW2_7 = 67,RW2_8 = 68,RW2_9 = 69,RW2_10 = 70,RW2_11 = 71, RW2_12 = 72, RW2_13 = 73, RW2_14 = 74,RW2_15 = 75,RW2_16 = 76, RW2_17 = 77,RW2_18 = 78,RW2_19 = 79,RW2_20 = 80,RW2_21 = 81, RW2_22 = 82,RW2_23 = 83,RW2_24 = 84, RW2_25 = 85,RW2_26 = 86,RW2_27 = 87, M1_1 = 89, M1_2 = 90, M1_3 = 91, M1_4 = 92, M1_5 = 93, M1_6 = 94, M1_7 = 95, M1_8 = 96, M1_9 = 97, M1_10 = 98, M1_11 = 99, M1_12 = 100, M1_13 = 101, M1_14 = 102, M1_15 = 103, M1_16 = 104, M1_17 = 105, M1_18 = 106, M1_19 = 107, M1_20 = 108, M1_21 = 109, M1_22 = 110, M2_1 = 111, M2_2 = 112, M2_3 = 113, M2_4 = 114, M2_5 = 115, M2_6 = 116, M2_7 = 117, M2_8 = 118, M2_9 = 119, M2_10 = 120, M2_11 = 121, M2_12 = 122, M2_13 = 123, M2_14 = 124, M2_15 = 125, M2_16 = 126, M2_17 = 127, M2_18 = 128, M2_19 = 129, M2_20 = 130, M2_21 = 131, M2_22 = 132)

# Removing Question specific meta data
Synap_trim <- Synap_rename %>% 
  filter(!row_number() %in% c(1:7))

unique_names <- unique(Synap_trim$V3)

#Exporting student-specific info into a .csv file for admin use
student_info <- Synap_trim %>% 
  select(V2,V3, V13, V14, V15) %>% 
  slice(-(1:2))

write.csv(student_info, file = "./Output_Files/student_info.csv")

#Dropping extraneous columns for analytical dataframe
Synap_trim2 <- Synap_trim %>% 
  select(- c(V1, V4, V5, V6, V7, V8, V9, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25, V26, V27, V28, V29, V30, V31, V32, V33)) %>% 
  rename(User.name = V2, User.email = V3)

#creating subset data frame where I make each row a question's data, similar to what's on the report page of the google sheets

#Reading/Writing Module 1 ####

#Changing the format so that each row corresponds to a question for Reading/Writing Module 1 (RWM1)
RWM1_transposed <- Synap_trim2 %>% 
  select(User.email,User.name,starts_with("RW1")) %>% 
  pivot_longer(cols = starts_with("RW1"), names_to = "QuestionNumber", values_to = "Answer")

#Making new Quesion_Domain column with the types of questions repeated until the end of the dataframe
## Calculate the number of times to repeat the initial 27 elements to match the number of rows in the dataset
repeat_times_domain <- ceiling(nrow(RWM1_transposed)/27) #ceiling ensures rounding up to the nearest whole number

RWM1_transposed2 <- RWM1_transposed %>% 
  mutate(Question_Domain = rep(Answer[1:27], times= repeat_times_domain)[1:nrow(RWM1_transposed)]) ##repeats the first 27 elements of the "Answer" column
##Selects only the number of rows that match the original dataset

#Making new Correct_Answer column with the correct answer repeated until the end of the dataframe
repeat_times_answer <- ceiling(nrow(RWM1_transposed)/27)

RWM1_transposed3 <- RWM1_transposed2 %>% 
  mutate(Correct_Answer = rep(Answer[28:54], times= repeat_times_domain)[1:nrow(RWM1_transposed)])

#Getting rid of the first 54 rows that only contained the correct answer data and question type data
RWM1_transposed4 <- RWM1_transposed3 %>% 
  slice(55:n())

#Creating new column that will give points if student answer is correct; also renaming columns to match what's on Google Sheets
RWM1_points <- RWM1_transposed4 %>% 
  mutate(Point = ifelse(Answer == Correct_Answer,1,0))

RWM1_points2 <- RWM1_points %>% 
  rename("Student Answer" = Answer,
         "Correct Answer" = Correct_Answer,
         "Question Domain" = Question_Domain)

#Making a new column that makes a simple question number
RWM1_points3 <- RWM1_points2 %>% 
  mutate("Question" = as.numeric(str_extract(QuestionNumber, "(?<=RW1_)\\d+")))
##(?<-RW1_): The text must be preceded by RW1_
##\\d: matches any single digit 0-9
##+: quantifies one or more digits for the preceding element

RWM1_final <- RWM1_points3 %>% 
  select(c("User.email", "User.name", "Question", "Correct Answer", "Student Answer", "Point", "Question Domain"))
  
#Reading/Writing Module 2 ####

#Changing the format so that each row corresponds to a question for Reading/Writing Module 2 (RWM2)
RWM2_transposed <- Synap_trim2 %>% 
  select(User.email,User.name,starts_with("RW2")) %>% 
  pivot_longer(cols = starts_with("RW2"), names_to = "QuestionNumber", values_to = "Answer")

#Making new Quesion_Domain column with the types of questions repeated until the end of the dataframe
repeat_times_domain2 <- ceiling(nrow(RWM2_transposed)/27)

RWM2_transposed2 <- RWM2_transposed %>% 
  mutate(Question_Domain = rep(Answer[1:27], times= repeat_times_domain2)[1:nrow(RWM2_transposed)])

#Making new Correct_Answer column with the correct answer repeated until the end of the dataframe
repeat_times_answer2 <- ceiling(nrow(RWM2_transposed)/27)

RWM2_transposed3 <- RWM2_transposed2 %>% 
  mutate(Correct_Answer = rep(Answer[28:54], times= repeat_times_answer2)[1:nrow(RWM2_transposed)])

#Getting rid of the first 54 rows that only contained the correct answer data and question type data
RWM2_transposed4 <- RWM2_transposed3 %>% 
  slice(55:n())

#Creating new column that will give points if student answer is correct; also renaming columns to match what's on Google Sheets

RWM2_points <- RWM2_transposed4 %>% 
  mutate(Point = ifelse(Answer == Correct_Answer,1,0))

RWM2_points2 <- RWM2_points %>% 
  rename("Student Answer" = Answer,
         "Correct Answer" = Correct_Answer,
         "Question Domain" = Question_Domain)

#Making a new column that makes a simple question number
RWM2_points3 <- RWM2_points2 %>% 
  mutate("Question" = as.numeric(str_extract(QuestionNumber, "(?<=RW2_)\\d+")))

RWM2_final <- RWM2_points3 %>% 
  select(c("User.email", "User.name", "Question", "Correct Answer", "Student Answer", "Point", "Question Domain"))

#Math Module 1 ####

#Changing the format so that each row corresponds to a question for Math Module 1 (MM1)
MM1_transposed <- Synap_trim2 %>% 
  select(User.email,User.name,starts_with("M1")) %>% 
  pivot_longer(cols = starts_with("M1"), names_to = "QuestionNumber", values_to = "Answer")

#Making new Quesion_Domain column with the types of questions repeated until the end of the dataframe
repeat_times_domain3 <- ceiling(nrow(MM1_transposed)/22)

MM1_transposed2 <- MM1_transposed %>% 
  mutate(Question_Domain = rep(Answer[1:22], times= repeat_times_domain3)[1:nrow(MM1_transposed)])

#Making new Correct_Answer column with the correct answer repeated until the end of the dataframe
repeat_times_answer3 <- ceiling(nrow(MM1_transposed)/22)

MM1_transposed3 <- MM1_transposed2 %>% 
  mutate(Correct_Answer = rep(Answer[23:44], times= repeat_times_domain)[1:nrow(MM1_transposed)])

#Getting rid of the first 45 rows that only contained the correct answer data and question type data
MM1_transposed4 <- MM1_transposed3 %>% 
  slice(45:n())

#Creating new column that will give points if student answer is correct; also renaming columns to match what's on Google Sheets
MM1_points <- MM1_transposed4 %>% 
  mutate(Point = ifelse(Answer == Correct_Answer,1,0))

MM1_points2 <- MM1_points %>% 
  rename("Student Answer pre" = Answer,
         "Correct Answer" = Correct_Answer,
         "Question Domain" = Question_Domain)

#Making a new column that makes a simple question number
MM1_points3 <- MM1_points2 %>% 
  mutate("Question" = as.numeric(str_extract(QuestionNumber, "(?<=M1_)\\d+")))

MM1_final <- MM1_points3 %>% 
  select(c("User.email", "User.name", "Question", "Correct Answer", "Student Answer pre", "Point", "Question Domain"))

#Extracting numeric values in the character string of Student Answer
extract_numeric_values2 <- function(text) {
  # Remove HTML tags (e.g., <p>) from the text
  clean_text <- str_replace_all(text, "<.*?>", "")
  # Check if the cleaned text contains a fraction (e.g., "a/b")
  if (grepl("\\d/\\d", clean_text)) {
    return(clean_text)
  } else {
    # If not a fraction, extract numeric values
    numeric_values <- str_extract(clean_text, "-?\\d+\\.?\\d*")
    return(numeric_values)
  }
}

MM1_final$`Student Answer` <- sapply(MM1_final$`Student Answer pre`, function(text) {
  numeric_value <- extract_numeric_values2(text)
  if(!is.na(numeric_value)) {
    return(numeric_value)
  } else {
    return(text)
  }
})

MM1_final2 <- MM1_final %>%
  mutate(Correct_Answers = str_split(`Correct Answer`, ", ")) %>%
  rowwise() %>%
  mutate(Point = ifelse(Question %in% c(16), any(`Student Answer` %in% Correct_Answers), `Student Answer` == `Correct Answer`)) %>%
  ungroup() %>%
  select(-Correct_Answers)

MM1_final2$Point <- as.numeric(MM1_final2$Point) 

MM1_final3 <- MM1_final2 %>% 
  select(-`Student Answer pre`)

#Math Module 2 ####

#Changing the format so that each row corresponds to a question for Math Module 2 (MM2)
MM2_transposed <- Synap_trim2 %>% 
  select(User.email,User.name,starts_with("M2")) %>% 
  pivot_longer(cols = starts_with("M2"), names_to = "QuestionNumber", values_to = "Answer")

#Making new Quesion_Domain column with the types of questions repeated until the end of the dataframe
repeat_times_domain4 <- ceiling(nrow(MM2_transposed)/22)

MM2_transposed2 <- MM2_transposed %>% 
  mutate(Question_Domain = rep(Answer[1:22], times= repeat_times_domain4)[1:nrow(MM2_transposed)])

#Making new Correct_Answer column with the correct answer repeated until the end of the dataframe
repeat_times_answer4 <- ceiling(nrow(MM2_transposed)/22)

MM2_transposed3 <- MM2_transposed2 %>% 
  mutate(Correct_Answer = rep(Answer[23:44], times= repeat_times_answer4)[1:nrow(MM2_transposed)])

#Getting rid of the first 44 rows that only contained the correct answer data and question type data
MM2_transposed4 <- MM2_transposed3 %>% 
  slice(45:n())

#Creating new column that will give points if student answer is correct; also renaming columns to match what's on Google Sheets
MM2_points <- MM2_transposed4 %>% 
  mutate(Point = ifelse(Answer == Correct_Answer,1,0))

MM2_points2 <- MM2_points %>% 
  rename("Student Answer pre" = Answer,
         "Correct Answer" = Correct_Answer,
         "Question Domain" = Question_Domain)

#Making a new column that makes a simple question number
MM2_points3 <- MM2_points2 %>% 
  mutate("Question" = as.numeric(str_extract(QuestionNumber, "(?<=M2_)\\d+")))

MM2_final <- MM2_points3 %>% 
  select(c("User.email", "User.name", "Question", "Correct Answer", "Student Answer pre", "Point", "Question Domain")) 
  # ungroup()

#Extracting numeric values in the character string of Student Answer
extract_numeric_values <- function(text) {
  # Remove HTML tags (e.g., <p>) from the text
  clean_text <- str_replace_all(text, "<.*?>", "")
  # Check if the cleaned text contains a fraction (e.g., "a/b")
  if (grepl("\\d/\\d", clean_text)) {
    return(clean_text)
  } else {
    # If not a fraction, extract numeric values
    numeric_values <- str_extract(clean_text, "-?\\d+\\.?\\d*")
    return(numeric_values)
  }
}

MM2_final$`Student Answer` <- sapply(MM2_final$`Student Answer pre`, function(text) {
  numeric_value <- extract_numeric_values(text)
  if(!is.na(numeric_value)) {
    return(numeric_value)
  } else {
    return(text)
  }
})

MM2_final2 <- MM2_final %>%
  mutate(Correct_Answers = str_split(`Correct Answer`, ", ")) %>%
  rowwise() %>%
  mutate(Point = ifelse(Question %in% c(9, 16), any(`Student Answer` %in% Correct_Answers), `Student Answer` == `Correct Answer`)) %>%
  ungroup() %>%
  select(-Correct_Answers)

MM2_final2$Point <- as.numeric(MM2_final2$Point)

MM2_final3 <- MM2_final2 %>% 
  select(-`Student Answer pre`)

#Combining all modules ####

RWM1_final <- RWM1_final %>% 
  mutate(Source = "RWM1")

RWM2_final <- RWM2_final %>% 
  mutate(Source = "RWM2")

MM1_final3 <- MM1_final3 %>% 
  mutate(Source = "MM1")

MM2_final3 <- MM2_final3 %>% 
  mutate(Source = "MM2")

#Combining all of the section dataframes and writing out a .csv ####

full_comb <- rbind(RWM1_final, RWM2_final, MM1_final3, MM2_final3)

write.csv(full_comb, file = "./Output_Files/full_comb.csv")

#RMarkdown report for each individual ####
unique_names <- unique(full_comb$User.email)

for(email in unique_names){
  individual_data <- full_comb %>% 
    filter(User.email == email)
  rmarkdown::render(
    input = "Individual_report_SAT1.Rmd",
    output_file = paste0(email, "_report.html"),
    params = list(User.email = email, User.name = unique(individual_data$User.name)),
    output_dir = "./HGL/SAT_1_Students"
  )
}