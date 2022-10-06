from tkinter import Frame, Text, Variable,Scrollbar, VERTICAL,RIGHT,  Y,LEFT,  BOTH, END
# from tkinter import Tk, StringVar
class TextExtension( Frame ):
    """Extends Frame.  Intended as a container for a Text field.  Better related data handling
    and has Y scrollbar now."""


    def __init__( self, master, textvariable = None, *args, **kwargs ):
        self.textvariable = textvariable
        if ( textvariable is not None ):
            if not ( isinstance( textvariable, Variable ) ):
                raise TypeError( "Variable type expected, {} given.".format( type( textvariable ) ) )
            self.textvariable.get = self.GetText
            self.textvariable.set = self.SetText

        # build
        self.YScrollbar = None
        self.Text = None

        super().__init__( master )

        self.YScrollbar = Scrollbar( self, orient = VERTICAL )

        self.Text = Text( self, yscrollcommand = self.YScrollbar.set, *args, **kwargs )
        self.YScrollbar.config( command = self.Text.yview )
        self.YScrollbar.pack( side = RIGHT, fill = Y )

        self.Text.pack( side = LEFT, fill = BOTH, expand = 1 )


    def Clear( self ):
        self.Text.delete( 1.0, END )


    def GetText( self ):
        text = self.Text.get( 1.0, END )
        if ( text is not None ):
            text = text.strip()
        if ( text == "" ):
            text = None
        return text


    def SetText( self, value ):
        self.Clear()
        if ( value is not None ):
            self.Text.insert( END, value.strip() )


# root = Tk()
# root.geometry("300x300+300+300")
#
# global my_txt
# my_txt = StringVar()
# app = TextExtension(root, textvariable=my_txt)
# app.pack(expand=True)
# my_txt.set("""
# Corps Members should be regarded as staff of your establishment and be given adequate job assignment and positions of responsibility
# commensurate with their qualifications, training and experience.
# 2. STATUTORY RESPONSIBILITIES OF EMPLOYERS
# 3. Provide Corps Members with a modest accommodation or at least reasonable allowance per month in lieu.
# 4. Provide transport for the corps members to and from the place of work or reasonable amount per month in lieu.
# 5. Extend medical facilities and other welfare services provided for other members of staff to corps members.
# 6. MONTHLY CLEARANCE LETTER: All Employers must issue clearance letters to only corps members who have satisfactorily performed
# their duties for the month. Corps members must submit their monthly clearance letters between 1st and 10th of every month to qualify for
# payment by the secretariat. NYSC pays Corps members monthly allowance through banks approved by NYSC.
# 7. The accepted line of communication on all issues shall be through Corps member􀂶s Employer to the Local Government Inspector to the
# State Coordinator and vice versa.
# 8. Release Corps members for Community Development Service (CDS) once a week.
# 9. Transport Corps members from Orientation Camp at the end of the orientation course to their places of primary assignment or pay an
# appropriate transportation fare to them on assumption of duty.
# 10. DISCIPLINE: Paragraph 1 above suggests that corps member shall be issued appropriate internal queries like any other staff member on
# violation of organization rules/regulations. Other cases of indiscipline which cannot be handled by our organization should be reported
# immediately to the NYSC State coordinator.
# 11. Employers are please requested to send quarterly evaluation reports on Corps members using NYSC
# """)
# root.mainloop()