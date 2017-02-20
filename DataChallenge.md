Take\_Home\_Challenge
================

Data Science Take-Home Challenge - Samba.tv

Loading Required Packages in

PLEASE PLACE DATA FILES IN SAME DIRECTORY

``` r
library(dplyr)
```

    ## 
    ## Attaching package: 'dplyr'

    ## The following objects are masked from 'package:stats':
    ## 
    ##     filter, lag

    ## The following objects are masked from 'package:base':
    ## 
    ##     intersect, setdiff, setequal, union

Reading in provided Data

``` r
test_tab <- read.csv('test_table.csv')
user_tab <- read.csv('user_table.csv')
```

Checking Structure for both tables

``` r
str(test_tab)
```

    ## 'data.frame':    453321 obs. of  9 variables:
    ##  $ user_id         : int  315281 497851 848402 290051 548435 540675 863394 527287 261625 10427 ...
    ##  $ date            : Factor w/ 5 levels "2015-11-30","2015-12-01",..: 4 5 5 4 1 4 5 4 5 5 ...
    ##  $ source          : Factor w/ 3 levels "Ads","Direct",..: 2 1 1 1 1 2 3 2 2 1 ...
    ##  $ device          : Factor w/ 2 levels "Mobile","Web": 2 2 2 1 2 1 1 2 1 1 ...
    ##  $ browser_language: Factor w/ 3 levels "EN","ES","Other": 2 2 2 3 2 2 3 1 2 2 ...
    ##  $ ads_channel     : Factor w/ 5 levels "Bing","Facebook",..: NA 3 2 2 3 NA NA NA NA 2 ...
    ##  $ browser         : Factor w/ 7 levels "Android_App",..: 4 4 2 1 3 1 1 2 1 1 ...
    ##  $ conversion      : int  1 0 0 0 0 0 0 0 0 0 ...
    ##  $ test            : int  0 1 0 1 1 1 0 0 1 0 ...

``` r
str(user_tab)
```

    ## 'data.frame':    452867 obs. of  4 variables:
    ##  $ user_id: int  765821 343561 118744 987753 554597 62371 987967 499510 364726 572551 ...
    ##  $ sex    : Factor w/ 2 levels "F","M": 2 1 2 1 1 2 2 1 1 2 ...
    ##  $ age    : int  20 27 23 27 20 29 31 29 29 21 ...
    ##  $ country: Factor w/ 17 levels "Argentina","Bolivia",..: 10 11 4 17 15 6 15 13 4 2 ...

And the Summaries of both tables to have a high level overview, also changing date from factor to as.Date

``` r
summary(user_tab)
```

    ##     user_id        sex             age             country      
    ##  Min.   :      1   F:188382   Min.   :18.00   Mexico   :128484  
    ##  1st Qu.: 249819   M:264485   1st Qu.:22.00   Colombia : 54060  
    ##  Median : 500019              Median :26.00   Spain    : 51782  
    ##  Mean   : 499945              Mean   :27.13   Argentina: 46733  
    ##  3rd Qu.: 749543              3rd Qu.:31.00   Peru     : 33666  
    ##  Max.   :1000000              Max.   :70.00   Venezuela: 32054  
    ##                                               (Other)  :106088

``` r
summary(test_tab)
```

    ##     user_id                date           source          device      
    ##  Min.   :      1   2015-11-30: 71025   Ads   :181877   Mobile:201756  
    ##  1st Qu.: 249816   2015-12-01: 70991   Direct: 90834   Web   :251565  
    ##  Median : 500019   2015-12-02: 70649   SEO   :180610                  
    ##  Mean   : 499938   2015-12-03: 99493                                  
    ##  3rd Qu.: 749522   2015-12-04:141163                                  
    ##  Max.   :1000000                                                      
    ##                                                                       
    ##  browser_language   ads_channel            browser         conversion     
    ##  EN   : 63137     Bing    : 13689   Android_App:155135   Min.   :0.00000  
    ##  ES   :377547     Facebook: 68425   Chrome     :101929   1st Qu.:0.00000  
    ##  Other: 12637     Google  : 68180   FireFox    : 40766   Median :0.00000  
    ##                   Other   :  4148   IE         : 61715   Mean   :0.04958  
    ##                   Yahoo   : 27435   Iphone_App : 46621   3rd Qu.:0.00000  
    ##                   NA's    :271444   Opera      :  6090   Max.   :1.00000  
    ##                                     Safari     : 41065                    
    ##       test       
    ##  Min.   :0.0000  
    ##  1st Qu.:0.0000  
    ##  Median :0.0000  
    ##  Mean   :0.4764  
    ##  3rd Qu.:1.0000  
    ##  Max.   :1.0000  
    ## 

``` r
#summary might be badly formatted

test_tab$date <- as.Date(test_tab$date)
```

We find that the number of rows don't match in regards to both tables, checking on that further. Also, checking to see if user ids have duplicates

``` r
all(test_tab$user_id %in% user_tab$user_id)
```

    ## [1] FALSE

``` r
paste('Duplicate user ids in test table: ',sum(duplicated(test_tab$user_id)))
```

    ## [1] "Duplicate user ids in test table:  0"

``` r
paste('Duplicate user ids in user table: ',sum(duplicated(user_tab$user_id)))
```

    ## [1] "Duplicate user ids in user table:  0"

We might consider informing the appropriate department about the missing user data.

Quickly Checking to see if there's any pattern within the user ids that are missing from the user table on a high level

``` r
missing_users <- test_tab[which(!(test_tab$user_id %in% user_tab$user_id)),]
summary(missing_users)
```

    ##     user_id            date               source       device   
    ##  Min.   :  1524   Min.   :2015-11-30   Ads   :184   Mobile:205  
    ##  1st Qu.:244920   1st Qu.:2015-12-01   Direct: 96   Web   :249  
    ##  Median :498514   Median :2015-12-03   SEO   :174               
    ##  Mean   :492665   Mean   :2015-12-02                            
    ##  3rd Qu.:727196   3rd Qu.:2015-12-04                            
    ##  Max.   :999040   Max.   :2015-12-04                            
    ##                                                                 
    ##  browser_language   ads_channel         browser      conversion     
    ##  EN   : 58        Bing    : 19   Android_App:158   Min.   :0.00000  
    ##  ES   :387        Facebook: 67   Chrome     :107   1st Qu.:0.00000  
    ##  Other:  9        Google  : 67   FireFox    : 45   Median :0.00000  
    ##                   Other   :  5   IE         : 59   Mean   :0.06828  
    ##                   Yahoo   : 26   Iphone_App : 47   3rd Qu.:0.00000  
    ##                   NA's    :270   Opera      :  6   Max.   :1.00000  
    ##                                  Safari     : 32                    
    ##       test       
    ##  Min.   :0.0000  
    ##  1st Qu.:0.0000  
    ##  Median :0.0000  
    ##  Mean   :0.4604  
    ##  3rd Qu.:1.0000  
    ##  Max.   :1.0000  
    ## 

Checking proportions of Users in missing user table and total test table in regards to conversion and test/control group to see if there's an imbalance

``` r
paste('Missing User Conversion rate', mean(missing_users$conversion))
```

    ## [1] "Missing User Conversion rate 0.0682819383259912"

``` r
paste('Missing User split rate', mean(missing_users$test))
```

    ## [1] "Missing User split rate 0.460352422907489"

``` r
paste('Total User Conversion rate', mean(test_tab$conversion))
```

    ## [1] "Total User Conversion rate 0.0495785547106796"

``` r
paste('Total User split rate', mean(test_tab$test))
```

    ## [1] "Total User split rate 0.476446050370488"

Nothing extremely glaring stands out, we can revisit the missing persons later to see if there's anything important

Let's go ahead and merge both the tables and look at conversion rates by country,

``` r
totaldata <- merge(x = test_tab, y = user_tab, by = 'user_id', all.x = TRUE)

by_country <- totaldata %>% 
              group_by(country) %>% 
              summarize(conversionRate = mean(conversion)) %>%
              arrange(desc(conversionRate))

by_country
```

    ## # A tibble: 18 × 2
    ##        country conversionRate
    ##         <fctr>          <dbl>
    ## 1        Spain     0.07971882
    ## 2           NA     0.06828194
    ## 3   Costa Rica     0.05349407
    ## 4    Nicaragua     0.05339878
    ## 5     Colombia     0.05133185
    ## 6  El Salvador     0.05076453
    ## 7       Mexico     0.05034090
    ## 8         Peru     0.05025842
    ## 9        Chile     0.04970360
    ## 10   Venezuela     0.04966619
    ## 11   Guatemala     0.04965289
    ## 12    Honduras     0.04925303
    ## 13     Ecuador     0.04907204
    ## 14    Paraguay     0.04886348
    ## 15     Bolivia     0.04863359
    ## 16      Panama     0.04808909
    ## 17   Argentina     0.01399439
    ## 18     Uruguay     0.01282051

We can confirm that Spain has the highest conversion rates, note : the NAs are the missing users we saw above

On a high level, checking conversion rate by country and test group, removing spain and NAs

``` r
by_countryAndGroup <- totaldata %>% 
              filter(country != 'Spain' & !is.na(country)) %>%
              group_by(country, test) %>% 
              summarize(conversionRate = mean(conversion)) %>%
              arrange(desc(conversionRate))

by_countryAndGroup
```

    ## Source: local data frame [32 x 3]
    ## Groups: country [16]
    ## 
    ##        country  test conversionRate
    ##         <fctr> <int>          <dbl>
    ## 1   Costa Rica     1     0.05473764
    ## 2    Nicaragua     1     0.05417676
    ## 3  El Salvador     0     0.05355404
    ## 4    Nicaragua     0     0.05264697
    ## 5   Costa Rica     0     0.05225564
    ## 6     Colombia     0     0.05208949
    ## 7        Chile     1     0.05129502
    ## 8       Mexico     1     0.05118631
    ## 9     Honduras     0     0.05090576
    ## 10   Guatemala     0     0.05064288
    ## # ... with 22 more rows

Uruguay and Argentina seem to be performing really badly, and we can explore further about what other factors might be indicative of that

The test is clearly trying to examine the effect of a localized translation by country, so to make sure the experiment was designed properly, we can check group assignment by country.

``` r
split_by_country <- totaldata %>% 
              filter(country != 'Spain' & !is.na(country)) %>%
              group_by(country) %>% 
              summarize(split_rate = mean(test)) %>%
              arrange(desc(split_rate))

split_by_country
```

    ## # A tibble: 16 × 2
    ##        country split_rate
    ##         <fctr>      <dbl>
    ## 1      Uruguay  0.8996130
    ## 2    Argentina  0.7997989
    ## 3     Paraguay  0.5031986
    ## 4       Panama  0.5024045
    ## 5      Bolivia  0.5010787
    ## 6        Chile  0.5007853
    ## 7       Mexico  0.5002568
    ## 8   Costa Rica  0.4989640
    ## 9         Peru  0.4989307
    ## 10    Colombia  0.4989271
    ## 11 El Salvador  0.4974924
    ## 12   Venezuela  0.4961939
    ## 13   Guatemala  0.4960661
    ## 14     Ecuador  0.4944322
    ## 15   Nicaragua  0.4914473
    ## 16    Honduras  0.4910131

So, Uruguay and Argentina look like they a very biased split rate between control and experiment, with a ~90% test group in Uruguay and ~80% test group in Argentina. This would definitely add bias to the test.

Another thing noticed was the availability of test data for only 5 days. Running the test for a little longer might help provide better insight

Looking at conversion rates by date to see if anything stands out

``` r
conversion_by_date <- totaldata %>% 
              filter(country != 'Spain' & !is.na(country)) %>%
              group_by(date) %>% 
              summarize(conversionRate = mean(conversion)) %>%
              arrange(date)

conversion_by_date
```

    ## # A tibble: 5 × 2
    ##         date conversionRate
    ##       <date>          <dbl>
    ## 1 2015-11-30     0.04725750
    ## 2 2015-12-01     0.04362219
    ## 3 2015-12-02     0.04618712
    ## 4 2015-12-03     0.04637385
    ## 5 2015-12-04     0.04513427

There doesn't seem to be a lot of variance in conversion rates across the period.

Based on our assumptions so far, running a two tailed t-test to validate the accuracy of previously reported findings

``` r
testable_data <- totaldata %>%
                 filter(!(country %in% c('Spain','Argentina','Uruguay')) & !is.na(country))

t_test1 <- t.test(testable_data$conversion[testable_data$test==1],testable_data$conversion[testable_data$test==0])

t_test1
```

    ## 
    ##  Welch Two Sample t-test
    ## 
    ## data:  testable_data$conversion[testable_data$test == 1] and testable_data$conversion[testable_data$test == 0]
    ## t = 0.35835, df = 350200, p-value = 0.7201
    ## alternative hypothesis: true difference in means is not equal to 0
    ## 95 percent confidence interval:
    ##  -0.001182831  0.001712121
    ## sample estimates:
    ##  mean of x  mean of y 
    ## 0.05041276 0.05014811

The Null Hypothesis has been accepted, there isn't a significant difference between the conversion rates of localized or a non-localized translation

``` r
testable_data_1 <- totaldata %>%
                 filter(country !='Spain' & !is.na(country))

t_test2 <- t.test(testable_data_1$conversion[testable_data_1$test==1],testable_data_1$conversion[testable_data_1$test==0])

t_test2
```

    ## 
    ##  Welch Two Sample t-test
    ## 
    ## data:  testable_data_1$conversion[testable_data_1$test == 1] and testable_data_1$conversion[testable_data_1$test == 0]
    ## t = -7.3539, df = 385260, p-value = 1.929e-13
    ## alternative hypothesis: true difference in means is not equal to 0
    ## 95 percent confidence interval:
    ##  -0.006181421 -0.003579837
    ## sample estimates:
    ##  mean of x  mean of y 
    ## 0.04341116 0.04829179

By running a t-test on the alternative possibility of including possibly bias-inducing data from Argentina and Uruguay, we find the results to be similar to what was observed in the initial findings

Controlling for the imbalances in split groups in Argentina/Uruguay seems to show that the localized version wasn't really negatively affecting conversion rates as much as stated.

Getting p-values by country, and conversion rates

``` r
test_by_country <- totaldata %>% 
                   group_by(country) %>%
                   filter(country != "Spain" & !is.na(country)) %>%
                   summarize(
                        split_ratio = mean(test),
                        control_count=n()*(1-split_ratio),
                        test_count=n()*(split_ratio),
                        control_conversion = mean(conversion[test==0]),
                        test_conversion = mean(conversion[test==1]),
                        p_values = t.test(conversion[test==1],conversion[test==0])$p.value,
                        Validity = p_values<0.05
                        ) %>%
                    arrange(p_values)

test_by_country
```

    ## # A tibble: 16 × 8
    ##        country split_ratio control_count test_count control_conversion
    ##         <fctr>       <dbl>         <dbl>      <dbl>              <dbl>
    ## 1       Mexico   0.5002568         64209      64275         0.04949462
    ## 2  El Salvador   0.4974924          4108       4067         0.05355404
    ## 3        Chile   0.5007853          9853       9884         0.04810718
    ## 4    Argentina   0.7997989          9356      37377         0.01507054
    ## 5     Colombia   0.4989271         27088      26972         0.05208949
    ## 6     Honduras   0.4910131          4361       4207         0.05090576
    ## 7    Guatemala   0.4960661          7622       7503         0.05064288
    ## 8    Venezuela   0.4961939         16149      15905         0.05034367
    ## 9   Costa Rica   0.4989640          2660       2649         0.05225564
    ## 10      Panama   0.5024045          1966       1985         0.04679552
    ## 11     Bolivia   0.5010787          5550       5574         0.04936937
    ## 12        Peru   0.4989307         16869      16797         0.04991404
    ## 13   Nicaragua   0.4914473          3419       3304         0.05264697
    ## 14     Uruguay   0.8996130           415       3719         0.01204819
    ## 15    Paraguay   0.5031986          3650       3697         0.04849315
    ## 16     Ecuador   0.4944322          8036       7859         0.04915381
    ## # ... with 3 more variables: test_conversion <dbl>, p_values <dbl>,
    ## #   Validity <lgl>

We notice that there is no significant difference between localized and non-localized translations on the website.

The table above runs a t-test based on Individual Latin American countries since the localized languages are based on those countries, The final column of Validity provides FALSE when test is insignificant with a significance value of 0.05, and TRUE when test is significant

Since we accept the NULL hypothesis, we can assume that the conversion rate hasn't increased either. One of the recommendations would be to increase the duration of the test beyond the 5 day period.

Conclusions: - Since the use of localized/non-localized translations happened by country, it would be fair to run t-tests individually grouped by countries. - Further Investigation on use of 80/20 and 90/10 split for test/control in Uruguay, Argentina - Test was run for 5 days, would gain more information regarding business use case and possibly run it for longer
