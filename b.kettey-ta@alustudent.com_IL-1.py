#!/usr/bin/env python3
# ALU Grade Calculator 
# Individual Coding Lab (Summatives) Benjamin Kettey-Tagoe
#==================================================================

import json
from typing import Dict, List, Tuple, Sequence

class GradingScale:
    """
    Dynamic grading scale class that can be easily modified and validated
    """
    
    def __init__(self):
        """
        Initialize with default ALU grading scale
        """
        self.scale = {
            'A+': {'min': 98, 'max': 100, 'gpa': 5.0},
            'A':  {'min': 89.99, 'max': 97.00, 'gpa': 4.8},
            'A-': {'min': 80, 'max': 96.99, 'gpa': 4.7},
            'B+': {'min': 75, 'max': 79.99, 'gpa': 4.3},
            'B':  {'min': 70, 'max': 74.99, 'gpa': 4.0},
            'B-': {'min': 65, 'max': 69.99, 'gpa': 3.7},
            'C+': {'min': 60, 'max': 64.99, 'gpa': 3.3},
            'C':  {'min': 55, 'max': 59.99, 'gpa': 3.0},
            'C-': {'min': 50, 'max': 54.99, 'gpa': 2.7},
            'D':  {'min': 40, 'max': 49.99, 'gpa': 2.0},
            'F':  {'min': 0,  'max': 39.99, 'gpa': 1.0}
        }
        self.max_gpa = 5.0
        self.passing_threshold = 50.0
        self._validate_scale()
    
    def _validate_scale(self):
        """
        Validate the grading scale for consistency
        """
        # Check for overlaps and gaps
        all_ranges = []
        for letter, data in self.scale.items():
            if data['min'] > data['max']:
                raise ValueError(f"Invalid range for grade {letter}: min > max")
            if data['gpa'] > self.max_gpa or data['gpa'] < 0:
                raise ValueError(f"Invalid GPA for grade {letter}: must be between 0 and {self.max_gpa}")
            all_ranges.append((data['min'], data['max'], letter))
        
        # Sort by minimum value
        all_ranges.sort(key=lambda x: x[0])
        
        # Check for coverage from 0 to 100
        if all_ranges[0][0] != 0 or all_ranges[-1][1] != 100:
            print("Warning: Grading scale may not cover full 0-100 range")
    
    def percentage_to_grade(self, percentage: float) -> Tuple[float, str]:
        """
        Convert percentage to GPA and letter grade
        """
        # Clamp percentage to valid range
        percentage = max(0.0, min(100.0, float(percentage)))
        
        # Find the appropriate grade
        for letter, data in self.scale.items():
            if data['min'] <= percentage <= data['max']:
                return data['gpa'], letter
        
        # should not reach here if scale is properly configured
        print(f"Warning: No grade found for {percentage}%. Using minimum grade.")
        return 1.0, 'F'
    
    def is_passing(self, percentage: float) -> bool:
        """
        Check if a percentage is passing
        """
        return float(percentage) >= self.passing_threshold
    
    def get_grade_boundaries(self) -> List[Tuple[str, float, float, float]]:
        """
        Get all grade boundaries in a sorted list
        Returns: List of (letter, min, max, gpa) tuples
        """
        boundaries = []
        for letter, data in self.scale.items():
            boundaries.append((letter, data['min'], data['max'], data['gpa']))
        
        # Sort by minimum score (descending for display purposes)
        boundaries.sort(key=lambda x: x[1], reverse=True)
        return boundaries
    
    def update_grade(self, letter: str, min_score: float, max_score: float, gpa: float):
        """
        Update a specific grade in the scale
        """
        if letter not in self.scale:
            print(f"Adding new grade: {letter}")
        
        self.scale[letter] = {
            'min': min_score,
            'max': max_score,
            'gpa': gpa
        }
        self._validate_scale()
    
    def export_scale(self) -> str:
        """
        Export scale to JSON string for backup/sharing
        """
        return json.dumps(self.scale, indent=2)
    
    def import_scale(self, json_str: str):
        """
        Import scale from JSON string
        """
        try:
            imported_scale = json.loads(json_str)
            # Validate structure
            for letter, data in imported_scale.items():
                if not all(key in data for key in ['min', 'max', 'gpa']):
                    raise ValueError(f"Invalid structure for grade {letter}")
            
            self.scale = imported_scale
            self._validate_scale()
            print("Grading scale imported successfully!")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error importing scale: {e}")


class Assignment:
    """
    Assignment class with validation and error handling
    """
    
    def __init__(self, name: str, weight: float, grade: float):
        """
        Initialize assignment with validation
        """
        self.name = self._validate_name(name)
        self.weight = self._validate_weight(weight)
        self.grade = self._validate_grade(grade)
        self.points = self.calculate_points()
    
    def _validate_name(self, name: str) -> str:
        """
        Validate assignment name
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Assignment name must be a non-empty string")
        return name.strip()
    
    def _validate_weight(self, weight: float) -> float:
        """
        Validate assignment weight
        """
        weight = float(weight)
        if weight <= 0 or weight > 100:
            raise ValueError("Weight must be between 0 and 100")
        return weight
    
    def _validate_grade(self, grade: float) -> float:
        """
        Validate assignment grade
        """
        grade = float(grade)
        if grade < 0 or grade > 100:
            raise ValueError("Grade must be between 0 and 100")
        return grade
    
    def calculate_points(self) -> float:
        """
        Calculate weighted points
        """
        return (self.grade * self.weight) / 100.0
    
    def update_grade(self, new_grade: float):
        """
        Update the grade and recalculate points
        """
        self.grade = self._validate_grade(new_grade)
        self.points = self.calculate_points()
    
    def update_weight(self, new_weight: float):
        """
        Update the weight and recalculate points
        """
        self.weight = self._validate_weight(new_weight)
        self.points = self.calculate_points()
    
    def get_info(self) -> Dict:
        """
        Get assignment information as dictionary
        """
        return {
            'name': self.name,
            'weight': self.weight,
            'grade': self.grade,
            'points': self.points
        }


class FormativeAssignment(Assignment):
    """
    Formative Assignment class
    """
    
    def __init__(self, name: str, weight: float, grade: float):
        super().__init__(name, weight, grade)
        self.assignment_type = "FA"
        self.description = "Formative Assignment (ongoing assessments)"
    
    def get_feedback(self, grading_scale: GradingScale) -> str:
        """
        Get feedback based on performance
        """
        if grading_scale.is_passing(self.grade):
            return f"Great job on {self.name}! Keep up the good work."
        else:
            return f"Keep working on {self.name} - you can improve on the next FA!"


class SummativeAssignment(Assignment):
    """
    Summative Assignment class
    """
    
    def __init__(self, name: str, weight: float, grade: float):
        super().__init__(name, weight, grade)
        self.assignment_type = "SA"
        self.description = "Summative Assignment (major evaluations)"
    
    def get_feedback(self, grading_scale: GradingScale) -> str:
        """
        Get feedback based on performance
        """
        if grading_scale.is_passing(self.grade):
            return f"Excellent work on {self.name}! This is a major achievement!"
        else:
            return f"Focus on improving for {self.name} - it's crucial for passing!"


class GPACalculator:
    """
    Enhanced GPA calculator with flexible grading scale
    """
    
    def __init__(self, grading_scale: GradingScale):
        self.grading_scale = grading_scale
    
    def calculate_category_gpa(self, assignments: Sequence[Assignment]):
        """
        Calculate GPA for a category of assignments
        """
        if not assignments:
            return {
                'total_percentage': 0.0,
                'gpa': 0.0,
                'letter_grade': 'N/A',
                'total_weight': 0.0,
                'weighted_points': 0.0
            }
        
        total_points = sum(assignment.points for assignment in assignments)
        total_weight = sum(assignment.weight for assignment in assignments)
        
        # Calculate percentage (handle division by zero)
        if total_weight == 0:
            percentage = 0.0
        else:
            percentage = (total_points / total_weight) * 100
        
        # Ensure percentage is within bounds
        percentage = max(0.0, min(100.0, percentage))
        
        gpa, letter = self.grading_scale.percentage_to_grade(percentage)
        
        return {
            'total_percentage': percentage,
            'gpa': gpa,
            'letter_grade': letter,
            'total_weight': total_weight,
            'weighted_points': total_points
        }
    
    def calculate_overall_gpa(self, fa_result: Dict, sa_result: Dict) -> Dict:
        """
        Calculate overall GPA from FA and SA results
        """
        fa_percentage = fa_result['total_percentage']
        sa_percentage = sa_result['total_percentage']
        
        # Determine overall percentage based on available data
        if fa_percentage == 0 and sa_percentage == 0:
            overall_percentage = 0.0
        elif fa_percentage == 0:
            overall_percentage = sa_percentage
        elif sa_percentage == 0:
            overall_percentage = fa_percentage
        else:
            # Equal weighting of FA and SA
            overall_percentage = (fa_percentage + sa_percentage) / 2
        
        overall_gpa, overall_letter = self.grading_scale.percentage_to_grade(overall_percentage)
        
        return {
            'overall_percentage': overall_percentage,
            'overall_gpa': overall_gpa,
            'overall_letter': overall_letter,
            'fa_data': fa_result,
            'sa_data': sa_result
        }


class GradeCalculator:
    """
    Main grade calculator with enhanced features
    """
    
    def __init__(self, student_name: str):
        self.student_name = student_name
        self.grading_scale = GradingScale()
        self.gpa_calculator = GPACalculator(self.grading_scale)
        self.formative_assignments: List[FormativeAssignment] = []
        self.summative_assignments: List[SummativeAssignment] = []
    
    def add_formative_assignment(self, name: str, weight: float, grade: float) -> bool:
        """
        Add formative assignment with error handling
        """
        try:
            assignment = FormativeAssignment(name, weight, grade)
            self.formative_assignments.append(assignment)
            
            print(f"\nAdded '{name}' to your FA assignments!")
            print(f"Grade: {assignment.grade:.2f}% | Weight: {assignment.weight:.2f}%")
            print(f"Points earned: {assignment.points:.2f}")
            print(f"{assignment.get_feedback(self.grading_scale)}")
            return True
        except ValueError as e:
            print(f"Error adding assignment: {e}")
            return False
    
    def add_summative_assignment(self, name: str, weight: float, grade: float) -> bool:
        """
        Add summative assignment with error handling
        """
        try:
            assignment = SummativeAssignment(name, weight, grade)
            self.summative_assignments.append(assignment)
            
            print(f"\nAdded '{name}' to your SA assignments!")
            print(f"Grade: {assignment.grade:.2f}% | Weight: {assignment.weight:.2f}%")
            print(f"Points earned: {assignment.points:.2f}")
            print(f"{assignment.get_feedback(self.grading_scale)}")
            return True
        except ValueError as e:
            print(f"Error adding assignment: {e}")
            return False
    
    def generate_report(self):
        """
        Generate comprehensive grade report
        """
        print("\n" + "=" * 60)
        print(f"COMPREHENSIVE GRADE REPORT FOR {self.student_name.upper()}")
        print("=" * 60)
        
        # Calculate results
        fa_result = self.gpa_calculator.calculate_category_gpa(self.formative_assignments)
        sa_result = self.gpa_calculator.calculate_category_gpa(self.summative_assignments)
        overall_result = self.gpa_calculator.calculate_overall_gpa(fa_result, sa_result)
        
        # Display sections
        self._display_category_section("FORMATIVE ASSIGNMENTS (FA)", self.formative_assignments, fa_result)
        self._display_category_section("SUMMATIVE ASSIGNMENTS (SA)", self.summative_assignments, sa_result)
        self._display_final_results(overall_result)
        self._display_grading_scale()
        
        print("\n" + "=" * 60)
    
    def _display_category_section(self, title: str, assignments: Sequence[Assignment], result: Dict):
        """
        Display a category section (FA or SA)
        """
        print(f"\n{title}:")
        print("-" * 50)
        
        if assignments:
            for i, assignment in enumerate(assignments, 1):
                info = assignment.get_info()
                status = "PASS" if self.grading_scale.is_passing(info['grade']) else "FAIL"
                print(f"{i}. {info['name']}")
                print(f"Grade: {info['grade']:.2f}% | Weight: {info['weight']:.2f}% | {status}")
                print(f"Points contributed: {info['points']:.2f}")
                print()
            
            print(f"CATEGORY SUMMARY:")
            print(f"Total Score: {result['total_percentage']:.2f}%")
            print(f"Letter Grade: {result['letter_grade']}")
            print(f"GPA: {result['gpa']:.2f}/{self.grading_scale.max_gpa}")
            print(f"Total Weight: {result['total_weight']:.2f}%")
            status = "PASS" if self.grading_scale.is_passing(result['total_percentage']) else "FAIL"
            print(f"Status: {status}")
        else:
            print("No assignments added yet.")
    
    def _display_final_results(self, overall_result: Dict):
        """
        Display final results and pass/fail determination
        """
        print(f"\nFINAL ACADEMIC RESULTS:")
        print("-" * 40)
        
        fa_data = overall_result['fa_data']
        sa_data = overall_result['sa_data']
        
        print(f"FA Category: {fa_data['total_percentage']:.2f}% | GPA: {fa_data['gpa']:.2f} ({fa_data['letter_grade']})")
        print(f"SA Category: {sa_data['total_percentage']:.2f}% | GPA: {sa_data['gpa']:.2f} ({sa_data['letter_grade']})")
        print(f"Overall Percentage: {overall_result['overall_percentage']:.2f}%")
        print(f"Overall Letter Grade: {overall_result['overall_letter']}")
        print(f"Overall GPA: {overall_result['overall_gpa']:.3f}/{self.grading_scale.max_gpa}")
        
        # Pass/fail determination
        self._determine_pass_fail(fa_data, sa_data, overall_result)
    
    def _determine_pass_fail(self, fa_data: Dict, sa_data: Dict, overall_result: Dict):
        """
        Determine if student passes based on ALU rules
        """
        fa_percentage = fa_data['total_percentage']
        sa_percentage = sa_data['total_percentage']
        has_fa = len(self.formative_assignments) > 0
        has_sa = len(self.summative_assignments) > 0
        
        if has_fa and has_sa:
            # Both categories - need 50% in both
            fa_pass = self.grading_scale.is_passing(fa_percentage)
            sa_pass = self.grading_scale.is_passing(sa_percentage)
            
            if fa_pass and sa_pass:
                print(f"\nCONGRATULATIONS! YOU PASSED THE COURSE!")
                print("Both your FA and SA categories meet the minimum requirement!")
                self._provide_performance_feedback(overall_result['overall_gpa'])
            else:
                print(f"\nUNFORTUNATELY, YOU NEED TO REPEAT THIS COURSE")
                print(f"You need at least {self.grading_scale.passing_threshold}% in BOTH FA and SA to pass")
                if not fa_pass:
                    print(f"Your FA total ({fa_percentage:.2f}%) is below {self.grading_scale.passing_threshold}%")
                if not sa_pass:
                    print(f"Your SA total ({sa_percentage:.2f}%) is below {self.grading_scale.passing_threshold}%")
        elif has_fa or has_sa:
            # Only one category
            category_name = "FA" if has_fa else "SA"
            percentage = fa_percentage if has_fa else sa_percentage
            
            print(f"\nCURRENT {category_name} PROGRESS:")
            if self.grading_scale.is_passing(percentage):
                print(f"Great! Your {category_name} score ({percentage:.2f}%) meets the requirement!")
                print(f"Add {('SA' if has_fa else 'FA')} assignments to get your complete course grade.")
            else:
                print(f"Your {category_name} score ({percentage:.2f}%) is below {self.grading_scale.passing_threshold}%. Keep working!")
        else:
            print(f"\nNo assignments added yet. Add some assignments to see your progress!")
    
    def _provide_performance_feedback(self, gpa: float):
        """
        Provide performance feedback based on GPA
        """
        if gpa >= 4.5:
            print(f"Outstanding performance with a GPA of {gpa:.3f}!")
        elif gpa >= 4.0:
            print(f"Excellent work with a GPA of {gpa:.3f}!")
        elif gpa >= 3.5:
            print(f"Good performance with a GPA of {gpa:.3f}!")
        elif gpa >= 3.0:
            print(f"Satisfactory work with a GPA of {gpa:.3f}!")
        else:
            print(f"You passed, but there's room for improvement. GPA: {gpa:.3f}")
    
    def _display_grading_scale(self):
        """
        Display the current grading scale
        """
        print(f"\nGRADING SCALE REFERENCE:")
        print("-" * 45)
        print("Score Range     | Letter | GPA")
        print("-" * 45)
        
        boundaries = self.grading_scale.get_grade_boundaries()
        for letter, min_score, max_score, gpa in boundaries:
            if max_score == 100:
                print(f"{min_score:2.0f}-{max_score:3.0f}%        |   {letter:2s}   | {gpa:.1f}")
            else:
                print(f"{min_score:2.0f}-{max_score:5.2f}%    |   {letter:2s}   | {gpa:.1f}")
        print(f"Maximum GPA: {self.grading_scale.max_gpa}")
        print(f"Passing threshold: {self.grading_scale.passing_threshold}%")
    
    def has_assignments(self) -> bool:
        """
        Check if any assignments have been added
        """
        return len(self.formative_assignments) > 0 or len(self.summative_assignments) > 0
    
    def quick_gpa_calculation(self):
        """
        Quick GPA calculation with direct input
        """
        print(f"\nQUICK GPA CALCULATION")
        print("-" * 30)
        
        try:
            fa_score = float(input("Enter your FA total score (0-100): "))
            sa_score = float(input("Enter your SA total score (0-100): "))
            
            if not (0 <= fa_score <= 100) or not (0 <= sa_score <= 100):
                print("Please enter scores between 0 and 100!")
                return
            
            # Create temporary results
            fa_result = {'total_percentage': fa_score, 'gpa': self.grading_scale.percentage_to_grade(fa_score)[0], 'letter_grade': self.grading_scale.percentage_to_grade(fa_score)[1]}
            sa_result = {'total_percentage': sa_score, 'gpa': self.grading_scale.percentage_to_grade(sa_score)[0], 'letter_grade': self.grading_scale.percentage_to_grade(sa_score)[1]}
            
            overall_result = self.gpa_calculator.calculate_overall_gpa(fa_result, sa_result)
            
            print(f"\nQUICK GPA RESULTS:")
            print("-" * 25)
            print(f"FA Score: {fa_score:.1f}% | GPA: {fa_result['gpa']:.2f} ({fa_result['letter_grade']})")
            print(f"SA Score: {sa_score:.1f}% | GPA: {sa_result['gpa']:.2f} ({sa_result['letter_grade']})")
            print(f"Overall: {overall_result['overall_percentage']:.2f}%")
            print(f"Letter Grade: {overall_result['overall_letter']}")
            print(f"GPA: {overall_result['overall_gpa']:.3f}/{self.grading_scale.max_gpa}")
            
        except ValueError:
            print("Please enter valid numbers!")


# Utility functions for input validation

def get_student_name() -> str:
    """
    Get and validate student name
    """
    while True:
        name = input("What's your name? ").strip()
        if not name:
            print("Please enter your name!")
            continue
        
        if name.replace('.', '', 1).isdigit():
            print("Your name cannot be just numbers! Please enter your actual name.")
            continue
        
        if not any(char.isalpha() for char in name):
            print("Your name must contain at least one letter!")
            continue
        
        if len(name) < 2:
            print("Your name must be at least 2 characters long!")
            continue
            
        return name


def get_assignment_details() -> Tuple[str, float, float]:
    """
    Get assignment details with validation
    """
    # Get assignment name
    while True:
        name = input("What's the name of this assignment? (e.g., Quiz 1, Midterm): ").strip()
        if not name:
            print("Please enter a name for your assignment!")
            continue
        
        if name.replace('.', '', 1).isdigit():
            print("Assignment name cannot be just numbers! Please enter a descriptive name.")
            continue
        
        if not any(char.isalpha() for char in name):
            print("Assignment name must contain at least one letter!")
            continue
        
        if len(name) < 2:
            print("Assignment name must be at least 2 characters long!")
            continue
            
        break
    
    # Get assignment weight
    while True:
        try:
            weight = float(input("Enter the weight as a percentage (e.g., 10 for 10%): "))
            if 0 < weight <= 100:
                break
            else:
                print("Please enter a number between 0.1 and 100!")
        except ValueError:
            print("Please enter a valid number!")
    
    # Get assignment grade
    while True:
        try:
            grade = float(input("Enter your grade out of 100 (e.g., 85 for 85%): "))
            if 0 <= grade <= 100:
                break
            else:
                print("Please enter a grade between 0 and 100!")
        except ValueError:
            print("Please enter a valid number!")
    
    return name, weight, grade


def show_help():
    """
    Display help information
    """
    print("\nHELP - Understanding the Grade Calculator")
    print("=" * 50)
    print(f"GOAL: Get at least 50% in both FA and SA categories")
    print()
    print("FORMATIVE ASSIGNMENTS (FA):")
    print("- Ongoing assignments like homework, quizzes, projects")
    print(f"- You need a total of 50% in all FA assignments combined")
    print()
    print("SUMMATIVE ASSIGNMENTS (SA):")
    print("- Major assessments like midterms, finals, big projects")
    print(f"- You need a total of 50% in all SA assignments combined")
    print()
    print("WEIGHTS:")
    print("- Each assignment has a weight (how much it counts)")
    print("- Higher weight = more important to your final grade")
    print()
    print("GPA CALCULATION:")
    print("- Overall percentage = (FA Total + SA Total) / 2")
    print("- GPA ranges from 1.0 to 5.0 based on grading scale")
    print("- Letter grades assigned based on percentage ranges")
    print("=" * 50)


def display_welcome():
    """
    Display welcome message
    """
    print("=" * 60)
    print("Welcome to ALU Grade Calculator - Enhanced Version!")
    print("This program helps you track assignments and calculate GPA.")
    print("=" * 60)


def display_grading_system():
    """
    Explain ALU's grading system
    """
    print("\nHere's how ALU grading works:")
    print("- FA (Formative Assignments): homework, quizzes, projects")
    print("- SA (Summative Assignments): midterms, finals, major projects")
    print(f"- To pass: You need at least 50% in BOTH FA and SA categories")
    print("- Each assignment has a weight (impact on final grade)")
    print("- GPA is calculated based on your overall percentage (5.0 scale)")


def main():
    """
    Main program function
    """
    display_welcome()
    
    # Get student information
    print("Let's start by getting your information:")
    student_name = get_student_name()
    print(f"Hi {student_name}! Nice to meet you!")
    
    # Create calculator
    calculator = GradeCalculator(student_name)
    
    # Explain system
    display_grading_system()
    
    # Main program loop
    while True:
        print(f"\nMAIN MENU - What would you like to do?")
        print("1. Add a Formative Assignment (FA)")
        print("2. Add a Summative Assignment (SA)")
        print("3. View comprehensive grade report")
        print("4. Quick GPA calculator")
        print("5. Help - explain how this works")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            print(f"\nAdding a new FA assignment")
            print("-" * 35)
            name, weight, grade = get_assignment_details()
            calculator.add_formative_assignment(name, weight, grade)
        
        elif choice == "2":
            print(f"\nAdding a new SA assignment")
            print("-" * 35)
            name, weight, grade = get_assignment_details()
            calculator.add_summative_assignment(name, weight, grade)
        
        elif choice == "3":
            if not calculator.has_assignments():
                print("\nYou haven't added any assignments yet!")
                print("Add some assignments first, then come back to see your report.")
            else:
                calculator.generate_report()
        
        elif choice == "4":
            calculator.quick_gpa_calculation()
        
        elif choice == "5":
            show_help()
        
        elif choice == "6":
            print(f"\nGoodbye {student_name}! Good luck with your studies!")
            print(f"Remember: You need 50% in both FA and SA to pass!")
            print("Keep working toward that perfect 5.0 GPA!")
            break
        
        else:
            print("\nThat's not a valid choice. Please pick a number from 1 to 6.")


if __name__ == "__main__":
    """
    Program entry point with error handling
    """
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please restart the program and try again.")
    finally:
        print("\nThank you for using ALU Grade Calculator!")
        print("Made by Benjamin Kettey-Tagoe for ALU students")