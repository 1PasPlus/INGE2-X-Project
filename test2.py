text = "bonjour"

text2 = "ça va"

text3 = text2+' '+text

print( text3)


if isinstance(output, list):
    # Assuming the first element in the list contains the summarized text
    rewritten_text = output[0].get('summary')
    counter = 0
    for characters in rewritten_text:
         counter +=1
    print(rewritten_text, "Le nombre de caratère est de ")
else:
    print("Unexpected response format. Could not extract summarized text.")