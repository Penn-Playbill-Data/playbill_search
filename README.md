# Search Program
playbill_search, ocr_search, and combined_search are able to run in the
command line. Playbill search searches through a folder and its subsets for
text files containing a search term or terms. OCR search searches through a
playbill text file for a search term in context of an anchor term inputted by
the user with four possible tests to run. Combined search utilizes uses
both programs to create subfolders, filter files, and provide a summary of
results.

## Playbill Search
#### Running
Open Terminal, enter `python3 playbill_search.py`. You may need to enter the
full pathname if your current directory does not contain the playbill_search
file. Prompts will then ask for the path of the folder to be searched as well
as the search query/ies. If you would like to search for two+ terms only when
they are together, type && in between the terms (i.e. 'Drury && Lane' vs
'Drury Lane'). The program also works with regex, so 'Shak.sp.?.?r.?' will
search for most if not all the spellings of Shakespeare for the period. If your
term includes a regex symbol (i.e. '.'), type a double backslash before the
character ('\\').

The found files will be copied and placed into a new
folder named after the query. This folder will be located in the inputted
folder.

## OCR Search
#### Running
Open Terminal, enter `python3 ocr_search.py ~/.../file_to_be_searched.txt`.
See above note about full pathname. Prompts will then ask if the user would
like to run a particular test, and then the required parameters for the
test(s) to be run.

##### Word Search
Prompt asks if the user would like to run the test. If any character other
than y or Y is entered, the test will not be run and False will be returned.
Prompts then ask for the anchor term, context term, and number of words to be
searched before and after the anchor term (i.e. 10 = 10 words before and ten
words after)

The test searches for the context term within n words before and after the anchor
term (i.e. search for Oberon within 10 words before and after Midsummer). The test
applies to every instance of the anchor term. Returns list of booleans telling
whether the context was found before, after, and/or together with the anchor term.

##### Character Search
Prompt asks if the user would like to run the test. If any character other
than y or Y is entered, the test will not be run and False will be returned.
Prompts then ask for the anchor term, context term, and number of words to be
searched before and after the anchor term (i.e. 10 = 10 characters before and ten
characters after)

Searches for the context term within n characters before and after the anchor term
(i.e. search for Oberon within 10 characters before and after Midsummer). The test
applies to every instance of the anchor term. Spaces count as characters while
punctuation does not. Character amounts are exact, perhaps trimming the beginning
or ending word. Returns list of booleans telling whether the context was found
before, after, and/or together with the anchor term.

##### Line Search
Prompt asks if the user would like to run the test. If any character other
than y or Y is entered, the test will not be run and False will be returned.
Prompts then ask for the anchor term, context term, and number of words to be
searched before and after the anchor term (i.e. 2 = 2 lines before and 2
lines after)

Searches for the context term within n lines before and after the anchor term
(i.e. search for Oberon within 10 lines before and after Midsummer). The test
applies to every instance of the anchor term. Lines are complete and not
trimmed. Returns list of booleans telling whether the context was found before,
after, and/or together with the anchor term.

##### Playbill Search
Prompt asks if the user would like to run the test. If any character other
than y or Y is entered, the test will not be run and False will be returned.
Prompts then ask for the anchor term and context term.

Searches for the context term in any position related to the anchor term.
The test applies to every instance of the anchor term. Returns list of three
booleans telling whether the context was found before, after, and/or together
with the anchor term.

##### Location Search
Prompt asks if the user would like to run the test. If any character other
than y or Y is entered, the test will not be run and False will be returned.
Prompts then ask for the anchor term, context term, starting index, and
percent of playbill to be searched. The starting index is the word indicating
where to trim the playbill. Entering 0 will start the search from the beginning of
the playbill. Percent informs how much of the playbill will be searched. If percent
is positive, the percentage will be measured after the starting index. If percent
is negative, the percentage will be measured before the starting index (i.e. starting
index of 50 and percent of 0.1 would search 10 percent of words in the playbill
starting with word 50. percent of -0.1 would search 10 percent of words in the
playbill ending with word 50). If no index is entered, or if the entered index
is not an integer, the search will use the anchor as the starting point,
searching for x percent before or after the anchor.

Searches for the context term before, after, and/or together with the anchor
term in x percent of the playbill starting at word y. The test applies to every
instance of the anchor term. Returns list of three booleans telling whether the
context was found before, after, and/or together with the anchor term.

#### Output
The program prints the search results from each search test to the console,
including the  test name, the file name, the anchor term, the context term,
booleans for if the term was found before, after, and/or together with the anchor
term, the line the anchor term was found if the search was successful, as well
as the parameters particular to the test run.

## Combined Search
#### Running
Open Terminal, enter `python3 combined_search.py [option]`. See above note
about pathnames. In place of [option], enter 1 to filter files based on results
(see **CAUTION** under filter below), 2 to create a subfolder holding copies of
the resulting files, or any other value to simply create a csv file containing
the results in the folder to be searched.

Prompts will ask the user whether they would like to use playbill_search. Entering
Y or y will run the program before proceeding, using the resulting folder for the
search. If the search is not run, the user will be prompted to enter a folder
to be searched. The user will then be led through the prompts for ocr_search.
The user will then be prompted to answer whether they would like to find matches
based off of whether the context term was or was not found before, after, or together
with the anchor term. The user can focus on one, two, or all three criteria.
When prompted, the user will be asked whether they would like matches to store
whether the criteria was True or False (i.e. search for every instance of the
context term before the anchor and every file where the context term is *not*
after the anchor). The matches will then be collected, and the function specified
in [option] will be performed.

##### Filter
**WARNING** Using this function will completely delete ANY files that do not
match the criteria specified in the criteria specified by the prompts above.
**DO NOT** use on OCR_TEXT folder or Theater folders! It is highly recommended
to use the subfolder function *before* using the filter function. No additional
prompts are necessary. A csv results file will be created in the folder.


##### Subfolder
This option will make a copy of all matching files and sort them into a subfolder
within the search folder. This folder will  be named "search [date/time]", and
will include a csv results file. Highly recommended to use this function, and then
to use the filter function on the subfolder if so desired.


##### Results
Entering any other values in place of [option]  will cause a csv results file
to be saved in the folder to be searched.

#### Note
Due to the nature of the OCR, it is *highly* recommended to
1. Use regular expressions to account for possible typos
* i.e. M.rry Wi.es or ..rry W..es to find Merry Wives
2. Use the False function to narrow your search.
* i.e. Want Falstaff in Henry the IVth not Merry Wives? Use not Merry Wives rather than Henry the IVth when using filter. Using the True function could ignore unpredictable typos and cause you to miss data.

### Other Classes / Programs
#### LocationMatrix.py
Creates a LocationMatrix object from a text file, separating every word into an entry in a list
of lists. The inner list contains the row contents, while the outer list contains the rows.
Also contains the methods necessary to trim the matrix, update / refresh the matrix, and
search the matrix so that the tests in ocr_search can be run. Use print_matrix for troubleshooting.

#### ocr_search_out.py
Takes the tests and result functions of ocr_search and provides new run functions, allowing
the tests to be run on all of the files in a folder. Also contains the code to convert
results to a format that can be converted into csv.

#### csv_dict_writer.py
Contains the functions necessary to format a properly designed list of lists and convert it
into a csv file, which will be returned in the given path name. Useful and transferable
to other projects.

## Installation
Download Folder.

## Authors
Anastasia Hutnick
