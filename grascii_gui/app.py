
import tkinter as tk
from tkinter import ttk

from grascii.searchers import GrasciiSearcher
from grascii.defaults import SEARCH
from grascii.regen import SearchMode


class Application(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.X)
        self.results_content = tk.StringVar()
        self.search_mode = tk.StringVar(value=SEARCH["SearchMode"])
        self.interpretation = tk.StringVar(value=SEARCH["Interpretation"])
        self.uncertainty = tk.StringVar(value=SEARCH["Uncertainty"])
        self.fix_first = tk.StringVar(value="false")
        self.annotation_mode = tk.StringVar(value=SEARCH["AnnotationMode"])
        self.aspirate_mode = tk.StringVar(value=SEARCH["AspirateMode"])
        self.disjoiner_mode = tk.StringVar(value=SEARCH["DisjoinerMode"])
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.create_search_bar()
        self.create_settings_frame()
        self.create_results_frame()

    def create_search_bar(self):

        def search():
            searcher = GrasciiSearcher()
            grascii = ent_search.get()
            results = searcher.search(
                    grascii=grascii,
                    search_mode=self.search_mode.get(),
                    interpretation=self.interpretation.get(),
                    uncertainty=int(self.uncertainty.get()),
                    fix_first=bool(self.fix_first.get()),
                    annotation_mode=self.annotation_mode.get(),
                    aspirate_mode=self.aspirate_mode.get(),
                    disjoiner_mode=self.disjoiner_mode.get(),
            )
            self.results_content.set(f"Results: {len(results)}\n\n" + "\n".join(results))

        def search_event(event):
            search()

        frm_search = tk.Frame(master=self)
        frm_search.grid(row=0, column=0, columnspan=2)
        ent_search = tk.Entry(master=frm_search)
        ent_search.bind("<Return>", search_event)
        ent_search.pack(fill=tk.Y, side=tk.LEFT)
        btn_search = tk.Button(master=frm_search, text="Search", command=search)
        btn_search.pack(fill=tk.Y, side=tk.LEFT)

    def create_settings_frame(self):
        frm_settings = tk.Frame(master=self)
        frm_settings.grid(row=1, column=0, padx=4, pady=4)
        lbl_settings = tk.Label(master=frm_settings, text="Settings")
        lbl_settings.grid(row=0, column=0, columnspan=2)
        lbl_search_mode = tk.Label(master=frm_settings, text="Search Mode")
        lbl_search_mode.grid(row=1, column=0)
        spn_search_mode = ttk.Spinbox(master=frm_settings, textvariable=self.search_mode, values=[member.value for member in SearchMode])
        spn_search_mode.grid(row=1, column=1)
        lbl_interpretation = tk.Label(master=frm_settings, text="Interpretation")
        lbl_interpretation.grid(row=2, column=0)
        spn_interpretation = ttk.Spinbox(master=frm_settings, textvariable=self.interpretation, values=["best", "all"])
        spn_interpretation.grid(row=2, column=1)
        lbl_uncertainty = tk.Label(master=frm_settings, text="Uncertainty")
        lbl_uncertainty.grid(row=3, column=0)
        spn_uncertainty = ttk.Spinbox(master=frm_settings, from_=0, to=2, textvariable=self.uncertainty)
        spn_uncertainty.grid(row=3, column=1)
        lbl_fix_first = tk.Label(master=frm_settings, text="Fix First")
        lbl_fix_first.grid(row=4, column=0)
        chk_fix_first = tk.Checkbutton(master=frm_settings)
        chk_fix_first.grid(row=4, column=1)
        lbl_annotation_mode = tk.Label(master=frm_settings, text="Annotation Mode")
        lbl_annotation_mode.grid(row=5, column=0)
        spn_annotation_mode = ttk.Spinbox(master=frm_settings, textvariable=self.annotation_mode, values=["discard", "retain", "strict"])
        spn_annotation_mode.grid(row=5, column=1)
        lbl_aspirate_mode = tk.Label(master=frm_settings, text="Aspirate Mode")
        lbl_aspirate_mode.grid(row=6, column=0)
        spn_aspirate_mode = ttk.Spinbox(master=frm_settings, textvariable=self.aspirate_mode, values=["discard", "retain", "strict"])
        spn_aspirate_mode.grid(row=6, column=1)
        lbl_disjoiner_mode = tk.Label(master=frm_settings, text="Disjoiner Mode")
        lbl_disjoiner_mode.grid(row=7, column=0)
        spn_disjoiner_mode = ttk.Spinbox(master=frm_settings, textvariable=self.disjoiner_mode, values=["discard", "retain", "strict"])
        spn_disjoiner_mode.grid(row=7, column=1)
        lbl_dictionaries = tk.Label(master=frm_settings, text="Dictionaries")
        lbl_dictionaries.grid(row=8, column=0, columnspan=2)
        choices = tk.StringVar(value=["preanniversary", "preanniversary-phrases"])
        lst_dictionaries = tk.Listbox(master=frm_settings, listvariable=choices, selectmode="extended")
        lst_dictionaries.grid(row=9, column=0, columnspan=2)

    def create_results_frame(self):
        frm_results = tk.Frame(master=self, width=50)
        frm_results.grid(row=1, column=1, sticky="nw")
        lbl_results = tk.Label(master=frm_results, textvariable=self.results_content, justify=tk.LEFT)
        lbl_results.pack()


def main():
    root = tk.Tk()
    app = Application(root)
    app.mainloop()