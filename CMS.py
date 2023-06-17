import itertools
import time

course_database = {
    "basic probability": {"subject": "Mathematics", "level": "Beginner", "instructor": "puvaneshwari", "rating": 4.5},
    "organic chemistry": {"subject": "Science", "level": "Intermediate", "instructor": "prabhas", "rating": 4.0},
    "applications of electronics": {"subject": "Physics", "level": "Advanced", "instructor": "madhu mohan",
                                    "rating": 4.2},
    "signal processing": {"subject": "optics", "level": "Intermediate", "instructor": "prabhu", "rating": 4.8},
    "engineering drawing": {"subject": "Art", "level": "Beginner", "instructor": "vaira vignesh", "rating": 3.9},
    "advance programming": {"subject": "programming", "level": "Intermediate", "instructor": "shanmugha priya",
                            "rating": 4.6},
    "web development": {"subject": "programming", "level": "Intermediate", "instructor": "manjusha", "rating": 4.0}
}


# Graph class to represent course connections
class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, course, subject, level):
        key = subject + '_' + level
        if key in self.graph:
            self.graph[key].append(course)
        else:
            self.graph[key] = [course]


# Hash Table class to store course attributes and ratings
class HashTable:
    def __init__(self):
        self.table = {}

    def insert(self, key, value):
        self.table[key] = value

    def get(self, key):
        return self.table.get(key)


# Queue class to represent course enrollment
class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, course):
        self.queue.append(course)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0

    def display(self):
        if not self.is_empty():
            print("Enrollment List:")
            for course in self.queue:
                print(course)
        else:
            print("Enrollment list is empty.")


# Build the graph and hash tables
course_graph = Graph()
course_attributes = HashTable()
course_ratings = HashTable()
course_reviews = HashTable()

# Generate all combinations of subjects and levels
all_subjects = ["Mathematics", "Science", "Physics", "optics", "Art", "programming"]
all_levels = ["Beginner", "Intermediate", "Advanced"]
all_combinations = list(itertools.product(all_subjects, all_levels))

for course, attributes in course_database.items():
    subject = attributes["subject"]
    level = attributes["level"]
    course_graph.add_edge(course, subject, level)
    course_attributes.insert(course, attributes)


# Perform personalized course recommendations based on subject and level
def recommend_courses():
    print("Select a Subject:")
    for index, subject in enumerate(all_subjects, start=1):
        print(f"{index}. {subject}")
    subject_choice = input("Enter your subject choice (1-{0}): ".format(len(all_subjects)))

    print("Select a Level:")
    for index, level in enumerate(all_levels, start=1):
        print(f"{index}. {level}")
    level_choice = input("Enter your level choice (1-{0}): ".format(len(all_levels)))

    subject_mapping = {str(index): subject for index, subject in enumerate(all_subjects, start=1)}
    level_mapping = {str(index): level for index, level in enumerate(all_levels, start=1)}

    if subject_choice in subject_mapping and level_choice in level_mapping:
        user_subject = subject_mapping[subject_choice]
        user_level = level_mapping[level_choice]

        key = user_subject + '_' + user_level
        recommended_courses = []

        if key in course_graph.graph:
            courses = course_graph.graph[key]
            for course in courses:
                attributes = course_attributes.get(course)
                if attributes:
                    recommended_courses.append((course, attributes["instructor"]))

        return recommended_courses
    else:
        print("Invalid subject or level choice. Please try again.")
        return []


# User management system
class UserManagementSystem:
    def __init__(self):
        self.users = {}
        self.ratings = HashTable()
        self.reviews = HashTable()
        self.enrollment_lists = {}

    def create_account(self):
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        self.users[username] = password
        self.enrollment_lists[username] = Queue()
        print("Account created successfully.")

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if username in self.users and self.users[username] == password:
            print("Login successful.")
            return username

        print("Invalid username or password.")
        return None

    def rate_course(self, username, course):
        rating = input(f"Rate the course '{course}': ")
        self.ratings.insert(course, rating)
        print("Course rated successfully.")

    def add_review(self, username, course, review):
        if course in self.reviews.table:
            self.reviews.table[course].append(review)
        else:
            self.reviews.table[course] = [review]

    def get_course_reviews(self, course):
        reviews = self.reviews.get(course)
        if reviews:
            print(f"Reviews for '{course}':")
            for review in reviews:
                print(review)
        else:
            print("No reviews found for the given course.")

    def enroll_in_course(self, username, course):
        self.enrollment_lists[username].enqueue(course)
        print(f"'{course}' added to the enrollment list.")

    def start_course(self, username):
        enrollment_list = self.enrollment_lists.get(username)
        if enrollment_list is not None:
            if not enrollment_list.is_empty():
                total_course = 0
                total_grade_points = 0

                print("Starting enrolled courses:")
                while not enrollment_list.is_empty():
                    course = enrollment_list.dequeue()
                    print(f"Now starting course: {course}")
                    time.sleep(2)  # Simulating course duration

                    # Ask for the final marks in the course
                    final_marks = float(input(f"Enter the final marks for '{course}': "))
                    credits = self.calculate_credits(course)
                    grade_points = self.calculate_grade_points(final_marks)

                    if grade_points < 5:
                        print(f"You failed the course: {course}. Please perform again for this course.")
                        enrollment_list.enqueue(course)
                    else:
                        total_course = total_course + 1
                        total_grade_points += grade_points

                sgpa = total_grade_points / total_course
                print("All courses completed.")

                print(f"SGPA: {sgpa}")
            else:
                print("No courses in the enrollment list.")
        else:
            print("User not found.")

    def calculate_credits(self, course):
        attributes = course_attributes.get(course)
        if attributes:
            if attributes["level"] == "Beginner":
                return 2
            elif attributes["level"] == "Intermediate":
                return 3
            elif attributes["level"] == "Advanced":
                return 4
        return 0

    def calculate_grade_points(self, final_marks):
        if final_marks >= 90:
            return 10
        elif final_marks >= 80:
            return 9
        elif final_marks >= 70:
            return 8
        elif final_marks >= 60:
            return 7
        elif final_marks >= 50:
            return 6
        elif final_marks >= 40:
            return 5
        else:
            return 0

    def display_enrollment_list(self, username):
        enrollment_list = self.enrollment_lists.get(username)
        if enrollment_list is not None:
            enrollment_list.display()
        else:
            print("User not found.")


# Create an instance of the UserManagementSystem
ums = UserManagementSystem()

# Menu-driven loop
while True:
    print("1. Create Account")
    print("2. Login")
    print("3. Rate a Course")
    print("4. Add a Review")
    print("5. Get Course Recommendations")
    print("6. Get Course Reviews")
    print("7. Enroll in a Course")
    print("8. Start Enrolled Courses")
    print("9. Display Enrollment List")
    print("10. Exit")
    choice = input("Enter your choice (1-10): ")

    if choice == "1":
        ums.create_account()
    elif choice == "2":
        username = ums.login()
    elif choice == "3":
        username = ums.login()
        if username is not None:
            course = input("Enter the course you want to rate: ")
            ums.rate_course(username, course)
        else:
            print("Please log in first.")
    elif choice == "4":
        username = ums.login()
        if username is not None:
            course = input("Enter the course you want to add a review for: ")
            review = input("Enter your review: ")
            ums.add_review(username, course, review)
        else:
            print("Please log in first.")
    elif choice == "5":
        recommended_courses = recommend_courses()
        print("Recommended Courses:")
        for course, instructor in recommended_courses:
            print(f"{course} - Instructor: {instructor}")
    elif choice == "6":
        course = input("Enter the course to get reviews: ")
        ums.get_course_reviews(course)
    elif choice == "7":
        username = ums.login()
        if username is not None:
            recommended_courses = recommend_courses()
            print("Available Courses:")
            for index, (course, instructor) in enumerate(recommended_courses, start=1):
                print(f"{index}. {course} - Instructor: {instructor}")
            course_choice = input("Enter the course number to enroll: ")
            if course_choice.isdigit() and int(course_choice) in range(1, len(recommended_courses) + 1):
                course_index = int(course_choice) - 1
                course = recommended_courses[course_index][0]
                ums.enroll_in_course(username, course)
            else:
                print("Invalid course choice. Please try again.")
        else:
            print("Please log in first.")
    elif choice == "8":
        username = ums.login()
        if username is not None:
            ums.start_course(username)
        else:
            print("Please log in first.")
    elif choice == "9":
        username = ums.login()
        if username is not None:
            ums.display_enrollment_list(username)
        else:
            print("Please log in first.")
    elif choice == "10":
        break
    else:
        print("Invalid choice. Please try again.")
