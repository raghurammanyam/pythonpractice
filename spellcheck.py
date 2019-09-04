import http.client
import xml.dom.minidom

data = """
0" ignoredups="0" ignoredigits="1" ignoreallcaps="1">
 %s 
 """
def spellCheck(word_to_spell):

    con = http.client.HTTPSConnection("www.google.com")
    print(con)
    con.request("POST", "/tbproxy/spell?lang=en", data % word_to_spell)
    response = con.getresponse()
    print(response.__dict__)
    dom = xml.dom.minidom.parseString(response.read())
    dom_data = dom.getElementsByTagName('spellresult')[0]

    if dom_data.childNodes:
        for child_node in dom_data.childNodes:
            result = child_node.firstChild.data.split()
        for word in result:
            print(word)
            if word_to_spell.upper() == word.upper():
                return True
        return False
    else:
        return True
spellCheck("Begumpets")