

letters = ["a", "b" , "c", "d"]
numbers = [1,2,3,4]
dictionary = dict()

for l in letters:
    dictionary[l] = numbers
# consider possibility of using negawatt

#dictonary2 = {k:v for (k,v) in letters,numbers}

#
# dictionary hearts:[1,2,3,4], diamond:[1,2,3,4]
# dictonary = {k:v for (k,v) in }
print(dictionary["a"][1])
#dictionary.pop("a")
print(dictionary["a"])
dictionary["a"].remove(1)


# for a in d.values()
# a.remove(4)       except value error
print(dictionary.values())
print(dictionary.items())
