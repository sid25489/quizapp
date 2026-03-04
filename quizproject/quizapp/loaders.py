import json
from typing import Tuple

def get_quiz_data():
    return [
        {
            "title": "Cricket Mastery",
            "description": "Test your cricket knowledge.",
            "time_limit": 10,
            "questions": [
                {"text": "Who won the first ICC Cricket World Cup?", "points": 1, "choices": [("West Indies", True), ("Australia", False), ("India", False), ("England", False)]},
                {"text": "How many runs does a century represent?", "points": 1, "choices": [("50", False), ("100", True), ("150", False), ("200", False)]},
                {"text": "Which player is known as 'Master Blaster'?", "points": 1, "choices": [("Don Bradman", False), ("Sachin Tendulkar", True), ("Brian Lara", False), ("Viv Richards", False)]},
                {"text": "How many players are in a cricket team?", "points": 1, "choices": [("10", False), ("11", True), ("12", False), ("9", False)]},
                {"text": "What is the length of a cricket pitch in yards?", "points": 1, "choices": [("20", False), ("22", True), ("24", False), ("26", False)]},
                {"text": "The 'Ashes' is a series played between which two countries?", "points": 1, "choices": [("India and Pakistan", False), ("England and Australia", True), ("South Africa and New Zealand", False), ("Sri Lanka and West Indies", False)]},
                {"text": "Which bowler has taken the most wickets in Test match cricket?", "points": 1, "choices": [("Shane Warne", False), ("James Anderson", False), ("Muttiah Muralitharan", True), ("Anil Kumble", False)]},
                {"text": "In a T20 match, how many overs does each team play?", "points": 1, "choices": [("10", False), ("20", True), ("50", False), ("40", False)]},
                {"text": "What does LBW stand for in cricket?", "points": 1, "choices": [("Leg Before Wicket", True), ("Long Bat Wicket", False), ("Left Behind Wicket", False), ("Leg By Wicket", False)]},
                {"text": "Who is the first batsman to score a double century in ODI?", "points": 1, "choices": [("Virender Sehwag", False), ("Sachin Tendulkar", True), ("Rohit Sharma", False), ("Chris Gayle", False)]},
            ]
        },
        {
            "title": "Football Fundamentals",
            "description": "Core knowledge about football.",
            "time_limit": 10,
            "questions": [
                {"text": "What is the duration of a regular football match?", "points": 1, "choices": [("80 minutes", False), ("90 minutes", True), ("100 minutes", False), ("120 minutes", False)]},
                {"text": "How many players are there in a standard football team on the field?", "points": 1, "choices": [("10", False), ("11", True), ("12", False), ("9", False)]},
                {"text": "Which country won the 2022 FIFA World Cup?", "points": 1, "choices": [("France", False), ("Argentina", True), ("Brazil", False), ("Croatia", False)]},
                {"text": "Which club is known as 'Los Blancos'?", "points": 1, "choices": [("FC Barcelona", False), ("Real Madrid", True), ("Atletico Madrid", False), ("Valencia", False)]},
                {"text": "Who has won the most Ballon d'Or awards?", "points": 1, "choices": [("Cristiano Ronaldo", False), ("Lionel Messi", True), ("Michel Platini", False), ("Johan Cruyff", False)]},
                {"text": "Which country has won the most World Cups?", "points": 1, "choices": [("Germany", False), ("Italy", False), ("Brazil", True), ("Argentina", False)]},
                {"text": "What is the distance from the penalty spot to the goal line?", "points": 1, "choices": [("10 yards", False), ("12 yards", True), ("14 yards", False), ("18 yards", False)]},
                {"text": "Which team is nicknamed 'The Red Devils'?", "points": 1, "choices": [("Liverpool", False), ("Manchester United", True), ("Arsenal", False), ("Chelsea", False)]},
                {"text": "In what year was the first FIFA World Cup held?", "points": 1, "choices": [("1926", False), ("1930", True), ("1934", False), ("1938", False)]},
                {"text": "Who holds the record for most goals in Champions League history?", "points": 1, "choices": [("Lionel Messi", False), ("Cristiano Ronaldo", True), ("Robert Lewandowski", False), ("Karim Benzema", False)]},
            ]
        },
        {
            "title": "Technology Today",
            "description": "General technology awareness.",
            "time_limit": 10,
            "questions": [
                {"text": "Who is the founder of Apple Inc.?", "points": 1, "choices": [("Bill Gates", False), ("Steve Jobs", True), ("Mark Zuckerberg", False), ("Larry Page", False)]},
                {"text": "What does HTTP stand for?", "points": 1, "choices": [("HyperText Transfer Protocol", True), ("HighText Transfer Protocol", False), ("HyperText Transfer Package", False), ("Hyper Transfer Text Protocol", False)]},
                {"text": "Which company acquired LinkedIn in 2016?", "points": 1, "choices": [("Google", False), ("Facebook", False), ("Microsoft", True), ("Amazon", False)]},
                {"text": "What does CPU stand for?", "points": 1, "choices": [("Central Process Unit", False), ("Central Processing Unit", True), ("Computer Personal Unit", False), ("Central Processor Unit", False)]},
                {"text": "Which programming language is known for its use in Machine Learning?", "points": 1, "choices": [("Java", False), ("C++", False), ("Python", True), ("Ruby", False)]},
                {"text": "Which social network has a bird logo?", "points": 1, "choices": [("Facebook", False), ("Twitter", True), ("Instagram", False), ("Snapchat", False)]},
                {"text": "What is the main language used for styling web pages?", "points": 1, "choices": [("HTML", False), ("CSS", True), ("JavaScript", False), ("PHP", False)]},
                {"text": "Who is the CEO of Tesla?", "points": 1, "choices": [("Jeff Bezos", False), ("Elon Musk", True), ("Tim Cook", False), ("Satya Nadella", False)]},
                {"text": "What is the most popular operating system for smartphones?", "points": 1, "choices": [("iOS", False), ("Android", True), ("Windows Phone", False), ("Symbian", False)]},
                {"text": "Which symbol is used for an email address?", "points": 1, "choices": [("#", False), ("@", True), ("!", False), ("*", False)]},
            ]
        },
        {
            "title": "Current Affairs Challenge",
            "description": "Test your current affairs knowledge.",
            "time_limit": 10,
            "questions": [
                {"text": "Who is the current President of the USA (as of 2024)?", "points": 1, "choices": [("Donald Trump", False), ("Joe Biden", True), ("Barack Obama", False), ("George Bush", False)]},
                {"text": "Which country is hosting the 2024 Summer Olympics?", "points": 1, "choices": [("USA", False), ("Japan", False), ("France", True), ("Australia", False)]},
                {"text": "What currency is officially used in the European Union?", "points": 1, "choices": [("Dollar", False), ("Pound", False), ("Euro", True), ("Franc", False)]},
                {"text": "Who leads the United Nations?", "points": 1, "choices": [("António Guterres", True), ("Ban Ki-moon", False), ("Kofi Annan", False), ("Boutros Boutros-Ghali", False)]},
                {"text": "Which nation recently landed a spacecraft near the moon's south pole?", "points": 1, "choices": [("USA", False), ("Russia", False), ("China", False), ("India", True)]},
                {"text": "The G20 summit of 2023 was held in which country?", "points": 1, "choices": [("Indonesia", False), ("India", True), ("Brazil", False), ("Italy", False)]},
                {"text": "What is the capital of Ukraine?", "points": 1, "choices": [("Minsk", False), ("Kyiv", True), ("Warsaw", False), ("Moscow", False)]},
                {"text": "Which company became the first to reach a $3 trillion market cap?", "points": 1, "choices": [("Microsoft", False), ("Apple", True), ("Amazon", False), ("Google", False)]},
                {"text": "Who is the Prime Minister of the UK (as of 2024)?", "points": 1, "choices": [("Boris Johnson", False), ("Rishi Sunak", True), ("Liz Truss", False), ("Theresa May", False)]},
                {"text": "Which country joined NATO in 2024?", "points": 1, "choices": [("Ukraine", False), ("Sweden", True), ("Finland", False), ("Georgia", False)]},
            ]
        },
        {
            "title": "Geopolitics & World Affairs",
            "description": "Geopolitical knowledge testing.",
            "time_limit": 10,
            "questions": [
                {"text": "Which treaty established the European Union?", "points": 1, "choices": [("Treaty of Paris", False), ("Treaty of Rome", False), ("Treaty of Maastricht", True), ("Treaty of Versailles", False)]},
                {"text": "What does NATO stand for?", "points": 1, "choices": [("North Atlantic Treaty Organization", True), ("National Alliance for Treaty Operations", False), ("North American Trade Organization", False), ("National Association of Treaty Organizations", False)]},
                {"text": "Which country is NOT a permanent member of the UN Security Council?", "points": 1, "choices": [("USA", False), ("UK", False), ("Germany", True), ("China", False)]},
                {"text": "Which water body separats the UK and France?", "points": 1, "choices": [("North Sea", False), ("Irish Sea", False), ("English Channel", True), ("Atlantic Ocean", False)]},
                {"text": "Where is the headquarters of the World Health Organization?", "points": 1, "choices": [("New York", False), ("Geneva", True), ("Paris", False), ("London", False)]},
                {"text": "Which two countries share the longest land border?", "points": 1, "choices": [("Russia and China", False), ("USA and Canada", True), ("India and Pakistan", False), ("Argentina and Chile", False)]},
                {"text": "What is the capital of Australia?", "points": 1, "choices": [("Sydney", False), ("Melbourne", False), ("Canberra", True), ("Perth", False)]},
                {"text": "The phrase 'Iron Curtain' is associated with which war?", "points": 1, "choices": [("World War I", False), ("World War II", False), ("Cold War", True), ("Vietnam War", False)]},
                {"text": "What is the smallest UN recognized country by area?", "points": 1, "choices": [("Monaco", False), ("Nauru", False), ("Tuvalu", False), ("Vatican City", True)]},
                {"text": "Which organization's goal is to regulate international trade?", "points": 1, "choices": [("IMF", False), ("World Bank", False), ("UN", False), ("WTO", True)]},
            ]
        },
        {
            "title": "Natural Science",
            "description": "Test your basic science knowledge.",
            "time_limit": 10,
            "questions": [
                {"text": "What is the chemical symbol for gold?", "points": 1, "choices": [("Au", True), ("Ag", False), ("Pb", False), ("Fe", False)]},
                {"text": "Which planet is known as the Red Planet?", "points": 1, "choices": [("Venus", False), ("Mars", True), ("Jupiter", False), ("Saturn", False)]},
                {"text": "What gas do plants absorb during photosynthesis?", "points": 1, "choices": [("Oxygen", False), ("Nitrogen", False), ("Carbon Dioxide", True), ("Hydrogen", False)]},
                {"text": "Who proposed the theory of relativity?", "points": 1, "choices": [("Isaac Newton", False), ("Albert Einstein", True), ("Galileo Galilei", False), ("Nikola Tesla", False)]},
                {"text": "What is the powerhouse of the cell?", "points": 1, "choices": [("Nucleus", False), ("Ribosome", False), ("Mitochondria", True), ("Endoplasmic Reticulum", False)]},
                {"text": "Which is the most abundant gas in the earth's atmosphere?", "points": 1, "choices": [("Oxygen", False), ("Carbon Dioxide", False), ("Nitrogen", True), ("Hydrogen", False)]},
                {"text": "What is the hardest natural substance on Earth?", "points": 1, "choices": [("Gold", False), ("Iron", False), ("Diamond", True), ("Platinum", False)]},
                {"text": "What force pulls objects toward the center of the earth?", "points": 1, "choices": [("Magnetism", False), ("Friction", False), ("Gravity", True), ("Inertia", False)]},
                {"text": "Water boils at how many degrees Celsius?", "points": 1, "choices": [("50", False), ("100", True), ("150", False), ("200", False)]},
                {"text": "What does DNA stand for?", "points": 1, "choices": [("Deoxyribonucleic Acid", True), ("Ribonucleic Acid", False), ("Deoxyribose Nitrogen Acid", False), ("Deoxyribose Nuclear Acid", False)]},
            ]
        },
        {
            "title": "World History Highlights",
            "description": "Historical events from around the globe.",
            "time_limit": 10,
            "questions": [
                {"text": "In which year did World War II end?", "points": 1, "choices": [("1940", False), ("1945", True), ("1950", False), ("1939", False)]},
                {"text": "Who was the first Emperor of Rome?", "points": 1, "choices": [("Julius Caesar", False), ("Augustus", True), ("Nero", False), ("Caligula", False)]},
                {"text": "The French Revolution began in which year?", "points": 1, "choices": [("1776", False), ("1789", True), ("1812", False), ("1848", False)]},
                {"text": "Who discovered America in 1492?", "points": 1, "choices": [("Vasco da Gama", False), ("Christopher Columbus", True), ("Ferdinand Magellan", False), ("Marco Polo", False)]},
                {"text": "The Great Wall of China was primarily built to protect against which empire?", "points": 1, "choices": [("Roman", False), ("Mongol", True), ("Persian", False), ("Ottoman", False)]},
                {"text": "Who was the first President of the United States?", "points": 1, "choices": [("Thomas Jefferson", False), ("Abraham Lincoln", False), ("George Washington", True), ("John Adams", False)]},
                {"text": "Which civilization built the pyramids of Giza?", "points": 1, "choices": [("Mayans", False), ("Greeks", False), ("Romans", False), ("Egyptians", True)]},
                {"text": "What was the name of the ship that brought the Pilgrims to America?", "points": 1, "choices": [("Santa Maria", False), ("Mayflower", True), ("Endeavour", False), ("Beagle", False)]},
                {"text": "Who was the leader of the Soviet Union during WWII?", "points": 1, "choices": [("Vladimir Lenin", False), ("Joseph Stalin", True), ("Leon Trotsky", False), ("Nikita Khrushchev", False)]},
                {"text": "The Renaissance began in which country?", "points": 1, "choices": [("France", False), ("Spain", False), ("Italy", True), ("Germany", False)]},
            ]
        },
        {
            "title": "Literature Classics",
            "description": "Famed literature and authors.",
            "time_limit": 10,
            "questions": [
                {"text": "Who wrote 'Romeo and Juliet'?", "points": 1, "choices": [("Charles Dickens", False), ("William Shakespeare", True), ("Jane Austen", False), ("Mark Twain", False)]},
                {"text": "Which novel starts with 'Call me Ishmael'?", "points": 1, "choices": [("Moby-Dick", True), ("1984", False), ("The Great Gatsby", False), ("Pride and Prejudice", False)]},
                {"text": "Who is the author of the Harry Potter series?", "points": 1, "choices": [("J.R.R. Tolkien", False), ("J.K. Rowling", True), ("George R.R. Martin", False), ("C.S. Lewis", False)]},
                {"text": "In which city is 'Les Misérables' primarily set?", "points": 1, "choices": [("London", False), ("Rome", False), ("Paris", True), ("Madrid", False)]},
                {"text": "What is the pen name of Samuel Langhorne Clemens?", "points": 1, "choices": [("Mark Twain", True), ("George Orwell", False), ("Lewis Carroll", False), ("O. Henry", False)]},
                {"text": "Who wrote '1984'?", "points": 1, "choices": [("Aldous Huxley", False), ("Ray Bradbury", False), ("George Orwell", True), ("H.G. Wells", False)]},
                {"text": "Which animal is the central figure in 'Animal Farm'?", "points": 1, "choices": [("A horse", False), ("A pig", True), ("A cow", False), ("A dog", False)]},
                {"text": "Who wrote 'Pride and Prejudice'?", "points": 1, "choices": [("Emily Brontë", False), ("Charlotte Brontë", False), ("Jane Austen", True), ("Virginia Woolf", False)]},
                {"text": "What is the name of the main character in 'The Catcher in the Rye'?", "points": 1, "choices": [("Holden Caulfield", True), ("Jay Gatsby", False), ("Huckleberry Finn", False), ("Tom Sawyer", False)]},
                {"text": "Who wrote 'The Odyssey'?", "points": 1, "choices": [("Virgil", False), ("Homer", True), ("Ovid", False), ("Sophocles", False)]},
            ]
        },
        {
            "title": "Cinema & Entertainment",
            "description": "Movies, shows, and popular culture.",
            "time_limit": 10,
            "questions": [
                {"text": "Who directed the movie 'Titanic'?", "points": 1, "choices": [("Steven Spielberg", False), ("Christopher Nolan", False), ("James Cameron", True), ("Martin Scorsese", False)]},
                {"text": "Which actor played Iron Man in the MCU?", "points": 1, "choices": [("Chris Evans", False), ("Chris Hemsworth", False), ("Robert Downey Jr.", True), ("Mark Ruffalo", False)]},
                {"text": "What is the highest-grossing film of all time?", "points": 1, "choices": [("Avengers: Endgame", False), ("Avatar", True), ("Titanic", False), ("Star Wars: The Force Awakens", False)]},
                {"text": "In the Matrix, what color pill does Neo take?", "points": 1, "choices": [("Blue", False), ("Red", True), ("Green", False), ("Yellow", False)]},
                {"text": "Which movie won the first Academy Award for Best Picture?", "points": 1, "choices": [("Wings", True), ("Gone with the Wind", False), ("Casablanca", False), ("Citizen Kane", False)]},
                {"text": "Who played the Joker in 'The Dark Knight'?", "points": 1, "choices": [("Jack Nicholson", False), ("Jared Leto", False), ("Heath Ledger", True), ("Joaquin Phoenix", False)]},
                {"text": "What is the name of the hobbit played by Elijah Wood in the Lord of the Rings movies?", "points": 1, "choices": [("Sam", False), ("Pippin", False), ("Merry", False), ("Frodo", True)]},
                {"text": "Which animated film features a character named Simba?", "points": 1, "choices": [("Aladdin", False), ("The Lion King", True), ("Mulan", False), ("Frozen", False)]},
                {"text": "Who is the creator of the 'Star Wars' franchise?", "points": 1, "choices": [("J.J. Abrams", False), ("George Lucas", True), ("Steven Spielberg", False), ("Peter Jackson", False)]},
                {"text": "What is the name of the fictional African country in 'Black Panther'?", "points": 1, "choices": [("Zamunda", False), ("Genovia", False), ("Wakanda", True), ("El Dorado", False)]},
            ]
        },
        {
            "title": "Space & Astronomy",
            "description": "Looking at the stars and planets.",
            "time_limit": 10,
            "questions": [
                {"text": "Which is the largest planet in our solar system?", "points": 1, "choices": [("Saturn", False), ("Jupiter", True), ("Neptune", False), ("Uranus", False)]},
                {"text": "What is the name of our galaxy?", "points": 1, "choices": [("Andromeda", False), ("Milky Way", True), ("Triangulum", False), ("Sombrero", False)]},
                {"text": "Who was the first person to walk on the moon?", "points": 1, "choices": [("Yuri Gagarin", False), ("Buzz Aldrin", False), ("Neil Armstrong", True), ("Michael Collins", False)]},
                {"text": "What is the closest star to Earth?", "points": 1, "choices": [("Proxima Centauri", False), ("Sirius", False), ("Sun", True), ("Alpha Centauri", False)]},
                {"text": "Which planet is famous for its large rings?", "points": 1, "choices": [("Jupiter", False), ("Uranus", False), ("Saturn", True), ("Neptune", False)]},
                {"text": "What is the name of the first artificial satellite launched into space?", "points": 1, "choices": [("Apollo 11", False), ("Sputnik 1", True), ("Explorer 1", False), ("Vostok 1", False)]},
                {"text": "How many planets are in our solar system?", "points": 1, "choices": [("7", False), ("8", True), ("9", False), ("10", False)]},
                {"text": "Which planet is known as the Morning Star or Evening Star?", "points": 1, "choices": [("Mercury", False), ("Venus", True), ("Mars", False), ("Jupiter", False)]},
                {"text": "What force keeps the planets in orbit around the sun?", "points": 1, "choices": [("Magnetism", False), ("Friction", False), ("Gravity", True), ("Inertia", False)]},
                {"text": "A light-year is a measure of what?", "points": 1, "choices": [("Time", False), ("Speed", False), ("Distance", True), ("Luminosity", False)]},
            ]
        },
        {
            "title": "General Mathematics",
            "description": "Math trivia and fundamentals.",
            "time_limit": 10,
            "questions": [
                {"text": "What is the value of Pi to two decimal places?", "points": 1, "choices": [("3.12", False), ("3.14", True), ("3.16", False), ("3.18", False)]},
                {"text": "What is the square root of 144?", "points": 1, "choices": [("10", False), ("11", False), ("12", True), ("14", False)]},
                {"text": "What is the only even prime number?", "points": 1, "choices": [("0", False), ("2", True), ("4", False), ("6", False)]},
                {"text": "How many degrees are in a full circle?", "points": 1, "choices": [("180", False), ("270", False), ("360", True), ("450", False)]},
                {"text": "What comes next in the Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, __?", "points": 1, "choices": [("11", False), ("12", False), ("13", True), ("14", False)]},
                {"text": "What is a polygon with 8 sides called?", "points": 1, "choices": [("Hexagon", False), ("Heptagon", False), ("Octagon", True), ("Nonagon", False)]},
                {"text": "What is 7 multiplied by 8?", "points": 1, "choices": [("54", False), ("56", True), ("64", False), ("48", False)]},
                {"text": "If a triangle has a 90-degree angle, what is it called?", "points": 1, "choices": [("Acute triangle", False), ("Obtuse triangle", False), ("Right triangle", True), ("Equilateral triangle", False)]},
                {"text": "What is the Roman numeral for 50?", "points": 1, "choices": [("X", False), ("L", True), ("C", False), ("D", False)]},
                {"text": "Simplify: 10 + 10 / 2", "points": 1, "choices": [("10", False), ("15", True), ("20", False), ("5", False)]},
            ]
        },
        {
            "title": "Bollywood Magic",
            "description": "Test your knowledge of Indian cinema.",
            "time_limit": 10,
            "questions": [
                {"text": "Who is known as the 'King of Bollywood'?", "points": 1, "choices": [("Salman Khan", False), ("Shah Rukh Khan", True), ("Aamir Khan", False), ("Akshay Kumar", False)]},
                {"text": "Which was the first Indian sound film?", "points": 1, "choices": [("Alam Ara", True), ("Raja Harishchandra", False), ("Mughal-e-Azam", False), ("Sholay", False)]},
                {"text": "In 'DDLJ', what is the name of Shah Rukh Khan's character?", "points": 1, "choices": [("Rahul", False), ("Raj", True), ("Prem", False), ("Aman", False)]},
                {"text": "Which movie features the song 'Chaiyya Chaiyya'?", "points": 1, "choices": [("Dil Se", True), ("Lagaan", False), ("Swades", False), ("Taal", False)]},
                {"text": "Who directed the movie '3 Idiots'?", "points": 1, "choices": [("Karan Johar", False), ("Rajkumar Hirani", True), ("Sanjay Leela Bhansali", False), ("Farhan Akhtar", False)]},
                {"text": "What is the highest-grossing Bollywood film of 2023?", "points": 1, "choices": [("Pathaan", False), ("Jawan", True), ("Animal", False), ("Gadar 2", False)]},
                {"text": "Which actress made her Bollywood debut in 'Om Shanti Om'?", "points": 1, "choices": [("Priyanka Chopra", False), ("Deepika Padukone", True), ("Anushka Sharma", False), ("Katrina Kaif", False)]},
                {"text": "Who played the character of 'Mogambo' in Mr. India?", "points": 1, "choices": [("Amjad Khan", False), ("Amrish Puri", True), ("Kader Khan", False), ("Gulshan Grover", False)]},
                {"text": "Which film was India's first submission for the Academy Award for Best International Feature Film?", "points": 1, "choices": [("Mother India", True), ("Lagaan", False), ("Salaam Bombay!", False), ("Devdas", False)]},
                {"text": "Who composed the music for the film 'Slumdog Millionaire'?", "points": 1, "choices": [("A.R. Rahman", True), ("Shankar-Ehsaan-Loy", False), ("Pritam", False), ("Vishal-Shekhar", False)]},
            ]
        }
    ]

def load_practice_quizzes(*, replace: bool = False) -> Tuple[int, int]:
    from quizapp.models import Quiz, Question, Choice
    
    quiz_data_list = get_quiz_data()
    
    created_quizzes_count = 0
    created_questions_count = 0

    for quiz_data in quiz_data_list:
        if replace:
            Quiz.objects.filter(title=quiz_data["title"]).delete()
        
        quiz, created = Quiz.objects.get_or_create(
            title=quiz_data["title"],
            defaults={
                "description": quiz_data["description"],
                "time_limit": quiz_data["time_limit"],
                "is_active": True,
            }
        )
        if created or replace:
            created_quizzes_count += 1
            for i, q in enumerate(quiz_data["questions"], 1):
                question = Question.objects.create(
                    quiz=quiz,
                    text=q["text"],
                    points=q["points"],
                    order=i
                )
                created_questions_count += 1
                for choice_text, is_correct in q["choices"]:
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        is_correct=is_correct
                    )
    return created_quizzes_count, created_questions_count
