

letters = ["a", "b" , "c", "d"]
numbers = [1,2,3,4]
dictionary = dict()

for l in letters:
    dictionary[l] = numbers
# negawatt

#dictonary2 = {k:v for (k,v) in letters,numbers}

#
# dictionary hearts:[1,2,3,4], diamond:[1,2,3,4]
# dictonary = {k:v for (k,v) in }
print(dictionary["a"][1])
dictionary.pop("a")
print(dictionary["a"][1])
print(dictionary)