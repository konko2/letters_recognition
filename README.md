# Letters recognition
 This program matches first 10 capital letters 
 of english alphabet on image: A, 'B', 'C', 'D', 'E', 'F',
 'G', 'H', 'I' and 'J'.
 
 This algorithm is very naive, 
 so letters should be plenty smooth, no tilted.
 There should not be shadow on the paper.
 

## HowTo
 To use it, you must have Python3 with installed PIL.
 To install PIL write in console:
 ```
 pip install pillow
```
Then, in Python, only import `find_letters` function from package. 

Example:
```
from letters_recognition import find_letters
image = find_letters('my/path/to/image.jpg')
image.show()
```

