from tkinter import *
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#background colour
body="#9EC5AB"
bodyNew="#FAAFBA"
button="#493E31"
text="#255651"

#text colour
headText="#022704"
titleText="#023B1C"
buttonText="#023B1C"
entryText="#BFD9C8"

class contentBasedRecommender:
    def __init__(self, matrix):
        self.similarMatrix = matrix

    def print_message(self, song, recomSong, recomNumber):
    	newRoot = Toplevel(root)
    	newRoot['background']=bodyNew
    	newRoot.title("Recommended Songs for "+str(song))
    	newRoot.geometry("700x600")
    	
    	f1=Frame(newRoot, bg=bodyNew)
    	f1.pack(fill="x", padx=50, pady=30)

    	state = "The "+ str(recomNumber)+" recommended songs for \""+str(song)+"\" are:\n"
    	l1=Label(f1, text=state, bg=bodyNew, fg=headText, justify=CENTER, font="comicsansm 20 bold")
    	l1.pack()

    	for i in range(recomNumber):
    		song = "Song " +str(i + 1)+": "+str(recomSong[i][1])
    		artist = "Artist: "+str(recomSong[i][2])
    		link = "Link: "+str(recomSong[i][3])
    		score = "Similarity Score: "+str(round(recomSong[i][0], 3))

    		recom = song + "\n" + artist + "\n" + link + "\n" + score + "\n" + "--------------------"

    		f2=Frame(newRoot, bg=bodyNew)
    		f2.pack(fill="x", padx=50, pady=10)

    		l2=Label(f2, text=recom, bg=bodyNew, fg=headText, justify=CENTER, font="comicsansm 15 bold")
    		l2.pack()

    def recommend(self, recommendation):
        songName = recommendation['songName']
        numberSongs = recommendation['numberSongs']
        recomendedSongs = self.similarMatrix[songName][:numberSongs]

        self.print_message(songName, recomendedSongs, numberSongs)

def model():
    global similarities

    data = pd.read_csv("/Users/arghyabandyopadhyay/Desktop/Music Recomendation System/spotify_millsongdata.csv")
    data = data.sample(n=3000).reset_index(drop=True)

    data['text'] = data['text'].str.replace(r'\n', '', regex=True)
    data['text'] = data['text'].str.replace(r'\r', '', regex=True)

    tfidf = TfidfVectorizer(analyzer='word', stop_words='english')
    lyrics_matrix = tfidf.fit_transform(data['text'])
    cosineMatrix = cosine_similarity(lyrics_matrix)

    for i in range(len(cosineMatrix)): 
        similarIndices = cosineMatrix[i].argsort()[:-50:-1]
        similarities[data['song'].iloc[i]] = [(cosineMatrix[i][x], data['song'][x], data['artist'][x], data['link'][x]) for x in similarIndices][1:]

    songs_list = data['song'].tolist()
    return songs_list

def printResult(event):
	global similarities

	songName = clicked.get()
	num = screen1.get()

	recommedations = contentBasedRecommender(similarities)
	recommendation = {
    	"songName": songName,
    	"numberSongs": int(num)
	}
	
	recommedations.recommend(recommendation)

def reset(event):
	global label1, label2, label3, label4, label5, clicked

	string1.set("")
	screen1.update()
	clicked.set(options[0])

	label1.config(text="Content Based Music Recommendation System")
	label2.config(text="Song Name: ")
	label3.config(text="Number of Recommendation: ")

#initialize
root=Tk()

#title
root.title("Content Based Music Recommendation System")

#background
root['background']=body

#size
root.geometry("600x500")
root.maxsize(600, 500)
root.minsize(600, 500)

#frame1
frame1=Frame(root, bg=body)
frame1.pack(fill="x", padx=50, pady=30)

label1=Label(frame1, text="Content Based Music Recommendation System", bg=body, fg=headText, justify=CENTER, font="comicsansm 20 bold")
label1.pack()

#frame2
frame2=Frame(root, bg=body)
frame2.pack(fill="x", padx=50, pady=10)

label2=Label(frame2, text="Song Name: ", bg=body, fg=titleText, justify=CENTER, font="comicsansm 20 bold")
label2.pack(side=LEFT)
  
# Dropdown menu options
similarities = {}
options = model()

# datatype of menu text
clicked = StringVar()
  
# initial menu text
clicked.set(options[0])
  
# Create Dropdown menu
drop = OptionMenu(frame2, clicked, *options)
drop.pack(fill="x", pady=50)

#frame3
frame3=Frame(root, bg=body)
frame3.pack(fill="x", padx=50, pady=10)

label3=Label(frame3, text="Number of Recommendation: ", bg=body, fg=titleText, justify=CENTER, font="comicsansm 20 bold")
label3.pack(side=LEFT)

string1=StringVar()
string1.set("")
screen1=Entry(frame3, textvar=string1, width=3, font="comicsansm 20 bold", bg=text, borderwidth=2, fg=entryText)
screen1.pack(side=LEFT, fill="x")

#frame6
frame4=Frame(root, bg=body)
frame4.pack(fill="x", pady=30)

button1=Button(frame4, text="Print", fg=buttonText, highlightthickness=6, highlightbackground=button, font="comicsansm 20 bold", padx=14, pady=10, relief="groove")
button1.grid(row=0, column=4, padx= 50)
button1.bind("<Button-1>",printResult)

button2=Button(frame4, text="Reset", fg=buttonText, highlightthickness=6, highlightbackground=button, font="comicsansm 20 bold", padx=14, pady=10, relief="groove")
button2.grid(row=0, column=6, padx= 50)
button2.bind("<Button-1>",reset)


root.mainloop()