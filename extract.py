from bs4 import BeautifulSoup

file = open("pybacklogpy_doc.html", "r")
html = ""

for line in file.readlines():
    html += line
file.close()

soup = BeautifulSoup(html, 'html.parser')

# Find all the method names based on the given structure
methods = soup.find_all('dl', class_='method')

for method in methods:
    print("# " + method.dt['id'])  # This will print the method name
    parameter = method.find('dd', class_='field-odd')
    if parameter is not None:
        args = parameter.find_all("li")
        for a in args:
            if a.strong is not None:
                args_name = a.strong.string
                a.strong.extract()
                print("- args_name: ", args_name , ", args_description: " ,a.p.string[2:])
