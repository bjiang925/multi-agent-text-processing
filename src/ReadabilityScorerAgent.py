# `re` module: use Python's regular expression functions for
# splitting text into sentences, words, and for pattern matching
import re

class ReadabilityScorerAgent:
    """
    This class contains all the functionality for the ReadabilityScore agent.
    Use Case: Test readability level of the input text using metrics, including:
              - Flesch Reading Ease: gives a text a score between 1 and 100
                    1-30: very difficult to read, best understood by university graduates
                    30-50: difficult to read, best understood by college graduates
                    50-60: fairly difficult to read
                    60-70: easily understood by 13- to 15-year-old students
                    70-80: fairly easy to read
                    80-90: easy to read
                    90-100: very easy to read, easily understood by an average 11-year-old student
              - Flesch-Kincaid Grade Level: assesses reading grade level of a text
                    0-3: basic, Kindergarten / Elementary
                    3-6: basic, Elementary
                    6-9: average, middle school
                    9-12: average, high school
                    12-15: advanced, college
                    15-18: advanced, post-grad
    """
    
    def count_sentences(self, text: str) -> int:
        """
        Count number of sentences in the input text using basic punctuation markers.
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip()]  # Remove empty strings.
        return len(sentences)
    
    def count_words(self, text: str) -> int:
        """
        Count number of words in the input text.
        """
        words = re.findall(r'\b\w+\b', text)
        return len(words)
    
    def count_syllables_in_word(self, word: str) -> int:
        """
        Estimate number of syllables in a single word using a basic heuristic.
        """
        word = word.lower()
        word = re.sub(r'[^a-z]', '', word)  # Remove non-alphabetic characters.
        if not word:
            return 0
        
        vowels = "aeiou"
        syllable_count = 0
        prev_char_was_vowel = False
        
        for i, char in enumerate(word):
            is_vowel = char in vowels
            # Treat 'y' as a vowel if it is not the first character.
            if char == "y" and i != 0:
                is_vowel = True
                
            if is_vowel and not prev_char_was_vowel:
                syllable_count += 1
                prev_char_was_vowel = True
            else:
                prev_char_was_vowel = is_vowel
        
        # Adjust for silent 'e' at the end.
        if word.endswith("e") and syllable_count > 1:
            syllable_count -= 1
            
        return syllable_count if syllable_count > 0 else 1
    
    def count_syllables(self, text: str) -> int:
        """
        Count syllables in the full text.
        """
        words = re.findall(r'\b\w+\b', text)
        total_syllables = sum(self.count_syllables_in_word(word) for word in words)
        return total_syllables
    
    def assess_readability(self, text: str) -> dict:
        """
        Assess readability metrics of the input text.

        Returns a dictionary with:
          - 'flesch_reading_ease': Flesch Reading Ease Score (clamped between 1 and 100)
          - 'flesch_kincaid_grade': Flesch-Kincaid Grade Level
        """
        sentences = self.count_sentences(text)
        words = self.count_words(text)
        syllables = self.count_syllables(text)
        
        # Protect against division by zero.
        if sentences == 0 or words == 0:
            return {"error": "Text must contain at least one sentence and one word."}
        
        avg_words_per_sentence = words / sentences
        avg_syllables_per_word = syllables / words

        # Calculate Flesch Reading Ease using the formula.
        flesch_reading_ease = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
        # Clamp the score to the range 1 to 100.
        flesch_reading_ease = max(1, min(flesch_reading_ease, 100))
        
        # Calculate Flesch-Kincaid Grade Level.
        flesch_kincaid_grade = (0.39 * avg_words_per_sentence) + (11.8 * avg_syllables_per_word) - 15.59

        return {
            "flesch_reading_ease": round(flesch_reading_ease, 2),
            "flesch_kincaid_grade": round(flesch_kincaid_grade, 2)
        }

def interpret_flesch_reading(score: float) -> str:
    """
    Provide a description based on the Flesch Reading Ease score.
    """
    if score <= 30:
        return "very difficult to read, best understood by university graduates"
    elif score <= 50:
        return "difficult to read, best understood by college graduates"
    elif score <= 60:
        return "fairly difficult to read"
    elif score <= 70:
        return "easily understood by 13- to 15-year-old students"
    elif score <= 80:
        return "fairly easy to read"
    elif score <= 90:
        return "easy to read"
    else:
        return "very easy to read, easily understood by an average 11-year-old student"

def interpret_flesch_kincaid(grade: float) -> str:
    """
    Provide a description based on the Flesch-Kincaid Grade Level.
    """
    if grade <= 3:
        return "basic, Kindergarten / Elementary"
    elif grade <= 6:
        return "basic, Elementary"
    elif grade <= 9:
        return "average, middle school"
    elif grade <= 12:
        return "average, high school"
    elif grade <= 15:
        return "advanced, college"
    elif grade <= 18:
        return "advanced, post-grad"
    else:
        return "beyond post-grad level"

# Check code #1
if __name__ == "__main__":
    # Sample text as a continuous paragraph.
    sample_text = (
        "In the realm of higher education and academic research, understanding the underlying structures of classic literature "
        "often proves challenging, especially when navigating archaic expressions and complex sentence structures. "
        "Students frequently encounter difficulties in decoding intricate phrases, and faculty are tasked with providing "
        "supplementary materials that facilitate comprehension. The clear articulation of these subjects is critical in "
        "bridging the gap between advanced theoretical concepts and practical application, ensuring that all learners can succeed."
    )
    
    # Instantiate the ReadabilityScorerAgent.
    scorer = ReadabilityScorerAgent()
    results = scorer.assess_readability(sample_text)
    
    # Get the scores.
    flesch_score = results.get("flesch_reading_ease")
    fk_grade = results.get("flesch_kincaid_grade")
    
    # Interpret the scores.
    flesch_interpretation = interpret_flesch_reading(flesch_score)
    fk_interpretation = interpret_flesch_kincaid(fk_grade)
    
    # Print the results along with interpretations.
    print("Readability Results:")
    print(f"Flesch Reading Ease Score: {flesch_score} - {flesch_interpretation}")
    print(f"Flesch-Kincaid Grade Level: {fk_grade} - {fk_interpretation}")


# check code #2
if __name__ == "__main__":
    # Provided sample text.
    sample_text = (
        "The quick brown fox jumps over the lazy dog. "
        "This sentence is designed to test readability. "
        "However, determining syllable counts can be surprisingly challenging!"
    )
    
    # Instantiate the ReadabilityScorerAgent.
    scorer = ReadabilityScorerAgent()
    results = scorer.assess_readability(sample_text)
    
    # Retrieve scores.
    flesch_score = results.get("flesch_reading_ease")
    fk_grade = results.get("flesch_kincaid_grade")
    
    # Interpret the scores.
    flesch_interpretation = interpret_flesch_reading(flesch_score)
    fk_interpretation = interpret_flesch_kincaid(fk_grade)
    
    # Print the results along with their interpretations.
    print("Readability Results:")
    print(f"Flesch Reading Ease Score: {flesch_score} - {flesch_interpretation}")
    print(f"Flesch-Kincaid Grade Level: {fk_grade} - {fk_interpretation}")