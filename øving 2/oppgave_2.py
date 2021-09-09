import matplotlib.pyplot as plt
import string



input_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mi sed quam rutrum placerat. Fusce finibus feugiat ante vitae porta. Maecenas velit erat, convallis quis nisi at, sodales cursus ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Ut vehicula dolor in lobortis aliquet. Donec dignissim lorem velit, eu sollicitudin mi lacinia blandit. Fusce malesuada gravida odio, vitae sollicitudin dolor interdum vitae. Sed sollicitudin, massa eu pharetra eleifend, enim metus suscipit nulla, et mollis nisi erat et elit. Proin bibendum ex vitae mauris pretium egestas. Fusce tristique erat et ornare gravida. Aliquam rhoncus risus a nulla feugiat, fermentum porttitor neque mattis. Donec eu nisi non odio laoreet rutrum. In venenatis leo id tellus sagittis, ac volutpat dui tincidunt."


dictionary = dict.fromkeys(string.ascii_lowercase, 0)


dictionary.update(a=2)
for i in range(len(input_text)):
    if input_text[i] in dictionary:
        dictionary[input_text[i].lower()] += 1
    else:
        dictionary[input_text[i].lower()] = 1


# for i in sorted(dictionary.items()): # sorterer dict'en men ble bedre å  legge inn bokstavene først i tillfelle ikke alle bokstavene i alfabetet er i stringen ser dette bedre ut



names = list(dictionary.keys())
values = list(dictionary.values())

plt.bar(range(len(dictionary)), values, tick_label=names)
plt.show()
