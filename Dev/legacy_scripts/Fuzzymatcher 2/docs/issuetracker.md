# Issue Tracker

Bugs and improvements in the program

- For the matcher_localduescategory(), it can be specialized so that the spreadsheet only contains data for Members. People who aren't members don't get a LocalDuesCategoryId attached to them.

- For the matcher and matcher_localduescategory functions, it might be easier to create a helper function such as name_creator in The Remerger part of the program that takes in a single object and generates all the required category name and id column names in a single dictionary

- In the case where the membership file has two different spellings of the same category entry, and one spelling is a perfect match to the entity file entry, the entity file entry is removed from the pool of fuzzy match candidates for the misspelled entry. This prevents the misspelled membership file entry from fuzzy matching to the entity file entry so its correct entity file name and Id must always be manually entered in the fuzzy match spreadsheet.

  - I decided it was more efficient to remove perfectly matching entries from the pool of fuzzy match candidates then to fix this bug but it can always be relooked at

  

  
  
  

