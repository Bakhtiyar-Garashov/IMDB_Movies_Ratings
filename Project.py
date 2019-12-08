import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk #to import tkinter and some internal features of it
import requests #for sending HTTP GET request to url
from bs4 import BeautifulSoup #to parse HTML content of website
import re #for using regular expressions

try:
    url = "http://www.imdb.com/chart/top" #data source website
    headers = {'Accept-Language': 'en-US,en;'} #to prevent language changes
    response = requests.get(url,headers=headers)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    movie_names = soup.find_all("td", {"class": "titleColumn"}) #to find td html tag elements' content (<td></td>)
    ratings = soup.find_all("td", {"class", "ratingColumn imdbRating"})
    all_movies=dict() #nested dictionary (keys are movie names values are year and rating as a list
    searchable_collection=dict() 
    
    # definition of main window and its properties
    main_window = Tk()
    main_window.geometry("700x350")
    main_window.configure(bg='#0c9463')
    main_window.iconbitmap('icon1.ico')
    main_window.title("IMDB movies and ratings application")
    main = Label(main_window, text="Welcome to IMDB movies and ratings application!", pady=130)
    main.config(bg='#0c9463', fg="White", font=("Courier", 13))
    main.pack()
    
    #definiton of some widgets (entry,label) in main window
    onelabel = Label(main_window, text="Enter movie name to find",padx=10)
    onelabel.pack_forget()
    search_button = tk.Button(main_window,text="Find movie",fg="black",padx=5,width=14,font=('Tahoma', '11'))
    search_button.pack_forget()
    user_input=Entry(main_window,width='30')
    aboutlabel = Label(main_window, text="This small application is developed for course project\nContact: bakhtiyar.garashov@ut.ee\nversion 1.0", pady=130)
    aboutlabel.pack_forget()
    watermark = Label(main_window, text="Developed by Bakhtiyar Garashov", pady=0)
    watermark.config(bg='#0c9463', fg="White", font=("Arial", 9))
    watermark.pack()
    title = Label(main_window, text="IMDB top 250 movies list",padx=10)
    title.pack_forget()
    
    #definition of listview (or treeview) and scrollbar widget
    list_all=ttk.Treeview(main_window)
    list_all.pack_forget()
    vsb = ttk.Scrollbar(main_window, orient="vertical", command=list_all.yview)
    list_all.configure(yscrollcommand=vsb.set)
    vsb.pack_forget()
    
    #definition of button
    button = tk.Button(main_window,text="Write to file",fg="black",pady=5,width=14,font=('Tahoma', '11'))
    button.pack_forget()

    #definition of function that returns all movies (250) list
    def all_movies_screen():
        main.pack_forget()
        onelabel.pack_forget()
        aboutlabel.pack_forget()
        user_input.pack_forget()
        watermark.pack_forget()
        search_button.pack_forget()
        list_all["columns"]=("rating",)
        list_all.column("#0", width=500, minwidth=500, stretch=tk.NO)
        list_all.heading("#0",text="Movie name",anchor=tk.CENTER)
        list_all.heading("rating", text="IMDB rating",anchor=tk.CENTER)
        vsb.pack(side='right', fill='y')
        title.config(bg='#0c9463', fg="White", font=("Consolas", 12))
        title.pack(side='top',pady=5)
        
        # get all data
        for name, rating in zip(movie_names, ratings): #zip is used for iterating over two variable at the same time
            name=name.text
            rating=rating.text
            name=name.strip()
            name=name.replace('\n','')
            rating=rating.strip()
            rating=rating.replace('\n','')
            values=list()
            list_all.insert('', 'end', text=name,values=(rating))
            year=re.findall('\((.*?)\)',name)
            only_name=name.split("(")[0]
            for i in year:
                values.append(i)
            values.append(rating)
            all_movies[only_name]=values
            
            #all movies is my full nested (to get max point :)) dictionary that contains all data                    
        list_all.configure(yscrollcommand=vsb.set)
        list_all.pack(side=tk.BOTTOM,fill=tk.Y)
        
        #function that creates and writes data to external txt file (find txt file in project directory)
        def get_backup():
            myfile=open('movies.txt','w')
            myfile.write("/* IMDB movies and ratings application. */ \n /* Author:Bakhtiyar Garashov */ \n")
            for name,rating in all_movies.items():
                myfile.write("{} {} \n".format(name,rating))
            myfile.close()
        button.config(command=lambda:get_backup())
        button.pack(side='bottom',pady=15)
    
    #definition of find a movie by name window
    def one_movie_screen():
        main.pack_forget()
        aboutlabel.pack_forget()
        watermark.pack_forget()
        list_all.pack_forget()
        vsb.pack_forget()
        button.pack_forget()
        title.pack_forget()
        user_input.pack(side='left',ipady=7,ipadx=5,padx=5)
        
        #function that returns a movie and its data to user as popup window
        def find_specific():
             for i,z in all_movies.items():
                i=i.split()
                i=" ".join(i[1:])
                searchable_collection[i]=z
             given_name=user_input.get()
             if given_name in searchable_collection.keys():
                 x=searchable_collection[given_name]
                 messagebox.showinfo("Found succesfully","Movie name: {}\nYear: {} \nIMDB rating: {}".format(given_name,x[0],x[1]))
             else:
                 messagebox.showerror("Oops :/","There is no matching information about {}".format(given_name))
        
        search_button.config(command=lambda:find_specific())
        search_button.pack(side='right',padx=20)
        onelabel.config(bg='#0c9463', fg="White", font=("Courier", 10))
        onelabel.pack(side='left')

    #creates about screen to give additional information
    def about_screen():
        main.pack_forget()
        onelabel.pack_forget()
        list_all.pack_forget()
        vsb.pack_forget()
        user_input.pack_forget()
        button.pack_forget()
        search_button.pack_forget()
        watermark.pack_forget()
        title.pack_forget()
        aboutlabel.config(bg='#0c9463', fg="White", font=("Cambria", 13))
        aboutlabel.pack()

    #to set center geometry of window on the screen
    def center(win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    #creates upper menu
    def create_menu(win_name):
        menubar = Menu(win_name)
        menubar.add_command(label="Get all movies", command=all_movies_screen)
        menubar.add_command(label="Find movie by name", command=one_movie_screen)
        menubar.add_command(label="About", command=about_screen)
        menubar.add_command(label="Exit", command=main_window.destroy)
        return menubar


    menu1 = create_menu(main_window)
    main_window.config(menu=menu1)
    center(main_window)
    main_window.mainloop()

#if something unexpected happens
except Exception as e:
    print(e)




