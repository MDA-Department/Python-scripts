# Program 1 (The Fuzzy matcher)

## member_id_creator(member_file_path, col_name)

Creates DataFrame with the necessary data for the fuzzy match from the membership file if it exists. 

### Parameters: 

**member_file_path :** ***Path***

The path where the membership file is located. 

**col_name : *str***

The name of the column that contains the category data necessary for the fuzzy match in the membership file. 

### Returns:

**DataFrame**

Contains columns for category name, corresponding Id data, and category name conjoined to Id for every unique category name-Id pair in the membership file.

### Notes:

- If the directory is set correctly in main() the program will loop through files in the directory and determine the member_file_path name itself.
- If the configuration file is set correctly the program will loop through the category names listed and determine the col_name itself.
- The category name conjoined to Id column in the returned DataFrame is used as a unique index for the membership data for the rest of the program.

### Examples:



## entity_file_creator(entity_file_path, ws_name)

Creates DataFrame with the necessary data for the fuzzy match from the entity file if it exists. 

### Parameters:

**entity_file_path : *Path***

The path where the entity file is located. 

**ws_name : *str***

The name of the worksheet that contains the category data necessary for the fuzzy match in the entity file. 

### Returns:

**DataFrame**

Contains columns for category name and corresponding Id data in the entity file.

### Notes:

- If the directory is set correctly in main() the program will loop through files in the directory and determine the entity_file_path name itself.
- If the configuration file is set correctly the program will loop through the category names listed and determine the ws_name itself.

### Examples:



## clean(col_name, member_df, member_file_path)

Uses an external dictionary to add a column of cleaned category data to the membership DataFrame.

### Parameters:

**col_name: *str***

The name of the column that contains the category data necessary for the fuzzy match in the membership file. 

**member_df: *DataFrame***

A DataFrame of data necessary for the fuzzy match from the membership file. 

**member_file_path: *Path***

The path where the membership file is located. 

### Returns:

**DataFrame**

 A copy of the member_df DataFrame with an additional column of cleaned category data.

### Notes:

- If the configuration file is set correctly the program will loop through the category names listed and determine the col_name itself.
- If the directory is set correctly in main() the program will loop through files in the directory and determine the member_file_path name itself.
- The member_df should be generated from the member_id_creator() function.
- member_file_path is used to locate a csv file known as the cleaning dictionary. In order for the program to work, a local must have a cleaning dictionary. The cleaning dictionary contains pairs, with the first item being a string found in the membership DataFrame and the second item being a string to replace the first item with in the membership DataFrame. A local's cleaning dictionary must be manually created by the user.
- The additional column of cleaned category data is the column the fuzzy match is performed on for the membership file side. This is intended to increase the accuracy of the fuzzy match to the entity file. 

### Examples:



## matcher(member_df, entity_df, mem_col_name, cleaned_mem_col_name, enti_col_name, enti_col_id)

Performs the fuzzy match.

### Parameters:

**member_df: *DataFrame***

A DataFrame of data necessary for the fuzzy match from the membership file. 

**entity_df: *DataFrame***

A DataFrame of data necessary for the fuzzy match from the entity file. 

**mem_col_name: *str***

The column name for the category data in the membership file. 

**cleaned_mem_col_name: *str***

The column name for the cleaned category data in the membership file. 

**enti_col_name: *str***

The column name for the category data in the entity file. 

**enti_col_id: *str***

The column name for the category Id data in the entity file. 

### Returns:

**DataFrame**

A DataFrame of the fuzzy match results. Contains the category data in the membership file alongside the best match(es) to the category data in the entity file based on category name and Unit or Employer Id. 

### Notes:

- Have considered creating a helper function that would allow a single object to be passed into parameter and create all the name and id strings similar to the name_creator() found in The Remerger. Unsure if this would be more efficient. Idea for later development.

### Examples:



## merger_localduescategory(member_df, entity_df, mem_col_name, cleaned_mem_col_name, enti_col_name, enti_col_id)

Performs the fuzzy match for LocalDuesCategory data category.

### Parameters:

**member_df: *DataFrame***

A DataFrame of data necessary for the fuzzy match from the membership file. 

**entity_df: *DataFrame***

A DataFrame of data necessary for the fuzzy match from the entity file. 

**mem_col_name: *str***

The column name for the category data in the membership file. 

**cleaned_mem_col_name: *str***

The column name for the cleaned category data in the membership file. 

**enti_col_name: *str***

The column name for the category data in the entity file. 

**enti_col_id: *str***

The column name for the category Id data in the entity file. 

### Returns:

**DataFrame**

A DataFrame of the fuzzy match results. Contains the category data in the membership file alongside the best match(es) to the category data in the entity file based on category name. 

### Notes:

- This function had to be separate from matcher() because LocalDuesCategory is not connected to a Unit or Employer. Therefore, it can only be matched on name, not be matched on both name and Unit Id or Employer Id, and required a different fuzzy match process.
- Have considered creating a helper function that would allow a single object to be passed into parameter and create all the name and id strings similar to the name_creator() found in The Remerger. Unsure if this would be more efficient. Idea for later development.

### Examples:



## runner(member_file_path, entity_file_path, member_entity_category_tuple)

Checks for if category data exists in both the membership and entity file. If it does, generates a spreadsheet of the fuzzy match. 

### Parameters:

**member_file_path: *DataFrame***

The path where the membership file is located. 

**entity_file_path: *DataFrame***

The path where the entity file is located. 

**member_entity_category_tuple: *str***

A tuple, with the first item being the column name of the category data in the membership file and the second item being the worksheet name of the category data in the entity file. 

### Returns:

**DataFrame**

A DataFrame of the fuzzy match results. Contains the category data in the membership file alongside the best match(es) to the category data in the entity file based on category name. 

### Notes:

- Similar to the helper function, have considered passing in all column identifier strings in a single dictionary into runner and then into matcher. The dictionary could be set up in the config file.

### Examples:



## main()

Loops through categories for each local membership-entity file pair in a given directory. 

### Notes:

- If the set-up of the directory changes, you would just edit the directory variable in this function.





# Program 2 (The Remerger)

## copyer(directory)

Makes a copy of each membership file in the directory.

### Parameters:

**directory: *Path***

The path to the folder where the membership file is located.  

### Notes:

- The name of the copy is the local number of the original membership file with '_w_entityids' attached to the end. It is this copy the cleaned fuzzy match spreadsheets are merged into, **not** the original version.

## name_creator(file_path)

Creates a dictionary containing the name and id strings for every column needed for the remerge of the cleaned fuzzy match spreadsheet into the membership file.

### Parameters:

**file_path: *DataFrame***

The path where the fuzzy match spreadsheet is located. 

### Returns:

**dict**

A dictionary containing the category data column name in the membership file, the category data column in the entity file, the category Id data column in the membership file and the category Id data column in the entity file. 

### Notes:

## remerger(names_list,member_df,fuzzy_match_df)

Remerges the cleaned fuzzy match spreadsheets on category name and Unit or Employer Id into the membership file.

### Parameters:

**names_list: *dict***

A dictionary of all strings of column names necessary for the remerge. 

**member_df: *DataFrame***

A DataFrame of the membership file. 

**fuzzy_match_df: *DataFrame***

A DataFrame of the fuzzy match spreadsheet. 

### Returns:

**DataFrame**

A DataFrame of the membership file with the correct category names and Ids from the entity file merged into it. 

### Notes:

* Every category that the local has a fuzzy match spreadsheet for will be remerged into the copy of the membership file made earlier.
* Entries in a fuzzy match spreadsheet that do not contain entity file data will be untouched in the remerged membership file.

## remerger_localduescategory(names_list,member_df,fuzzy_match_df)

Remerges the cleaned fuzzy match spreadsheets on category name into the membership file. 

### Parameters:

**names_list: *dict***

A dictionary of all strings of column names necessary for the remerge. 

**member_df: *DataFrame***

A DataFrame of the membership file. 

**fuzzy_match_df: *DataFrame***

A DataFrame of the fuzzy match spreadsheet. 

### Returns:

**DataFrame**

A DataFrame of the membership file with the correct category names and Ids from the entity file merged into it. 

### Notes:

* This remerge function happens after the first remerge function. So the program will first merge in the cleaned fuzzy match spreadsheet data for non-LocalDuesCategory categories, then merge in the cleaned fuzzy match spreadsheet data for LocalDuesCategory.
* Although the function has localduescategory in the name, nothing specific to LocalDuesCategory is hardcoded into it. The function can be used to remerge a cleaned fuzzy match spreadsheet of any category by category name only.

### main()

Creates DataFrames of the fuzzy match spreadsheet and membership file and passes in through the remerger functions. 

### Notes:

* If the set-up of the directory changes, you would just edit the directory variable in this function.

# 
