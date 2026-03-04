import json
import os
import random
import google.generativeai as genai

FALLBACK_QUESTIONS = {
    "Cricket Mastery": [
        {"text": "Who holds the record for the highest individual score in a Test match?", "points": 1, "choices": ["Brian Lara", "Sachin Tendulkar", "Virender Sehwag", "Matthew Hayden"], "correct_choice_index": 0},
        {"text": "Which country won the first T20 World Cup in 2007?", "points": 1, "choices": ["Australia", "India", "Pakistan", "England"], "correct_choice_index": 1},
        {"text": "What is the term for a bowler taking three wickets in consecutive deliveries?", "points": 1, "choices": ["Clean Sweep", "Triple Strike", "Hattrick", "Fifer"], "correct_choice_index": 2},
        {"text": "Who has achieved 100 international centuries?", "points": 1, "choices": ["Ricky Ponting", "Virat Kohli", "Sachin Tendulkar", "Jacques Kallis"], "correct_choice_index": 2},
        {"text": "Which of these is NOT a fielding position in cricket?", "points": 1, "choices": ["Gully", "Short leg", "Quarterback", "Silly point"], "correct_choice_index": 2},
    ],
    "Football Fundamentals": [
        {"text": "Who is the all-time leading goalscorer in the FIFA World Cup?", "points": 1, "choices": ["Pele", "Miroslav Klose", "Ronaldo Nazario", "Lionel Messi"], "correct_choice_index": 1},
        {"text": "Which club has won the most UEFA Champions League titles?", "points": 1, "choices": ["AC Milan", "Real Madrid", "Bayern Munich", "Liverpool"], "correct_choice_index": 1},
        {"text": "In what year was the Premier League founded?", "points": 1, "choices": ["1990", "1992", "1995", "1988"], "correct_choice_index": 1},
        {"text": "What is the circumference of a standard size 5 football?", "points": 1, "choices": ["65-67 cm", "68-70 cm", "71-73 cm", "60-62 cm"], "correct_choice_index": 1},
        {"text": "Which country won the first ever European Championship in 1960?", "points": 1, "choices": ["Soviet Union", "Yugoslavia", "France", "Germany"], "correct_choice_index": 0},
    ],
    "Technology Today": [
        {"text": "What does 'RAM' stand for?", "points": 1, "choices": ["Random Access Memory", "Read Access Memory", "Run Alternate Module", "Real Algorithm Memory"], "correct_choice_index": 0},
        {"text": "The popular version control system 'Git' was created by?", "points": 1, "choices": ["Bill Gates", "Linus Torvalds", "Steve Jobs", "Ken Thompson"], "correct_choice_index": 1},
        {"text": "Which programming language is mainly used for building Android apps?", "points": 1, "choices": ["Swift", "Kotlin", "Ruby", "PHP"], "correct_choice_index": 1},
        {"text": "What does 'API' stand for?", "points": 1, "choices": ["Advanced Programming Interface", "Application Programming Interface", "Automated Process Integration", "Application Process Interface"], "correct_choice_index": 1},
        {"text": "Which company bought GitHub in 2018?", "points": 1, "choices": ["Google", "Amazon", "Facebook", "Microsoft"], "correct_choice_index": 3},
    ],
    "Current Affairs Challenge": [
        {"text": "What major global climate summit takes place annually?", "points": 1, "choices": ["G20", "COP", "WEF", "NATO Summit"], "correct_choice_index": 1},
        {"text": "Which country recently became the newest member of NATO?", "points": 1, "choices": ["Ukraine", "Sweden", "Austria", "Switzerland"], "correct_choice_index": 1},
        {"text": "Where is the headquarters of the African Union?", "points": 1, "choices": ["Nairobi", "Cape Town", "Addis Ababa", "Cairo"], "correct_choice_index": 2},
        {"text": "BRICS represents Brazil, Russia, India, China, and which other country?", "points": 1, "choices": ["South Korea", "South Africa", "Saudi Arabia", "Spain"], "correct_choice_index": 1},
        {"text": "What is the global minimum corporate tax rate heavily debated recently?", "points": 1, "choices": ["10%", "15%", "20%", "25%"], "correct_choice_index": 1},
    ],
    "Geopolitics & World Affairs": [
        {"text": "The Strait of Hormuz connects the Persian Gulf to which ocean?", "points": 1, "choices": ["Atlantic", "Indian", "Pacific", "Arctic"], "correct_choice_index": 1},
        {"text": "Which country has the world's largest proven oil reserves?", "points": 1, "choices": ["Saudi Arabia", "Venezuela", "Canada", "USA"], "correct_choice_index": 1},
        {"text": "What is the official currency of Japan?", "points": 1, "choices": ["Yuan", "Won", "Yen", "Rupee"], "correct_choice_index": 2},
        {"text": "Which country is NOT a member of the G7?", "points": 1, "choices": ["Canada", "Italy", "China", "France"], "correct_choice_index": 2},
        {"text": "What is the capital of the European Union de facto?", "points": 1, "choices": ["Paris", "Berlin", "Brussels", "Amsterdam"], "correct_choice_index": 2},
    ],
    "Natural Science": [
        {"text": "What is the rarest blood type?", "points": 1, "choices": ["O negative", "AB negative", "A positive", "B negative"], "correct_choice_index": 1},
        {"text": "Which part of the brain controls balance and coordination?", "points": 1, "choices": ["Cerebrum", "Cerebellum", "Brain stem", "Hypothalamus"], "correct_choice_index": 1},
        {"text": "What is the chemical formula for table salt?", "points": 1, "choices": ["NaCl", "KCl", "NaOH", "HCl"], "correct_choice_index": 0},
        {"text": "How many bones are in the adult human body?", "points": 1, "choices": ["206", "208", "210", "205"], "correct_choice_index": 0},
        {"text": "Which planet is the hottest in the solar system?", "points": 1, "choices": ["Mercury", "Venus", "Mars", "Jupiter"], "correct_choice_index": 1},
    ],
    "World History Highlights": [
        {"text": "Who was the first female Pharaoh of ancient Egypt?", "points": 1, "choices": ["Cleopatra", "Nefertiti", "Hatshepsut", "Sobekneferu"], "correct_choice_index": 2},
        {"text": "The Byzantine Empire's capital was?", "points": 1, "choices": ["Rome", "Athens", "Constantinople", "Alexandria"], "correct_choice_index": 2},
        {"text": "Which famous conqueror never lost a battle?", "points": 1, "choices": ["Napoleon", "Genghis Khan", "Alexander the Great", "Julius Caesar"], "correct_choice_index": 2},
        {"text": "The Industrial Revolution began in which country?", "points": 1, "choices": ["France", "USA", "Germany", "Great Britain"], "correct_choice_index": 3},
        {"text": "When did the Berlin Wall fall?", "points": 1, "choices": ["1989", "1991", "1987", "1990"], "correct_choice_index": 0},
    ],
    "Literature Classics": [
        {"text": "Who wrote 'The Great Gatsby'?", "points": 1, "choices": ["Ernest Hemingway", "F. Scott Fitzgerald", "John Steinbeck", "William Faulkner"], "correct_choice_index": 1},
        {"text": "In 'To Kill a Mockingbird', what is the name of the protagonist?", "points": 1, "choices": ["Scout", "Jem", "Atticus", "Boo"], "correct_choice_index": 0},
        {"text": "Who is the villain in 'Peter Pan'?", "points": 1, "choices": ["Shere Khan", "Captain Hook", "Lord Voldemort", "Cruella de Vil"], "correct_choice_index": 1},
        {"text": "Which novel opens with 'It was the best of times, it was the worst of times'?", "points": 1, "choices": ["A Tale of Two Cities", "Oliver Twist", "David Copperfield", "Great Expectations"], "correct_choice_index": 0},
        {"text": "What is the longest novel ever written?", "points": 1, "choices": ["War and Peace", "In Search of Lost Time", "Les Misérables", "Clarissa"], "correct_choice_index": 1},
    ],
    "Cinema & Entertainment": [
        {"text": "What is the highest-grossing animated film of all time?", "points": 1, "choices": ["Frozen II", "The Lion King (2019)", "Inside Out 2", "Incredibles 2"], "correct_choice_index": 2},
        {"text": "Which movie won the first Academy Award for Best Animated Feature?", "points": 1, "choices": ["Toy Story", "Shrek", "Spirited Away", "Monsters, Inc."], "correct_choice_index": 1},
        {"text": "Who played Wolverine in the X-Men film series?", "points": 1, "choices": ["Chris Evans", "Ryan Reynolds", "Hugh Jackman", "Patrick Stewart"], "correct_choice_index": 2},
        {"text": "In what year was the first Harry Potter movie released?", "points": 1, "choices": ["2000", "2001", "2002", "1999"], "correct_choice_index": 1},
        {"text": "Which director is famous for the 'Dark Knight' trilogy?", "points": 1, "choices": ["Steven Spielberg", "Quentin Tarantino", "Christopher Nolan", "Martin Scorsese"], "correct_choice_index": 2},
    ],
    "Space & Astronomy": [
        {"text": "What is the name of the first human to orbit the Earth?", "points": 1, "choices": ["Neil Armstrong", "Yuri Gagarin", "John Glenn", "Buzz Aldrin"], "correct_choice_index": 1},
        {"text": "Which galaxy is expected to collide with the Milky Way?", "points": 1, "choices": ["Triangulum", "Andromeda", "Sombrero", "Whirlpool"], "correct_choice_index": 1},
        {"text": "What are comets mostly made of?", "points": 1, "choices": ["Rock", "Metal", "Ice and dust", "Gas"], "correct_choice_index": 2},
        {"text": "What is a 'supernova'?", "points": 1, "choices": ["A new star forming", "The birth of a galaxy", "The explosion of a star", "A black hole merging"], "correct_choice_index": 2},
        {"text": "How long does it take for sunlight to reach Earth?", "points": 1, "choices": ["8 minutes", "10 minutes", "1 year", "Instantaneous"], "correct_choice_index": 0},
    ],
    "General Mathematics": [
        {"text": "What is the value of the algebraic constant 'e' roughly?", "points": 1, "choices": ["3.14", "2.71", "1.61", "1.41"], "correct_choice_index": 1},
        {"text": "What shape represents a 20-sided die?", "points": 1, "choices": ["Dodecahedron", "Icosahedron", "Octahedron", "Tetrahedron"], "correct_choice_index": 1},
        {"text": "What is 15% of 200?", "points": 1, "choices": ["20", "25", "30", "35"], "correct_choice_index": 2},
        {"text": "In a right-angled triangle, what relates the three sides?", "points": 1, "choices": ["Euler's Formula", "Pythagorean Theorem", "Fermat's Last Theorem", "Golden Ratio"], "correct_choice_index": 1},
        {"text": "What is the derivative of x^2?", "points": 1, "choices": ["x", "2x", "x^3", "2x^2"], "correct_choice_index": 1},
    ],
    "Bollywood Magic": [
        {"text": "Which actor is known as the 'Tragedy King' of Bollywood?", "points": 1, "choices": ["Raj Kapoor", "Dilip Kumar", "Dev Anand", "Guru Dutt"], "correct_choice_index": 1},
        {"text": "What was the name of India's first colour film?", "points": 1, "choices": ["Alam Ara", "Mughal-e-Azam", "Kisan Kanya", "Mother India"], "correct_choice_index": 2},
        {"text": "Which movie features the iconic dialogue 'Mogambo khush hua'?", "points": 1, "choices": ["Mr. India", "Sholay", "Don", "Deewar"], "correct_choice_index": 0},
        {"text": "Who is the legendary playback singer known as the 'Nightingale of India'?", "points": 1, "choices": ["Asha Bhosle", "Lata Mangeshkar", "Kishore Kumar", "Mohammed Rafi"], "correct_choice_index": 1},
        {"text": "Which film won the Best Picture at the Filmfare Awards in 1996?", "points": 1, "choices": ["Dil To Pagal Hai", "Raja Hindustani", "Dilwale Dulhania Le Jayenge", "Kuch Kuch Hota Hai"], "correct_choice_index": 2},
        {"text": "Who played the character 'Gabbar Singh' in Sholay?", "points": 1, "choices": ["Amjad Khan", "Sanjeev Kumar", "Amitabh Bachchan", "Pran"], "correct_choice_index": 0},
        {"text": "Which Bollywood movie was nominated for Oscars in 2002?", "points": 1, "choices": ["Lagaan", "Devdas", "Swades", "Rang De Basanti"], "correct_choice_index": 0},
    ]
}

def generate_questions_for_topic(topic, count=5):
    """
    Attempts to generate new questions via Gemini AI.
    If no API key is configured, falls back to the pre-loaded offline bank.
    """
    # Using the directly provided API Key
    api_key = os.environ.get("AIzaSyA5lQj3CXT1VW2DToCD6rSNffLB88SemLg", "")
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"""
            Generate exactly {count} multiple-choice trivia questions about "{topic}".
            Return ONLY a valid, raw JSON array (do not wrap it in markdown block like ```json).
            Each object must have:
            - "text": the question string
            - "points": 1
            - "choices": array of exactly 4 string choices
            - "correct_choice_index": integer (0 to 3) representing the correct choice.
            """
            response = model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:-3].strip()
            elif text.startswith("```"):
                text = text[3:-3].strip()
                
            return json.loads(text)
        except Exception as e:
            print(f"Gemini generation failed: {e}")
            pass

    # Use the fallback database if Gemini isn't available or fails
    bank = FALLBACK_QUESTIONS.get(topic, [])
    
    if not bank:
        # If the topic is missing from fallbacks entirely, simulate however many we need 
        return [
            {"text": f"Simulated test question {i} about {topic}?", "points": 1, "choices": ["Option A", "Option B", "Option C", "Option D"], "correct_choice_index": 0}
            for i in range(1, count + 1)
        ]
        
    # Shuffle and return 5
    shuffled = bank.copy()
    random.shuffle(shuffled)
    return shuffled[:count]
