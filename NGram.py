import string
from collections import Counter
def input_processing():
    # Read the input file
    file_path = input("Enter the path to the file: ")
    with open(file_path, 'r') as file:
            # Convert to lowercase
            content = file.read().lower()
            # Remove the Punctuation
            content = content.translate(str.maketrans('', '', string.punctuation))
            # Tokenize the corpus
            tokens = content.split()
    return tokens
def model():
      tokens=input_processing()
      # Extracting unigrams, bigrams and trigrams
      unigrams=tokens
      bigrams=[(tokens[i], tokens[i+1]) for i in range(len(tokens)-1)]
      trigrams = [(tokens[i], tokens[i+1], tokens[i+2]) for i in range(len(tokens)-2)]
      # Count the occurences
      unigram_counts = Counter(unigrams)
      bigram_counts = Counter(bigrams)
      trigram_counts = Counter(trigrams)
      
      ngram_counts_dict = {}
      ngram_counts_dict.update(unigram_counts)
      ngram_counts_dict.update(bigram_counts)
      ngram_counts_dict.update(trigram_counts)
     
      # Display n gram counts 
      print(ngram_counts_dict)
      # Compute conditional probabilities and store it in another file

      total_unigrams = sum(unigram_counts.values())
      unigram_probs = {word: count / total_unigrams for word, count in unigram_counts.items()}
      bigram_probs = {(w1, w2): count / unigram_counts[w1] for (w1, w2), count in bigram_counts.items()}
      trigram_probs = {(w1, w2, w3): count / bigram_counts[(w1, w2)] for (w1, w2, w3), count in trigram_counts.items()}
      
      with open("ngram_probabilities.txt", "w") as f:
        f.write("Unigram Probabilities:\n")
        for word, prob in unigram_probs.items():
            f.write(f"P({word}) = {prob:.4f}\n")

        f.write("\nBigram Conditional Probabilities:\n")
        for (w1, w2), prob in bigram_probs.items():
            f.write(f"P({w2} | {w1}) = {prob:.4f}\n")

        f.write("\nTrigram Conditional Probabilities:\n")
        for (w1, w2, w3), prob in trigram_probs.items():
            f.write(f"P({w3} | {w1}, {w2}) = {prob:.4f}\n")

        return unigram_probs, bigram_probs, trigram_probs
def nextWordPredictions(unigram_probs, bigram_probs, trigram_probs):
    phrase = input("\nEnter a phrase to predict the next word: ").lower()
    phrase = phrase.translate(str.maketrans('', '', string.punctuation))
    tokens = phrase.split()
    
    if not tokens:
        print("Please enter at least one word.")
        return

    if len(tokens) >= 2:
        w1, w2 = tokens[-2], tokens[-1]
        candidates = {k[2]: v for k, v in trigram_probs.items() if k[0] == w1 and k[1] == w2}
        if candidates:
            next_word = max(candidates, key=candidates.get)
            print(f"Most probable next word (trigram): {next_word}")
            return

    if len(tokens) >= 1:
        w1 = tokens[-1]
        candidates = {k[1]: v for k, v in bigram_probs.items() if k[0] == w1}
        if candidates:
            next_word = max(candidates, key=candidates.get)
            print(f"Most probable next word (bigram): {next_word}")
            return

    # Check if any of the input words even exist
    if all(word not in unigram_probs for word in tokens):
        print("Sorry, the input phrase does not exist in the model.")
        return

    # Fallback: Unigram prediction
    next_word = max(unigram_probs, key=unigram_probs.get)
    print(f"Most probable next word (unigram/fallback): {next_word}")
unigram_probs, bigram_probs, trigram_probs = model()
nextWordPredictions(unigram_probs,bigram_probs, trigram_probs)
