# python-course-scripts
Tools for Running Python Course

#### To initialize python course for year 2018 and with folder "class" run the below command

`python ./pycoursehelper.py gdrive initialize -y 2018 -f class`

#### To create a folder for mock test for year 2018 with mock folder name as "mock1" run the below command

`python ./pycoursehelper.py gdrive initialize -y 2018 -f mock1`

#### To create shared folders for students for year 2018 inside "class" follow the steps below
* Create a CSV file using the template specifed in `templates/student_details.csv`
* Then run the following command 
`python ./pycoursehelper.py gdrive share -y 2018 -t class -f <path_to_csv_file_with_contains_student_details>`

#### To create shared folder for a single student for year 2018 inside "class" run the command below

`python ./pycoursehelper.py gdrive share -y 2018 -t class -d <student_unique_folder_name>,<student_email_id>`

#### To unshare the folders shared to students for year 2018 inside folder "class" follow the steps below
* Create a CSV file using the template specifed in `templates/student_details.csv`
* Then run the following command 
`python ./pycoursehelper.py gdrive unshare -y 2018 -t class -f <path_to_csv_file_with_contains_student_details>`

#### To unshare the folder shared to one student for year 2018 inside folder "class" run the command below

`python ./pycoursehelper.py gdrive unshare -y 2018 -t class -d <student_unique_folder_name>,<student_email_id>`

#### To delete all folders present in year 2018 inside folder "class" run the command below

`python ./pycoursehelper.py gdrive delete -y 2018 -t class -a`
