#!/usr/bin/python




import csv
import pprint
pp = pprint.PrettyPrinter(indent=4)
import sys
import getopt
import re

changes = {}

import argparse
parser = argparse.ArgumentParser()

parser.add_argument ("infile", metavar="CSV", nargs="+", type=str, help="data file") 
args = parser.parse_args()

sample_names = []

SIMILARITY_CUTOFF = 95

#
# Function that investigates the similarity between two samples. 
#
#
def similar_samples( sample_name1, sample_name2):

    combined_changes = dict()


    for gene in ( changes[ sample_name1 ]):
        for change, fraction in changes[ sample_name1 ][ gene ]:
            if ( gene not in combined_changes):
                combined_changes[gene] = dict()
            if ( change not in combined_changes[gene]):
                combined_changes[gene][change] = []

            combined_changes[ gene ][ change ].append(float(fraction))

    for gene in ( changes[ sample_name2 ]):
        for change, fraction in changes[ sample_name2 ][ gene ]:
            if ( gene not in combined_changes):
                combined_changes[gene] = dict()
            if ( change not in combined_changes[gene]):
                combined_changes[gene][change] = []

            combined_changes[ gene ][ change ].append(float(fraction))



#    pp.pprint( combined_changes )

    passed_changes = 0
    failed_changes = 0

    for gene in combined_changes.keys():
        for change in combined_changes[gene].keys():
        
            if ( len(combined_changes[ gene ][change ]) == 1):
#                print "Single change"
                failed_changes +=1
                continue

            sum = 0
            count = 0
            for a in combined_changes[ gene][ change ]:
        
                sum += a
                count += 1

                mean = sum/ count
            

            for a in combined_changes[ gene ][ change ]:
                if ( mean > a + 2  or mean < a - 2):
#                    print "\t".join( [ str(mean), str(a)])
                    failed_changes += 1
                else:
                    passed_changes += 1


#    print "passed changes: %d, failed changes: %d" % ( passed_changes, failed_changes)

    similarity = passed_changes * 100 / (passed_changes + failed_changes);
    return similarity

    if ( similarity > SIMILARITY_CUTOFF):
        print " vs ".join([sample_name1, sample_name2]) + " : Similar samples"
        return 1
    else:
        print " vs ".join([sample_name1, sample_name2]) + " : Different samples"
        return 0



#    print "mean %.2f \n" % ( sum/ count)



def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


for filename in args.infile:
    

    sample_name = re.sub(r'^.*\/(.*?)[\.|_].*', r'\1', filename)
    sample_name = re.sub(r'(.*?)[\.|_].*', r'\1', filename)
    print sample_name
#    sample_name = re.search("^(.*)\_", filename).group(1)
    changes[ sample_name ] = dict()
    sample_names.append( sample_name )

    gene = ""

    for line in csv.reader( open(filename), delimiter="\t"):

#        print "Line length :: " + str(  len(line))

        if ( len(line) == 1):
#            print line
            gene = line[0]
            
            if ( gene == "Int"):
                break

            if ( gene not in changes[ sample_name ]):
                changes[ sample_name ][ gene ] = []

        for item in line[2:]:
                
            if not item.strip():
                continue

            item = item.split(":")
            item[1] = item[1].rstrip("%")
#            print "Appending :: " + gene + "  " + line[1]+item[0] + "  " + item[1]

#            changes[ sample_name ].append([line[1]+item[0],item[1]])
            changes[ sample_name ][ gene ].append([line[1]+item[0],item[1]])
            
#pp.pprint(changes)


import xlwt
book = xlwt.Workbook()
sheet = book.add_sheet('QC')

styles = dict(
    bold = 'font: bold 1',
    italic = 'font: italic 1',
    # Wrap text in the cell
    wrap_bold = 'font: bold 1; align: wrap 1;',
    # White text on a blue background
    reversed = 'pattern: pattern solid, fore_color blue; font: color white;',
    # Light orange checkered background
    light_orange_bg = 'font: 1, pattern: pattern fine_dots, fore_color white, back_color orange;',
    # Heavy borders
    bordered = 'border: top thick, right thick, bottom thick, left thick;',
    # 16 pt red text
    big_red = 'font: height 320, color red;',
)


red_bg  = xlwt.easyxf('pattern: pattern diamonds, fore_color white, back_color red;')
light_red_bg  = xlwt.easyxf('pattern: pattern fine_dots, fore_color white, back_color red;')
orange_bg  = xlwt.easyxf('pattern: pattern diamonds, fore_color white, back_color orange;')
light_orange_bg  = xlwt.easyxf('pattern: pattern fine_dots, fore_color white, back_color orange;')

#for idx, k in enumerate(sorted(styles)):
#    style = xlwt.easyxf(styles[k])
#    sheet.write(idx, 0, k)

for i in range(0, len(sample_names)):
    sheet.write(i + 1, 0, sample_names[i], )
    sheet.write(0, i + 1, sample_names[i], )

    for j in range(i, len(sample_names)):
#    for j in range(i, i+1):
        
        similarity = similar_samples( sample_names[ i ], sample_names[ j ])
        print "\t".join( [sample_names[ i ], sample_names[ j ], "%.2f" % similarity, str(i), str(j) ])


        if ( similarity > 98.00):
            sheet.write(i + 1, j + 1, "%.2f" % similarity, red_bg)
            if ( i != j):
                sheet.write(j + 1, i + 1, "%.2f" % similarity, red_bg)

        elif( similarity > 95.00):
            sheet.write(i + 1, j + 1, "%.2f" % similarity, light_red_bg)
            if ( i != j):
                sheet.write(j + 1, i + 1, "%.2f" % similarity, light_red_bg)

        elif( similarity > 90.00):
            sheet.write(i + 1, j + 1, "%.2f" % similarity, orange_bg)
            if ( i != j):
                sheet.write(j + 1, i + 1, "%.2f" % similarity, orange_bg)

        elif( similarity > 80.00):
            sheet.write(i + 1, j + 1, "%.2f" % similarity, light_orange_bg)
            if ( i != j):
                sheet.write(j + 1, i + 1, "%.2f" % similarity, light_orange_bg)

        else:
            sheet.write(i + 1, j + 1, "%.2f" % similarity)
            if ( i != j):
                sheet.write(j + 1, i + 1, "%.2f" % similarity)


book.save('crosssample_QC.xls')



exit()
