import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from random import sample

with open("../multithreaded_hangman/common_words.txt") as f:
    words = sample(f.readlines(), 100)
word = words[0].lower().strip()
print(f"word: {word}")


# root (2 rows, 2 columns)
#   |- player_area_frame (n rows, 1 column)
#     |- series of tk.Labels (row=i), for i=0 to n
#   |- game_area
#     |- game drawing
#     |- label with underscores
#   |- chat_area_frame (2 rows, 1 column)
#     |- ScrollableText (row=0)
#     |- text_input_area_frame (row=1, 1 row, 2 columns)
#       |- Entry (column=0)
#       |- Quit Button (column=1)


class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="black")
        self.parent = parent

        self.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(0, minsize=150)

        self.player_status = PlayerStatus(self)
        self.player_status.grid(row=0, rowspan=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.game_area = GameArea(self)
        self.game_area.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)

        self.chat_box = ChatBox(self)
        self.chat_box.grid(row=1, column=1, sticky=tk.W + tk.E + tk.S)

        self.chat_box.user_input.user_entry.bind("<Key-Return>", self.process_entry)
        self.chat_box.user_input.quit_button["command"] = self.quit_application

    def quit_application(self):
        self.parent.destroy()

    def process_entry(self, _event):
        msg = self.chat_box.user_input.entry_var.get().split(',')
        match msg:
            case ["GS", guess]:
                self.update_chat_box(guess)

                if guess == word:
                    self.game_area.update_word(' '.join(word))
                    self.update_chat_box("You got the word!!")

            case ["PS", player_name, player_points]:
                self.player_status.add_adjust_player(player_name, player_points)
        self.chat_box.user_input.entry_var.set("")

    def update_chat_box(self, msg):
        self.chat_box.output_text["state"] = "normal"
        self.chat_box.output_text.insert("end", msg + "\n")
        self.chat_box.output_text["state"] = "disabled"


class PlayerStatus(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="red")
        self.parent = parent

        # let the player labels expand to fill the left bar
        self.columnconfigure(0, weight=1)

        # Player names and scores
        self.players = dict()

    def add_adjust_player(self, player_name, player_points):
        if player_name not in self.players:
            string_var = tk.StringVar(value=f"{player_name}: {player_points}")
            label = tk.Label(self, textvariable=string_var)

            self.players[player_name] = {"label": label, "var": string_var}
            self.players[player_name]["label"].grid(row=len(self.players) - 1, column=0, sticky=tk.W + tk.E)
        else:
            self.players[player_name]["var"].set(f"{player_name}: {player_points}")

        self.sort_players()

    def sort_players(self):
        lis = list(self.players.items())

        lis = sorted(lis, key=lambda p: int(p[1]['var'].get().split(':')[1]), reverse=True)

        for i in range(len(lis)):
            lis[i][1]["label"].grid(row=i)


class GameArea(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="green")
        self.parent = parent
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.timer = Timer(self)
        self.timer.grid(row=0, column=0, sticky=tk.W + tk.E + tk.S)

        # the word
        self.word_var = tk.StringVar(value=' '.join("_" * len(word)))
        self.word_label = tk.Label(self, textvariable=self.word_var)
        self.word_label.grid(row=1, column=0, sticky=tk.W + tk.E + tk.S)

    def update_word(self, new_word):
        self.word_var.set(new_word)


class Timer(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.timer_value = tk.IntVar(value=0)
        self.timer = tk.Label(self, textvariable=self.timer_value)


class ChatBox(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="blue")
        self.parent = parent

        # Chat area with user input and output
        self.rowconfigure("all", weight=1)
        self.columnconfigure(0, weight=1)

        # Chat box with everyone's messages
        self.output_text = ScrolledText(self, height=15, state="disabled")
        self.output_text.grid(row=0, column=0, columnspan=2, sticky=tk.W + tk.E)

        self.user_input = UserInput(self)
        self.user_input.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E)


class UserInput(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # User input frame
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        # user entry and quit button
        self.entry_var = tk.StringVar()
        self.user_entry = tk.Entry(self, textvariable=self.entry_var)
        self.user_entry.grid(row=1, column=0, sticky=tk.W + tk.E)

        # quit button
        self.quit_button = tk.Button(self, text="Quit", width=5)
        self.quit_button.grid(row=1, column=1, sticky=tk.E)


root = tk.Tk()
# second_monitor = "-1600+200"
second_monitor = ""
root.geometry(f"800x400{second_monitor}")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.grid()

MainApplication(root)

root.mainloop()
