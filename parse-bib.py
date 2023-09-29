# Libraries
import bibtexparser
import bibtexparser.middlewares as middlewares

# Subroutines
def squash(s):
    new = ""
    for x in s:
        new += x
    return new

def strEntryMinimal(entry,sep_cr,sep_tab):
    # Check entry type and format
    if entry.entry_type == "article":
        format = ["author", "title", "journal", "year", "volume", "number", "pages", "doi", "note"]
    elif entry.entry_type == "inproceedings":
        format = ["author", "title", "booktitle", "year", "volume", "number", "pages", "doi", "note"]
    elif entry.entry_type == "misc":
        format = ["author", "title", "note", "year", "volume", "number", "pages", "doi"]
    elif entry.entry_type == "mastersthesis":
        format = ["author", "title", "year", "school"]
    # Get values for fields in format
    values = [""] * len(format);
    for field in entry.fields:
        if field.key in format:
            values[format.index(field.key)] = field.value
    # Print
    str = ['@', entry.entry_type, '{', entry.key]
    for i in range(len(format)):
        if values[i] != "":
            str.append(',')
            str.append(sep_cr)
            str.append(sep_tab)
            str.append(format[i])
            str.append(' = {')
            str.append(values[i])
            str.append('}');
    str.append(sep_cr)
    str.append('}')
    str = squash(str)
    return str

def printEntryMinimal(file,entry):
    str = strEntryMinimal(entry,"\n","\t")
    file.write(str)
    file.write("\n\n")

def printEntryWebsite(file,entry):
    # Check entry type and format
    if entry.entry_type == "article":
        format = ["author-str", "title", "journal", "year", "volume", "number", "pages", "doi", "url", "abstract", "pdf", "github", "video", "note"]
    elif entry.entry_type == "inproceedings":
        format = ["author-str", "title", "booktitle", "year", "volume", "number", "pages", "doi", "url", "abstract", "pdf", "github", "video", "note"]
    elif entry.entry_type == "misc":
        format = ["author-str", "title", "note", "year", "volume", "number", "pages", "doi", "url", "abstract", "pdf", "github", "video"]
    elif entry.entry_type == "mastersthesis":
        format = ["author-str", "title", "school", "year", "volume", "number", "pages", "doi", "url", "abstract", "pdf", "github", "video"]
    else:
        return

    # Get values for fields in format
    values = [""] * len(format);
    for field in entry.fields:
        if field.key in format:
            values[format.index(field.key)] = field.value

    # Build string
    # Build citation
    str_citation = [""];
    str_citation.append(values[0]);
    str_citation.append(", <b>'");
    str_citation.append(values[1].replace("{","").replace("}",""));
    str_citation.append("'</b>, <i>");
    str_citation.append(values[2].replace("{","").replace("}",""));
    str_citation.append("</i>")
    if entry.entry_type == "article" or entry.entry_type == "inproceedings" or entry.entry_type == "misc":
        if values[4] != "":
            str_citation.append(", vol. {}".format(values[4]))
        if values[5] != "":
            str_citation.append(", no. {}".format(values[5]))
        if values[6] != "":
            str_citation.append(", pp. {}".format(values[6]))
    str_citation.append(", {}.".format(values[3]))
    if values[7] != "":
        str_citation.append(" doi: {}.".format(values[7]))
    if entry.entry_type == "article" or entry.entry_type == "inproceedings":
        if values[13] != "":
            str_citation.append(" <i>({})</i>".format(values[13]))
    str_citation = squash(str_citation)
    str_bibtex = strEntryMinimal(entry,"<br>","").replace("\\","\\\\")

    str = ["- citation: \"{}\"\n".format(str_citation)]
    if values[8] != "":
        str.append("  url: {}\n".format(values[8]))
    if values[9] != "":
        str.append("  abstract: \"{}\"\n".format(values[9]))
    if values[10] != "":
        str.append("  pdf: {}\n".format(values[10]))
    if values[11] != "":
        str.append("  github: {}\n".format(values[11]))
    if values[12] != "":
        str.append("  video: {}\n".format(values[12]))
    str.append("  bibtex: \"{}\"\n".format(str_bibtex))

    file.write(squash(str))
    file.write("\n\n")


    # Old attempt with names
    """
    str_auth = values[0]
    str_auth = str_auth.split(' and ')
    for name in str_auth:
        words = name.split('{');
        if words[-1][-1] == '}':
            surnames.append(words[-1][0:len(words[-1])-2])
        else:
            words = name.split(' ');
            surnames.append(words[-1]);

    str_citation = "";
    for i in range(len(surnames)):
        str_citation += surnames[i];
        if i == len(surnames) - 2:
            str_citation += " and "
        else:
            str_citation += ", "
    str_citation += "<b>'{}'</b>".format(values[1])
    if entry.entry_type == "article" || entry.entry_type == "inproceedings" || entry.entry_type == "misc":
        str_citation += ", <i>'{}'</i>, ".format(values[2])
    elif entry.entry_type == "mastersthesis":
        str_citation += ". <i>'Master's thesis. {}'</i>, ".format(values[3])

    print(squash(str_citation))

    for field in entry.fields:
        if field.key == "author":
            for i in range(len(field.value)):
                #str_auth += field.value[i].first[0][0]
                #str_auth += ". "
                if field.value[i].last[0] == "":
                    str_auth += field.value[i].first
                else:
                    str_auth += field.value[i].last
                str_auth += " "
                #str_auth += field.value[i].von
                #str_auth += field.value[i].last
                #str_auth += field.value[i].jr
                if i == len(field.value) - 2:
                    str_auth += " and "
                else:
                    str_auth += ", "

            break
    print(squash(str_auth))

    return
    """


def printHeader(file,title):
    file.write("##### Personal bibliography #####\n");
    file.write("# {} automatically parsed\n\n".format(title));

# Import bibliography
library = bibtexparser.parse_file("./bibliography.bib")

# Parsing status
if len(library.failed_blocks) > 0:
    print("Some blocks failed to parse.")
    exit(0)
else:
    print(f"Parsed all {len(library.entries)} entries successfully.")


####################### Minimal bibligraphy  #######################

# Create output files
bib = open('./parsed-minimal/bibliography.bib','w');
bib_journal = open('./parsed-minimal/bibliography-journal.bib','w');
bib_conference = open('./parsed-minimal/bibliography-conference.bib','w');
bib_preprint = open('./parsed-minimal/bibliography-preprint.bib','w');
bib_thesis = open('./parsed-minimal/bibliography-thesis.bib','w');

# Print headers
printHeader(bib,"Full minimal bibliography");
printHeader(bib_journal,"Minimal journal bibliography");
printHeader(bib_conference,"Minimal conference bibliography");
printHeader(bib_preprint,"Minimal preprint bibliography");
printHeader(bib_thesis,"Minimal thesis bibliography");

# Parse minimal bibliography
for entry in library.entries:
    printEntryMinimal(bib,entry)
    if entry.entry_type == 'article':
        printEntryMinimal(bib_journal,entry)
    elif entry.entry_type == 'inproceedings':
        printEntryMinimal(bib_conference,entry)
    elif entry.entry_type == 'misc':
        printEntryMinimal(bib_preprint,entry)
    elif entry.entry_type == 'mastersthesis':
        printEntryMinimal(bib_thesis,entry)

# Close files
bib.close()
bib_journal.close();
bib_conference.close()
bib_preprint.close()
bib_thesis.close()

####################### Website  #######################

# Crete output files
yml_journal = open('./parsed-website/publications-journal.yml','w');
yml_conference = open('./parsed-website/publications-conference.yml','w');
yml_preprint = open('./parsed-website/publications-preprint.yml','w');
yml_thesis = open('./parsed-website/publications-thesis.yml','w');

# Parse website bibliography
for entry in library.entries:
    if entry.entry_type == 'article':
        printEntryWebsite(yml_journal,entry)
    elif entry.entry_type == 'inproceedings':
        printEntryWebsite(yml_conference,entry)
    elif entry.entry_type == 'misc':
        printEntryWebsite(yml_preprint,entry)
    elif entry.entry_type == 'mastersthesis':
        printEntryWebsite(yml_thesis,entry)
