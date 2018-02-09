## 2018/02/02

### Revised Non-Blind Predictions fromr Stefan M. Kast

nb### unique IDs will be used for non-blind submissions that were made 
after challenge deadline.

Stefan M. Kast submitted revisions for type III pKa predictions for SM22.
Only SM22 macroscopic pKa predictions were modified. 

New submission files:
./20180127_corrections_Kast  
typeIII-ECRISM-3.csv
typeIII-ECRISM-4.csv
typeIII-ECRISM-5.csv
typeIII-ECRISM-6.csv
typeIII-ECRISM-7.csv
typeIII-ECRISM-8.csv

I renamed these files to match the expected format coming from submission system.
$ cp typeIII-ECRISM-3.csv nb001-976-typeIII-ECRISM-3.csv
$ cp nb001-976-typeIII-ECRISM-3.csv ../../typeIII_predictions

$ cp typeIII-ECRISM-4.csv nb002-976-typeIII-ECRISM-4.csv
$ cp nb002-976-typeIII-ECRISM-4.csv ../../typeIII_predictions

$ cp typeIII-ECRISM-5.csv nb003-976-typeIII-ECRISM-5.csv
$ cp nb003-976-typeIII-ECRISM-5.csv ../../typeIII_predictions

$ cp typeIII-ECRISM-6.csv nb004-976-typeIII-ECRISM-6.csv
$ cp nb004-976-typeIII-ECRISM-6.csv ../../typeIII_predictions

$ cp typeIII-ECRISM-7.csv nb005-976-typeIII-ECRISM-7.csv 
$ cp nb005-976-typeIII-ECRISM-7.csv ../../typeIII_predictions

$ cp typeIII-ECRISM-8.csv nb006-976-typeIII-ECRISM-8.csv 
$ cp nb006-976-typeIII-ECRISM-8.csv  ../../typeIII_predictions


## 2018/02/05

### Epik Reference Calculations for Type III

Bas Rustenburg provided type III pKa predictions calculated by Epik. 
These will be used as reference calculations.

./20180205_Epik_typeIII_Rustenburg/typeIII-epik_sequential-1.csv

I renamed this file to match the expected format coming from submission system.
$ cp typeIII-epik_sequential-1.csv nb007-976-typeIII-epik_sequential-1.csv
$ cp nb007-976-typeIII-epik_sequential-1.csv ../typeIII_predictions


## 2018/02/09

I had to manually fix some non-UTF-8 characters in some submissions.

I removed Stefan Kast's initial submissions( later replaced by nb001-nb006) from typeIII_predictions directory.

(py35) lski1946:typeIII_predictions isikm$ ls *976-typeIII-ECRISM-3.csv  
7r4si-976-typeIII-ECRISM-3.csv nb001-976-typeIII-ECRISM-3.csv
(py35) lski1946:typeIII_predictions isikm$ mv 7r4si-976-typeIII-ECRISM-3.csv /Users/isikm/lab/SAMPL6-repos/sampl6-physicochemical-properties/predictions/20180127_corrections_Kast/removed
(py35) lski1946:typeIII_predictions isikm$ ls *-976-typeIII-ECRISM-4.csv 
nb002-976-typeIII-ECRISM-4.csv u3ufx-976-typeIII-ECRISM-4.csv
(py35) lski1946:typeIII_predictions isikm$ mv u3ufx-976-typeIII-ECRISM-4.csv /Users/isikm/lab/SAMPL6-repos/sampl6-physicochemical-properties/predictions/20180127_corrections_Kast/removed
(py35) lski1946:typeIII_predictions isikm$ ls *-976-typeIII-ECRISM-5.csv 
5cte6-976-typeIII-ECRISM-5.csv nb003-976-typeIII-ECRISM-5.csv
(py35) lski1946:typeIII_predictions isikm$ mv 5cte6-976-typeIII-ECRISM-5.csv /Users/isikm/lab/SAMPL6-repos/sampl6-physicochemical-properties/predictions/20180127_corrections_Kast/removed
(py35) lski1946:typeIII_predictions isikm$ ls *-976-typeIII-ECRISM-6.csv 
jwvdv-976-typeIII-ECRISM-6.csv nb004-976-typeIII-ECRISM-6.csv
(py35) lski1946:typeIII_predictions isikm$ mv jwvdv-976-typeIII-ECRISM-6.csv /Users/isikm/lab/SAMPL6-repos/sampl6-physicochemical-properties/predictions/20180127_corrections_Kast/removed
(py35) lski1946:typeIII_predictions isikm$ ls *-976-typeIII-ECRISM-7.csv 
fsjzf-976-typeIII-ECRISM-7.csv nb005-976-typeIII-ECRISM-7.csv
(py35) lski1946:typeIII_predictions isikm$ mv fsjzf-976-typeIII-ECRISM-7.csv /Users/isikm/lab/SAMPL6-repos/sampl6-physicochemical-properties/predictions/20180127_corrections_Kast/removed
(py35) lski1946:typeIII_predictions isikm$ ls *-976-typeIII-ECRISM-8.csv 
64b4o-976-typeIII-ECRISM-8.csv nb006-976-typeIII-ECRISM-8.csv
(py35) lski1946:typeIII_predictions isikm$ mv 64b4o-976-typeIII-ECRISM-8.csv /Users/isikm/lab/SAMPL6-repos/sampl6-physicochemical-properties/predictions/20180127_corrections_Kast/removed

I decided that it will be better to keep a copy of adjusted submission file bundle under type III analysis directory.

$ tar -cvf typeIII_predictions.tar typeIII_predictions
$  mv typeIII_predictions.tar ../analysis_of_pKa_predictions/analysis_of_typeIII_predictions/

