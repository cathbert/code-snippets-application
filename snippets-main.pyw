# import libraries
import tkinter as tk
from tkinter import ttk, colorchooser
from tkinter import messagebox, filedialog
from datetime import datetime
from database import Database
from tkcalendar import Calendar, DateEntry
import os
import random
#from fontTools.ttLib import TTFont
from tkinter import Menu
from ttkthemes import ThemedTk, THEMES
import pyglet

from dictionary_database import search_all_matching, search_word, get_all_words
from tkinter import IntVar

# ----- Create base folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db = Database()


pyglet.font.add_file('fonts/Base 02.ttf')
pyglet.font.add_file('fonts/Blacksword.otf')
pyglet.font.add_file('fonts/Lcd.ttf')
pyglet.font.add_file('fonts/europa_.TTF')
pyglet.font.add_file('fonts/SF Espresso Shack Bold Italic.ttf')

pyglet.font.load('Digital-7 Mono')
blacksword = pyglet.font.load('Blacksword')


THEME_COLOR = '#004D54'
TITLE_FONT = ("Century Gothic", 22)
TEXT_ENTRY_FONT = ("Century Gothic", 11)

# Main window for the application
class Application(ThemedTk):
    def __init__(self, *args, **kwargs):
        ThemedTk.__init__(self, *args, **kwargs, fonts=True, themebg=True)  # initialize the inherited tkinter library
        theme_color = '#004D54'  # Set theme color
        self.set_theme("arc")

        # ------------------------------------MAIN WINDOW CUSTOMIZATION-------------------------------------------------
        self.title('Ephitome Snippets Pro')  # Window title
        self.geometry('830x570+200+50')  # Window size in width and height then position on the screen
        self.iconbitmap("icons/ephitome.ico")  # Window icon
        self.minsize(830, 570)  # Window minimum size
        self.config(bg=THEME_COLOR)  # Configure window background color
        # self.overrideredirect(True)

        # -------------------------------------------MENU SECTION-------------------------------------------------------
        my_menu = Menu(self, background=THEME_COLOR, borderwidth=2, relief=tk.GROOVE)  # Initialize
        self.config(menu=my_menu)

        # Create a menu item
        file_menu = Menu(my_menu, tearoff=False, background=THEME_COLOR, fg="#ffff00")
        my_menu.add_cascade(label="File", menu=file_menu, background=THEME_COLOR,)
        file_menu.add_command(label="New...")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        # Create an edit menu item
        edit_menu = Menu(my_menu, tearoff=False, background=THEME_COLOR, fg="#ffff00")
        my_menu.add_cascade(label="Pages", menu=edit_menu)
        edit_menu.add_command(label="Contacts")
        edit_menu.add_command(label="Dictionary")
        edit_menu.add_command(label="Snippets")
        edit_menu.add_command(label="Comprehensive Notes")

        # Create an Options menu item
        option_menu = Menu(my_menu, tearoff=False, background=THEME_COLOR, fg="#ffff00")
        my_menu.add_cascade(label="About GoofyCoder Utility Application", menu=option_menu)
        option_menu.add_command(label="Info")
        option_menu.add_command(label="GoofyCoder Info")

        # ----- LOAD ALL IMAGES
        main_logo_img = tk.PhotoImage(file="icons/ephitome.png")
        python_icon_img = tk.PhotoImage(file="images/py_icon.png")
        utilities_icon = tk.PhotoImage(file="icons/compose.png")
        ephitome_icon = tk.PhotoImage(file="icons/ephitome.png")
        #ephitome_icon_north = tk.PhotoImage(file="icons/1.png")
        ephitome_icon_west = tk.PhotoImage(file="icons/2.png")
        ephitome_icon_south = tk.PhotoImage(file="icons/3.png")
        ephitome_icon_east = tk.PhotoImage(file="icons/4.png")
        ephitome_icon_north1 = tk.PhotoImage(file="icons/5.png")
        ephitome_icon_west1 = tk.PhotoImage(file="icons/6.png")
        ephitome_icon_south1 = tk.PhotoImage(file="icons/7.png")
        ephitome_icon_east1 = tk.PhotoImage(file="icons/8.png")
        origaart_icon = tk.PhotoImage(file="icons/origaart_icon.png")
        encyclopedia_icon = tk.PhotoImage(file="icons/britannica_logo.png")
        # -------------------------------------------TIME AND LOGOS SECTION---------------------------------------------
        time_and_logo = tk.Frame(self, bg=THEME_COLOR)  # Create the frame to hold the digital time and top buttons
        time_and_logo.pack(fill=tk.X, padx=5, pady=5)

        # -----This is button serve as a link to the main page and logo for goofycoder
        ephitome_main_button = tk.Button(time_and_logo, image=ephitome_icon, activebackground=THEME_COLOR, bg=THEME_COLOR, relief='flat', bd=0,
                                      text='', fg='#00ff00', font=TITLE_FONT , compound='center',command=lambda: self.show_frame(SnippetsPage))
        ephitome_main_button.image = ephitome_icon
        ephitome_main_button.pack(side='left')

        # -----Bind button to change color when mouse hover on it
        #ephitome_main_button.bind('<Enter>', lambda e: ephitome_main_button.config(bg="#DDD7A6"))
        #ephitome_main_button.bind('<Leave>', lambda e: ephitome_main_button.config(bg=THEME_COLOR))

        # -----Function to iterate through time and configure the time display label
        def clock_it(label):
            def clock():
                label.config(text=f"{datetime.now().time().strftime('%H:%M:%S')}")
                label.after(1000, clock)

            clock()

        # -----This is the label to display time
        time_display_label = tk.Label(time_and_logo, text='This is time', font=('Digital-7 Mono', 20, 'bold'), fg="#ffff00",
                                      bg=THEME_COLOR)
        time_display_label.pack(side=tk.LEFT)

        clock_it(time_display_label)  # Now use clock it function to display time to the window

        # -----Frame to hold the python logo
        python_icon_frame = tk.Frame(time_and_logo, bg=THEME_COLOR)
        python_icon_frame.pack(side=tk.RIGHT, padx=4, fill=tk.X)

        # ----- STANDARD BAR BUTTONS
        dictionary_btn_img = tk.PhotoImage(file="icons/read.png")
        diary_btn_img = tk.PhotoImage(file="icons/library.png")

        utilities_button = tk.Button(time_and_logo, text='Utilities', compound=tk.TOP, fg='white', image=utilities_icon, bg=THEME_COLOR, relief='flat', bd=0, 
                                               activebackground=THEME_COLOR, command=lambda: self.show_frame(UtilitiesPage))
        utilities_button.image = utilities_icon
        utilities_button.pack(side=tk.LEFT)

        dictionary_button = tk.Button(time_and_logo, text='Dictionary', compound=tk.TOP, fg='white', bd=0, image=dictionary_btn_img, bg=THEME_COLOR, relief='flat', 
                                               activebackground=THEME_COLOR, command=lambda: self.show_frame(Dictionary))
        dictionary_button.image = dictionary_btn_img
        dictionary_button.pack(side=tk.LEFT)

        diary_button = tk.Button(time_and_logo, text='Diary', compound=tk.TOP, fg='white', image=diary_btn_img, bd=0, bg=THEME_COLOR, relief='flat', 
                                               activebackground=THEME_COLOR, command=lambda:self.show_frame(MyDiary))
        diary_button.image = diary_btn_img
        diary_button.pack(side=tk.LEFT)

        origaart_button = tk.Button(time_and_logo, text='Origaart', compound=tk.TOP, fg='white', image=origaart_icon, bd=0, bg=THEME_COLOR, relief='flat', 
                                               activebackground=THEME_COLOR, command=lambda:self.show_frame(Authentication))
        origaart_button.image = origaart_icon
        origaart_button.pack(side=tk.LEFT)

        encyclopedia_button = tk.Button(time_and_logo, text='Britannica', compound=tk.TOP, fg='white', image=encyclopedia_icon, bd=0, bg=THEME_COLOR, relief='flat', 
                                               activebackground=THEME_COLOR, command=lambda:self.show_frame(BritannicaEncyclopedia))
        encyclopedia_button.image = encyclopedia_icon
        encyclopedia_button.pack(side=tk.LEFT)
        
        def shift():
            x1,y1,x2,y2 = canvas.bbox("marquee")
            if(x2<0 or y1<0): #reset the coordinates
                x1 = canvas.winfo_width()
                y1 = canvas.winfo_height()//2
                canvas.coords("marquee",x1,y1)  
            else:
                canvas.move("marquee", -2, 0)
            canvas.after(1000//fps,shift)

        canvas = tk.Canvas(time_and_logo, bg = THEME_COLOR)
        canvas.pack(fill=tk.X, expand=1, side = tk.LEFT)
        text_var=db.get_all_quotes()[10000]
        canvas.create_text(0,-2000,text=f'{text_var[0]}:{text_var[1]} -{text_var[2]} -{text_var[3]}',font=("Century Gothic", 13),fill='#ffff00',tags=("marquee",),anchor='w')
        x1,y1,x2,y2 = canvas.bbox("marquee")
        width = x2-x1
        height = y2-y1
        canvas['width']=width
        canvas['height']=height
        fps=40    #Change the fps to make the animation faster/slower
        shift()

        # -----This frame will hold the current user logo and name
        watchdog_frame = tk.Frame(python_icon_frame, bg=THEME_COLOR)
        watchdog_frame.pack(side=tk.LEFT, padx=1)

        # -----Python logo label
        python_icon = tk.Button(python_icon_frame, relief=tk.FLAT, bd=0, image=python_icon_img, 
                                                   bg=THEME_COLOR, command=self.destroy,
                                                   activebackground=THEME_COLOR)
        python_icon.image = python_icon_img
        python_icon.pack(side=tk.RIGHT)

       
        icons_list = [
            ephitome_icon_west, ephitome_icon_south, ephitome_icon_east,
            ephitome_icon_north1, ephitome_icon_west1, ephitome_icon_south1, ephitome_icon_east1
        ]
        def watch_dog_live(lb):
            def watch_dog():
                num = random.choice([0,1,2,3,5,6,])
                lb.config(image=icons_list[num])
                lb.after(100, watch_dog)
            watch_dog()


        # -----Current user button with icon
        watchdog_icon = tk.Label(watchdog_frame, image=ephitome_icon_west, text="WatchDog", 
                                                 compound=tk.CENTER, anchor=tk.W, 
                                                 bg=THEME_COLOR, relief='flat', bd=0,
                                                 activebackground="#CCBF99",
                                                 font=("Century Gothic", 8, 'bold'))
        watchdog_icon.image = ephitome_icon_west
        watchdog_icon.pack()

        watch_dog_live(watchdog_icon)

        watchdog_icon.bind("<Enter>", lambda e: watchdog_icon.config())

        # ---------------------------------------ALL PROGRAM PAGES SECTION----------------------------------------------
        container = tk.Frame(self)  # Create main frame
        container.pack(side='top', fill='both', expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # -----This dictionary will contain all pages
        self.frames = {}

        # -----Loop through all pages available then get the selected
        for page in (SnippetsPage, Dictionary, UtilitiesPage, MyDiary, OrigaartPage, Authentication, BritannicaEncyclopedia,):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky='news')

        # -----Now show the main page on initialization
        self.show_frame(SnippetsPage)

    # -----This method solely render pages
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Main page for the application, the first to be rendered
class SnippetsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        style = ttk.Style()

        def cut_text():
            copy_text()
            delete_text()

        def copy_text():
            selection = snippets_display_screen.tag_ranges(tk.SEL)
            if selection:
                self.clipboard_clear()
                self.clipboard_append(snippets_display_screen.get(*selection))

        def paste_text():
            snippets_display_screen.insert(tk.INSERT, self.clipboard_get())

        def paste_image():
            global img
            try:
                img = tk.PhotoImage(file=self.clipboard_get())
                position = snippets_display_screen.index(tk.INSERT)
                snippets_display_screen.image_create(position, image=img)
            except tk.TclError:
                pass

        def delete_text():
            selection = snippets_display_screen.tag_ranges(tk.SEL)
            if selection:
                snippets_display_screen.delete(*selection)

        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="GoofyCoder.com")
        menu.add_command(label="Cut", command=cut_text)

        menu.add_command(label="Copy text", command=copy_text)
        menu.add_command(label="Paste text", command=paste_text)
        menu.add_command(label="Paste image", command=paste_image)
        menu.add_command(label="Delete", command=delete_text)

        def show_popup(event):
            menu.post(event.x_root, event.y_root)

        # ----- Theme color for the window
        theme_color = '#004D54'

        # ----- set the theme
        self.config(bg=theme_color)

        # ----- this function serves to get the file from path and name of the file
        def new_file():
            # ----- this statement with get the file path
            file = filedialog.askopenfilename()
            if len(file) == 0:
                pass
            # ----- check if file has the required extension
            else:
                if file.endswith('.py'):
                    # ----- this function declaration will clear the text area, entry area and id area
                    clear_fields()
                    # ----- now open the file in read mode
                    with open(file, 'r') as f:
                        try:
                            # ----- Split file absolute path to get the name of the file
                            title = os.path.split(file)[1].split('.')[0]
                            # ----- Insert file name into search entry
                            search.insert(0, title)
                            # ----- Read the file using the file handle
                            code = f.read()
                            # ----- Insert the contents of the file into the text area
                            snippets_display_screen.insert(tk.END, code)
                            # ----- Finally return turple with filename and contents, in this case, code
                            return title, code
                        except UnicodeDecodeError:
                            messagebox.showerror("File error", "File Error, system cant decode file!")
                else:
                    messagebox.showerror("None type", "You are trying to load a file that does not have .py extension!")
        # ----- This function will fill the search and screen area when invoked
        def fill_out(_=None):
            # ----- this function declaration will clear the text area, entry area and id area
            clear_fields()
            # ----- Add clicked list item to entry box
            search.insert(0, snippets_list.get("anchor"))
            # ----- Search snippet in database using the title pulled from the listbox, in this case snippets list
            snippet = db.search_snippet(snippets_list.get("anchor"))
            # ----- Get snippet id from the data pulled from the database snippet entry
            iid = snippet[0]
            # ----- Get snippet code from the data pulled from the database snippet entry
            title = snippet[1]
            code = snippet[2]

            # ----- Insert the code data into text area to display it
            snippets_display_screen.insert(tk.END, "\n")
            snippets_display_screen.insert(tk.END, code)

            # ----- Display snippet id in the entry area in this case, snippet id area
            snippet_id.insert(0, iid)

        # ----- This function is used to save the contents of the file selected to database
        def save_snippet():
            # ----- Get the snippet name from search entry, the text displayed
            title = search.get()

            # ----- Get all the text displayed the text area, in this case, the screen
            code = snippets_display_screen.get('0.1', tk.END)

            # ----- This statement will write data the database and and return a status message
            database_insert_status = db.insert_snippet(title, code)

            # ----- Now check that status message to see if its a "success, empty, failure or exists" message
            if database_insert_status == "success":

                # ----- With success, insert code or file contents to screen
                snippets_display_screen.insert(tk.END, code)

                # ----- this function declaration will clear the text area, entry area and id area
                clear_fields()

                # ----- Show a success message to user
                messagebox.showinfo("Success", "Database update successful!")

                # Finally update the snippets list with new database contents, adding the new snippet to snippets list
                update(db.get_all_snippets())
                snippets_count_label.config(text=f'Snippets avail: {len(db.get_all_snippets())}')

            # ----- The following statements will serve to warn and alert the user
            elif database_insert_status == "not user":
                messagebox.showerror("Failed", "You are not a user!")
            elif database_insert_status == "empty":
                messagebox.showerror("Empty fields", "Database update unsuccessfully, you are trying to save nothing!")
            elif database_insert_status == "exists":
                messagebox.showwarning("Alert", "Snippet already in database!")
                snippets_display_screen.insert(tk.END, code)

        # -----This function sorely check whats being typed in the search area and compare with database contents to get
        # the matching items
        def check(_):
            # ----- Grab what is typed in the search entry in real time
            typed = search.get()

            # ----- If typed, in this case the search area empty, fill out the snippets list
            if typed == "":
                data = db.get_all_snippets()

            # ----- Now iterate all the snippets name in database and compare with whats being typed and update data
            else:
                data = []
                for item in db.get_all_snippets():
                    if typed.lower() in item.lower():
                        data.append(item)

            # ----- Finally update the snippets list
            update(data, db.fetch_recents())

        # ----- This function sorely get data and update the snippets list
        def update(snippets, recents):

            # ----- First delete the snippets list
            snippets_list.delete(0, tk.END)
           
            # ----- Now iterate and insert snippets into the list
            for snippet in snippets:
                snippets_list.insert(tk.END, snippet)
            

        # ----- Search the database for only a single snippet
        def search_snippet(_=None):
            try:
                # ----- Get whatever name displayed in the search area
                title = search.get()
                db.add_to_recent(title)

                # ----- Search database for the required snippet using the name/title
                snippet = db.search_snippet(title)

                # ----- Slice the snippet turple to get item on index 0, which is the snippet id
                sid = snippet[0]

                # ----- Slice the snippet turple to get item on index 1, which is the snippet code or contents
                code = snippet[1]

                # ----- this function declaration will clear the text area, entry area and id area
                clear_fields()

                # ----- Now insert the code/contents of the snippet into the screen
                snippets_display_screen.insert(tk.END, code)

                # ----- Update the snippet id area to display the currently displayed snippet
                snippet_id.insert(0, sid)

                # Finally update the snippets list with new database contents, adding the new snippet to snippets list
                update(db.get_all_snippets(), db.fetch_recents())

            except TypeError:
                messagebox.showerror("None type", "You are trying to search for an empty field!")

        # ----- Delete selected snippet
        def delete_snippet():
            # ----- Get selected snippet from the snippets list
            title = snippets_list.get("anchor")

            # ----- Check if there is something in variable title
            if len(title) < 1:
                messagebox.showerror("Error", "No title selected, Please select Snippet to delete!")
            else:
                # ----- A popup box will ask for the user's confirmation to delete
                ask = messagebox.askyesno("Alert", "Do you wish to proceed deleting this Snippet?")

                # ----- If yes then delete
                if ask:

                    # ----- Delete from database and return a deletion status
                    deletion_status = db.delete_snippet(title)

                    # ----- If deletion status is success
                    if deletion_status == 'success':

                        # ----- this function declaration will clear the text area, entry area and id area
                        clear_fields()

                        # Finally update the snippets list with new database contents, adding the new snippet to
                        # snippets list
                        update(db.get_all_snippets(), db.fetch_recents())
                        snippets_count_label.config(
                            text=f"Snippets avail: {len(db.get_all_snippets())}")

                        # ----- Show success popup
                        messagebox.showinfo("Success", "Snippet delete successful!")
                    else:
                        # ----- Else Show warning
                        messagebox.showwarning("Failure", "Snippet delete unsuccessful!")

        # ----- Update a single snippet
        def update_db():

            # ----- Get whatever is in the search area
            title = search.get()

            # ----- Get whatever is in the text area
            code = snippets_display_screen.get('0.1', tk.END)

            # ----- Call database method and update changes made in title and code and return update status
            update_status = db.update_snippet(snippet_id.get(), title, code)

            # ----- Check status message if its true then proceed to update the snippets list
            if update_status:
                update(db.get_all_snippets(), db.fetch_recents())
                messagebox.showinfo("Success", "Snippet update successful!")
            else:
                messagebox.showwarning("Failure", "Snippet update unsuccessful!")

        # ----- Run code/snippet in the textarea/screen
        def run():

            # ----- Grab code in the textarea/screen
            code = snippets_display_screen.get('0.1', tk.END)

            # ----- Check if there is something in the textarea/screen
            if len(code) > 1:

                # ----- Open a file with a .py extension and write mode
                with open("test_code.py", 'w') as f:

                    # ----- Write code/text from the textarea/screen to the .py file
                    f.write(code)

                # ----- Now use os module to execute the file
                os.startfile("test_code.py")

            else:
                messagebox.showwarning("Failure", "Select snippet to run!")

        # ----- Clear all fields in the window
        def clear_fields():
            search.delete(0, tk.END)
            snippets_display_screen.delete('0.1', tk.END)
            snippet_id.delete(0, tk.END)

        # ----- Load images for the buttons
        cloud_btn_img = tk.PhotoImage(file="icons/safe.png")
        update_snpt_btn_img = tk.PhotoImage(file="icons/compose.png")
        cloud_delete_btn_img = tk.PhotoImage(file="icons/delete.png")
        run_snpt_btn_img = tk.PhotoImage(file="icons/play.png")
        clear_snpt_btn_img = tk.PhotoImage(file="icons/broom.png")

        # ----- search area frame
        search_frame = tk.Frame(self, bg=theme_color, relief=tk.SUNKEN, bd=1)
        search_frame.pack(fill=tk.X, padx=5)

        # ----- Delete snippet button
        delete_snippet_button = tk.Button(search_frame, text='DELETE', fg='#00ff00', activebackground=theme_color, compound=tk.TOP, image=cloud_delete_btn_img, bg=theme_color, bd=0,
                                          command=delete_snippet)
        delete_snippet_button.image = cloud_delete_btn_img
        delete_snippet_button.pack(side='left')

        # ----- Save snippet button
        save_snippet_button = tk.Button(search_frame, text='SAVE', fg='#00ff00', activebackground=theme_color, compound=tk.TOP, image=cloud_btn_img, bg=theme_color, bd=0, command=save_snippet)
        save_snippet_button.image = cloud_btn_img
        save_snippet_button.pack(side='left', padx=10)

        # ----- Update snippet button
        update_snippet_button = tk.Button(search_frame, text='UPDATE', fg='#00ff00', activebackground=theme_color, compound=tk.TOP, image=update_snpt_btn_img, bg=theme_color, bd=0,
                                          command=update_db)
        update_snippet_button.image = update_snpt_btn_img
        update_snippet_button.pack(side='left')

        # ----- Run snippet button
        run_code_button = tk.Button(search_frame, text='RUN', fg='#00ff00', activebackground=theme_color, compound=tk.TOP, image=run_snpt_btn_img, bd=0, bg=theme_color,
                                    command=run)
        run_code_button.image = run_snpt_btn_img
        run_code_button.pack(side='left')

        # ----- Clear snippet button
        clear_code_button = tk.Button(search_frame, text='CLEAR', fg='#00ff00', activebackground=theme_color, compound=tk.TOP, image=clear_snpt_btn_img, bd=0, bg=theme_color,
                                      command=clear_fields)
        clear_code_button.image = clear_snpt_btn_img
        clear_code_button.pack(side='left')

        # ----- Search area entry box
        style.layout("my.TEntry",
                   [('Entry.plain.field', {'children': [(
                       'Entry.background', {'children': [(
                           'Entry.padding', {'children': [(
                               'Entry.textarea', {'sticky': 'nswe'})],
                                    'sticky': 'nswe'})], 'sticky': 'nswe'})],
                                        'border':'2', 'sticky': 'nswe'})])
        style.configure('my.TEntry', fg='#483d8b', insertbackground='#115F54', fieldbackground='#115F54', bd=0, relief=tk.FLAT, icursor=5)
        search = ttk.Entry(search_frame, font=("Century Gothic", 12) , style='my.TEntry', foreground='#00ff00')
        search.pack(expand=True, side='left', padx=5, fill=tk.X)
        search.focus_set()

        # ----- Clear snippet button
        search.bind('<Return>', search_snippet)
        search_btn_img = tk.PhotoImage(file="icons/import.png")

        # ----- Search snippet button
        search_snippet_button = tk.Button(search_frame, bg=theme_color, activebackground=theme_color, bd=0, command=search_snippet)
        search_snippet_button.image = search_btn_img
        search_snippet_button.pack(side='left')

        # ----- Bind the search button
        search.bind("<KeyRelease>", check)

        # ----- Get new snippet button
        get_new_snippet_button = tk.Button(search_frame, activebackground=theme_color, image=search_btn_img, bg=theme_color, bd=0, command=new_file)
        get_new_snippet_button.image = search_btn_img
        get_new_snippet_button.pack(side='left')

        # ----- All buttons bindings -----
        '''
        delete_snippet_button.bind("<Enter>", lambda x: main_label.config(text="delete snippet"))
        delete_snippet_button.bind("<Leave>", lambda x: main_label.config(text="Snippets"))

        save_snippet_button.bind("<Enter>", lambda x: main_label.config(text="save snippet"))
        save_snippet_button.bind("<Leave>", lambda x: main_label.config(text="Snippets"))

        search_snippet_button.bind("<Enter>", lambda x: main_label.config(text="search snippet"))
        search_snippet_button.bind("<Leave>", lambda x: main_label.config(text="Snippets"))

        update_snippet_button.bind("<Enter>", lambda x: main_label.config(text="update snippet"))
        update_snippet_button.bind("<Leave>", lambda x: main_label.config(text="Snippets"))

        get_new_snippet_button.bind("<Enter>", lambda x: main_label.config(text="get new snippet from file"))
        get_new_snippet_button.bind("<Leave>", lambda x: main_label.config(text="Snippets"))

        run_code_button.bind("<Enter>", lambda x: main_label.config(text="test run snippet"))
        run_code_button.bind("<Leave>", lambda x: main_label.config(text="Snippets"))

        clear_code_button.bind("<Enter>", lambda x: main_label.config(text="clear everything in text area"))
        clear_code_button.bind("<Leave>", lambda x: main_label.config(text="Snippets"))
        '''
        # ----- Snippet id area label -----
        snippet_id_frame = tk.Frame(search_frame, bg=THEME_COLOR)
        snippet_id_frame.pack(side='right', anchor=tk.E)
        snippet_id_label = tk.Label(snippet_id_frame, text="Snippet ID: ", fg='#00ff00', bg=theme_color,
                                    font=("Century Gothic", 12))
        snippet_id_label.pack(side='left')

        # ----- Snippet id area entry -----
        snippet_id = tk.Entry(snippet_id_frame, relief="flat", bg=theme_color, font=("Century Gothic", 12),
                              fg='#00ff00')
        snippet_id.pack(side='left')

        # ----- Main frame to hold listbox and textbox
        main_frame = tk.Frame(self, bg=theme_color, padx=5, pady=8)
        main_frame.pack(fill='both', expand=True)
        
        snippets_list_and_recents_frame = tk.Frame(main_frame, bg=theme_color)
        snippets_list_and_recents_frame.pack(side='left', fill=tk.Y)

        # ----- Snippets count label
        snippets_count_label = tk.Label(snippets_list_and_recents_frame, text=f'Snippets avail: {len(db.get_all_snippets())}',
                                        bg=theme_color, fg='#00ff00', font=("Century Gothic", 9, 'bold'))
        snippets_count_label.pack(side='top') 

        all_snippets_frame = tk.Frame(snippets_list_and_recents_frame, bg=theme_color)
        all_snippets_frame.pack(fill=tk.Y, expand=True)

        # ---- Create scrollbar for the listbox

        style.layout("TScrollbar",
        [('My.Horizontal.Scrollbar.trough', {'children':
            [('Horizontal.Scrollbar.leftarrow', {'side': 'left', 'sticky': ''}),
             ('Horizontal.Scrollbar.rightarrow', {'side': 'right', 'sticky': ''}),
             ('Horizontal.Scrollbar.thumb', {'unit': '1', 'children':
                 [('Horizontal.Scrollbar.grip', {'sticky': ''})],
            'sticky': 'nswe'})],
        'sticky': 'we'})])

        style.configure("TScrollbar", gripcount=0,
                background=theme_color, darkcolor="DarkGreen", lightcolor="LightGreen",
                troughcolor="gray", bordercolor="blue", arrowcolor="white")
        
        snippets_list_scrollbar = ttk.Scrollbar(all_snippets_frame)
        snippets_list_scrollbar['style'] = "TScrollbar"

        

        # ----- Listbox to display all snippets
        snippets_list = tk.Listbox(all_snippets_frame, width=40, bg=theme_color, fg="yellow",
                                   yscrollcommand=snippets_list_scrollbar.set, font=("Century Gothic", 10), selectmode=tk.BROWSE, selectforeground='black', selectbackground='#00ff00', activestyle=None,  selectborderwidth=1)
        snippets_list.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        

        # ----- Update the snippets list with database contents
        update(db.get_all_snippets(), db.fetch_recents())

        # ----- Snippets list bindings
        snippets_list.bind("<<ListboxSelect>>", fill_out)
        snippets_list.bind('<Return>', search_snippet)
        
        # ----- Snippets list scrollbar
        snippets_list_scrollbar.pack(side='left', fill='y', expand=True)
        snippets_list_scrollbar.config(command=snippets_list.yview)

        # ----- Create scrollbar for the text area
        display_scrollbar_x = ttk.Scrollbar(main_frame, orient='horizontal', style='TScrollbar')
        display_scrollbar_y = ttk.Scrollbar(main_frame, style='TScrollbar')

        # ----- Pack scrollbars to window
        # display_scrollbar_x.pack(side='bottom', fill='x')
        display_scrollbar_y.pack(side='right', fill='y')

        # ----- Main screen to view snippet contents
        snippets_display_screen = tk.Text(main_frame, height=40, width=250, bg=theme_color, wrap='word',
                                          selectbackground="#00ff00", selectforeground='black', fg="#ffcc00",
                                          font=("Courier New", 14),
                                          yscrollcommand=display_scrollbar_y.set)
        snippets_display_screen.pack(side='left', fill=tk.Y, padx=5)

        snippets_display_screen.bind("<Button-3>", show_popup)

        display_scrollbar_y.config(command=snippets_display_screen.yview)
        # display_scrollbar_x.config(command=snippets_display_screen.xview)

class Dictionary(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.config(bg=THEME_COLOR)
        
        # Frame for main title label and logo
        mainlabel_frame = tk.Frame(self, bg=THEME_COLOR, relief='groove', bd=1)
        mainlabel_frame.pack(anchor=tk.N)

        title_label = tk.Label(mainlabel_frame, text="GoofyCoder's Websters English Dictionary", font=("Century Gothic", 16, 'bold'), bg=THEME_COLOR,
                               fg='#ffff00')
        title_label.pack()

        def search(_=None):
            typed_word = search_entry.get()
            if dictionary_var.get() == 1 and len(typed_word) > 1:
                defination_box.config(state=tk.NORMAL)
                search_entry.delete(0, "end")
                defination_box.delete(1.0, tk.END)
                defination_box.insert(1.0, typed_word.capitalize() + "\n")
                defination_box.insert(2.0, "_" * 30 + "\n")
                defination_box.insert(4.0, search_word(typed_word))
                defination_box.config(state=tk.DISABLED)

        def update(data_list):
            # list_box.delete(0, tk.END)
            words_list_box.delete(0, tk.END)
            # Add words to listbox
            for word_item in data_list:
                words_list_box.insert(tk.END, word_item)

        def what_selected(typed_from_keyboard):
            if typed_from_keyboard == "":
                data = []
            else:
                data = []
                for item in search_all_matching(typed_from_keyboard):
                    data.append(item)
                update(data)

        def check(_=None):
            # grab what is typed
            typed = search_entry.get()
            what_selected(typed)
            # self.update()

        def fill_out(_=None):
            # Delete whatever is in the entry box
            search_entry.delete(0, tk.END)

            # Add clicked list item to entry box
            search_entry.insert(0, words_list_box.get("anchor"))
            search(words_list_box.get("anchor"))

        search_widget_frame = tk.Frame(self, bg=THEME_COLOR)
        search_widget_frame.pack(anchor=tk.N)

        def check_me():
            pass

        def cut_text():
            copy_text()
            delete_text()

        def copy_text():
            selection = defination_box.tag_ranges(tk.SEL)
            if selection:
                self.clipboard_clear()
                self.clipboard_append(defination_box.get(*selection))

        def paste_text():
            defination_box.insert(tk.INSERT, self.clipboard_get())

        def paste_image():
            global img
            try:
                img = tk.PhotoImage(file=self.clipboard_get())
                position = defination_box.index(tk.INSERT)
                defination_box.image_create(position, image=img)
            except tk.TclError:
                pass

        def delete_text():
            selection = defination_box.tag_ranges(tk.SEL)
            if selection:
                defination_box.delete(*selection)

        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="MucaiT's Websters Dictionary 2021")
        menu.add_command(label="Cut", command=cut_text)

        menu.add_command(label="Copy text", command=copy_text)
        menu.add_command(label="Paste text", command=paste_text)
        menu.add_command(label="Paste image", command=paste_image)
        menu.add_command(label="Delete", command=delete_text)

        def show_popup(event):
            menu.post(event.x_root, event.y_root)

        checkbuttons_frame = tk.Frame(search_widget_frame)
        checkbuttons_frame.pack(side=tk.LEFT)

        images = os.path.join(BASE_DIR, 'img')# images directory path
        on_image = tk.PhotoImage(file=os.path.join(images, 'button_on.png'))
        off_image = tk.PhotoImage(file=os.path.join(images, 'button_off.png'))
        dictionary_var = IntVar()
        dictionary_check = tk.Checkbutton(search_widget_frame, image=off_image, selectimage=on_image, indicatoron=False,
                                          variable=dictionary_var, onvalue=1, offvalue=0, bd=0,
                                          text="Dictionary", bg=THEME_COLOR, command=check_me)
        dictionary_check.image = (on_image, off_image)
        dictionary_check.pack(side=tk.LEFT)
        dictionary_check.select()

        search_text = tk.Label(search_widget_frame, bg=THEME_COLOR, text="Search ", font=TEXT_ENTRY_FONT)
        search_text.pack(side=tk.LEFT)

        search_entry = tk.Entry(search_widget_frame, width=34, font=TEXT_ENTRY_FONT)
        search_entry.pack(pady=20, side=tk.LEFT)
        search_entry.focus_set()
        search_entry.bind("<KeyRelease>", check)

        search_img = tk.PhotoImage(file=os.path.join(images, 'search.png'))
        search_btn = tk.Button(search_widget_frame, image=search_img, bg=THEME_COLOR, width=80,
                               activebackground='#5e5924', command=search)
        search_btn.image = search_img
        search_btn.pack(side=tk.LEFT, padx=5)

        defination_frame = tk.Frame(self)
        defination_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        defination_box_scrbar = tk.Scrollbar(defination_frame)
        defination_box = tk.Text(defination_frame, width=40, bg=THEME_COLOR,height=20, font=TEXT_ENTRY_FONT,
                                 yscrollcommand=defination_box_scrbar.set, fg='white')
        defination_box.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        defination_box_scrbar.pack(side=tk.LEFT, fill=tk.Y)
        defination_box_scrbar.config(command=defination_box.yview)

        words_listbox_scrbar = tk.Scrollbar(defination_frame)
        words_list_box = tk.Listbox(defination_frame, font=TEXT_ENTRY_FONT, bg=THEME_COLOR, yscrollcommand=words_listbox_scrbar.set, fg='#ffff00')
        words_list_box.pack(side=tk.LEFT, fill=tk.Y)
        words_listbox_scrbar.pack(side=tk.LEFT, fill=tk.Y)
        words_listbox_scrbar.config(command=words_list_box.yview)

        self.bind("<Return>", search)
        words_list_box.bind("<<ListboxSelect>>", fill_out)
        defination_box.bind("<Button-3>", show_popup)

        update(get_all_words())

class UtilitiesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        style = ttk.Style()
        theme_color = '#004D54'
        self.config(bg=THEME_COLOR)
        
        # Frame for main title label and logo
        mainlabel_frame = tk.Frame(self, bg=THEME_COLOR, relief='groove', bd=1)
        mainlabel_frame.pack(anchor=tk.N)


        # ----- Load images for the buttons
        cloud_btn_img = tk.PhotoImage(file="icons/safe.png")
        update_snpt_btn_img = tk.PhotoImage(file="icons/compose.png")
        cloud_delete_btn_img = tk.PhotoImage(file="icons/delete.png")
        run_snpt_btn_img = tk.PhotoImage(file="icons/play.png")
        clear_snpt_btn_img = tk.PhotoImage(file="icons/broom.png")

        background = tk.PhotoImage(file='images/background.png')

        style.layout("my.TNotebook",
                   [('Notebook.plain.field', {'children': [(
                       'Notebook.background', {'children': [(
                           'Notebook.padding', {'children': [(
                               'Notebook.textarea', {'sticky': 'nswe'})],
                                    'sticky': 'nswe'})], 'sticky': 'nswe'})],
                                        'border':'2', 'sticky': 'nswe'})])
        style.configure('my.TNotebook', fg='#483d8b', insertbackground='#115F54', fieldbackground=THEME_COLOR, bd=0, relief=tk.GROOVE, icursor=5)
        # ----------------- Main notebook
        notebook = ttk.Notebook(self, style="my.TNotebook")
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=8)

        # ------------------- Frames
        todo_page_frame = tk.Frame(notebook, bg=THEME_COLOR)
        diary_page_frame = tk.Frame(notebook, bg=THEME_COLOR)
        color_select_page_frame = tk.Frame(notebook, bg=THEME_COLOR)
        calculator_page_frame = tk.Frame(notebook, bg=THEME_COLOR)

        notebook.add(todo_page_frame, text='ToDo')
        notebook.add(diary_page_frame, text='Diary')
        notebook.add(color_select_page_frame, text='Color Select')
        notebook.add(calculator_page_frame, text='Calculator')

        # ============================================TODO_SECTION ==========================================
        # ----- search area frame
        search_frame = tk.Frame(todo_page_frame, bg=theme_color, relief=tk.FLAT, bd=0)
        search_frame.pack(fill=tk.X)

        # ----- Delete snippet button
        delete_snippet_button = tk.Button(search_frame, text='DELETE', fg='#00ff00', activebackground=theme_color, compound=tk.TOP, image=cloud_delete_btn_img, 
                                                        bg=theme_color, bd=0)
        delete_snippet_button.image = cloud_delete_btn_img
        delete_snippet_button.pack(side='left')

        # ----- Save snippet button
        save_snippet_button = tk.Button(search_frame, text='SAVE', fg='#00ff00',activebackground=theme_color, compound=tk.TOP, image=cloud_btn_img, bg=theme_color, bd=0)
        save_snippet_button.image = cloud_btn_img
        save_snippet_button.pack(side='left', padx=10)

        # ----- Update snippet button
        create_todo_button = tk.Button(search_frame, text='CREATE', fg='#00ff00', activebackground=theme_color, compound=tk.TOP, image=update_snpt_btn_img, 
                                                      bg=theme_color, bd=0)
        create_todo_button.image = update_snpt_btn_img
        create_todo_button.pack(side='left')

        # ----- Run snippet button
        open_todo_button = tk.Button(search_frame, text='OPEN', fg='#00ff00', activebackground=theme_color, compound=tk.TOP, image=run_snpt_btn_img, bd=0, bg=theme_color)
        open_todo_button.image = run_snpt_btn_img
        open_todo_button.pack(side='left')

        # ----- Clear snippet button
        clear_code_button = tk.Button(search_frame, text='CLEAR', fg='#00ff00', activebackground=theme_color, compound=tk.TOP, image=clear_snpt_btn_img, bd=0, bg=theme_color)
        clear_code_button.image = clear_snpt_btn_img
        clear_code_button.pack(side='left')

        # ----- Search area entry box
        style.layout("my.TEntry",
                   [('Entry.plain.field', {'children': [(
                       'Entry.background', {'children': [(
                           'Entry.padding', {'children': [(
                               'Entry.textarea', {'sticky': 'nswe'})],
                                    'sticky': 'nswe'})], 'sticky': 'nswe'})],
                                        'border':'2', 'sticky': 'nswe'})])
        style.configure('my.TEntry', fg='#483d8b', insertbackground='#115F54', fieldbackground='#115F54', bd=0, relief=tk.FLAT, icursor=5)
        search = ttk.Entry(search_frame, font=("Century Gothic", 12) , style='my.TEntry', foreground='#00ff00')
        search.pack(expand=True, side='left', padx=5, fill=tk.X)
        search.focus_set()

       
        search_btn_img = tk.PhotoImage(file="icons/import.png")

        # ----- Search snippet button
        search_snippet_button = tk.Button(search_frame, bg=theme_color, activebackground=theme_color, bd=0)
        search_snippet_button.image = search_btn_img
        search_snippet_button.pack(side='left')



        # ----- Get new snippet button
        get_new_snippet_button = tk.Button(search_frame, activebackground=theme_color, image=search_btn_img, bg=theme_color, bd=0)
        get_new_snippet_button.image = search_btn_img
        get_new_snippet_button.pack(side='left')

        # ----- All buttons bindings -----
        '''
        delete_snippet_button.bind("<Enter>", lambda x: main_label.config(text="delete snippet"))
        delete_snippet_button.bind("<Leave>", lambda x: main_label.config(text="Snippets"))

        save_snippet_button.bind("<Enter>", lambda x: main_label.config(text="save snippet"))
        save_snippet_button.bind("<Leave>", lambda x: main_label.config(text="Snippets"))

        search_snippet_button.bind("<Enter>", lambda x: main_label.config(text="search snippet"))
        search_snippet_button.bind("<Leave>", lambda x: main_label.config(text="Snippets"))

        update_snippet_button.bind("<Enter>", lambda x: main_label.config(text="update snippet"))
        update_snippet_button.bind("<Leave>", lambda x: main_label.config(text="Snippets"))

        get_new_snippet_button.bind("<Enter>", lambda x: main_label.config(text="get new snippet from file"))
        get_new_snippet_button.bind("<Leave>", lambda x: main_label.config(text="Snippets"))

        run_code_button.bind("<Enter>", lambda x: main_label.config(text="test run snippet"))
        run_code_button.bind("<Leave>", lambda x: main_label.config(text="Snippets"))

        clear_code_button.bind("<Enter>", lambda x: main_label.config(text="clear everything in text area"))
        clear_code_button.bind("<Leave>", lambda x: main_label.config(text="Snippets"))
        '''
        # ----- Snippet id area label -----
        snippet_id_frame = tk.Frame(search_frame, bg=THEME_COLOR)
        snippet_id_frame.pack(side='right', anchor=tk.E)
        snippet_id_label = tk.Label(snippet_id_frame, text="Snippet ID: ", fg='#00ff00', bg=theme_color,
                                    font=("Century Gothic", 12))
        snippet_id_label.pack(side='left')

        # ----- Snippet id area entry -----
        snippet_id = tk.Entry(snippet_id_frame, relief="flat", bg=theme_color, font=("Century Gothic", 12),
                              fg='#00ff00')
        snippet_id.pack(side='left')

        # ----- Main frame to hold listbox and textbox
        main_frame = tk.Frame(todo_page_frame, bg=THEME_COLOR)
        main_frame.pack(fill='both', expand=True)
        

        canvas = tk.Canvas(main_frame, width=400, height=400, bg=THEME_COLOR, bd=0,relief=tk.FLAT)
        # canvas.create_text(100, 200, text="Hello there", fill='red')
        
        canvas.create_image(20,30, image=update_snpt_btn_img, anchor=tk.CENTER)
        
        canvas.pack(fill=tk.BOTH, expand=True)

        # ===============================COLOR PICKER SECTION================================
        def color():
            my_color = colorchooser.askcolor()
            my_label2.config(text=f"Color hex: {my_color[1]}\nRGB Color: {my_color[0]}", bg=my_color[1])
            color_select_page_frame.config(bg=my_color[1])

        my_label2 = tk.Label(color_select_page_frame,  font=("Helvetica", 32), bg=THEME_COLOR)
        my_label2.pack()

        my_button = tk.Button(color_select_page_frame, text="Pick A Color", 
                                                       bg=THEME_COLOR, command=color,
                                                       relief=tk.GROOVE, bd=0,
                                                       font=("Century Gothic", 18, 'bold'),
                                                       activebackground=THEME_COLOR,
                                                       activeforeground='#00ff00')
        my_button.pack()

        # ==============================CALCULATOR SECTION=========================

        
        screen = tk.Entry(calculator_page_frame, borderwidth=0, relief=tk.FLAT, bg=THEME_COLOR, 
                                                           font=("Century Gothic", 14),
                                                           fg='#00ff00')
        screen.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='news')
        #e.insert(0, "Enter Your Name: ")

        def Button_Clicker(number):
            new_number = screen.get() + str(number)
            screen.delete(0, tk.END)
            screen.insert(0, new_number)

        def Button_Clear():
            screen.delete(0, tk.END)

        def Button_Add(first_number):
            global f_num
            global math
            math = "addition"
            f_num = first_number
            #e.insert(0, first_number)
            screen.delete(0, tk.END)

        def Button_Subtract(first_number):
            global f_num
            global math
            math = "subtraction"
            f_num = first_number
            #e.insert(0, first_number)
            screen.delete(0, tk.END)

        def Button_Multiply(first_number):
            global f_num
            global math
            math = "multiplication"
            f_num = first_number
            #e.insert(0, first_number)
            screen.delete(0, tk.END)

        def Button_Divide(first_number):
            global f_num
            global math
            math = "division"
            f_num = first_number
            #e.insert(0, first_number)
            screen.delete(0, tk.END)

        def Button_Equal(second_number):
            num_1 = f_num
            if math == "addition":
                screen.delete(0, tk.END)
                try:
                    screen.insert(0, int(num_1) + int(second_number))
                except ValueError:
                    pass
            if math == "subtraction":
                screen.delete(0, tk.END)
                try:
                    screen.insert(0, int(num_1) - int(second_number))
                except ValueError:
                    pass
            if math == "multiplication":
                screen.delete(0, tk.END)
                try:
                    screen.insert(0, int(num_1) * int(second_number))
                except ValueError:
                    pass
            if math == "division":
                screen.delete(0, tk.END)
                try:
                    screen.insert(0, int(num_1) / int(second_number))
                except ValueError:
                    pass


        button_1 = tk.Button(calculator_page_frame, text="1", padx=40, pady=20, command=lambda: Button_Clicker(1))
        button_2 = tk.Button(calculator_page_frame, text="2", padx=40, pady=20, command=lambda: Button_Clicker(2))
        button_3 = tk.Button(calculator_page_frame, text="3", padx=40, pady=20, command=lambda: Button_Clicker(3))
        button_4 = tk.Button(calculator_page_frame, text="4", padx=40, pady=20, command=lambda: Button_Clicker(4))
        button_5 = tk.Button(calculator_page_frame, text="5", padx=40, pady=20, command=lambda: Button_Clicker(5))
        button_6 = tk.Button(calculator_page_frame, text="6", padx=40, pady=20, command=lambda: Button_Clicker(6))
        button_7 = tk.Button(calculator_page_frame, text="7", padx=40, pady=20, command=lambda: Button_Clicker(7))
        button_8 = tk.Button(calculator_page_frame, text="8", padx=40, pady=20, command=lambda: Button_Clicker(8))
        button_9 = tk.Button(calculator_page_frame, text="9", padx=40, pady=20, command=lambda: Button_Clicker(9))
        button_0 = tk.Button(calculator_page_frame, text="0", padx=40, pady=20, command=lambda: Button_Clicker(0))
        button_clear = tk.Button(calculator_page_frame, text="Clear", padx=79, pady=20, command=Button_Clear)
        button_add = tk.Button(calculator_page_frame, text="+", padx=39, pady=20, command=lambda: Button_Add(screen.get()))
        button_equal = tk.Button(calculator_page_frame, text="=", padx=91, pady=20, command=lambda: Button_Equal(screen.get()))

        button_subtract = tk.Button(calculator_page_frame, text="-", padx=41, pady=20, command=lambda: Button_Subtract(screen.get()))
        button_multiply = tk.Button(calculator_page_frame, text="*", padx=41, pady=20, command=lambda: Button_Multiply(screen.get()))
        button_divide = tk.Button(calculator_page_frame, text="/", padx=41, pady=20, command=lambda: Button_Divide(screen.get()))

        button_1.grid(row=3, column=0, sticky='w')
        button_2.grid(row=3, column=1, sticky='w')
        button_3.grid(row=3, column=2, sticky='w')

        button_4.grid(row=2, column=0, sticky='w')
        button_5.grid(row=2, column=1, sticky='w')
        button_6.grid(row=2, column=2, sticky='w')

        button_7.grid(row=1, column=0, sticky='w')
        button_8.grid(row=1, column=1, sticky='w')
        button_9.grid(row=1, column=2, sticky='w')

        button_0.grid(row=4, column=0, sticky='w')
        button_clear.grid(row=4, column=1, columnspan=2, sticky='w')

        button_add.grid(row=5, column=0, sticky='w')
        button_subtract.grid(row=5, column=1, sticky='w')
        button_multiply.grid(row=5, column=2, sticky='w')
        button_divide.grid(row=6, column=0, sticky='w')

        button_equal.grid(row=6, column=1, columnspan=2, sticky='w')

        def myClick():
            hello = "Hello " + screen.get()
            myLabel = Label(root, text=hello)
            myLabel.pack()

        #myButton = Button(root, text="Enter Your Stock Quote", command=myClick)
        #myButton.pack()


class MyDiary(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        theme_color = "#003B4A"
        theme_font = ("helvetica", 12)
        entries_bg_color = "#003B4A"
        entries_fg_color = "#ffff00"

        self.config(bg=theme_color)

        # --> Frame to hold the page title
        events_page_title_frame = tk.Frame(self, bg=theme_color, padx=7)
        events_page_title_frame.pack(fill=tk.BOTH)

        # --> Set page title
        events_page_title = tk.Label(events_page_title_frame, text="Events Database", font=theme_font, relief=tk.RAISED,
                                     bg=theme_color, fg="#ffff00", bd=2)
        events_page_title.pack(side="top", fill="both", expand=True)

       

class OrigaartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.config(bg=THEME_COLOR)
        
        # Frame for main title label and logo
        mainlabel_frame = tk.Frame(self, bg=THEME_COLOR, relief='groove', bd=1)
        mainlabel_frame.pack(anchor=tk.N)

        title_label = tk.Label(mainlabel_frame, text="Ariginal Artworks of Africa", font=("Century Gothic", 16, 'bold'), bg=THEME_COLOR,
                               fg='#ffff00')
        title_label.pack()


class Authentication(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.config(bg=THEME_COLOR)
        
        # Frame for main title label and logo
        mainlabel_frame = tk.Frame(self, bg=THEME_COLOR, relief='groove', bd=1)
        mainlabel_frame.pack(anchor=tk.N)

        title_label = tk.Label(mainlabel_frame, text="Authentication", font=("Century Gothic", 16, 'bold'), bg=THEME_COLOR,
                               fg='#ffff00')
        title_label.pack()

         # ----- Main frame to hold listbox and textbox
        main_frame = tk.Frame(self, bg=THEME_COLOR)
        main_frame.pack(fill='both', expand=True)

        def login(e=None):
            pwd = password.get()
            if pwd == '1':
                password.delete(0, tk.END)
                controller.show_frame(OrigaartPage)
            elif pwd == '':
                password.delete(0, tk.END)
                msg.config(text = 'Enter Password Please', fg='red')
            else:
                password.delete(0, tk.END)
                msg.config(text = 'Wrong Password', fg='red')

        password = tk.Entry(main_frame, relief=tk.GROOVE, bd=0, show='*',
                                        font=("Century Gothic", 18))
        password.focus_set()
        password.pack()
        

        my_button = tk.Button(main_frame, text="Login", 
                                                       bg=THEME_COLOR, command=login,
                                                       relief=tk.GROOVE, bd=1,
                                                       font=("Century Gothic", 18, 'bold'),
                                                       activebackground=THEME_COLOR,
                                                       activeforeground='#00ff00')
        my_button.pack()

        msg = tk.Label(main_frame, font=("Century Gothic", 18), bg=THEME_COLOR)
        msg.pack()


class BritannicaEncyclopedia(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.config(bg=THEME_COLOR)
        
        # Frame for main title label and logo
        mainlabel_frame = tk.Frame(self, bg=THEME_COLOR, relief='groove', bd=1)
        mainlabel_frame.pack(anchor=tk.N)

        title_label = tk.Label(mainlabel_frame, text="Britannica Student Encyclopedia", font=("Century Gothic", 16, 'bold'), bg=THEME_COLOR, fg='#ffff00')
        title_label.pack()

        def search(_=None):
            typed_word = search_entry.get()
            if dictionary_var.get() == 1 and len(typed_word) > 1:
                defination_box.config(state=tk.NORMAL)
                search_entry.delete(0, "end")
                defination_box.delete(1.0, tk.END)
                #defination_box.insert(2.0, typed_word.capitalize() + "\n")
                #defination_box.insert(2.0, "_" * 30 + "\n")
                img = tk.PhotoImage(file=db.get_thread_image(typed_word))
                defination_box.image_create(9.0, image=img)
                defination_box.image = img
                defination_box.insert(6.0, db.search_word_thread(typed_word))
                #defination_box.config(state=tk.DISABLED)

        def update(data_list):
            # list_box.delete(0, tk.END)
            words_list_box.delete(0, tk.END)
            # Add words to listbox
            for word_item in data_list:
                words_list_box.insert(tk.END, word_item)

        def what_selected(typed_from_keyboard):
            if typed_from_keyboard == "":
                data = []
            else:
                data = []
                for item in db.search_all_matching_thread(typed_from_keyboard):
                    data.append(item)
                update(data)

        def check(_=None):
            # grab what is typed
            typed = search_entry.get()
            what_selected(typed)
            # self.update()

        def fill_out(_=None):
            # Delete whatever is in the entry box
            search_entry.delete(0, tk.END)

            # Add clicked list item to entry box
            search_entry.insert(0, words_list_box.get("anchor"))
            search(words_list_box.get("anchor"))

        def fill_out(_=None):
            # ----- this function declaration will clear the text area, entry area and id area
            clear_fields()
            # ----- Add clicked list item to entry box
            search_entry.insert(0, words_list_box.get("anchor"))
            # ----- Search snippet in database using the title pulled from the listbox, in this case snippets list
            data = db.search_word_thread(words_list_box.get("anchor"))
            # ----- Get snippet id from the data pulled from the database snippet entry
            iid =data[0]
            # ----- Get snippet code from the data pulled from the database snippet entry
            title =data[1]
            thread =data[2]
            img = data[3]

            # ----- Insert the code data into text area to display it
            #defination_box.insert(1.0, title)
            #defination_box.insert(tk.END, "\n")
            #defination_box.insert(2.0, "_" * 30 + "\n")
            img = tk.PhotoImage(file=img)
            defination_box.image_create(3.0, image=img)
            defination_box.image = img
            defination_box.insert(tk.END, "\n")
            defination_box.insert(tk.END, thread)
            

        search_widget_frame = tk.Frame(self, bg=THEME_COLOR)
        search_widget_frame.pack(anchor=tk.N)

        def check_me():
            pass

        def cut_text():
            copy_text()
            delete_text()

        def copy_text():
            selection = defination_box.tag_ranges(tk.SEL)
            if selection:
                self.clipboard_clear()
                self.clipboard_append(defination_box.get(*selection))

        def paste_text():
            defination_box.insert(tk.INSERT, self.clipboard_get())

        def paste_image():
            global img
            try:
                img = tk.PhotoImage(file=self.clipboard_get())
                position = defination_box.index(tk.INSERT)
                defination_box.image_create(position, image=img)
            except tk.TclError:
                pass

        def delete_text():
            selection = defination_box.tag_ranges(tk.SEL)
            if selection:
                defination_box.delete(*selection)

        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Ephitome")
        menu.add_command(label="Cut", command=cut_text)

        menu.add_command(label="Copy text", command=copy_text)
        menu.add_command(label="Paste text", command=paste_text)
        menu.add_command(label="Paste image", command=paste_image)
        menu.add_command(label="Delete", command=delete_text)

        def show_popup(event):
            menu.post(event.x_root, event.y_root)

        checkbuttons_frame = tk.Frame(search_widget_frame)
        checkbuttons_frame.pack(side=tk.LEFT)

        images = os.path.join(BASE_DIR, 'img')# images directory path
        on_image = tk.PhotoImage(file=os.path.join(images, 'button_on.png'))
        off_image = tk.PhotoImage(file=os.path.join(images, 'button_off.png'))

        def delete_my_thread():
            # ----- Get selected snippet from the snippets list
            title = words_list_box.get("anchor")

            # ----- Check if there is something in variable title
            if len(title) < 1:
                messagebox.showerror("Error", "No title selected, Please select Snippet to delete!")
            else:
                # ----- A popup box will ask for the user's confirmation to delete
                ask = messagebox.askyesno("Alert", "Do you wish to proceed deleting this Snippet?")

                # ----- If yes then delete
                if ask:

                    # ----- Delete from database and return a deletion status
                    deletion_status = db.delete_thread(title)

                    # ----- If deletion status is success
                    if deletion_status == 'success':
                        clear_fields()
                        # Finally update the snippets list with new database contents, adding the new snippet to
                        # snippets list
                        update(db.get_all_thread_words())

                        # ----- Show success popup
                        messagebox.showinfo("Success", "Thread delete successful!")
                    else:
                        # ----- Else Show warning
                        messagebox.showwarning("Failure", "Thread delete unsuccessful!")
        
        def update_thread():

            # ----- Get whatever is in the search area
            title = search_entry.get()

            # ----- Get whatever is in the text area
            thread = defination_box.get('0.1', tk.END)
            print(db.get_thread_id(title))
            # ----- Call database method and update changes made in title and code and return update status
            update_status = db.update_thread(db.get_thread_id(title), title, thread)

            # ----- Check status message if its true then proceed to update the snippets list
            if update_status:
                update(db.get_all_thread_words())
                messagebox.showinfo("Success", "Thread update successful!")
            else:
                messagebox.showwarning("Failure", "Thread update unsuccessful!")

        delete_thread_button = tk.Button(search_widget_frame, text='Delete Thread', bg=THEME_COLOR, fg='#ffff00' , command=delete_my_thread)
        delete_thread_button.pack(side=tk.LEFT)

        update_thread_button = tk.Button(search_widget_frame, text='Tpdate Thread', bg=THEME_COLOR, fg='#ffff00' , command=update_thread)
        update_thread_button.pack(side=tk.LEFT)

        dictionary_var = IntVar()
        dictionary_check = tk.Checkbutton(search_widget_frame, image=off_image, selectimage=on_image, indicatoron=False,
                                          variable=dictionary_var, onvalue=1, offvalue=0, bd=0,
                                          text="Dictionary", bg=THEME_COLOR, command=check_me)
        dictionary_check.image = (on_image, off_image)
        dictionary_check.pack(side=tk.LEFT)
        dictionary_check.select()

        search_text = tk.Label(search_widget_frame, bg=THEME_COLOR, text="Search ", font=TEXT_ENTRY_FONT)
        search_text.pack(side=tk.LEFT)

        search_entry = tk.Entry(search_widget_frame, width=34, font=TEXT_ENTRY_FONT)
        search_entry.pack(pady=20, side=tk.LEFT)
        search_entry.focus_set()
        search_entry.bind("<KeyRelease>", check)

        def clear_fields():
            search_entry.delete(0, tk.END)
            defination_box.delete('0.1', tk.END)
            

        def new_thread():
            window = tk.Toplevel()
            window.focus_set()
            def cut_text():
                copy_text()
                delete_text()

            def copy_text():
                selection = content.tag_ranges(tk.SEL)
                if selection:
                    self.clipboard_clear()
                    self.clipboard_append(content.get(*selection))

            def paste_text():
                content.insert(tk.INSERT, self.clipboard_get())

            def paste_image():
                global img
                try:
                    img = tk.PhotoImage(file=self.clipboard_get())
                    position = snippets_display_screen.index(tk.INSERT)
                    content.image_create(position, image=img)
                except tk.TclError:
                    pass

            def delete_text():
                selection = snippets_display_screen.tag_ranges(tk.SEL)
                if selection:
                    content.delete(*selection)

            menu = tk.Menu(window, tearoff=0)
            menu.add_command(label="GoofyCoder.com")
            menu.add_command(label="Cut", command=cut_text)

            menu.add_command(label="Copy", command=copy_text)
            menu.add_command(label="Paste", command=paste_text)
            menu.add_command(label="Paste Image", command=paste_image)
            menu.add_command(label="Delete", command=delete_text)

            image_path_frame = tk.Frame(window, bg=THEME_COLOR)
            image_path_frame.pack()
            

            def get_image_path():
                path = filedialog.askopenfilename()
                image_path.delete(0, tk.END)
                image_path.insert(0, path)

            def threadSave():
                image = image_path.get()
                title = thread_title.get().capitalize()
                thread = content.get('0.1', tk.END)

                if len(title) > 0 and len(thread) > 0:
                    if '/' not in image:
                        image = 'images/Encyclopedia-images/dumy.png'
                        status = db.insert_encyclopedia_thread(title, thread, image)
                        print(status)
                        update(db.get_all_thread_words())
                        clear_fields()
                        messagebox.showinfo("Success", "Thread save successful!")
                        
                    else:
                        status = db.insert_encyclopedia_thread(title, thread, image)
                        print(status)
                        update(db.get_all_thread_words())
                        clear_fields()
                        messagebox.showinfo("Success", "Thread saved successful!")
                else:
                    # ----- Else Show warning
                    messagebox.showwarning("Failure", "Failed to save thread!")

            def clear_fields():
                image_path.delete(0, tk.END)
                thread_title.delete(0, tk.END)
                content.delete('0.1', tk.END)


            image_path = tk.Entry(image_path_frame, width= 80, bg=THEME_COLOR, fg='#ffff00')
            image_path.pack(side=tk.LEFT)

            get_path = tk.Button(image_path_frame, text='Select Images', command=get_image_path, bg=THEME_COLOR, fg='#ffff00')
            get_path.pack(side=tk.LEFT)

            def show_popup(event):
                menu.post(event.x_root, event.y_root)

            content = tk.Text(window, bg=THEME_COLOR, fg='#ffff00')
            content.focus_set()
            content.pack(fill=tk.BOTH)

            content.bind("<Button-3>", show_popup)

            thread_save_frame = tk.Frame(window, bg=THEME_COLOR)
            thread_save_frame.pack(fill=tk.X)

            thread_title = tk.Entry(thread_save_frame, bg=THEME_COLOR, fg='#ffff00')
            thread_title.pack(side=tk.LEFT, fill=tk.X)

            save_thread = tk.Button(thread_save_frame, text='Save Thread', command=threadSave, bg=THEME_COLOR, fg='#ffff00')
            save_thread.pack(side=tk.LEFT)

            window.mainloop()



        search_btn = tk.Button(search_widget_frame, text='New Encyclopedia Thread', compound=tk.TOP,bg=THEME_COLOR, fg='#ffff00', activebackground='#5e5924', command=new_thread)
        search_btn.pack(side=tk.LEFT, padx=5)

        defination_frame = tk.Frame(self, bg=THEME_COLOR)
        defination_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        words_listbox_scrbar = tk.Scrollbar(defination_frame)
        words_list_box = tk.Listbox(defination_frame, font=TEXT_ENTRY_FONT, bg=THEME_COLOR, yscrollcommand=words_listbox_scrbar.set, fg='#ffff00')
        words_list_box.pack(side=tk.LEFT, fill=tk.Y)
        words_listbox_scrbar.pack(side=tk.LEFT, fill=tk.Y)
        words_listbox_scrbar.config(command=words_list_box.yview)

        words_list_box.bind("<<ListboxSelect>>", fill_out)

        defination_box_scrbar = tk.Scrollbar(defination_frame)
        defination_box = tk.Text(defination_frame, width=40, bg=THEME_COLOR,height=20, font=TEXT_ENTRY_FONT, yscrollcommand=defination_box_scrbar.set, fg='white')
        defination_box.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        defination_box_scrbar.pack(side=tk.LEFT, fill=tk.Y)
        defination_box_scrbar.config(command=defination_box.yview)

        self.bind("<Return>", search)
        
        defination_box.bind("<Button-3>", show_popup)

        update(db.get_all_thread_words())

        side_bar = tk.Frame(defination_frame, bg=THEME_COLOR)
        side_bar.pack(side=tk.LEFT, fill=tk.Y)

        sidebar_info = tk.Label(side_bar, text='Related Topics:', bg=THEME_COLOR, font=("Century Gothic", 16, 'bold'), fg='#bef74a')
        sidebar_info.pack(side=tk.TOP, anchor=tk.N)

        information_bar = tk.Listbox(side_bar, font=TEXT_ENTRY_FONT, bg=THEME_COLOR, bd=0, relief=tk.FLAT, fg='#ffff00')
        information_bar.pack(side=tk.TOP, fill=tk.Y)
        

if __name__ == "__main__":
    app = Application()
    app.mainloop()
