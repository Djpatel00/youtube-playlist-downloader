import time
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from urllib.error import URLError
from pytube import Playlist,request
from pytube import YouTube
import threading
import os
import win32clipboard
import re



load_1=0

class Playlist_downloader(Frame):
    
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        create_main()
        self.main_frame = None
        self.hover_frame=None
        self.create_hoverframe()
        self.createwidgits()
        self.create_scrollbar()
        #status label
        self.status_label = Label(self.master, text="Status ", font=("arial",17, "bold"),bg='#282828', fg='#fff')
        self.status_label.place(x=370, y=240)
        self.status= Label(self.master, text="Welcome", font=("arial",13, "bold"),width=27,anchor="w",bg='#919191')
        self.status.place(x=450, y=245)

    # create scrollbar
    def create_scrollbar(self):
        # Creating main frame
        if self.main_frame == None:
            self.main_frame= Frame(self.master,highlightthickness=4)
            self.main_frame.place( x=50, y=310, width=676, height=220)

        # Create Canvas
        self.my_Canvas= Canvas(self.main_frame,bg='#919191')
        self.my_Canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add Scrollbar to canvas
        self.m_sc = Scrollbar(self.main_frame, orient = VERTICAL, command=self.my_Canvas.yview)
        self.m_sc.pack(side=RIGHT, fill=Y)

        # Configure Canvas
        self.my_Canvas.configure(yscrollcommand=self.m_sc.set)
        self.my_Canvas.bind('<Configure>', lambda e: self.my_Canvas.configure(scrollregion= self.my_Canvas.bbox("all")))

        def _bind_to_mousewheel(event):
            self.my_Canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_from_mousewheel(event):
            self.my_Canvas.unbind_all("<MouseWheel>")  

        self.my_Canvas.bind('<Enter>', _bind_to_mousewheel)
        self.my_Canvas.bind('<Leave>', _unbind_from_mousewheel)

        # For MouseWheel
        def _on_mousewheel(event):
            self.my_Canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        #Create another frame inside Canvas
        self.second_frame= Frame(self.my_Canvas,bg='#919191')

        #Add new frame
        self.my_Canvas.create_window((0,0),window=self.second_frame,anchor='nw')

    # create widgets
    def createwidgits(self):
        self.link_label = Label(self.master,text="Enter Url           :", font=("arial",11, "bold"),bg='#282828', fg='#fff')
        self.link_label.place(x=50,y=135)

        # creating a entry point
        self.link_text = Entry(self.master,width=49 ,relief= RIDGE  ,insertbackground= "red",font=("arial",12), textvariable=video_link)
        self.link_text.delete(0,END)
        self.link_text.place(x=180,y=137)

        #paste button
        pbtn1 = Button( self.master, image=bg3,text=" Paste   ",compound="left",font=('arial',11,"bold"), command=self.paste_text, bg='red')
        pbtn1.place(x=635, y=132)
       

        # creating a destination label
        destination_label = Label(self.master,text="Choose folder :", font=("arial",11, "bold"),bg='#282828', fg='#fff')
        destination_label.place(x=50,y=178)

        # creating a destination box
        show_destination = Entry(self.master,width=49,font=("arial",12),insertbackground= "red",textvariable=Download_path)
        show_destination.delete(0,END)
        show_destination.place(x=180, y=178)
        
        #browse buttons
        browse_but = Button(self.master, text="Browse",image=bg2,compound="left", command=self.browse, relief=RAISED , font=('Helvetica',11,"bold"),bg='red',padx=3)
        browse_but.place(x=635, y=175)

        #create fetch button
        self.fetch_1 = Button(self.master, image=y1, compound="left", text=" Fetch ", command=self.validation,relief=RAISED , font=("arial",11, "bold"),bg='red')
        self.fetch_1.place(x=50, y=210)

    #paste button
    def paste_text(self):
        self.link_text.configure(state=NORMAL)
        self.link_text.delete(0, END)
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        self.link_text.insert(0, data)

    #Validation
    def validation(self):
        
        self.change_status("Checking...")
        global url,folder
        url = video_link.get()
        folder = Download_path.get()

        if url == "":
            self.change_status("Empty url box","yellow")
            return messagebox.showerror("Error",f"Enter the PLAYLIST LINK.")

        if folder == "":
            self.change_status("Folder not selected","yellow")
            return messagebox.showerror("Error",f"Select the Destination folder.")
        
        var=os.path.isdir(folder)
        if var==False:
            self.change_status("Incorrect Folder Path","yellow")
            return messagebox.showerror("Error",f"Please give correct folder path, or use BROWSE Button.")
        
        self.change_status("Checking URL...")
        
        threading.Thread(target=self.check_url).start()
        
        threading.Thread(target=Slide).start()
    
    #change status
    def change_status(self,var,var2="#919191"):
        self.status.config(text=var,bg=var2)
    
    #Check video url is valid or not
    def check_url(self):
        p=Playlist(url)
        try:
            sum=0
            for video in p.videos:
                if sum>0:
                    break
                video.streams.get_lowest_resolution()
                sum+=1
            self.check_ok(1)
        except URLError:
            time.sleep(3)
            finish_slide()
            self.check_ok(0)
            self.change_status("No Internet","yellow")
            return  messagebox.showerror("Error",f"Please turn on Internet.")
        except KeyError:
            time.sleep(3)
            finish_slide()
            self.check_ok(0)
            self.change_status("URL Not Valid","yellow")
            return  messagebox.showerror("Error",f"Please give a valid playlist link or try YOUTUBE downloader.")

    def check_ok(self,var):
        if var == 0:
            return
        i=0
        self.fetch_1.destroy()
        p=Playlist(url)
        v=p.videos[0].streams.filter(type="video",progressive=True)
        self.radio_frame=Frame(self.master)
        for item in v:
            self.R1 = Radiobutton(self.radio_frame, text=item.resolution, font=("arial",11, "bold"), variable=quality,bg='#282828', fg='#fff', value=item.itag,selectcolor="black",width=6)
            self.R1.grid(row=0, column=i)
            i+=1

        finish_slide()
        self.radio_frame.place(x=50, y=210)
        self.change_status("Select Quality")                
        
        self.R1.select()
        # create a download all button
        self.download_but1 = Button(self.master, image=a1, compound="left", text=" Download ALL ", command=lambda: self.change_check_v(1) ,relief=RAISED , font=("arial",11, "bold"),bg='red')
        self.download_but1.place(x=50, y=245)
        
        # create a download selected button
        self.download_but2 = Button(self.master, image=a2, compound="left", text="  Select  ", command=lambda: self.change_check_v("h") ,relief=RAISED , font=("arial",11, "bold"),padx=4,bg='red')
        self.download_but2.place(x=195, y=245)

    def change_check_v(self,var):
        self.check_v=var
        messagebox.showwarning("Warning","If the size is not found, highest quality video will be downloaded for the particular video.")
        self.call_download()

    def call_download(self):
        if type(self.check_v) == int:
            threading.Thread(target=self.download_all).start()
            print("all")
        else:
            print("selected")
            threading.Thread(target=self.download_selected_videos).start()
    
    # define browse button function
    def browse(self):
        # set directory
        downlaod_dir = filedialog.askdirectory(initialdir="Downlaod path")
        Download_path.set(downlaod_dir)

    def change_value_cancel(self,var):
        var.config(state=DISABLED)
        self.all_cancel=True
        global is_cancelled
        is_cancelled=True

    #creating downloading labels
    def create_downl_labels(self):
        self.create_hoverframe()
        #creating labels
        L2 = Label(self.hover_frame,text = "Sr. No.",font=("Arial", 10, "bold"), width=5,bg='#ff0000',fg='#fff')
        L2.grid(row=0,column=0,padx=1,pady=3)

        L2 = Label(self.hover_frame,text = "Status",font=("Arial", 10, "bold"), width=20,bg='#ff0000',fg='#fff')
        L2.grid(row=0,column=1,padx=1,pady=3)
                
        L3 = Label(self.hover_frame,text = "Title", font=("Arial", 10, "bold"), width=44,bg='#ff0000',fg='#fff')
        L3.grid(row=0,column=2,padx=1,pady=3)
        
        L4 = Label(self.hover_frame,text = "Cancel", font=("Arial", 10, "bold"), width=8,bg='#ff0000',fg='#fff')
        L4.grid(row=0,column=3,padx=1,pady=3)
     
    #download all videos
    def download_all(self):
        self.initialize_download()
        p = Playlist(url)
        video_quality=quality.get()
        self.all_cancel=False
        #creating labels
        self.create_downl_labels()

        self.change_status("Connecting...")
        change_load_var(1)
        self.sum=0
        self.Cancel_b=Button(self.master,image=cross, compound="left", command=lambda: self.change_value_cancel(self.Cancel_b),text=" Cancel ALL  ",font=("Arial", 11, "bold"),bg='#ff0000',relief="raised",)
        self.Cancel_b.place(x=50, y=537)
        self.length_=0
        global is_cancelled
        i=1
        threading.Thread(target=load_animation, args=[1]).start()
            
        for video in p.videos:
            if self.all_cancel:
                self.stop_download('Download Cancelled','Yellow')
                return
            else:
                is_cancelled=False

            filename="\\"+re.sub("[^a-zA-Z0-9 \.]", "", video.title)
            
            try:
                stream = video.streams.get_by_itag(video_quality)
            except:
                stream = video.streams.get_highest_resolution()

            self.change_status("Connecting...")
            self.download_with_size(i,filename,stream)
                
            i+=1
                
        self.stop_download('Successfully Downloaded All','#0a5d00')

    def stop_download(self,text,colour):
        self.Cancel_b.destroy()
        global is_cancelled
        is_cancelled=True
        self.change_status(text,colour)
        change_load_var(0)
        time.sleep(3)
        after_download(round(self.sum, 2), self.length_,folder,10)

    def download_with_size(self,i,filename,stream):

        #Making new labels                
        L2 = Label(self.second_frame,text = i,fg='#fff',font=("arial",10,"bold"), bg='#282828', width=5)
        L2.grid(row=i,column=0,padx=1,pady=2)
    
        C1 = Label(self.second_frame, bg='#282828',fg='#fff',font=("arial",10), text="Downloading...",width=20)
        C1.grid(row=i,column=1,padx=1,pady=2)
        
        L3 = Label(self.second_frame,text = filename[1:],fg='#fff',font=("arial",10), bg='#282828', width=44, anchor="w")
        L3.grid(row=i,column=2,padx=1,pady=3)

        L4 = Button(self.second_frame,text = "Cancel", width=10,font=("arial",8),bg='#282828',fg='red',command=lambda:cancel_download(L4))
        L4.grid(row=i,column=3,padx=1,pady=1)

        self.my_Canvas.configure(scrollregion=self.my_Canvas.bbox("all"))
        try:
            filesize = add1(stream.filesize)  # get the video size
            file_path=f'{folder}{filename}.mp4'
            
            with open(file_path, 'wb') as f:
                        
                stream = request.stream(stream.url) # get an iterable stream
                downloaded = 0
                self.change_status("Downloading...")
                while True:
                    if is_cancelled:
                        C1.config(text = 'Download cancelled')
                        L4.config(state=DISABLED)
                        self.sum+=0
                        f.close()
                        os.remove(file_path)
                        break
                
                    chunk = next(stream, None) # get next chunk of video
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        C1['text'] = f'Downloaded {add1(downloaded)} / {filesize}'
                        self.master.update_idletasks()
                    else:
                        C1.config(bg='#0a5d00',fg='#fff', text=f"Downloaded {filesize} MB")  
                        L4.config(state=DISABLED)
                        self.length_+=1
                        self.sum+=filesize 
                        break
                    print('done')
                
        except Exception as e:
                    print(e)

    #download selected videos
    def download_selected_videos(self):
        # define scrobar ---------------------------------------
        self.initialize_download()
        self.change_status("Fetching Videos...")
        self.stop_size=0
        print("In the second fun")
        
        self.p=Playlist(url)
        
        cover_button()

        global length
        length = len(self.p.videos)

        self.create_hoverframe()
        #creating title labels
        self.tem_L1 = Label(self.hover_frame,text = "Sr. No.",font=("Arial", 10, "bold"), width=5,bg='#ff0000',fg='#fff')
        self.tem_L1.grid(row=0,column=0,padx=1,pady=3)

        self.tem_L2 = Label(self.hover_frame,text = "CheckBox",font=("Arial", 10, "bold"), width=8,bg='#ff0000',fg='#fff')
        self.tem_L2.grid(row=0,column=1,padx=1,pady=3)
                
        self.tem_L3 = Label(self.hover_frame,text = "Title", font=("Arial", 10, "bold"), width=56,bg='#ff0000',fg='#fff')
        self.tem_L3.grid(row=0,column=2,padx=1,pady=3)

        self.tem_L4 = Label(self.hover_frame,text = "Size", font=("Arial", 10, "bold"), width=8,bg='#ff0000',fg='#fff')
        self.tem_L4.grid(row=0,column=3,padx=1,pady=3)

        i=0
        
        for video in self.p.videos:
            
            self.change_status("Fetching Videos...")
            check.append(f"c{i}")
            check[i]=StringVar()

            #creating data labels
            L2 = Label(self.second_frame,text = i+1, width=5,font=("Arial", 10, "bold"),bg='#282828',fg='#fff')
            L2.grid(row=i+1,column=0,pady=1,padx=1, sticky='w')
        
            globals()[f"C{i}"] = Checkbutton(self.second_frame, variable = check[i],bg='#282828',fg='#fff', onvalue = video.watch_url, offvalue = "",width=6,  selectcolor="red")
            globals()[f"C{i}"].grid(row=i+1,column=1,pady=1,padx=1)
            
            L3 = Label(self.second_frame,text =video.title, width=56,font=("Arial", 10), anchor="w",bg='#282828',fg='#fff')
            L3.grid(row=i+1,column=2,pady=1,padx=1)
            dict[f"{video.watch_url}"]=i+1
            L4 = Button(self.second_frame,text = f"Fetch", width=9,bg='#282828',fg='#fff')
            L4.config(command=lambda l = video.watch_url,z = i+1: threading.Thread(target=self.fetch_size, args=[l,z]).start() )
            L4.grid(row=i+1,column=3,pady=1,padx=1)

            self.my_Canvas.configure(scrollregion=self.my_Canvas.bbox("all"))
            i+=1

        self.change_status("Videos Fetched Successful")
        self.B1=Button(self.master,image=d1, compound="left", text=" Download   ",font=("Arial", 11, "bold"),bg='#ff0000',fg='#fff',relief="raised",command=self.sel)
        self.B1.place(x=50, y=537)
        self.B3=Button(self.master,image=b2, compound="left", text="Select all   ",font=("Arial", 11, "bold"),bg='#ff0000',fg='#fff',relief="raised",command=self.select_all)
        self.B3.place(x=175, y=537)
        self.B4=Button(self.master,image=b3, compound="left", text="Deselect all   ",font=("Arial", 11, "bold"),bg='#ff0000',fg='#fff',relief="raised",command=self.deselect_all)
        self.B4.place(x=292, y=537)
        self.B6=Button(self.master,image=b2, compound="left", text=" Custom Select ",font=("Arial", 11, "bold"),bg='#ff0000',fg='#fff',relief="raised",command=self.popup_win)
        self.B6.place(x=427, y=537)
        
        self.B5=Button(self.master,image=b4, compound="left", text=" Fetch all size   ",font=("Arial", 11, "bold"),bg='#ff0000',fg='#fff',relief="raised",command=lambda: threading.Thread(target=self.fetch_all).start())
        self.B5.place(x=580, y=537)
        print(len (check))
    
    def popup_win(self):
  
        tp= Toplevel(root)
        tp.iconbitmap("icon.ico")
        tp.resizable(False, False)
        tp.grab_set()
        tp.geometry("155x152+350+200")
        tp.config(background="#3D0000")
        fp=Frame(tp,height=152,width=155,background="#EEEEEE")
        fp.place(x=0,y=0)
        label = Label(fp,text="Enter Info according to 'Sr. No.'", font=("arial",11, "bold"),bg='#3D0000', fg='#fff', wraplength = 150)
        label.place(x=2,y=7)

        label = Label(fp,text="From  : ",width=7,font=("arial",10, "bold"),bg="#EEEEEE")
        label.place(x=25,y=60)

        label = Label(fp,text= "To      : ",width=7,bg="#EEEEEE",font=("arial",10, "bold"))
        label.place(x=25,y=90)
        
        
        entry1= Entry(fp, width= 7)
        entry1.place(x=85, y=60)
        entry2= Entry(fp, width= 7)
        entry2.place(x=85, y=90)
        entry1.focus()
        
        button1= Button(fp, text="Ok",width=6,font=("arial",10, "bold"), command= lambda: vali(entry1.get(),entry2.get()), bg="#ff0000")
        button1.place(x=90,y=120)

        button1= Button(fp, text="Cancel",width=6,font=("arial",10, "bold"), command=lambda:closewin(tp), bg="#ff0000")
        button1.place(x=7,y=120)
        
        def vali(var1,var2):
                a=var1
                b=var2
                if(a and b):
                    try:
                        a=int(a)
                        b=int(b)
                    except:
                        messagebox.showerror("Error",f"Please enter a Valid Number.")
                        clear_l()
                        return

                    if(a>=b or a<=0 or b<=0):
                        messagebox.showerror("Error",f"Please provide a valid 'RANGE'.")
                        clear_l()
                        return
                    if(b>len(check)):
                        messagebox.showerror("Error",f"Please provide a valid 'RANGE'.")
                        clear_l()
                        return
                    print("hello")
                else:
                    messagebox.showerror("Error",f"Textbox is empty.")
                    clear_l()
                    return
                self.select_custom(a,b,tp)
                

        def clear_l():
            entry1.delete(0,END)
            entry2.delete(0,END)
            entry1.focus()
    
        def closewin(tp):
            tp.grab_release()
            tp.destroy()

    #select all
    def select_all(self):
        for i in range(0,len(check)):
            globals()[f"C{i}"].select()
    
    def select_custom(self,var1,var2,tp):
        tp.destroy()
        for i in range(var1-1,var2):
            globals()[f"C{i}"].select()
    
    #deselect all
    def deselect_all(self):
        for i in range(0,len(check)):
            globals()[f"C{i}"].deselect()

    #fetch all sizes
    def fetch_all(self):
        try:
            for key, value in dict.items():
               threading.Thread(target=self.fetch_size, args=[key,value]).start()
        except:
            print("Exitning due to error.")

    # fetch size
    def fetch_size(self,ur_l,r):
        self.change_status("Fetching Size")
        print("In function fetch")
        p=YouTube(ur_l)
        if(quality.get() == "1"):
            size=p.streams.get_highest_resolution().filesize
            size=add1(size)
        else:
            size=p.streams.get_lowest_resolution().filesize
            size=add1(size)

        
        label=Label(self.second_frame,text = f"{size} MB", width=9,bg='#282828',fg='#fff')
        if self.stop_size == 1:
                return
        label.grid(row=r,column=3,pady=1,padx=1)
        self.change_status("Size Fetched Successfully")
    
    def sel(self):
        thisset = {""}
            
        for j in range(0,length): 
            thisset.add(check[j].get())
                
        thisset.remove("")

        threading.Thread(target=self.download_g,args=[thisset]).start()

    def create_hoverframe(self):
        if self.hover_frame != None:
            self.hover_frame.destroy()

        self.hover_frame= Frame(self.master)
        self.hover_frame.place(x=56,y=285)

    def destroy_tem(self):
        self.stop_size=1
        time.sleep(2)    
        self.B6.destroy()
        self.B1.destroy()
        self.B3.destroy()
        self.B4.destroy()
        self.B5.destroy()
    
    #download selected videos:
    def download_g(self,thisset):
        if len(thisset) == 0:
            self.change_status("No video Selected","yellow")
            return messagebox.showerror("Error",f"Please Select Videos.")
        self.change_status("Downloading...")
        self.destroy_tem()
        self.initialize_download()
        self.length_=0
        self.sum=0
        self.all_cancel=False

        self.Cancel_b=Button(self.master,image=cross, compound="left", command=lambda: self.change_value_cancel(self.Cancel_b),text=" Cancel ALL  ",font=("Arial", 11, "bold"),bg='#ff0000',relief="raised",)
        self.Cancel_b.place(x=50, y=537)


        #creating labels
        self.create_downl_labels()
        global is_cancelled
        i=1
        change_load_var(1)
        threading.Thread(target=load_animation,args=[1]).start()
        
        video_quality=quality.get()

        for video in thisset:
                yt = YouTube(video)

                if self.all_cancel:
                    self.stop_download('Download Cancelled','Yellow')
                    return
                else:
                    is_cancelled=False

                filename="\\"+re.sub("[^a-zA-Z0-9 \.]", "", yt.title)

                try:
                    stream = yt.streams.get_by_itag(video_quality)
                except:
                    stream = yt.streams.get_highest_resolution()                
                
                self.change_status("Connecting...")
                self.download_with_size(i,filename,stream)

                i+=1
    
        self.stop_download('Successfully Downloaded All','#1fc600')
        
      
    #destroy scrollbar    
    def destroy_scrollbar(self):
        self.main_frame.destroy()
        self.main_frame = None

    def initialize_download(self):
        self.destroy_scrollbar()
        self.create_scrollbar()
        self.download_but1.config(state=DISABLED,bg="#919191")
        self.download_but2.config(state=DISABLED,bg="#919191")
        for child in self.radio_frame.winfo_children():
            child.configure(state='disable')


class Video_downloader(Frame):
    
    def __init__(self, master):
        Frame.__init__(self, master)
        
        self.master = master
        create_main()
        self.createwidgits()
        
        #status label
        self.status_label = Label(self.master, text="Status ", font=("arial",17, "bold"),bg='#282828', fg='#fff')
        self.status_label.place(x=370, y=240)
        self.status= Label(self.master, text="Welcome", font=("arial",13, "bold"),width=27,anchor="w",bg='#919191')
        self.status.place(x=450, y=245)

    # create widgets
    def createwidgits(self):
        self.link_label = Label(self.master,text="Enter Url           :", font=("arial",11, "bold"),bg='#282828', fg='#fff')
        self.link_label.place(x=50,y=135)

        # creating a entry point
        self.link_text = Entry(self.master,width=49 ,relief= RIDGE  ,insertbackground= "red",font=("arial",12), textvariable=video_link)
        self.link_text.delete(0,END)
        self.link_text.place(x=180,y=137)

        #paste button
        pbtn1 = Button( self.master, image=bg3,text=" Paste   ",compound="left",font=('arial',11,"bold"), command=self.paste_text, bg='red')
        pbtn1.place(x=635, y=132)
       

        # creating a destination label
        destination_label = Label(self.master,text="Choose folder :", font=("arial",11, "bold"),bg='#282828', fg='#fff')
        destination_label.place(x=50,y=178)

        # creating a destination box
        show_destination = Entry(self.master,width=49,font=("arial",12),insertbackground= "red",textvariable=Download_path)
        show_destination.delete(0,END)
        show_destination.place(x=180, y=178)
        
        #browse buttons
        browse_but = Button(self.master, text="Browse",image=bg2,compound="left", command=self.browse, relief=RAISED , font=('Helvetica',11,"bold"),bg='red',padx=3)
        browse_but.place(x=635, y=175)

        self.fetch = Button(self.master, image=y1, compound="left",text=" Get Link  ", command=self.validation,relief=RAISED , font=("arial",11, "bold"),bg='red')
        self.fetch.place(x=50, y=210)

    #change staus label    
    def change_status(self,var,var2="#919191"):
        self.status.config(text=var,bg=var2)
 
    #paste button
    def paste_text(self):
        self.link_text.configure(state=NORMAL)
        self.link_text.delete(0, END)
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        self.link_text.insert(0, data)

    # define browse button function
    def browse(self):
        # set directory
        downlaod_dir = filedialog.askdirectory(initialdir="Downlaod path")
        Download_path.set(downlaod_dir)

        #Validation
    def validation(self):
        self.fetch.config(state=DISABLED)
        self.change_status("Checking...")
        global url,folder
        url = video_link.get()
        folder = Download_path.get()
        
        if url == "":
            self.fetch.config(state=NORMAL)
            self.change_status("Empty url box","yellow")
            return messagebox.showerror("Error",f"Enter the PLAYLIST LINK.")

        if folder == "":
            self.fetch.config(state=NORMAL)
            self.change_status("Folder not selected","yellow")
            return messagebox.showerror("Error",f"Select the Destination folder.")
        
        var=os.path.isdir(folder)
        if var==False:
            self.fetch.config(state=NORMAL)
            self.change_status("Incorrect Folder Path","yellow")
            return messagebox.showerror("Error",f"Please give correct folder path, or use BROWSE Button.")
        threading.Thread(target=self.fetch_size).start()
    
    def fetch_size(self):
        #create quality buttons
        global js
        js = 4
        global yt
        try:          
            yt = YouTube(url)
        except:
            self.fetch.config(state=NORMAL)
            self.change_status("InValid URL","yellow")
            return messagebox.showerror("Error",f"Please enter a valid Youtube URL.")

        self.change_status("Fetching Resolution...")
        
        
        self.frame_1 = Frame(self.master,bg="#282828")
        self.frame_1.place(x=50,y=210)
        threading.Thread(target=Slide).start()
        i=0
        try:
            for item in yt.streams.filter(type="video",progressive=True):
                tag=item.itag
                size=add1(yt.streams.get_by_itag(tag).filesize)
                self.R1 = Radiobutton(self.frame_1, text=f"{item.resolution} \t({size} MB)", font=("arial",11, "bold"), variable=quality,bg='#282828', fg='#fff', value=tag,selectcolor="black")
                self.R1.grid(row=i,column=0,padx=2,pady=3)
                i+=1
        except URLError:
            finish_slide()
            self.fetch.config(state=NORMAL)
            self.change_status("NO Internet","yellow")
            return messagebox.showerror("Error",f"Please turn on Internet.")
        self.R1.select()

        if self.fetch != None:
            self.fetch.destroy()
        
        finish_slide()
        # create a download  button
        self.download_but1 = Button(self.master,image=d1, compound="left", text=" Download  ", command=threading.Thread(target=self.download).start,relief=RAISED , font=("arial",11, "bold"),bg='red')
        self.download_but1.place(x=50, y=500)
        self.change_status("Select Quality")
        print(quality.get())

    def download(self):
        self.download_but1.destroy()

        self.Cancel_b=Button(self.master,image=cross, compound="left", command=lambda:cancel_download(self.Cancel_b),text=" Cancel ",font=("Arial", 11, "bold"),bg='#ff0000',relief="raised",)
        self.Cancel_b.place(x=50, y=500)

        # print(quality.get())
        stream=yt.streams.get_by_itag(quality.get())
        self.filename="/"+re.sub("[^a-zA-Z0-9 \.]", "", yt.title)
        
        filesize = add1(stream.filesize)  # get the video size
        file_path=f'{folder}{self.filename}.mp4'

        self.change_status(f"Downloading...")

        for child in self.frame_1.winfo_children():
                child.configure(state='disable')

        global is_cancelled
        is_cancelled=False
        global stop_
        stop_=0
        self.create_l()
        self.sum=0
        change_load_var(1)
        threading.Thread(target=load_animation,args=[1]).start()
        threading.Thread(target=self.loading).start()
        try:
            
            with open(file_path, 'wb') as f:
              
                stream = request.stream(stream.url) # get an iterable stream
                downloaded = 0
                self.change_status("Downloading...")
                while True:
                    if is_cancelled:
                        self.change_status("Download Cancelled.","yellow")
                        self.load_3.config(text = 'Download cancelled')
                        self.length_=0
                        self.sum=0
                        f.close()
                        os.remove(file_path)
                        break
                
                    chunk = next(stream, None) # get next chunk of video
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        self.load_3['text'] = f'Downloaded {add1(downloaded)} / {filesize}'
                        self.master.update_idletasks()
                    else:
                        self.length_=1
                        self.change_status("Downloaded Successfully.","#1fc600") 
                        self.sum=filesize   
                        break
                    print('done')
        except Exception as e:
            print(e)
        change_load_var(0)
        stop_=1
        
        after_download(self.sum, self.length_,folder,1)
        
    def loading(self):
        if stop_==1:
            self.destroy_l()
            return
        
        self.load_.config(image=c1)
        self.master.update_idletasks()
        time.sleep(1)
        self.load_.config(image=c2)
        self.master.update_idletasks()
        time.sleep(1)
        self.load_.config(image=c3)
        self.master.update_idletasks()
        time.sleep(1)
        self.load_.config(image=c4)
        self.master.update_idletasks()
        time.sleep(1)
        self.load_.config(image=c5)
        self.master.update_idletasks()
        time.sleep(1)
        self.load_.config(image=c6)
        self.master.update_idletasks()
        time.sleep(1)
        
        self.loading()
    
    def create_l(self):
        self.load_ = Label(self.master,bg="#282828")
        self.load_.place(x=388,y=417)
        self.load_2 = Label(self.master,bg="#282828",text="Downloading",font=("arial",20,"bold"),fg="yellow")
        self.load_2.place(x=210,y=400)
        self.load_3 = Label(self.master,bg="#282828", font=("arial",14,"bold"),fg="#fff")
        self.load_3.place(x=250,y=370)
        
    def destroy_l(self):
        self.load_.destroy()
        self.load_3.destroy()
        self.Cancel_b.destroy()
        if self.sum !=0:
            self.load_2.config(text="Filename  :",font=("arial",20,"bold"),fg="#fff")
            self.btn = Button(self.master, text="View",fg="#fff",bg="red",font=("arial",13,"bold"),width=10,command=lambda: messagebox.showinfo("information",f"Filename: {self.filename[1:]}.mp4") )
            self.btn.place(x=370,y=402)
        else:
            self.load_2.config(text= "Download Cancelled.")

def finish_slide():
    global load_frameS
    global slide_load
    try:   
        if load_frameS != None:
                slide_load.destroy()
                slid_load__ = Label(load_frameS,image=load7)
                slid_load__.place(x=190,y=250)
                time.sleep(1)
                load_frameS.destroy()
    except Exception as e:
        print("caught error", e)

#7 seconds sleep
def Slide():
        global load_frameS
        global slide_load
        load_frameS= Frame(root,bg = '#add123')
        load_frameS.grid(row=0,column=0)
        load=Label(load_frameS, image=load_img)
        load.grid(row=0,column=0)
        slide_load = Label(load_frameS,image=load1 )
        lod= Label(load_frameS,text="Checking URL... Please Wait",font=("arial", 20, "bold"),bg="#919191")
        lod.place(x=200, y=303)
      
        slide_load.place(x=190,y=250)
        root.update_idletasks()
        time.sleep(2)
        try:
            slide_load.config(image=load2)
            root.update_idletasks()
            time.sleep(3)
            slide_load.config(image=load3)
            root.update_idletasks()
            time.sleep(3)
            slide_load.config(image=load4)
            root.update_idletasks()
            time.sleep(3)
            slide_load.config(image=load5)
            root.update_idletasks()
            time.sleep(3)
            slide_load.config(image=load6)
            root.update_idletasks()
            time.sleep(3)
            slide_load.config(image=load7)
            root.update_idletasks()
            time.sleep(3)
            slide_load.destroy()
            load_frameS.destroy()
        except:
            print("Deleted Successfully.")

#after download
def after_download(sum, len,folder,var):
        
        messagebox.showinfo("information",f"Your videos are downloaded successfully.\nStorage used: {sum} MB\nItems Downloaded: {len} ")
        B2=Button(root,image=t1, compound="left", text="   Finish   ",font=("Arial", 11, "bold"), bg='#0a5d00',fg='#fff',relief="raised",command=lambda : clear(var))
        B2.place(x=50, y=538)
        B1=Button(root,image=bg2,compound="left",text="  Open Folder  ",font=("Arial", 11, "bold"), bg='red', fg='#fff',relief="raised")
        B1.place(x=160, y=537)
        B1.config(command= lambda: os.startfile(folder) )
        B3=Button(root,image=s,compound="left",text="  Show Status  ",font=("Arial", 11, "bold"), bg='red', fg='#fff',relief="raised", command=lambda : messagebox.showinfo("information",f"Your videos are downloaded successfully.\nStorage used: {sum} MB\nItems Downloaded: {len} "))
        B3.place(x=303, y=537)
        
#refresh
def clear(var):
    global check
    global show_label
    global dict
    show_label = {}
    check=[]
    dict = {}
    for item in root.winfo_children():
            item.destroy()
    if var == 1:
        label_bg = Label( root, image = bg_video)
        label_bg.grid(row=0, column=0)
        Video_downloader(root)
    else:
        label_bg = Label( root, image = bg)
        label_bg.grid(row=0, column=0)
        Playlist_downloader(root)

def load_animation(var):
    global load_1
    if load_1==0:
        print("returning")
        return
    load_frame = Frame(root, bg="#282828")
    load_frame.place(x=0,y=80)
    global after_load    
    
    if var==1:
        after_load = Label(load_frame,image=z9,borderwidth=0)
        after_load.grid(row=0,column=0)
        root.update_idletasks()
        time.sleep(2)
    
        after_load.config(image=z1)
        root.update_idletasks()
        time.sleep(2)
        after_load.config(image=z2)
        root.update_idletasks()
        time.sleep(1)
        after_load.config(image=z3)
        root.update_idletasks()
        time.sleep(1)
    
        after_load.config(image=z4)
        root.update_idletasks()
        time.sleep(1)
    
    after_load.config(image=z8)
    root.update_idletasks()
    time.sleep(1)
    after_load.config(image=z5)
    root.update_idletasks()
    time.sleep(1)
    after_load.config(image=z6)
    root.update_idletasks()
    time.sleep(1)
    after_load.config(image=z7)
    root.update_idletasks()
    time.sleep(1)
    load_animation(var+1)
    
def change_load_var(var):
    global load_1
    load_1=var

def add1(sum):
    return round(sum/1048576,2)

def create_main():
    
    # creating playlist button
    playlist_button= Button(root, text="Playlist Downloader", font=("helvetica",12, "bold"),bg='#282828', width=32,command=lambda : clear(10), fg='#f00',padx=1)
    playlist_button.place(x=50,y=85)
    # creating video button
    video_button= Button(root, text="Video Downloader", font=("helvetica",12, "bold"),bg='#282828', width=33,command=lambda: clear(1), fg='#f00')
    video_button.place(x=385,y=85)

def cover_button():
    global temp_frame
    temp_frame=Frame(root,width=676,height=35,bg="#282828",highlightthickness=0)
    temp_frame.place(x=50,y=85)

    But2=Button(temp_frame,image=b, compound="left",text=" Back    ",font=("Arial", 11, "bold"), bg='yellow',relief="raised",command=lambda :clear(10))
    But2.place(x=0,y=0)

def cancel_download(var):
    var.config(state=DISABLED)
    global is_cancelled
    is_cancelled = True

# Creating object
root = Tk()
root.iconbitmap("icon.ico")

# size of the window
root.geometry('772x578+200+50')  
root.title('YTube Downloader')  
root.resizable(False, False)

# name of the window
root.title("Playlist Downloader")

# Setting Background Image
bg= PhotoImage(file="images\ytimage.png")
bg2= PhotoImage(file="images/older.png")
bg3= PhotoImage(file ="images/paste.png")
load_img= PhotoImage(file = "images/loading.png")
load1= PhotoImage(file = "images/l1.png")
load2= PhotoImage(file = "images/l2.png")
load3= PhotoImage(file = "images/l3.png")
load4= PhotoImage(file = "images/l4.png")
load5= PhotoImage(file = "images/l5.png")
load6= PhotoImage(file = "images/l6.png")
load7= PhotoImage(file = "images/l7.png")
bg_video= PhotoImage(file="images\ytimage1.png")
c1 = PhotoImage(file="images\c1.png")
c2 = PhotoImage(file="images\c2.png")
c3 = PhotoImage(file="images\c3.png")
c4 = PhotoImage(file="images\c4.png")
c5 = PhotoImage(file="images\c5.png")
c6 = PhotoImage(file="images\c6.png")
a2 = PhotoImage(file="images\\a2.png")
a1 = PhotoImage(file="images\\a1.png")
d1 = PhotoImage(file="images\\d1.png")
y1 = PhotoImage(file="images\\y1.png")
t1 = PhotoImage(file="images\\t1.png")
b = PhotoImage(file="images\\b.png")

z1 = PhotoImage(file="images\\z1.png")
z2 = PhotoImage(file="images\\z2.png")
z3 = PhotoImage(file="images\\z3.png")
z4 = PhotoImage(file="images\\z4.png")
z5 = PhotoImage(file="images\\z5.png")
z6 = PhotoImage(file="images\\z6.png")
z7 = PhotoImage(file="images\\z7.png")
z8 = PhotoImage(file="images\\z8.png")
z9 = PhotoImage(file="images\\z9.png")

b2 = PhotoImage(file="images\\b2.png")
b3 = PhotoImage(file="images\\b3.png")
b4 = PhotoImage(file="images\\b4.png")

s = PhotoImage(file="images\\s.png")
cross = PhotoImage(file="images\\cross.png")

# ---------------------
quality = StringVar()
# show_label = {}
# check=[]
# dict = {}
video_link = StringVar()
Download_path = StringVar()


clear(10)




root.mainloop()