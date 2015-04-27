import xml.etree.ElementTree as ET

tree = ET.parse("stanford.xml")

root = tree.getroot()

for item in root.iter('success'):
    print "Sequence ID \n"
    for child in item.iter("sequence"):
        print child.attrib, child.text
    print "\n"
    print "PR Mutations \n"
    for natasha in item.iter("PR_mutations"):
        for natasha in item.iter("mutation"):
            print natasha.attrib, natasha.text
    print "\n"
    print "RT Mutations \n"
    for child in item.iter("RT_mutations"):
        for child in item.iter("mutation"):
            print child.attrib, child.text
    print "\n"
    print "Comments \n"
    for child in item.iter("comments"):
        for child in item.iter("comment"):
            print child.attrib, child.text
