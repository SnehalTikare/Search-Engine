import tkinter as tk
from query_processing import *
import webbrowser
window = tk.Tk()
#window.geometry("600x600+300+200")
 
# Gets the requested values of the height and widht.
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()
 
# Gets both half the screen width/height and window width/height
positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(window.winfo_screenheight()/3 - windowHeight/2)
 
# Positions the window in the center of the page.
window.geometry("+{}+{}".format(positionRight, positionDown))
window.title("UIC's search engine")
frame_1 = tk.Frame(master=window,relief=tk.GROOVE, borderwidth=5,width=600, height=600)
def add_href(url):
        # return '<a href="' + url + '">' + url + '</a>' + '<pre> Score : ' + str(score) + '</pre><br>'
        return '<a href="' + url + '">' + url + '</a><br><br>'
def display():
    """Print the character associated to the key pressed"""
    user_query = user_input.get()
    #result["text"] = user_query
    query=[]
    query.append(user_query)
    top_links = get_result(query)
    frame_2 = tk.Frame(master=window,relief=tk.RAISED, borderwidth=5)
    for index,link in enumerate(top_links) :
        #url = add_href(link)
        lb = tk.Label(master = frame_1, text=link)
        lb.grid(row=index+6,column=1)
        lb.bind("<Button-1>", lambda event: webbrowser.open(lb["text"]))
        #lb.pack()
   
#frame_1 = tk.Frame(master=window,relief=tk.GROOVE, borderwidth=5)
title = tk.Label(master=frame_1,text="Search UIC")
title.grid(row=3,column=1)
#title.place(x=150,y=10)
#title.pack()
user_input = tk.Entry(master = frame_1,width=30)
user_input.grid(row=4,column=1)
#user_input.place(x=70,y=30)
#user_input.pack()

search_button = tk.Button( master = frame_1, text="Search",command=display)
search_button.grid(row=4,column=2)
#search_button.place(x=300,y=30)

#result = tk.Label(master = frame_1,text="")
#result.place(x=70,y=120)

#button.pack()
# Bind keypress event to handle_keypress()
#search_button.bind("<Button-1>", handle_click)
# frame_1.columnconfigure(0, weight=2)
# frame_1.rowconfigure(0, weight=2)
# frame_1.grid(row=0, column=0)
frame_1.pack(fill=tk.BOTH)
window.mainloop()