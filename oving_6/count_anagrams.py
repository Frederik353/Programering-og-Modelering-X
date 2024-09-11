
def antall_anagrammer(tekst):
    words = tekst.split(" ")
    antall_anagram = 0
    for word in words:
        if word == word[::-1]:
            antall_anagram  += 1
    return antall_anagram

print(antall_anagrammer("hei otto har du betalt dine regninger"))