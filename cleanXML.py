import xml.etree.ElementTree as ET

# Strings to replace
replacements = {'<br clear="none"/>':'', '<br />':'', '<br/>':'', '<br>':''}

# Open file, read it replace string and write in a new file line by line
fileToRead = 'juriSommaire.xml'
fileToWrite = 'juriSommaireClean.xml'
with open(fileToRead) as infile, open(fileToWrite, 'w') as outfile:
    for line in infile:
        for src, target in replacements.iteritems():
            line = line.replace(src, target)
        outfile.write(line)

# Parse XML
tree = ET.parse('juriSommaireClean.xml')

# Get the root of the XML
root = tree.getroot()

# Down the tree TEXTE then BLOC_TEXTUEl then CONTENU
texte = root.find('TEXTE')
bloc_textuel = texte.find('BLOC_TEXTUEL')
contenu = bloc_textuel.find('CONTENU')

# Get text from children from CONTENU = paragraphs <p></p>
p = ''
for child in contenu:
 	p = p + child.text

# Print full text
print p