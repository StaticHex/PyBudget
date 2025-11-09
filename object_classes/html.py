from object_classes.transaction import Transaction
from data_classes.ttype import TransactionType
from settings.dformat import dateFormat
from utils.local import formatCurrencyAsString
from datetime import datetime
import          json
import          pdfkit
import          os
import          re

class HTMLWriter:
    __cssValues = {
        'R':'report',
        'W':'withdrawl',
        'D':'deposit'
    }
    def __init__(self):
        # class vars:
        self.__indent   = 0         # (Int) used for formatting HTML

        self.__stack    = []        # (List<string>) used to ensure right html
                                    # tag is closed

        self.__html     = ""

        # Create Header
        self.__write('<!DOCTYPE html>')
        self.__open_tag('html')
        self.__open_tag('head')
        self.__open_tag('style')

        # load in CSS
        f = open('./assets/styles.css','r')
        for line in [x.replace('\n','') for x in f.readlines()]:
            self.__write(line)
        self.__close_tag(2)

        # Start the body tag
        self.__open_tag('body')

    def createPDF(
        self,       # (Ref) A reference to this class, required by all members
        file_path   # (String) pdf file to write out to
    ):
        # Safety, close out any unclosed tags
        while self.__indent > 0:
            self.__close_tag()

        msize='0.5in'
        pdfkit.from_string( 
            self.__html, 
            file_path, 
            configuration=pdfkit.configuration(
                wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
            ),
            options={
                'footer-center': '[page]',
                'page-size': 'Letter',
                'margin-top': msize,
                'margin-bottom': msize,
                'margin-left': msize,
                'margin-right': msize,
            }
        )
    
    def createHTML(
        self,       # (Ref) A reference to this class, required by all members
        file_path   # (String) html file to write out to
    ):
        # Safety, close any unclosed tags
        while self.__indent > 0:
            self.__close_tag()
        f = open(file_path, 'w')
        f.write(self.__html)
        f.close()

    """
    ============================================================================
    = Open Tag Method                                                          =
    = ------------------------------------------------------------------------ =
    = description:                                                             =
    = Specifies we're opening a new HTML tag up. Creates the tag and then      =
    = auto-increments the indent                                               =
    ============================================================================
    """
    def __open_tag(
        self,           # (Ref) A reference to this class, required by all 
                        # members
        name,           # (String) Name of the tag to open
        options = {}    # (Dict) any options to add to the tag
    ):
        opts = len(options) and self.__format_options(options) or ''
        args = {
            'tab':self.__tab(),
            'name':name,
            'opts':opts and f' {opts}' or ''
        }
        self.__html += '{tab}<{name}{opts}>\n'.format(**args)
        self.__indent += 1
        self.__stack.append(name)

    def createHeader(self, startDate, endDate):
        if isinstance(startDate, datetime):
            startDate = startDate.strftime("%m/%d/%Y")
        if isinstance(endDate, datetime):
            endDate = endDate.strftime("%m/%d/%Y")
        self.__open_tag('h1',{'style':'text-align: center;'})
        self.__write(f'Budget Report {startDate} ~ {endDate}')
        self.__close_tag()

    def processTransaction(self, transaction, total):
        # Calculate the new total after applying our transaction
        newTotal = total
        if transaction.type == TransactionType.DEPOSIT:
            newTotal += transaction.amount
        elif transaction.type == TransactionType.WITHDRAWL:
            newTotal -= transaction.amount
        
        # Get type as symbol as this is used a lot of places
        ttypeVal = transaction.type.value[0]
        # Print the transaction data in the report
        tColor = HTMLWriter.__cssValues[ttypeVal]
        if transaction.recurring:
            tColor = 'scheduled'
        self.__open_tag('div',{'class':f'{tColor} pop'})
        if transaction.recurring:
            # Margin order -- margin: top right bottom left
            style = 'color:#9999cc; padding:5px 5px 0px 5px; display:inline-block;'
            self.__open_tag('i',{'style':style})
            self.__open_tag('strong')
            self.__write('Recurring')
            self.__close_tag(2)
        self.__open_tag('div',{'class':'rounded'})
        self.__open_tag('span',{'class':'percent10 divider'})
        self.__open_tag('h4',{'class':'nopad'})
        self.__write(transaction.date.strftime(dateFormat))
        self.__close_tag(2)
        self.__open_tag('span',{'class':'percent10 divider'})
        self.__open_tag('h4',{'class':'nopad','style':'text-align:center;'})
        self.__write(ttypeVal)
        self.__close_tag(2)
        self.__open_tag('span',{'class':'percent70 divider'})
        self.__open_tag('h4',{'class':'nopad','style':'padding-left:10px;'})
        self.__write(transaction.name)
        self.__close_tag(2)
        opts = {
            'style':'display: inline-block; width:11%; text-align: right;'
        }
        if transaction.amount < 0:
            opts['class'] = 'red'
        self.__open_tag('span',opts)
        self.__open_tag('h4',{'class':'nopad'})
        self.__write(formatCurrencyAsString(transaction.amount))
        self.__close_tag(3)
        if transaction.type != TransactionType.REPORT:
            rClass = transaction.recurring and 'S' or ttypeVal
            self.__open_tag('div',{'class':f'total-bar-{rClass}'})
            self.__open_tag('span',{'class':'percent50'})
            self.__open_tag('strong',{'class':'nopad'})
            self.__write('Total:')
            self.__close_tag(2)
            self.__open_tag(
                'span',
                {
                    'class':'percent50',
                    'style':'text-align: right;'
                }
            )
            self.__open_tag(
                'strong',
                {
                    'class':newTotal < 0 and 'nopad red' or 'nopad'
                }
            )
            self.__write(formatCurrencyAsString(newTotal))
            self.__close_tag(3)
        self.__close_tag()
        return newTotal

    """
    ============================================================================
    = Close Tag Method                                                         =
    = ------------------------------------------------------------------------ =
    = description:                                                             =
    = Specifies we're closing an HTML tag. Creates the tag and then auto       =
    = decrements the indent                                                    =
    ============================================================================
    """
    def __close_tag(
        self,   # (Ref) A reference to this class, required by all members 
        num=1   # (Int) The number of tags to close (default is 1)
    ):
        for _ in range(0, num):
            name = self.__stack.pop()
            self.__indent -= 1
            tag = self.__tab()+'</'+name+'>\n'
            self.__html += tag

    """
    ============================================================================
    = Write Method                                                             =
    = ------------------------------------------------------------------------ =
    = description:                                                             =
    = Writes out text or HTML to the body of a tag without changing the indent =     
    ============================================================================
    """    
    def __write(
        self,   # (Ref) A reference to this class, required by all members
        text    # (String) Text to write out to the body of the tag
    ):
        self.__html += self.__tab()+text+'\n'

    """
    ============================================================================
    = Open Tag Method                                                          =
    = ------------------------------------------------------------------------ =
    = description:                                                             =
    = Calculates the number of spaces to add to the beginning of an HTML tag   =
    = based on the current indent level                                        =
    = ------------------------------------------------------------------------ =
    = returns:                                                                 =
    = (String) A string of whitespace to pad the beginning of a line with      =
    ============================================================================
    """
    def __tab(
        self    # (Ref) A reference to this class, required by all members
    ):
        return ' '*4*self.__indent

    """
    ============================================================================
    = Format Options Method                                                    =
    = ------------------------------------------------------------------------ =
    = description:                                                             =
    = Takes in a dict of options for a tag and strings them together into the  =
    = proper format.                                                           =
    = ------------------------------------------------------------------------ =
    = returns:                                                                 =
    = (String) A string consisting of all the options for a tag                =   
    ============================================================================
    """     
    def __format_options(
        self,   # (Ref) A reference to this class, required by all members
        options # (Dict) Options to concatenate into a string
    ):
        # Lambda function which adds quotes to option if it's a string and
        # converts the option to a string otherwise.
        f = lambda x: '"'+x+'"' if isinstance(x, str) else str(x)
        return ' '.join([k+"="+f(options[k]) for k in options])