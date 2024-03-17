#print ("Hello World")


from GoogleNews import GoogleNews

gnews = GoogleNews()

gnews.set_time_range('01/03/2024','16/03/2024')

gnews.search('bictoin')

print(gnews.results())

