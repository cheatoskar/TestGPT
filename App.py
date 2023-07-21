import customtkinter as ctk
from tkinter import ttk
from tkinter import *
import tkinter as tk
from fpdf import FPDF
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog
import fitz

#pip install customtkinter, fpdf, PyPDF2


# Hauptfenster
root = ctk.CTk()
root.geometry(root.geometry("1920x1080"))
root.title("TestGPT")
root.iconbitmap("Icon.ico")
ctk.set_appearance_mode("dark")
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "dark")
# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the size of the window to the screen size
#root.geometry("%dx%d" % (screen_width, screen_height))

# Titel
titel_label = ctk.CTkLabel(root, text="Davinci Modell", font=ctk.CTkFont(size=32, weight="bold"))
titel_label.pack(padx=10, pady=(40, 20))

# Tabview
tabview = ctk.CTkTabview(root, height=800)
tabview.pack(padx=10, pady=10, fill="both", expand=True)

# Erster Tab: Importiere Test
tab1 = tabview.add("Importiere Test")

# Fenster
frame = ctk.CTkScrollableFrame(tab1) # erstelle ein scrollbares Frame
frame.pack(fill="both", expand=True) # packe es mit fill und expand Argumenten

# Ladebalken hinzufügen
progressbar = ctk.CTkProgressBar(
    master = tab1,
    orientation="horizontal",
    mode="indeterminate",
    indeterminate_speed=2,
)

#Ladebalken anzeigen
def show_progressbar():
    progressbar.pack(padx=20, pady=10)
    progressbar.start()
    update_subject_label()
    fill_table()
    
#Ladebalken verstecken
def hide_progressbar():
    progressbar.pack_forget()

# Textfeld für Import
import_textbox = ctk.CTkTextbox(frame, width=300, height=500, font=ctk.CTkFont(size=15)) # packe alle Widgets in das frame Widget
import_textbox.pack(pady=10, fill="x", padx=100)
importiere_test = ctk.CTkButton(frame, text="Importiere Test", command = show_progressbar) # binde die progressbar.start Methode an den Button
importiere_test.pack(padx=100, fill="x", pady=(5, 20))

def pdf_hochladenfunc():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        pdf_document = fitz.open(file_path)
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
        pdf_document.close()

        import_textbox.delete("1.0", tk.END)  # Clear existing text
        import_textbox.insert(tk.END, text)



pdf_hochladen = ctk.CTkButton(frame, text="Lade PDF hoch", command = pdf_hochladenfunc) # binde die progressbar.start Methode an den Button
pdf_hochladen.pack(padx=100)

schulfach_frame = ctk.CTkFrame(frame)
schulfach_frame.pack(padx=100, pady=(20, 5), fill="both")
schulfach_label = ctk.CTkLabel(
    schulfach_frame, text="Schulfach", font=ctk.CTkFont(weight="bold")
)
schulfach_label.pack()

def update_subject_label(*args):
    global selected_subject
    selected_subject = schulfach_dropdown.get()
    subject_label.configure(text=f"Fach: {selected_subject}")
    
    
selected_subject = StringVar(value="Deutsch")   

schulfach_dropdown = ctk.CTkComboBox(
    schulfach_frame, values=["Deutsch", "Geschichte", "Englisch"], variable = selected_subject
)
schulfach_dropdown.pack(pady=10)


difficulty_frame = ctk.CTkFrame(frame)
difficulty_frame.pack(padx=100, pady=5, fill="both")
difficulty_label = ctk.CTkLabel(
    difficulty_frame, text="Bewertungsgrad", font=ctk.CTkFont(weight="bold")
)
difficulty_label.pack()

#Wir definieren die Variable difficulty_value nur einmal und setzen den Anfangswert auf "Kreative"
difficulty_value = ctk.StringVar(value="Standart")

# Wir erstellen drei Radiobuttons und übergeben ihnen dieselbe Variable und unterschiedliche Werte
radiobutton1 = ctk.CTkRadioButton(
    difficulty_frame,
    text="Kreative",
    variable = difficulty_value,
    value="Kreative",
)
radiobutton1.pack(side="top", padx=(20, 10), pady=10)

radiobutton2 = ctk.CTkRadioButton(
    difficulty_frame,
    text="Standart",
    variable = difficulty_value,
    value="Standart",
)
radiobutton2.pack(side="top", padx=(20, 10), pady=10)

radiobutton3 = ctk.CTkRadioButton(
    difficulty_frame,
    text="Genau",
    variable=difficulty_value,
    value="Genau",
)
radiobutton3.pack(side="top", padx=(20, 10), pady=10)

features_frame = ctk.CTkFrame(frame)
features_frame.pack(padx=100, pady=5, fill="both")
features_label = ctk.CTkLabel(
    features_frame, text="Features", font=ctk.CTkFont(weight="bold")
)
features_label.pack()

check_var_box1 = StringVar(value="on")


checkbox1 = ctk.CTkCheckBox(features_frame, text="Trainingsdaten",  variable=check_var_box1, onvalue="on", offvalue="off")
checkbox1.pack(side="top", padx=30, pady=10, )
checkbox2 = ctk.CTkCheckBox(features_frame, text="Internet")
checkbox2.pack(side="top", padx=10, pady=10)








# Zweiter Tab: Ergebnis
tab2 = tabview.add("Ergebnis")


def fill_table(*args):
    # Diese Funktion füllt die Tabelle mit den entsprechenden Fehlerarten
    global selected_subject
    selected_subject = schulfach_dropdown.get()
    # Wir leeren zunächst die Tabelle
    error_table.delete(*error_table.get_children())
    # Wir erstellen ein Wörterbuch mit den Fehlerarten für jedes Fach
    error_types = {"Deutsch": ["Inhalt", "Rechtschreibung", "Zeichensetzung", "Grammatik", "Ausdruck", "Formalien"],
                   "Geschichte": ["Inhalt", "Rechtschreibung", "Zeichensetzung", "Grammatik", "Ausdruck", "Formalien"],
                   "Englisch": ["Inhalt", "Ausdruck", "Sprachrichtigkeit", "Grammatik", "Wortschatz", "Zeichensetzung"]}
    # Wir fügen neue Zeilen in die Tabelle ein mit den Fehlerarten für das ausgewählte Fach
    for error in error_types[selected_subject]:
        error_table.insert("", "end", values=(error, 0, 0))

erreichte_punkzahl = None
gesamtpunkzahl = None
prozent_leistung = None

def punkte_berechnen():
    global erreichte_punkzahl, gesamtpunkzahl, prozent_leistung
    erreichte_punkzahl = 10
    gesamtpunkzahl = 20
    prozent_leistung = (erreichte_punkzahl/gesamtpunkzahl)*100


# lege die Gewichtung der Zeilen und Spalten im Frame fest
tab2.grid_rowconfigure (0, weight=1) # die erste Zeile nimmt den gesamten vertikalen Platz ein
tab2.grid_columnconfigure (0, weight=1) # die erste Spalte nimmt vier Fünftel des horizontalen Platzes ein
tab2.grid_columnconfigure (0, weight=1) # die zweite Spalte nimmt ein Fünftel des horizontalen Platzes ein

result_textbox = ctk.CTkTextbox(tab2, font=ctk.CTkFont(size=15), wrap='word', xscrollcommand=None, yscrollcommand=None, height=0)
result_textbox.grid(rowspan=3, row=0, column=0, sticky=NSEW)
#result_textbox.configure(state='disabled')  # Set the state to DISABLED

# erstelle einen Frame für die Zusammenfassung
summary_frame = ctk.CTkFrame(tab2)
summary_frame.grid(row=0, column=3,columnspan = 3, sticky=NSEW) # positioniere den Frame in der zweiten Zelle des Frames

# lege die Gewichtung der Zeilen und Spalten im Frame fest
summary_frame.grid_rowconfigure (2, weight=1) # die erste Zeile nimmt ein Drittel des vertikalen Platzes ein
summary_frame.grid_rowconfigure (0, weight=2) # die zweite Zeile nimmt zwei Drittel des vertikalen Platzes ein
summary_frame.grid_columnconfigure (0, weight=1) # die einzige Spalte nimmt den gesamten horizontalen Platz ein

subject_label = ctk.CTkLabel(summary_frame, text=f"Fach: {selected_subject.get()}", font=("Calibri", 32))
subject_label.grid(row=0, column=0, sticky=N)

points_label = ctk.CTkLabel(summary_frame, text=f"Punktzahl: {erreichte_punkzahl}/{gesamtpunkzahl}", font=("Calibri", 24))
points_label.grid(row = 0, column = 0, sticky = W)

percent_label = ctk.CTkLabel(summary_frame, text=f"Leistung " + str(prozent_leistung) + "%", font=("Calibri", 24))
percent_label.grid(row = 0, column = 0,)

bundesland_frame = ctk.CTkFrame(summary_frame)
bundesland_frame.grid(row = 0, column = 0, sticky = E)
bundesland_label = ctk.CTkLabel(
    bundesland_frame, text="Klasenstufe", font=ctk.CTkFont(weight="bold")
)
bundesland_label.grid(row = 0, column = 0, sticky = E)
bundesland_dropdown = ctk.CTkComboBox(
    #bundesland_frame, values=["Bayern", "Baden Württemberg", "Berlin", "Brandenburg", "Bremen", "Hamburg", "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen", "Nordrhein Westpfalen", "Rheinland-Pfalz", "Saarland", "Sachsen", "Sachsen-Anhalt", "Schleswig-Hollstein", "Thüringen"]
    bundesland_frame, values=["Bayern"]
)
bundesland_dropdown.grid(row = 0, column = 0, sticky = E)


klasse_frame = ctk.CTkFrame(summary_frame)
klasse_frame.grid(row = 0, column = 0, sticky = NE)
klasse_label = ctk.CTkLabel(
    klasse_frame, text="Klasenstufe", font=ctk.CTkFont(weight="bold")
)
klasse_label.grid(row = 0, column = 0, sticky = E)
klasse_dropdown = ctk.CTkComboBox(
    klasse_frame, values=["Klasse 1-4", "Klasse 5-7", "Klasse 8-10", "Klasse 11-12"]
)
klasse_dropdown.grid(row = 0, column = 0, sticky = E)

grade_label = ctk.CTkLabel(summary_frame, text=f"Oberstufe: ", font=("Calibri", 32))
grade_label.grid(row = 2, column = 0, sticky = NE)

note_label = ctk.CTkLabel(summary_frame, text=f"Note: ", font=("Calibri", 32))
note_label.grid(row = 2, column = 0, sticky = NW)




# erstelle ein Label für die Gesamtpunkte und Note
total_label = ctk.CTkLabel(summary_frame, text = "Punktzahl" + str(  erreichte_punkzahl) + "/" + str(  gesamtpunkzahl), font=("Arial", 24))
total_label.grid(row=1, column=0, sticky=W) # positioniere das Label in der dritten Zelle des Frames


# erstelle eine Tabelle für die Fehlerarten und Punkte
error_table = ttk.Treeview(summary_frame)
error_table.grid(row=1, column=0, sticky=NSEW) # positioniere die Tabelle in der zweiten Zelle des Frames


# definiere die Spalten und Überschriften der Tabelle
error_table["columns"] = ("Fehlerart", "Anzahl", "Abzug")
error_table["show"] = "headings"
error_table.heading("Fehlerart", text="Fehlerart")
error_table.heading("Anzahl", text="Anzahl")
error_table.heading("Abzug", text="Abzug")

def save_to_pdf():
 # Get text to save from result_textbox
    text_to_save = result_textbox.get("1.0", tk.END)
    
    # Get student name from user input
    student_name = simpledialog.askstring("Student Name", "Enter student name:")
    if not student_name:
        return  # Cancelled or empty input
    
    # Get current date
    import datetime
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Create PDF with custom filename
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text_to_save)
    pdf_file_name = f"{student_name}_TestErgebniss_{current_date}.pdf"
    pdf.output(pdf_file_name)
    messagebox.showinfo("PDF wurde gespeichert", f"Text wurde unter {pdf_file_name} gespeichert")

save_to_pdf_button = ctk.CTkButton(summary_frame, text="PDF Speichern", command = save_to_pdf)
save_to_pdf_button.grid(row=3, column = 0, sticky = W)

#Soll spaeter noch die restlichen Textboxen clearen und auf den ersten Tab umschalten
def start_neuer_test():
    result_textbox.delete("1.0", tk.END)
    import_textbox.delete("1.0", tk.END)
    
neuer_test = ctk.CTkButton(summary_frame, text="Neur Test", command = start_neuer_test)
neuer_test.grid(row = 3, column = 0, sticky = SE)

def open_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        # Open the PDF using PyMuPDF
        pdf_document = fitz.open(file_path)
        # Get the first page of the PDF document
        page = pdf_document.load_page(0)
        # Get the image of the PDF page as a PhotoImage
        pdf_image = tk.PhotoImage(data=page.get_pixmap().tobytes("ppm"))
        
        # Remove the previous PDF label, if exists
        for widget in pdf_frame.winfo_children():
            widget.destroy()

        # Create an image label to display the PDF page
        pdf_label = ttk.Label(pdf_frame, image=pdf_image)
        pdf_label.image = pdf_image  # Keep a reference to prevent garbage collection
        pdf_label.pack(padx=10, pady=10)

        # Close the PDF document (don't forget to close it when you're done with it)
        pdf_document.close()

# Tab 3 - Saved PDFs
tab3 = tabview.add("Saved PDFs")

# Create a separate frame inside tab3 to hold the PDF label
pdf_frame = ttk.Frame(tab3)
pdf_frame.pack(expand=1, fill="both")

# File Explorer Widget
open_button = ttk.Button(tab3, text="Open PDF", command=open_pdf)
open_button.pack(padx=10, pady=10)

# Pack the tabbed interface
tabview.pack(expand=1, fill="both")

# Den Root-Window an die Bildschirmgröße anpassen
root.pack_propagate(False)
root.mainloop()




