print("____Welcome to the python Mad Lib Generator____ ")
adj1=input("Enter an adjective (eg: Slimmy or Sparkly): ")
animal=input("Enter an animal:")
verb_past=input("Enter a verb in past tense :")
place= input("Enter the place")
food=input("Enter the food ")
number=input("Enter the number:")
emotion=input("Enter the emotion ")
story = f"""
--- Your Custom Story ---
Yesterday, a {adj1} {animal} suddenly {verb_past} right in the middle of {place}.
Everyone nearby stopped eating their {food} and stared for {number} seconds.
Honestly, I have never felt so {emotion} in my entire life!
"""

# 3. Display the result
print(story)