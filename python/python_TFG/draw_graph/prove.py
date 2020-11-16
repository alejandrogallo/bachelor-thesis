import tkinter;
import dgraph;

def callback():
    if type(int(E1.get())) is int:
        if int(E1.get())<=6:
            dgraph.construct_graph(int(E1.get()));
def callin():
    print(type(int(E1.get())) );

top = tkinter.Tk();




L1 = tkinter.Label(top, text="Graph dimension")

E1 = tkinter.Entry(top, bd =2);

E1.pack(side = 'right');
L1.pack( side = 'left');

tkinter.Frame(master = top, width=200, height=200, bg="", colormap="new").pack();


b = tkinter.Button(top, text = 'Create graph', command = callback, padx = 100);
c = tkinter.Button(top, text = 'Exit', command = quit, padx = 100);

b.pack(side = 'left');
c.pack(side = 'right');

tkinter.Frame(master = top, width=100, height=100, bg="", colormap="new").pack();


top.mainloop(
    );

