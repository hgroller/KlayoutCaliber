##########################
#Caliber to Klayout Deck Conversion
#Expermiental  Testing
#Tracy Groller 1/29/21
#Beta 1.0
##########################

import sys
import re
import pya
import gc
gc.collect()

#----------------------------------------------------------------
#Print Functions  - several flavors:
#----------------------------------------------------------------
def print_arr(list):
    #Print as Array
    print(*list, sep = "\n")

def print_nob(list):
    #print without Brackets
    for x in list:
      print(*x) 
#----------------------------------------------------------------
#Replace Match with Old /New
#----------------------------------------------------------------
def replace_it(old,new,l):
    nl = ([list(map(lambda x: x if x != old else new, i)) for i in l])
    print_nob(nl)
#----------------------------------------------------------------
#File Read Calibre Deck find match
#----------------------------------------------------------------
def file_read(fn,match):
    my_list = []
    fileName = fn
    if fileName:
        print(fileName)
        with open(fileName, 'r') as reader:
            try:
                 found = lines_that_contain(match, reader)
                 for x in found:
                     x = x.rstrip('\n')
                     x = x.replace('"', '')
                     #------Create List of List to parse
                     y = x.split()
                     #print(y)
                     my_list.append(y)
            finally:
                reader.close()
                return my_list
#----------------------------------------------------------------
#Search List of List for Match
#----------------------------------------------------------------
def find(value,lst):
    #match Search
    matching = [s for s in lst if value in s]
    #for x in matching:
      #print(*x)
    return matching
   # print(*matching, sep = "\n")
#----------------------------------------------------------------
#Build lists of matched lines - several flavors:
#----------------------------------------------------------------
def lines_that_equal(line_to_match, fp):
      return [line for line in fp if line == line_to_match]

def lines_that_contain(string, fp):
      return [line for line in fp if string in line]

def lines_that_start_with(string, fp):
      return [line for line in fp if line.startswith(string)]

def lines_that_end_with(string, fp):
      return [line for line in fp if line.endswith(string)]
#----------------------------------------------------------------
#Build Klayout Enclosure from match
#----------------------------------------------------------------
#{"act XCUT surrounds act NEM" { @ < 2 Microns
   #ENCLOSURE  "act NEM"  "act XCUT" < 2 ABUT >= 0 < 90 SINGULAR
   #Result1 =  CUT "act NEM" "act XCUT"
#}
def build_enc(list):
  print("Translation from Caliber")
  for x in list:
    #print(x[0],x[2],x[4],x[6]) 
    print(x[4] + '_ENC =  {}.enclosing({}, {})'.format(x[4], x[2], x[6]))
    form = x[4] + "_ENC.output(" '"' + x[4] +  " Surrounds " + x[2] + " < #{'%.12g' % cut} µm\")"
    print(form)
#----------------------------------------------------------------
# StartGUI
#----------------------------------------------------------------
class GuiDialog(pya.QDialog):
  view = pya.Application.instance().main_window().current_view()
  def __init__(self, parent = None):
    """ Dialog constructor """
    super(GuiDialog, self).__init__()
 # text input    
    element =  QInputDialog.getText(self, 'FindMatch', 'Enter text', QLineEdit.Normal, "")                                                                                                                          
#-----------------------------------------------------------------
#Process Deck
#-----------------------------------------------------------------
    fileName = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
    #element = 'ENCLOSURE'
    #new = 'enclosing'
    list = file_read(fileName,element)
    print("Caliber Read")
    print_nob(list)
    #replace_it(old,new,list)
    nlist = find(element, list)
    build_enc(nlist)
    gc.collect()
#-----------------------------------------------------------------
#End Process Deck
#---------------------- -Display Dialog ------------------------
dialog = GuiDialog(pya.Application.instance().main_window())  
#-----------------------------------------------------------------
#Below Code is Experminetal to translate Calibre to Klayout
#{"act XCUT surrounds act NEM" { @ < 2 Microns
   #ENCLOSURE  "act NEM"  "act XCUT" < 2 ABUT >= 0 < 90 SINGULAR
   #Result1 =  CUT "act NEM" "act XCUT"
#}
#Refrence met_encl = metal2.enclosing(metal1, min_cut)
#Refrence met_encl.output("Metal2 surrounds Metal1 < #{'%.12g' % cut} µm")
#print(f"Match Found: {y[0]},  {y[2]},   {y[4]},   {y[6]}")
#print("Translating Caliber to KLayout")
#Rule
#print('met_end =  {}.enclosing({}, {})'.format(y[2], y[4], y[6]))
#Marker
#form = "met_end.output(" '"' + y[2] +  " Surrounds " + y[4] + " < #{'%.12g' % cut} µm\")"
#print(form)

                   
