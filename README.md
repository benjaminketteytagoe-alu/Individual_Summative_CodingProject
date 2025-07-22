# Individual_Summative_CodingProject

## ALU Grade Calculator

This is a command-line Python application developed as part of the Individual Coding Lab (IL-1) at the African Leadership University. The program calculates a student's GPA and letter grade based on percentage scores, using a flexible and customizable grading scale. It also determines whether the score is a passing mark or not.

## Features

- Input validation for percentage scores
- Dynamic mapping from percentage to GPA and letter grade
- Identifies whether the score is a pass or fail
- Grading scale can be updated or extended
- Portable and works in any Python 3 environment

## How It Works

When the script is executed, it performs the following:

1. Prompts the user to enter a score between 0 and 100.
2. Determines the corresponding GPA using ALU’s grading scale.
3. Outputs the GPA, letter grade, and a pass/fail message.

## Requirements

- Python 3.x installed
- No external dependencies or libraries required

## How to Run

To execute the program, use the following command in a terminal or command prompt:

python b.kettey-ta@alustudent.com\_IL-1.py

If you are using a Unix-based system (Linux/macOS), you may add the following shebang at the top of the file to make it executable:



#!/usr/bin/env python3

Then run:
chmod +x b.kettey-ta@alustudent.com\_IL-1.py

## Sample Output

Enter the student's score: 92
GPA: 4.8
Grade: A
Pass: Yes

## Customization

You can modify the grading criteria by updating the `GradingScale` class in the script. The class allows:

- Adding new grade ranges
- Updating or removing existing ones
- Exporting and importing grading scales using JSON

## Author

- Name: Benjamin Kettey-Tagoe  
- Email: b.kettey-ta@alustudent.com  
- Institution: African Leadership University  

## License

This project is submitted as part of coursework at ALU.
