# Music-Recommendation-System

We extract features from the content of the song descriptions to create an object representation. Define a similarity function among these object representations which mimics what human understands as an item-item similarity.

TF-IDF is a technique used for information retrieval. Term Frequency-Inverse Document Frequency (TF-IDF) matches text and words. It is a technique used for information retrieval. It weights a term’s frequency (TF) and inverse document frequency (IDF).

The higher the TF*IDF score, the more strange the word in that context and thus, the more critical the term.

Formulae:
1. TF(word1) = Number of time word1 appears/Total number of words
2. IDF = log(Total number of documents/Number of documents containing the term)

