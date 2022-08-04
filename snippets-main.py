# import libraries
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from database import Database
import os
from fontTools.ttLib import TTFont
from tkinter import Menu

# ----- Create base folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db = Database()

# -----Loading and installing font
fonts_path = os.path.join(BASE_DIR, 'fonts')
for font in os.listdir(fonts_path):
    this_font = TTFont(os.path.join(fonts_path, font))
    this_font.save(os.path.join(fonts_path, font))


# Main window for the application
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)  # initialize the inherited tkinter library
        theme_color = '#004D54'  # Set theme color

        # ------------------------------------MAIN WINDOW CUSTOMIZATION-------------------------------------------------
        self.title('GoofyCoder Utility Application')  # Window title
        self.geometry('830x570+200+50')  # Window size in width and height then position on the screen
        self.iconbitmap("images/goofy_coder.ico")  # Window icon
        self.minsize(830, 570)  # Window minimum size
        self.config(bg=theme_color)  # Configure window background color
        # self.overrideredirect(True)

        # -------------------------------------------MENU SECTION-------------------------------------------------------
        my_menu = Menu(self)  # Initialize
        self.config(menu=my_menu)

        # Create a menu item
        file_menu = Menu(my_menu)
        my_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New...")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        # Create an edit menu item
        edit_menu = Menu(my_menu)
        my_menu.add_cascade(label="Pages", menu=edit_menu)
        edit_menu.add_command(label="Contacts")
        edit_menu.add_command(label="Dictionary")
        edit_menu.add_command(label="Snippets")
        edit_menu.add_command(label="Comprehensive Notes")

        # Create an Options menu item
        option_menu = Menu(my_menu)
        my_menu.add_cascade(label="About GoofyCoder Utility Application", menu=option_menu)
        option_menu.add_command(label="Info")
        option_menu.add_command(label="GoofyCoder Info")

        # Load the main logo image
        main_logo_img = tk.PhotoImage(file="images/Goofy-Coder-Banner.png")
        python_icon_img = tk.PhotoImage(file="images/py_icon.png")
        exit_image = tk.PhotoImage(file="images/exit_icon.png")
        current_user_img = tk.PhotoImage(file="images/current_user_icon.png")

        # -------------------------------------------TIME AND LOGOS SECTION---------------------------------------------
        time_and_logo = tk.Frame(self, bg=theme_color)  # Create the frame to hold the digital time and top buttons
        time_and_logo.pack(fill=tk.X)

        # -----This is button serve as a link to the main page and logo for goofycoder
        goofy_main_button = tk.Button(time_and_logo, image=main_logo_img, bg=theme_color, relief='flat', bd=0,
                                      activebackground="#CCBF99", command=lambda: self.show_frame(SnippetsPage))
        goofy_main_button.image = main_logo_img
        goofy_main_button.pack(side='left', padx=20, pady=10)

        # -----Bind button to change color when mouse hover on it
        goofy_main_button.bind('<Enter>', lambda e: goofy_main_button.config(bg="#DDD7A6"))
        goofy_main_button.bind('<Leave>', lambda e: goofy_main_button.config(bg="#CCBF98"))

        # -----Function to iterate through time and configure the time display label
        def clock_it(label):
            def clock():
                label.config(text=f"{datetime.now().time().strftime('%H:%M:%S')}")
                label.after(1000, clock)

            clock()

        # -----This is the label to display time
        time_display_label = tk.Label(time_and_logo, text='This is time', font=('Digital-7 Mono', 20,), fg="#ffff00",
                                      bg=theme_color)
        time_display_label.pack(side=tk.LEFT)

        clock_it(time_display_label)  # Now use clock it function to display time to the window

        # -----Frame to hold the python logo
        python_icon_frame = tk.Frame(time_and_logo, bg=theme_color)
        python_icon_frame.pack(side=tk.RIGHT, padx=10, fill=tk.X)

        # -----Create exit button with icon logo
        exit_icon = tk.Button(time_and_logo, image=exit_image, bg=theme_color, relief='flat', bd=0,
                              activebackground="#CCBF99", command=lambda: self.destroy())
        exit_icon.image = exit_image
        exit_icon.pack(side=tk.RIGHT)

        # -----This frame will hold the current user logo and name
        current_user_frame = tk.Frame(python_icon_frame, bg=theme_color)
        current_user_frame.pack(side=tk.LEFT, padx=10)

        # -----Python logo label
        python_icon = tk.Label(python_icon_frame, image=python_icon_img, bg=theme_color)
        python_icon.image = python_icon_img
        python_icon.pack(side=tk.RIGHT)

        # -----Current user button with icon
        current_user_icon = tk.Button(current_user_frame, image=current_user_img, bg=theme_color, relief='flat', bd=0,
                                      activebackground="#CCBF99")
        current_user_icon.image = current_user_img
        current_user_icon.pack()

        # -----Label for current username
        current_username = tk.Label(current_user_frame, text=f"----------------", bg=theme_color,
                                    font=("helvetica", 12))
        current_username.pack(pady=0)
        # ---------------------------------------ALL PROGRAM PAGES SECTION----------------------------------------------
        container = tk.Frame(self)  # Create main frame
        container.pack(side='top', fill='both', expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # -----This dictionary will contain all pages
        self.frames = {}

        # -----Loop through all pages available then get the selected
        for page in (SnippetsPage,):
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

        # ----- Main label
        main_label = tk.Label(self, width=30, text='Snippets', font=("Blacksword", 35), fg='#00ff00', bg=theme_color)
        main_label.pack()

        # ----- search area frame
        search_frame = tk.Frame(self, bg=theme_color)
        search_frame.pack()

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
            update(data)

        # ----- This function sorely get data and update the snippets list
        def update(snippets):

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
                update(db.get_all_snippets())

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
                        update(db.get_all_snippets())
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
                update(db.get_all_snippets())
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
        cloud_btn_img = tk.PhotoImage(file="images/Treasure-Chest-icon.png")
        update_snpt_btn_img = tk.PhotoImage(file="images/update_db.png")
        cloud_delete_btn_img = tk.PhotoImage(file="images/Cannon-icon.png")
        run_snpt_btn_img = tk.PhotoImage(file="images/Pirate-Ship-icon.png")
        clear_snpt_btn_img = tk.PhotoImage(file="images/clear_broom.png")

        # ----- Snippets count label
        snippets_count_label = tk.Label(search_frame, text=f'Snippets avail: {len(db.get_all_snippets())}',
                                        bg=theme_color, fg='#00ff00', font=("helvetica", 14))
        snippets_count_label.pack(side='left', padx=20)

        # ----- Delete snippet button
        delete_snippet_button = tk.Button(search_frame, image=cloud_delete_btn_img, bg=theme_color, bd=0,
                                          command=delete_snippet)
        delete_snippet_button.image = cloud_delete_btn_img
        delete_snippet_button.pack(side='left')

        # ----- Save snippet button
        save_snippet_button = tk.Button(search_frame, image=cloud_btn_img, bg=theme_color, bd=0, command=save_snippet)
        save_snippet_button.image = cloud_btn_img
        save_snippet_button.pack(side='left', padx=10)

        # ----- Update snippet button
        update_snippet_button = tk.Button(search_frame, image=update_snpt_btn_img, bg=theme_color, bd=0,
                                          command=update_db)
        update_snippet_button.image = update_snpt_btn_img
        update_snippet_button.pack(side='left')

        # ----- Run snippet button
        run_code_button = tk.Button(search_frame, image=run_snpt_btn_img, bd=0, bg=theme_color, font=("helvetica", 12),
                                    command=run)
        run_code_button.image = run_snpt_btn_img
        run_code_button.pack(side='left')

        # ----- Clear snippet button
        clear_code_button = tk.Button(search_frame, image=clear_snpt_btn_img, bd=0, bg=theme_color,
                                      font=("helvetica", 12), command=clear_fields)
        clear_code_button.image = clear_snpt_btn_img
        clear_code_button.pack(side='left')

        # ----- Search area entry box
        search = tk.Entry(search_frame, font=('helvetica', 14), width=40)
        search.pack(expand=True, side='left', padx=5)

        # ----- Clear snippet button
        search.bind('<Return>', search_snippet)
        search_btn_img = tk.PhotoImage(file="images/search_btn_img.png")

        # ----- Search snippet button
        search_snippet_button = tk.Button(search_frame, bg=theme_color, bd=0, command=search_snippet)
        search_snippet_button.image = search_btn_img
        search_snippet_button.pack(side='left')

        # ----- Bind the search button
        search.bind("<KeyRelease>", check)

        # ----- Get new snippet button
        get_new_snippet_button = tk.Button(search_frame, image=search_btn_img, bg=theme_color, bd=0, command=new_file)
        get_new_snippet_button.image = search_btn_img
        get_new_snippet_button.pack(side='left')

        # ----- All buttons bindings -----
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

        # ----- Snippet id area label -----
        snippet_id_label = tk.Label(search_frame, text="Snippet ID: ", fg='#00ff00', bg=theme_color,
                                    font=("helvetica", 14))
        snippet_id_label.pack(side='left')

        # ----- Snippet id area entry -----
        snippet_id = tk.Entry(search_frame, relief="flat", bg=theme_color, font=("helvetica", 12))
        snippet_id.pack(side='left')

        # ----- Main frame to hold listbox and textbox
        main_frame = tk.Frame(self, bg=theme_color, padx=5, pady=8)
        main_frame.pack(fill='both', expand=True)

        # ---- Create scrollbar for the listbox
        snippets_list_scrollbar = tk.Scrollbar(main_frame)

        # ----- Listbox to display all snippets
        snippets_list = tk.Listbox(main_frame, height=40, width=40, bg=theme_color, fg="yellow",
                                   yscrollcommand=snippets_list_scrollbar.set, font=("verdana", 10))
        snippets_list.pack(side='left', fill=tk.Y)

        # ----- Update the snippets list with database contents
        update(db.get_all_snippets())

        # ----- Snippets list bindings
        snippets_list.bind("<<ListboxSelect>>", fill_out)
        snippets_list.bind('<Return>', search_snippet)

        # ----- Snippets list scrollbar
        snippets_list_scrollbar.pack(side='left', fill='y')
        snippets_list_scrollbar.config(command=snippets_list.yview)

        # ----- Create scrollbar for the text area
        display_scrollbar_x = tk.Scrollbar(main_frame, orient='horizontal')
        display_scrollbar_y = tk.Scrollbar(main_frame)

        # ----- Pack scrollbars to window
        # display_scrollbar_x.pack(side='bottom', fill='x')
        display_scrollbar_y.pack(side='right', fill='y')

        # ----- Main screen to view snippet contents
        snippets_display_screen = tk.Text(main_frame, height=40, width=250, bg=theme_color, wrap='word',
                                          selectbackground="#ff55aa", selectforeground='black', fg="#ffcc00",
                                          font=('Courier New', 14),
                                          yscrollcommand=display_scrollbar_y.set)
        snippets_display_screen.pack(side='left', fill=tk.Y)

        snippets_display_screen.bind("<Button-3>", show_popup)

        display_scrollbar_y.config(command=snippets_display_screen.yview)
        # display_scrollbar_x.config(command=snippets_display_screen.xview)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
